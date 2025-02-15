#!/usr/bin/env python3

import argparse
import logging
import sys

from bluetooth_manager.manager import BluetoothManager, BluetoothManagerError


def main(args: argparse.Namespace):
    """
    Main entry point for the CLI tool.

    Args:
        args (argparse.Namespace): Command line arguments.

    Raises:
        BluetoothManagerError: If an error occurs during Bluetooth device management.
    """
    bluetooth_manager = BluetoothManager(config_path=args.config, channel=args.channel)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if args.manage:
        bluetooth_manager.manage_connections()
        logging.info("Bluetooth device management has started.")

    if args.scan:
        logging.info("Scanning for available bluetooth devices...")
        devices = bluetooth_manager.discover_devices()
        logging.info(
            f"{len(devices)} bluetooth device(s) found:\n" +
            "\n".join(f"{mac}  {name}" for mac, name in devices)
        )

    if args.connect:
        logging.info(f"Attempting to connect to {args.connect}...")
        bluetooth_manager.connect_device(args.connect)
        logging.info(f"Connected to device {args.connect}.")

    if args.disconnect:
        logging.info("Disconnecting from all devices...")
        bluetooth_manager.disconnect_all_devices()
        logging.info("All devices have been disconnected.")

    if args.list:
        logging.info("Listing connected devices...")
        devices = bluetooth_manager.list_connected_devices()
        logging.info(
            f"{len(devices)} connected bluetooth device(s) found:\n" +
            "\n".join(f"{mac}  {name}" for mac, name in devices)
        )


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="CLI tool for managing Bluetooth devices.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--manage", action="store_true",
        help="Manage connections automatically."
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Scan for available Bluetooth devices."
    )
    parser.add_argument(
        "--connect", metavar="MAC", type=str,
        help="Connect to a specific Bluetooth device by MAC address."
    )
    parser.add_argument(
        "--disconnect", action="store_true",
        help="Disconnect all devices."
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List all connected devices."
    )
    parser.add_argument(
        "--channel", type=str, default="default",
        help="Specify the channel otherwise the default channel is used."
    )
    parser.add_argument(
        "--config", type=str,
        help="Configuration to load."
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Enable verbose output."
    )
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        main(parse_args())
    except BluetoothManagerError as e:
        logging.error(f"Bluetooth manager error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)
