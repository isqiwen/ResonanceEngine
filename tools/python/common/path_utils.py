def EncloseString(aString, aSymbol):
    """封闭字符串两侧"""
    if not isinstance(aSymbol, (str, tuple, list)) or len(aSymbol) not in {1, 2}:
        raise ValueError("aSymbol must be a string or a sequence of length 2.")
    if isinstance(aSymbol, str):
        return f"{aSymbol}{aString}{aSymbol}"
    return f"{aSymbol[0]}{aString}{aSymbol[1]}"
