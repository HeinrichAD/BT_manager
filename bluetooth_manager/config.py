import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union
import yaml


def load_config(
    config_path: Optional[Union[str, Path]] = None,
    channel: str = "default"
) -> Dict[str, Any]:
    """
    Load the configuration file and return the configuration dictionary.

    Args:
        config_path (Optional[Union[str, Path]]):
            Path to the configuration file.
            Also see `get_config_path` for more details.
        channel (str):
            The channel name to load from the configuration file.
            Default is "default".

    Returns:
        Dict[str, Any]: The configuration dictionary.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        KeyError: If the configuration file does not contain the expected keys.
        RuntimeError: If there is an error parsing the configuration file.
    """
    config_path = get_config_path(config_path)
    logging.debug(f"Loading configuration from {config_path}")

    try:
        config = yaml.safe_load(config_path.read_text())
    except FileNotFoundError as e:
        # this should never happen, but just in case
        raise FileNotFoundError(f"Configuration file not found at {config_path}") from e
    except yaml.YAMLError as e:
        raise RuntimeError("Error parsing the configuration file") from e

    try:
        config = config["bluetooth_manager"]
        channel_config = {}
        if channel != "default":
            channel_config = config[channel]
        return {**config["default"], **channel_config}
    except KeyError as e:
        raise KeyError("Configuration file does not contain the expected keys") from e


def get_config_path(config_path: Optional[Union[str, Path]] = None) -> Path:
    """
    Get the path to the configuration file.

    config_path (Optional[Union[str, Path]]):
        Path to the configuration file.
        If not provided, the function will look for the configuration file in the following order:
        1. The path specified in the `config_path` argument.
        2. The path specified in the `BLUETOOTH_MANAGER_CONFIG` environment variable.
        3. The default path "config.yaml" in the current directory.
        4. The default configuration file included within the package.

    Returns:
        Path: The path to the configuration file.

    Raises:
        FileNotFoundError: If the configuration file is not found.
    """
    if config_path is not None:
        config_path = Path(config_path)
        if config_path.exists():
            return config_path
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    config_path = os.getenv("BLUETOOTH_MANAGER_CONFIG", None)
    if config_path is not None:
        config_path = Path(config_path)
        if config_path.exists():
            return config_path
        logging.warning(f"Configuration file from `BLUETOOTH_MANAGER_CONFIG` not found at {config_path}")

    config_path = Path("config.yaml")
    if config_path.exists():
        return config_path

    logging.warning("No configuration file found. Using default configuration.")
    config_path = Path(__file__).parent / "config.yaml"
    if config_path.exists():
        return config_path

    raise FileNotFoundError("No configuration file not found.")
