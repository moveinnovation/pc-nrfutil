# About this fork

This is a fork of [`anszom`'s fork](https://github.com/anszom/pc-nrfutil) of
Nordic's [`nrfutil`](https://github.com/NordicSemiconductor/pc-nrfutil). Whereas
`anszom`'s fork adds support for OTA DFU via. a native bluetooth device using
[`BLE_GATT`](https://github.com/ukBaz/BLE_GATT), this fork attempts to do the
same using `bluepy`.


## Installation

```
$ [sudo] python setup.py install
```

## Usage

The `bluepy` transport backend has not yet :been added to the `nrfutil` CLI
tool. However, after installation, the functionality can be accessed via the
python package:

```

import nordicsemi.dfu.dfu_mode_jumper as dfu_mode_jumper
import nordicsemi.dfu.dfu as dfu

ZIP_FILE_PATH = "foo-dfu_package.zip"
ADDR          = "XX:XX:XX:XX:XX:XX"

jumper = dfu_mode_jumper.DfuModeJumper(ADDR)
my_transport = jumper.IntoDfuTransportBluepy()
my_dfu = dfu.Dfu(ZIP_FILE_PATH, my_transport, 0)

jumper.jump_to_dfu_mode()

# at this point the device with address ADDR should be disconnected.

my_dfu.dfu_send_images()
```

For the time being, the jumping to DFU mode is its own module separate from the
actual DFU, to better be able to test against `anszom`'s fork, which assumes
that the device is already in DFU mode.


Below is a copy of Nordic's original README.

# nRF Util

[![Latest version](https://img.shields.io/pypi/v/nrfutil.svg)](https://pypi.python.org/pypi/nrfutil)
[![License](https://img.shields.io/pypi/l/nrfutil.svg)](https://pypi.python.org/pypi/nrfutil)
[![Build Status](https://dev.azure.com/NordicSemiconductor/Wayland/_apis/build/status/pc-nrfutil?branchName=master)](https://dev.azure.com/NordicSemiconductor/Wayland/_build?definitionId=30)

nRF Util is a Python package and command-line utility that supports Device
Firmware Updates (DFU) and cryptographic functionality.

![screenshot](screenshot.gif)

## Documentation

See the
[InfoCenter](https://infocenter.nordicsemi.com/topic/ug_nrfutil/UG/nrfutil/nrfutil_intro.html)
pages for information on how to install and use nRF Util.

## Feedback

Please report issues on the [DevZone](https://devzone.nordicsemi.com) portal.

## Contributing

Feel free to propose changes by creating a pull request.

If you plan to make any non-trivial changes, please start out small and ask seek
an agreement before putting too much work in it. A pull request can be declined
if it does not fit well within the current product roadmap.

In order to accept your pull request, we need you to sign our Contributor
License Agreement (CLA). You will see instructions for doing this after having
submitted your first pull request.

## License

See the [LICENSE](LICENSE) file for details.
