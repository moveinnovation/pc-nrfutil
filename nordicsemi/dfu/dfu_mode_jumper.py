import nordicsemi.dfu.dfu_transport_ble_native as dfu_transport_ble_native
import nordicsemi.dfu.dfu_transport_ble_bluepy as dfu_transport_ble_bluepy
import nordicsemi.dfu.dfu as dfu

from bluepy.btle import *
from bluepy.btle import Peripheral, ADDR_TYPE_RANDOM
import logging

LOG_LEVEL  = logging.INFO
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
logging.basicConfig(level = LOG_LEVEL, format = LOG_FORMAT)

class DfuModeJumper():
    BUTTONLESS_UUID = "8ec90003-f315-4f60-9fb8-838830daea50"

    def from_addr(addr):
        p = Peripheral(addr, addrType = ADDR_TYPE_RANDOM)
        logging.info("New peripheral opened.")
        return DfuModeJumper(p)

    def __init__(self, p):
        if isinstance(p, str):
            p = Peripheral(p, addrType = ADDR_TYPE_RANDOM)
            logging.info("New peripheral opened.")

        elif not isinstance(p, Peripheral):
            raise ValueError("DfuModeJumper.__init__(): expected str or "
                             f"Peripheral, but got {type(p).__name__}.")
        self.p = p

        self.buttonless_char        = self.p.getCharacteristics(uuid = DfuModeJumper.BUTTONLESS_UUID)[0]
        self.buttonless_char_handle = self.buttonless_char.getHandle()
        logging.info("Got buttonless characteristic and handle.")

        cccd_handle = self.buttonless_char_handle + 1
        res = self.p.writeCharacteristic(cccd_handle, b"\x02\x00", withResponse = True)
        logging.info("Subscribed to indications for buttonless characteristic "
                     f"with response: {res}.")

    def jump_to_dfu_mode(self):
        res = self.p.writeCharacteristic(self.buttonless_char_handle,
                                         b"\x01",
                                         withResponse = True)
        logging.info("Successfully wrote to buttonless characteristic with"
                     f" response: {res}")

        time.sleep(1) # TODO: do we need to enforce a sleep here? if so, is
                      #       there an official recommendation on how long?

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
