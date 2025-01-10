import os
import sys
from pathlib import Path

python_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(python_project_root))

from common.shell_utils import run_command
from common.logger_config import Logger
from common.file_utils import clean


def check_python_version():
    """
    Detect Python version and ensure it meets the requirements (>= 3.7).
    """
    _, version_output, _ = run_command(["python", "--version"])
    Logger.Info(f"Detected Python version: {version_output}")

    version_parts = version_output.split()[1].split(".")
    major, minor = int(version_parts[0]), int(version_parts[1])

    if major < 3 or (major == 3 and minor < 7):
        Logger.Error("Python 3.7 or higher is required!")
        sys.exit(1)

    return f"{major}.{minor}"

def check_virtualenv_exists():
    """
    Check if the virtual environment already exists.
    """
    success, _, _ = run_command(["pipenv", "--venv"], check=False)
    return success

def delete_virtualenv(target_root):
    """
    Delete the existing virtual environment.
    """
    Logger.Info("Deleting existing virtual environment...")
    run_command(["pipenv", "--rm"])

    venv_path = Path(target_root) / ".venv"
    if venv_path.exists():
        Logger.Info(f"Force deleting virtual environment directory: {venv_path}")
        clean(venv_path)
    else:
        Logger.Info("No .venv directory found, skipping manual deletion.")

def check_pipenv():
    """
    Check if Pipenv is installed.
    """
    success, _, _ = run_command(["pipenv", "--version"], check=False)

    if not success:
        Logger.Error("Pipenv doesn't exist!")
        sys.exit(1)

def activate_pipenv_env():
    """
    Ensure Pipenv environment is active and install required packages.
    """
    Logger.Info("Activating pipenv virtual environment...")
    # Check if a Pipenv virtual environment exists
    success, venv_path, _ = run_command(["pipenv", "--venv"], check=False)

    if success:
        Logger.Info(f"Pipenv virtual environment detected: {venv_path}")
    else:
        Logger.Error("No Pipenv environment found. Please create one first using `pipenv install`.")
        sys.exit(1)

    # Activate the virtual environment
    env = os.environ.copy()
    env["PIPENV_VENV_IN_PROJECT"] = "TRUE"  # Use in-project virtual environment

    return env

def create_virtualenv(python_version, pypi_source):
    """
    Initialize a pipenv virtual environment in the target root directory.
    """

    # Set environment variables
    env = os.environ.copy()
    env["PIPENV_VENV_IN_PROJECT"] = "TRUE"
    env["PIPENV_MAX_DEPTH"] = "10"

    # Upgrade pip
    Logger.Info("Upgrading pip...")
    run_command(["python", "-m", "pip", "install", "--upgrade", "pip", "-i", pypi_source], env=env)

    # Install pipenv
    Logger.Info("Installing pipenv...")
    run_command(["python", "-m", "pip", "install", "pipenv", "-i", pypi_source], env=env)

    # Initialize virtual environment
    Logger.Info("Initializing virtualenv...")
    run_command(["pipenv", "--python", python_version], env=env)

    # Upgrade pip in the virtual environment
    Logger.Info("Upgrading pip in virtualenv...")
    run_command(["pipenv", "install", "-i", pypi_source], env=env)

def setup(target_root):
    """
    Main function to execute the script.
    """
    # Backup the current working directory
    work_dir_backup = os.getcwd()

    # Set script path and target root
    script_path = Path(__file__).resolve()

    if not target_root:
        Logger.Error(f"Error using {script_path}")
        Logger.Error("Usage:")
        Logger.Error(f"    python {script_path} target-root")
        sys.exit(1)

    target_root = Path(target_root).resolve()
    if not target_root.is_dir():
        Logger.Error(f"Error: Target root {target_root} does not exist or is not a directory.")
        sys.exit(1)

    Logger.Info(f"Checking target root...\nTARGET_ROOT = {target_root}")
    os.chdir(target_root)

    # Define PyPI source
    pypi_source = "https://pypi.tuna.tsinghua.edu.cn/simple"

    Logger.Info("########################################################################################")
    Logger.Info(f"# SCRIPT_PATH          = {script_path}")
    Logger.Info(f"# TARGET_ROOT          = {target_root}")
    Logger.Info(f"# PYPI_SOURCE          = {pypi_source}")
    Logger.Info("########################################################################################")

    Logger.Info("Starting initializing python virtual environment...\n")

    try:
        # Check Python version
        python_version = check_python_version()

        if check_virtualenv_exists():
            Logger.Info("Virtual environment already exists.")
            user_input = input("Do you want to delete the existing virtual environment? (y/n): ").strip().lower()
            if user_input == "y":
                delete_virtualenv(target_root)
                create_virtualenv(python_version, pypi_source)
            else:
                Logger.Info("Using the existing virtual environment.")
        else:
            create_virtualenv(python_version, pypi_source)
    except Exception as e:
        Logger.Error("\nFailed initializing virtual environment.")
        Logger.Error(f"Error: {e}")
        os.chdir(work_dir_backup)
        sys.exit(1)

    Logger.Info("Successfully initialized virtual environment.")
    os.chdir(work_dir_backup)

if __name__ == "__main__":
    target_root = sys.argv[1] if len(sys.argv) > 1 else None
    setup(target_root)
