from email.policy import default
import click
from pyubx2 import UBXMessage, UBXReader, FIXMODE, FIXTYPE
from pynmeagps import NMEAMessage
from serial import Serial
from  serial.tools import list_ports_osx

@click.command()
@click.option('--serial', default='u-blox GNSS receiver', help='Serial port to use.')
@click.option('--baud', default=460800, help='Baud rate.')
@click.option('--verbose', default=False, help='Print every message.')

def main(serial, baud):
    BAUD = 460800
    BAUD = baud

    print("Hello from read-ublox!\n")
    portname:str=""
    for port in list_ports_osx.comports():
        print(f"Checking: {port=}")
        if port.description.find(serial) == 0:
            portname = port.device
            print(f"Found u-blox port {port}")
            break
        # print(f"{port.device=}: {port.description}")
    # portname="/dev/cu.usbmodem11301"
    if not portname:
        print(f" no u-blox found!")
        return
    with Serial(port=portname, baudrate=BAUD) as stream:
        ubx_in = UBXReader(stream)
        try:
            msg_count = 0
            for _, msg in ubx_in:
                msg_count +=1
                # print(f"{type(msg)=}")
                if isinstance(msg, UBXMessage):
                    print(f"UBX : {msg_count: 6d}, id: {msg.identity}", end="")
                    if hasattr(msg,"lat"):
                        print (f", lat: {msg.lat}, lon:{msg.lon}", end="")
                    if msg.identity == "NAV-PVT":
                        if hasattr(msg,"fixType") :
                            print (f", fix: {getattr(msg, "fixType")}", end="")
                    print("")

                elif isinstance(msg, NMEAMessage) and hasattr(msg,"lat"):
                    continue
                    print(f"NMEA: {msg_count: 6d}, id: {msg.identity}", end="")
                    print (f", lat: {msg.lat}, lon:{msg.lon}", end="")
                    print("")
                        # fixtype = FIXTYPE[msg.fixType] # type: ignore
        except KeyboardInterrupt as k:
            print("\nShutting down\n")
            return 0


if __name__ == "__main__":
    main()
