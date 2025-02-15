from concurrent.futures import ThreadPoolExecutor, wait
import logging
import os
from pathlib import Path
import re
import subprocess
import time
from typing import Any, List, Optional, Union

from .config import load_config
from .exceptions import BluetoothManagerError


class BluetoothManager:
    """
    Manage Bluetooth operations with dynamic device handling and concurrent connection limits.
    """

    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        channel: str = "default"
    ):
        """
        Initialize the BluetoothManager with the provided configuration.

        Args:
            config_path (Optional[Union[str, Path]]):
                Path to the configuration file.
                Also see `get_config_path` for more details.
            channel (str):
                The channel name to load from the configuration file.
                Default is "default".
        """
        self.config = load_config(config_path, channel)
        self.bluetoothctl_path = self.config["bluetoothctl_path"]
        self.max_connections = self.config["max_connections"]
        self.executor = ThreadPoolExecutor(max_workers=self.max_connections)
        self.setup_logging()

    def setup_logging(self):
        """
        Setup the python logger based on the configuration file.
        """
        log_path = self.config["logging"].get("file", None)
        if log_path is not None:
            # ensure log directory exists
            Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_path,
            level=getattr(logging, self.config["logging"]["level"]),
            format=self.config["logging"]["format"]
        )

    def run_bluetoothctl_command(
        self,
        command: str,
        wait_time: Optional[Union[int, float]] = None
    ):
        """
        Execute a command in the bluetoothctl environment and handle its output.

        Args:
            command (str): The command to execute in the bluetoothctl environment.
            wait_time (Optional[Union[int, float]]):
                The maximum time to wait for the command to complete in seconds.
                If not provided, the default timeout from the configuration will be used.

        Returns:
            str: The output of the command execution.

        Raises:
            BluetoothManagerError: If an error occurs during command execution.
        """
        wait_time = wait_time or self.config \
            .get(command, {}).get("timeout_seconds", self.config["scan"]["timeout_seconds"])
        env = os.environ.copy()  # use the system's environment variables
        with subprocess.Popen(
            [self.bluetoothctl_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        ) as process:
            if process.stdin is None:
                raise BluetoothManagerError("Failed to open stdin for bluetoothctl.")
            stderr: Optional[str] = None
            try:
                process.stdin.write(f"{command}\nexit\n")
                process.stdin.flush()
                stdout, stderr = process.communicate(timeout=wait_time)
                if stderr:
                    raise BluetoothManagerError("Error executing command.", command, stderr)
                return stdout
            except subprocess.TimeoutExpired as e:
                process.kill()
                raise BluetoothManagerError(
                    "Command timeout. Bluetooth operation did not respond in time.",
                    command, stderr
                ) from e

    def discover_devices(self) -> List[Any]:
        """
        Scan for available bluetooth devices.

        The scan response is parsed using the regular expression from the configuration file.
        By default, the MAC address and name of the devices are extracted.

        Returns:
            List[Any]: A list of whatever is extracted from the scan response.
                By default, a list of tuples containing the MAC address and name of the devices is returned.

        Raises:
            BluetoothManagerError: If an error occurs during command execution.
        """
        self.run_bluetoothctl_command("scan on")
        time.sleep(self.config["scan"]["duration"])
        output = self.run_bluetoothctl_command("devices")
        self.run_bluetoothctl_command("scan off")
        return re.findall(self.config["scan"]["device_regex"], output)

    def connect_device(self, device_mac):
        """
        Connect to a specific bluetooth device.

        Args:
            device_mac (str): The MAC address of the device to connect to.

        Raises:
            BluetoothManagerError: If an error occurs during command execution.
        """
        output = self.run_bluetoothctl_command(
            f"connect {device_mac}",
            wait_time=self.config["connection"]["response_timeout"]
        )
        if self.config["connection"]["expected_response"] in output:
            logging.info(f"Successfully connected to {device_mac}.")
        else:
            logging.error(f"Failed to connect to {device_mac}.")

    def disconnect_all_devices(self):
        """
        Disconnect from all connected devices.

        Raises:
            BluetoothManagerError: If an error occurs during command execution.
        """
        self.run_bluetoothctl_command("disconnect")
        logging.info("All devices have been disconnected.")

    def list_connected_devices(self) -> List[Any]:
        """
        List all connected devices.

        Returns:
            List[Any]: A list of whatever is extracted from the scan response.
                By default, a list of tuples containing the MAC address and name of the devices is returned.

        Raises:
            BluetoothManagerError: If an error occurs during command execution.
        """
        output = self.run_bluetoothctl_command("devices Connected")
        return re.findall(self.config["list"]["device_regex"], output)

    def manage_connections(self):
        """
        Manage connections to discovered devices.

        Raises:
            BluetoothManagerError: If an error occurs during command execution.
        """
        devices = self.discover_devices()
        connected_devices = self.list_connected_devices()
        devices_to_connect = [mac for mac in devices if mac not in connected_devices]
        futures = [self.executor.submit(self.connect_device, mac) for mac in devices_to_connect]
        wait(futures)
        logging.info("All device connection attempts are complete.")
