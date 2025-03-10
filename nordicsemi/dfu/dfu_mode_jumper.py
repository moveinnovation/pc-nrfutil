from nordicsemi.dfu import dfu, dfu_transport_ble_native, dfu_transport_ble_bluepy
from bluepy import btle

import time
import logging
logger = logging.getLogger(__name__)

class DfuModeJumper():
    BUTTONLESS_UUID = "8ec90003-f315-4f60-9fb8-838830daea50"

    def __init__(self, p):
        if isinstance(p, str):
            p = btle.Peripheral(p, addrType = btle.ADDR_TYPE_RANDOM)
            logger.info("DfuModeJumper: New Peripheral opened.")
        elif isinstance(p, btle.Peripheral):
            logger.info("DfuModeJumper: Using existing Peripheral.")
        else:
            raise ValueError("DfuModeJumper: init() expected str (device MAC "
                             f"addr) or Peripheral, but got {type(p).__name__}.")
        self.p = p

        self.buttonless_char   = self.p.getCharacteristics(uuid = DfuModeJumper.BUTTONLESS_UUID)[0]
        self.buttonless_handle = self.buttonless_char.getHandle()
        logger.info("DfuModeJumper: Got buttonless characteristic and handle.")

        cccd_handle = self.buttonless_handle + 1
        res = self.p.writeCharacteristic(cccd_handle, b"\x02\x00", withResponse = True)
        logger.info("DfuModeJumper: Subscribed to buttonless char indications.")

    def jump_to_dfu_mode(self):
        _ = self.p.writeCharacteristic(self.buttonless_handle, b"\x01", withResponse = True)
        logger.info("DfuModeJumper: initiated jump to DFU mode. "
                    "Device should disconnect momentarily.")

        time.sleep(1) # TODO: do we need to enforce a sleep here? if so, is
                      #       there an official recommendation on how long?

        try: p.disconnect()
        except: pass

    def get_bootloader_addr(self):
        # given a mac address string; increment the address and construct new 
        # mac address string with colon separated bytes.
        addr_out = int(self.p.addr.replace(":", ""), 16) + 1
        tmp = "{:x}".format(addr_out)     # format as lower case hex number.
        tmp = (12 - len(tmp)) * "0" + tmp # pad with leading zeroes if necessary.
        return ":".join(tmp[i:i + 2] for i in range(12)[::2]) # insert colons.


    def intoDfuTransportBleNative(self):
        return dfu_transport_ble_native.DfuTransportBleNative(self.get_bootloader_addr())

    def intoDfuTransportBleBluepy(self):
        return dfu_transport_ble_bluepy.DfuTransportBleBluepy(self.get_bootloader_addr())
