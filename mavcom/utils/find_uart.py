__all__ = ['find_uart_devices']

import serial.tools.list_ports



def find_uart_devices(name="FT231X") -> list:
    ftdi_devices = []
    # List all connected serial ports
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if name in port.description:
            ftdi_devices.append(port)
    return ftdi_devices


if __name__ == "__main__":
    ftdi_devices = find_uart_devices()
    if ftdi_devices:
        print("Found FTDI UART devices:")
        for device in ftdi_devices:
            print(f" - {device.device} ({device.description})")
    else:
        print("No FTDI UART devices found.")
