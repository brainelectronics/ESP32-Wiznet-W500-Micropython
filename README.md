# Micropython-ESP32-W5500 (Wiznet)

Connect your ESP32 to W5500 (Wiznet) ethernet module. and use Python requests as http client

![Untitled](https://user-images.githubusercontent.com/92551110/189515479-bfadad62-0bf1-4efc-84bb-ae88b58ec12a.png)

---------------

<!-- MarkdownTOC -->

- [General](#general)
- [Installation](#installation)
  - [Install required tools](#install-required-tools)
- [Setup](#setup)
  - [Manually](#manually)
    - [Upload files to board](#upload-files-to-board)
- [Hardware](#hardware)
  - [Wiring](#wiring)
- [Limitations](#limitations)

<!-- /MarkdownTOC -->

## General

Forked from
[Ayyoubzadeh/ESP32-Wiznet-W500-Micropython][ref-ayyoubzadeh-esp32-wiznet-w500]

Same as code posted by [vinz-uts on Micropython Forum][ref-upy-forum-wiznet5k]

## Installation

### Install required tools

Python3 must be installed on your system. Check the current Python version
with the following command

```bash
python --version
python3 --version
```

Depending on which command `Python 3.x.y` (with x.y as some numbers) is
returned, use that command to proceed.

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Setup

### Manually

#### Upload files to board

Copy the module to the MicroPython board and import them as shown below
using [Remote MicroPython shell][ref-remote-upy-shell]

Open the remote shell with the following command. Additionally use `-b 115200`
in case no CP210x is used but a CH34x.

```bash
rshell -p /dev/tty.SLAB_USBtoUART --editor nano
```

Perform the following command to copy all files and folders to the device

```bash
mkdir /pyboard/lib

cp wiznet5k*.py /pyboard/
cp -r lib/* /pyboard/lib

cp main.py /pyboard
cp boot.py /pyboard
```

## Hardware

ESP32 ESP-WROOM-32 with W5500 (or W5100)

### Wiring

| ESP32 Board       | W5500 |
| ----------------- | ----- |
| 3V3               | VCC   |
| GND               | GND   |
| GPIO15(HSPI_CS)   | CS    |
| GPIO14(HSPI_CLK)  | SCK   |
| GPIO13(HSPI_MOSI) | MOSI  |
| GPIO12(HSPI_MISO) | MISO  |
| GPIO19            | RST   |
| GPIO4 User LED    |       |

Top view of WIZ5500 Mini module

```
             LAN
             | |
             | |
            || ||
        -------------
  GND  | GND    GND  | GND
  GND  | GND    3.3V | 3.3V
  MOSI | MISO   3.3V | 3.3V
  SCK  | SCK    NC   | NC
  CS   | CS     RST  | 3.3V
  NC   | INT    MISO | MISO
        -------------
```

## Limitations

 - Only Works with http (not https)
 - Does not support asyncio
     - [W5500-EVB-PICO: setblocking, SOL_SOCKET, SO_REUSEADDR NOT working; Cannot use Asyncio start_server()][ref-micropython-w5500-async-issue]

<!-- Links -->
[ref-ayyoubzadeh-esp32-wiznet-w500]: https://github.com/Ayyoubzadeh/ESP32-Wiznet-W500-Micropython
[ref-upy-forum-wiznet5k]: https://forum.micropython.org/viewtopic.php?t=5851&start=10
[ref-remote-upy-shell]: https://github.com/dhylands/rshell
[ref-micropython-w5500-async-issue]: https://github.com/micropython/micropython/issues/8938
