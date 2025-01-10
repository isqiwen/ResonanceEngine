import os
import sys
from pathlib import Path

python_project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(python_project_root))

from common.logger_config import Logger
from common.shell_utils import run_command
from common.file_utils import clean
from common.platform_utils import Platform

from ci_helpers.ci_constants import CONAN_USER_HOME, CMAKE_VERSION
from ci_helpers.venv_setup import check_pipenv, activate_pipenv_env


def setup_conan_home():
    os.environ["CONAN_HOME"] = str(CONAN_USER_HOME)

    if not CONAN_USER_HOME.exists():
        Logger.Error(f"Existing Conan configuration not found at {CONAN_USER_HOME}.")
        sys.exit(1)

def _enable_revisions_in_conan(conan_conf_file):
    """
    Enable 'core.revisions_enabled' in Conan 2.x by modifying 'global.conf'.
    """
    conan_conf_file = Path(conan_conf_file)

    if not conan_conf_file.exists():
        Logger.Info(f"global.conf not found at {conan_conf_file}. Creating a new one...")
        conan_conf_file.touch()

    with open(conan_conf_file, "r") as f:
        lines = f.readlines()

    revisions_enabled = any("core.revisions_enabled = 1" in line for line in lines)

    if revisions_enabled:
        Logger.Info("Revisions are already enabled in global.conf.")
    else:
        with open(conan_conf_file, "a") as f:
            f.write("\ncore.revisions_enabled = 1\n")
        Logger.Info("Enabled revisions in Conan configuration.")

def _update_conan_profile(profile_path, section, key, value):
    """
    Update a specific key-value pair in a Conan profile.
    :param profile_name: Name of the profile to update (e.g., "default").
    :param section: Section of the profile (e.g., "settings", "options").
    :param key: Key to update (e.g., "compiler.cppstd").
    :param value: Value to set (e.g., "17").
    """
    # Locate the profile file
    profile_path = Path(profile_path)
    if not profile_path.exists():
        raise FileNotFoundError(f"Profile '{profile_path.stem}' not found at {profile_path.parent}")

    # Read the profile file
    with open(profile_path, "r") as f:
        lines = f.readlines()

    # Locate the section
    section_found = False
    updated = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f"[{section}]"):
            section_found = True
            new_lines.append(line)
            continue

        if section_found and (not stripped or stripped.startswith("[")):
            # End of the current section
            if not updated:
                new_lines.append(f"{key}={value}\n")
                updated = True
            section_found = False

        if section_found and stripped.startswith(f"{key}="):
            # Update the key-value pair
            new_lines.append(f"{key}={value}\n")
            updated = True
        else:
            new_lines.append(line)

    # Append the new key-value pair if not found
    if not updated:
        if not section_found:
            new_lines.append(f"\n[{section}]\n")
        if value is not None:
            new_lines.append(f"{key}={value}\n")
        else:
            new_lines.append(f"{key}\n")

    # Write back to the profile
    with open(profile_path, "w") as f:
        f.writelines(new_lines)

    Logger.Info(f"Profile '{profile_path.stem}' updated: [{section}] {key}={value}")

def _initialize_conan_profile(profile_name="default"):
    """
    Initialize or update a Conan profile using commands.
    """
    Logger.Info(f"Checking if profile '{profile_name}' exists...")
    success, _, _ = run_command(["pipenv", "run", "conan", "profile", "show", "--profile", profile_name], check=False, env=os.environ)
    if success:
        Logger.Info(f"Profile '{profile_name}' exists.")
    else:
        Logger.Error(f"Profile '{profile_name}' not found. Creating using 'conan profile detect'...")
        run_command(["pipenv", "run", "conan", "profile", "detect", "--name", profile_name])

    Logger.Info(f"Updating default profile...")
    conan_profile_path = CONAN_USER_HOME / "profiles" / profile_name
    _update_conan_profile(conan_profile_path, "settings", "compiler.cppstd", 17)
    _update_conan_profile(conan_profile_path, "options", "*:*.shared", True)
    _update_conan_profile(conan_profile_path, "tool_requires", "cmake/" + CMAKE_VERSION, None)

    if Platform.is_linux():
        _update_conan_profile(conan_profile_path, "settings", "compiler.libcxx", "libstdc++11")

    Logger.Info(f"Profile '{profile_name}' updated successfully.")

def _install_conan():
    """
    Install Conan in the active Pipenv virtual environment.
    """
    Logger.Info("Installing conan in the pipenv virtual environment...")
    run_command(["pipenv", "run", "pipenv", "install", "conan"])
    Logger.Info("Conan installed successfully.")

def _create_conan_user_home():
    """
    Create a custom Conan user home and configure it.
    """
    # Set CONAN_USER_HOME
    os.environ["CONAN_HOME"] = str(CONAN_USER_HOME)

    if CONAN_USER_HOME.exists():
        Logger.Info(f"Existing Conan configuration found at {CONAN_USER_HOME}. Deleting...")
        clean(CONAN_USER_HOME)

    Logger.Info("Initializing Conan configuration...")
    run_command(["pipenv", "run", "conan", "config", "home"])

    _initialize_conan_profile()

    Logger.Info(f"Conan user home successfully created and configured at {CONAN_USER_HOME}")

def _configure_conan():
    """
    Configure Conan with basic settings and mirror.
    """
    Logger.Info("Configuring Conan...")
    # Enable revisions and use Tsinghua mirror
    _create_conan_user_home()

    # Check and set the default profile
    run_command(["pipenv", "run", "conan", "profile", "show", "-pr:b", "default"])

def conan_setup():
    # Check for required tools
    check_pipenv()

    # Activate existing Pipenv virtual environment
    activate_pipenv_env()

    # Install Conan
    _install_conan()

    # Configure Conan
    _configure_conan()

    Logger.Info("Conan setup complete!")


if __name__ == "__main__":
    conan_setup()
