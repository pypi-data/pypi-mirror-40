# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Us6(KaitaiStruct):
    """:field header: header
    :field syncpacket: syncpacket
    :field packetindex: packetindex
    :field groundindexack: groundindexack
    :field packettype: packettype
    :field payloadsize: payloadsize
    :field rebootcounter: rebootcounter
    :field uptime: uptime
    :field unixtime: unixtime
    :field tempmcu: tempmcu
    :field tempfpga: tempfpga
    :field magnetometerx: magnetometerx
    :field magnetometery: magnetometery
    :field magnetometerz: magnetometerz
    :field gyroscopex: gyroscopex
    :field gyroscopey: gyroscopey
    :field gyroscopez: gyroscopez
    :field cpucurrent: cpucurrent
    :field tempradio: tempradio
    :field payloadreserved1: payloadreserved1
    :field payloadreserved2: payloadreserved2
    :field tempbottom: tempbottom
    :field tempupper: tempupper
    :field payloadreserved3: payloadreserved3
    :field epsvbat: epsvbat
    :field epscurrent_sun: epscurrent_sun
    :field epscurrent_out: epscurrent_out
    :field epsvpanel01: epsvpanel01
    :field epsvpanel02: epsvpanel02
    :field epsvpanel03: epsvpanel03
    :field epscurrent01: epscurrent01
    :field epscurrent02: epscurrent02
    :field epscurrent03: epscurrent03
    :field epsbatttemp: epsbatttemp
    :field payloadreserved4: payloadreserved4
    :field saterrorflags: saterrorflags
    :field satoperationstatus: satoperationstatus
    :field crc: crc
    
    .. seealso::
       Source - https://www.gaussteam.com/radio-amateur-information-for-unisat-6/
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = self._io.read_bytes(16)
        self.syncpacket = self._io.ensure_fixed_contents(b"\x55\x53\x36")
        self.packetindex = self._io.read_u2le()
        self.groundindexack = self._io.read_u2le()
        self.packettype = self._io.read_u1()
        self.payloadsize = self._io.read_u1()
        self.rebootcounter = self._io.read_u2le()
        self.uptime = self._io.read_u4le()
        self.unixtime = self._io.read_u4le()
        self.tempmcu = self._io.read_s1()
        self.tempfpga = self._io.read_s1()
        self.magnetometerx = self._io.read_s2le()
        self.magnetometery = self._io.read_s2le()
        self.magnetometerz = self._io.read_s2le()
        self.gyroscopex = self._io.read_s2le()
        self.gyroscopey = self._io.read_s2le()
        self.gyroscopez = self._io.read_s2le()
        self.cpucurrent = self._io.read_u2le()
        self.tempradio = self._io.read_s1()
        self.payloadreserved1 = self._io.read_u1()
        self.payloadreserved2 = self._io.read_u1()
        self.tempbottom = self._io.read_u1()
        self.tempupper = self._io.read_u1()
        self.payloadreserved3 = self._io.read_u1()
        self.epsvbat = self._io.read_u2le()
        self.epscurrent_sun = self._io.read_u2le()
        self.epscurrent_out = self._io.read_u2le()
        self.epsvpanel01 = self._io.read_u2le()
        self.epsvpanel02 = self._io.read_u2le()
        self.epsvpanel03 = self._io.read_u2le()
        self.epscurrent01 = self._io.read_u2le()
        self.epscurrent02 = self._io.read_u2le()
        self.epscurrent03 = self._io.read_u2le()
        self.epsbatttemp = self._io.read_u2le()
        self.payloadreserved4 = self._io.read_u1()
        self.saterrorflags = self._io.read_u2le()
        self.satoperationstatus = self._io.read_u1()
        self.crc = self._io.read_u1()


