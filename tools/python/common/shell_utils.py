import subprocess
import sys

from .logger_config import Logger

def run_command(command, check=True, shell=False, env=None):
    """
    Run a system command and handle errors, compatible with Windows and Linux.

    Args:
        command (list or str): Command to run (list for POSIX, str for Windows).
        check (bool): If True, raise exception on non-zero return code.
        shell (bool): If True, run command through the shell.
        env (dict): Custom environment variables.

    Returns:
        tuple: (success, stdout, stderr) where success is a boolean indicating command success.
    """

    if not isinstance(command, str) and not isinstance(command, list):
        return False, "", f"Command format is invalid: {command}"

    try:
        result = subprocess.run(
            command,
            check=check,
            shell=shell,
            env=env,
            text=True,
            capture_output=True
        )
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        if not check:
            # Return False if check is disabled
            return False, e.stdout.strip(), e.stderr.strip()
        else:
            # Print error and terminate if check is enabled
            Logger.Error(f"Error: Command '{command}' failed with exit code {e.returncode}.")
            Logger.Error(f"Standard Output:\n{e.stdout}")
            Logger.Error(f"Error Output:\n{e.stderr}")
            sys.exit(e.returncode)
    except FileNotFoundError:
        # Handle case where the command is not found
        Logger.Error(f"Error: Command not found: {command}")
        return False, "", f"Command not found: {command}"
