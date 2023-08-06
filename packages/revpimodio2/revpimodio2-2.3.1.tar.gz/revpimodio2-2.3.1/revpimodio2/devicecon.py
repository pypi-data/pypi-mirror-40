# -*- coding: utf-8 -*-
"""Modul fuer die Verwaltung der Devices."""
__author__ = "Sven Sager"
__copyright__ = "Copyright (C) 2018 Sven Sager"
__license__ = "LGPLv3"
from serial import Serial
from threading import Thread, Event


class ConBluetooth(Thread):

    def __init__(self, devpath="/dev/ttyConBridge", baud=115200):
        super().__init__()

        if not isinstance(devpath, str):
            raise TypeError("devpath must be <class 'str'>")
        if not isinstance(baud, int):
            raise TypeError("baud must be <class 'int'>")

        self._baud = baud
        self._con = Serial()
        self._devpath = devpath
        self._exit = Event()

        self._terminator = b'\r'

    def _cmd_echo_off(self):
        """Schaltet das Echo aus."""
        if not self._con.is_open:
            raise RuntimeError("connection is closed")

        # Echomodus abschalten
        self._con.write(b'ATE0' + self._terminator)
        response = b'\x00'
        while response != b'':
            response = self._con.readline()
            if response.strip() == b'OK':
                return True
        return False

    def _cmd_ok(self):
        """Sendet OK an Gegenstelle."""
        self._con.write(b'OK' + self._terminator)

    def _get_terminator(self):
        """Getter fuer Terminator."""
        return self._terminator.decode()

    def _set_terminator(self, value):
        """Getter fuer Terminator."""
        if not isinstance(value, str):
            raise TypeError("value must be <class 'str'>")
        self._terminator = value.encode()

    def close(self):
        """Beendet die serielle Kommunikation."""
        self._exit.set()
        self._con.cancel_read()

    def run(self):
        """Hauptschleife."""
        buff = bytearray(0)
        while not self._exit.is_set():
            dat = self._con.read()
            if dat == b'\r':
                print(buff)
                buff = bytearray(0)
            elif dat == b'':
                continue
            else:
                buff += dat  #.strip()

    def send_bytes(self, payload):
        """Sendet Bytes an die Schnittstelle."""
        if not isinstance(payload, bytes):
            raise TypeError("payload must be <class 'bytes'>")
        self._con.write(payload)

    def send_text(self, text):
        """Sendet einen Text oder Bytes an die Schnittstelle."""
        if not isinstance(text, str):
            raise TypeError("text must be <class 'str'>")
        self._con.write(text.encode() + self._terminator)

    def start(self):
        # Serielle Schnittstelle konfigurieren
        self._con.baudrate = self._baud
        self._con.port = self._devpath
        self._con.timeout = 5
        self._con.open()

        if not self._cmd_echo_off():
            self._con.close()
            raise RuntimeError("could not switch echo off")

        # Thread starten
        super().start()

    terminator = property(_get_terminator, _set_terminator)
