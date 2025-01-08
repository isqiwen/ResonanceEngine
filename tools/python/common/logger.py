from pathlib import Path
from logging import FATAL, ERROR, WARN, INFO, DEBUG, NOTSET
from logging import getLogger, StreamHandler, FileHandler, Handler
from logging import Formatter as FormatterBase
from threading import RLock


class LogBufferTypeNotSupported(Exception):
    pass

class LeveledLogBuffer:

    def __init__(self, *, aSize = 10):
        self.myData = []
        self.myBufferSize = aSize

    def __iter__(self):
        for levelAndLog in self.myData:
            yield levelAndLog

    def Log(self, aLevel, aLog):
        if len(self.myData) >= self.myBufferSize:
            self.myData.remove(self.myData[0])
        self.myData.append((aLevel, aLog))

    def Error(self, aLog):
        self.Log(ERROR, aLog)

    def Warning(self, aLog):
        self.Log(WARN, aLog)

    def Info(self, aLog):
        self.Log(INFO, aLog)

    def Debug(self, aLog):
        self.Log(DEBUG, aLog)

    def Clear(self):
        self.myData.clear()


class Formatter(FormatterBase):

    def __init__(self):
        super().__init__(
            fmt = "[{asctime}.{msecs:03.0f}][{levelname:7}] {message}",
            datefmt = "%H:%M:%S",
            style = "{"
        )


formatter = Formatter()
streamHandler = StreamHandler()
streamHandler.setFormatter(formatter)


class LoggerSingleton:

    def __init__(self):
        self.myLogger = getLogger('Aether')
        self.myLogger.addHandler(streamHandler)

        self.EnableFormat()

    def SetLevel(self, aLevel):
        self.myLogger.setLevel(aLevel)

    def EnableFormat(self):
        self.Log = self.LogFormatted

    def DisableFormat(self):
        self.Log = self.myLogger.log

    def LogFormatted(self, aLevel, aMessage, *args, **kwargs):
        try:
            messages = aMessage.split(':', 1)
            message = '[{:12}]{}'.format(messages[0], messages[1])
        except:
            message = aMessage
        self.myLogger.log(aLevel, message, *args, **kwargs)

    def Error(self, aMessage, *args, **kwargs):
        self.Log(ERROR, aMessage, *args, **kwargs)

    def Warning(self, aMessage, *args, **kwargs):
        self.Log(WARN, aMessage, *args, **kwargs)

    def Info(self, aMessage, *args, **kwargs):
        self.Log(INFO, aMessage, *args, **kwargs)

    def Debug(self, aMessage, *args, **kwargs):
        self.Log(DEBUG, aMessage, *args, **kwargs)

    def AddLogFile(self, aFilePath, aMode = 'a', aEncoding = 'utf-8'):
        handler = FileHandler(aFilePath, mode = aMode, encoding = aEncoding)
        handler.setFormatter(formatter)
        self.myLogger.addHandler(handler)

    def RemoveLogFile(self, aFilePath = None):
        toRemove = []
        absFilePath = Path(aFilePath).resolve() if aFilePath else None
        handlers = self.myLogger.handlers
        for h in handlers:
            if not isinstance(h, FileHandler):
                continue
            if not absFilePath:
                toRemove.append(h)
                continue
            logFilePath = Path(h.stream.name).resolve()
            if absFilePath == logFilePath:
                toRemove.append(h)
        for h in toRemove:
            handlers.remove(h)


Logger = LoggerSingleton()
Logger.SetLevel(INFO)

backgroundLogBuffer = LeveledLogBuffer(aSize = 1024)


class LogBufferHandler(Handler):

    def __init__(self, aLogBuffer):
        super().__init__()
        self.myBuffer = aLogBuffer

    @property
    def buffer(self):
        return self.myBuffer

    def emit(self, aRecord):
        try:
            self.myBuffer.Log(aRecord.levelno, aRecord.msg)
        except:
            pass


backgroundLogBufferHandler = LogBufferHandler(backgroundLogBuffer)


class BufferedLoggerSingleton(LoggerSingleton):

    def __init__(self):
        super().__init__()
        self.myLogger.addHandler(backgroundLogBufferHandler)

    def AddLogFile(self, aFilePath, aMode = 'a', aEncoding = 'utf-8'):
        super().AddLogFile(aFilePath, aMode, aEncoding)
        if backgroundLogBufferHandler in self.myLogger.handlers:
            # remove buffer handler from handlers
            handlers = self.myLogger.handlers
            handlers.remove(backgroundLogBufferHandler)
            # stub for flushing
            fileHandler = handlers[-1]
            self.myLogger.handlers = [fileHandler]
            # flush everything to the file handler
            logBuffer = backgroundLogBufferHandler.buffer
            for level, log in logBuffer:
                self.myLogger.log(level, log)
            logBuffer.Clear()
            # rever handlers
            self.myLogger.handlers = handlers


BufferedLogger = BufferedLoggerSingleton()
BufferedLogger.SetLevel(INFO)
