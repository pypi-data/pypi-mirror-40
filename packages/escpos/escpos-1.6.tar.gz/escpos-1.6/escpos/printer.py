#!/usr/bin/python
import os
import usb.core
import usb.util
import serial
import socket

from .escpos import Escpos
from .constants import *
from .exceptions import *

try:
    import paramiko
except:
    print('LOG: paramiko module not found!')

winprint = None

if os.name == 'nt':
    try:
        import win32print as winprint
    except:
        print('LOG: Missing win32 lib!')


class Usb(Escpos):
    """ Define USB printer """

    def __init__(self, idVendor, idProduct, interface=0, in_ep=0x82, out_ep=0x01):
        """
        @param idVendor  : Vendor ID
        @param idProduct : Product ID
        @param interface : USB device interface
        @param in_ep     : Input end point
        @param out_ep    : Output end point
        """
        self.idVendor  = idVendor
        self.idProduct = idProduct
        self.interface = interface
        self.in_ep     = in_ep
        self.out_ep    = out_ep
        self.open()

    def open(self):
        """ Search device on USB tree and set is as escpos device """
        self.device = usb.core.find(idVendor=self.idVendor, idProduct=self.idProduct)
        if self.device is None:
            print("Cable isn't plugged in")

        if self.device.is_kernel_driver_active(0):
            try:
                self.device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                print("Could not detatch kernel driver: %s" % str(e))

        try:
            self.device.set_configuration()
            self.device.reset()
        except usb.core.USBError as e:
            print("Could not set configuration: %s" % str(e))


    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(self.out_ep, msg, self.interface)


    def __del__(self):
        """ Release USB interface """
        if self.device:
            usb.util.dispose_resources(self.device)
        self.device = None


class Serial(Escpos):
    """ Define Serial printer """

    def __init__(self, devfile="/dev/ttyS0", baudrate=9600, bytesize=8, timeout=1):
        """
        @param devfile  : Device file under dev filesystem
        @param baudrate : Baud rate for serial transmission
        @param bytesize : Serial buffer size
        @param timeout  : Read/Write timeout
        """
        self.devfile  = devfile
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.timeout  = timeout
        self.open()

    def open(self):
        """ Setup serial port and set is as escpos device """
        self.device = serial.Serial(port=self.devfile, baudrate=self.baudrate,
            bytesize=self.bytesize, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE, timeout=self.timeout, dsrdtr=True)

        if self.device is not None:
            print("Serial printer enabled")
        else:
            print("Unable to open serial printer on: %s" % self.devfile)

    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(msg)

    def __del__(self):
        """ Close Serial interface """
        if self.device is not None:
            self.device.close()


class Network(Escpos):
    """ Define Network printer """

    def __init__(self, host, port=9100, timeout=10):
        """
        @param host : Printer's hostname or IP address
        @param port : Port to write to
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.open()

    def open(self):
        """ Open TCP socket and set it as escpos device """
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device.settimeout(self.timeout)
        self.device.connect((self.host, self.port))

        if self.device is None:
            print("Could not open socket for %s" % self.host)

    def _raw(self, txt):
        """ Print any command sent in raw format """
        if type(txt) == str:
            txt = bytes(txt, 'UTF-8')
        self.device.sendall(txt)

    def __del__(self):
        """ Close TCP connection """
        self.device.shutdown(socket.SHUT_RDWR)

    def close(self):
        """ Close TCP connection """
        self.device.shutdown(socket.SHUT_RDWR)


class File(Escpos):
    """ Define Generic file printer """

    def __init__(self, devfile="/dev/usb/lp0", encoding=None):
        """
        @param devfile : Device file under dev filesystem
        """
        self.devfile = devfile
        self.open()
        if encoding:
            self.encoding == encoding
        else:
            self.encoding == 'cp850'

    def open(self):
        """ Open system file """
        self.device = open(self.devfile, "wb")
        if self.device is None:
            print("Could not open the specified file %s" % self.devfile)

    def _raw(self, txt):
        """ Print any command sent in raw format """
        if type(txt) == str:
            txt = bytes(txt, 'UTF-8')
        self.device.write(txt)

    def close(self):
        """ Close system file """
        if self.device:
            self.device.close()

    def __del__(self):
        """ Close system file """
        if self.device:
            self.device.close()


class FileSSH(Escpos):
    """ Define Generic file printer on remote machine"""

    def __init__(self, username_, password_, hostname_,  port_, devfile):
        """
        @param devfile : Device file under dev filesystem
        """
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(hostname_, int(port_), username=username_, password=password_)
        self.sftp_client = self.ssh_client.open_sftp()
        self.devfile = devfile

    def open(self):
        """ Open system file """
        self.device = self.sftp_client.open(self.devfile, 'wb')

        if self.device is None:
            print("Could not open the specified file %s" % self.devfile)

    def _raw(self, msg):
        """ Print any command sent in raw format """
        self.device.write(msg)

    def close(self):
        """ Close system file """
        if self.device:
            self.device.close()

    def __del__(self):
        """ Close system file """
        if self.device:
            self.device.close()


class UsbWin(Escpos):

    def __init__(self, printer_name):
        """
        @param devfile : Printer name on Windows
        Ex,: SATPOS
        """
        self.printer_name = printer_name

    def open(self):
        """ Open device printer """
        self.device = winprint.OpenPrinter(self.printer_name)
        winprint.StartDocPrinter(self.device, 1, ("test of raw data", None, "RAW"))
        winprint.StartPagePrinter(self.device)

    def _raw(self, txt):
        if type(txt) == str:
            txt = bytes(txt, "utf-8")
        winprint.WritePrinter(self.device, txt)

    def close(self):
        if self.device:
            winprint.EndPagePrinter(self.device)
            winprint.EndDocPrinter(self.device)
            winprint.ClosePrinter(self.device)

    def __del__(self):
        """ Close device printer """
        if self.device:
            winprint.EndPagePrinter(self.device)
            winprint.EndDocPrinter(self.device)
            winprint.ClosePrinter(self.device)
