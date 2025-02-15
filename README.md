# Bluetooth Manager Package

<!-- markdownlint-disable MD033 -->
<p style="text-align: center;">
  <img src="docs/BTmlogo.jpeg" alt="Bluetooth Manager" style="max-width: 400px;" />
</p>
<!-- markdownlint-enable MD033 -->

## Overview

The package `bluetooth_manager`, BT manager for short, is designed for programmable management of Bluetooth devices via `bluetoothctl` on compatible systems.
It provides a powerful interface for integrating Bluetooth capabilities into larger applications or for standalone usage, ensuring high-level control and efficient management of Bluetooth devices.

Always consider alternatives that may be more suitable for your use case:

- [PyBluez](https://github.com/pybluez/pybluez): Cross-platform Bluetooth Python extension module which is unfortunately not under development anymore.
- [Bleak](https://github.com/hbldh/bleak): Cross-platform Bluetooth Low Energy client library
- [Bless](https://github.com/kevincar/bless): Cross-platform Bluetooth Low Energy server library
- [PyQt](https://www.riverbankcomputing.com/software/pyqt/): Python bindings for cross-platform [QtBluetooth](https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtbluetooth/qtbluetooth-module.html) API

## Features

- **Device Scanning**: Rapid detection of all nearby Bluetooth devices in discoverable mode.
- **Concurrent Connections**: Supports managing multiple connections simultaneously with a configurable cap to balance system load.
- **Error Handling**: Robust custom exceptions and detailed logging facilitate troubleshooting and enhance operational visibility.

## Dependencies

- Python 3.6 or later.
- A system-wide installation of `bluez`, `bluetoothctl`.

## Installation

To install `bluetooth_manager`, make sure that all system requirements are met.
It is also recommended to install the package within a virtual environment.

1. Install system requirements

    ```bash
    sudo apt-get install -y python3 python3-pip bluez bluetoothctl
    python3 -m pip install wheel
    ```

2. Create virtual environment

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install package

    ```bash
    pip install git+https://github.com/HeinrichAD/BT_manager.git
    ```

## Usage

Incorporate `bluetooth_manager` in your Python scripts as follows:

1. Import `BluetoothManager`
2. Create an instance of `BluetoothManager`
3. Initiate device connection management

Here's a straightforward example of initializing the manager and starting the device connection process:

```python
from bluetooth_manager.manager import BluetoothManager

# Initialize the manager with a limit of four concurrent connections
bluetooth_manager = BluetoothManager(max_connections=4)

# Begin the connection management process
bluetooth_manager.manage_connections()
```

## Examples

For more examples take a look into the [examples](examples) directory.

## About this fork

This fork is mainly based on the source code of [LoQiseaking69](https://github.com/LoQiseaking69)'s repository [BT_manager](https://github.com/LoQiseaking69/BT_manager), but also includes some of the features of [HermiTech-LLC](https://github.com/HermiTech-LLC)'s repository [Bluetooth_manager](https://github.com/HermiTech-LLC/Bluetooth_manager), which I assume/suspect is a fork of the former.
Please correct me if I am wrong.
<!--
I think the second is a fork of the first, because the code is almost identical and in the readme the images from the first repository are still linked.
Also, he is still the author in the setup.py of the second repository.
-->
