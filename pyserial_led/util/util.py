import serial.tools.list_ports


def find_port():
    ports = serial.tools.list_ports.comports()
    for p in ports:
        if "ACM" in p[0]:
            print("Found port '{0}' for use.".format(p[0]))
            return p[0]

    arduino_print_ports()
    raise Exception("No arduino port found!")


def arduino_print_ports():
    print("Listing ports")
    port = None
    ports = serial.tools.list_ports.comports()
    for p in ports:
        print(p)
    return port
