# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cas4(KaitaiStruct):
    """:field cas4_pwr_volt: pwr_volt
    :field cas4_pwr_cur: pwr_cur
    :field cas4_convert_volt: convert_volt
    :field cas4_convert_cur: convert_cur
    :field cas4_obc_temp: obc_temp
    :field cas4_rf_amp_temp: rf_amp_temp
    :field cas4_rcv_agc_volt: rcv_agc_volt
    :field cas4_rf_fwd: rf_fwd
    :field cas4_rf_ref: rf_ref
    :field cas4_obc_volt: obc_volt
    :field cas4_obc_reset: obc_reset
    :field cas4_pkt_cnt: pkt_cnt
    :field cas4_sat_num: sat_num
    :field cas4_op_mode: op_mode
    :field cas4_pwr_on_op_mode: pwr_on_op_mode
    :field cas4_i2c_watchdog: i2c_watchdog
    :field cas4_i2c_recon_cnt: i2c_recon_cnt
    :field cas4_tc_watchdog: tc_watchdog
    :field cas4_tc_reset_cnt: tc_reset_cnt
    :field cas4_adc_watchdog: adc_watchdog
    :field cas4_adc_reset_cnt: adc_reset_cnt
    :field cas4_spi_watchdog: spi_watchdog
    :field cas4_spi_init_cnt: spi_init_cnt
    :field cas4_cpu_watchdog: cpu_watchdog
    :field cas4_cpu_reset_cnt: cpu_reset_cnt
    :field cas4_framecounter: framecounter
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25header = self._io.read_bytes(16)
        self.syncpacket = self._io.ensure_fixed_contents(b"\xEB\x90")
        _on = (self.framecounter % 4)
        if _on == 0:
            self._raw_telemetry = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_telemetry))
            self.telemetry = self._root.Frame1(io, self, self._root)
        elif _on == 1:
            self._raw_telemetry = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_telemetry))
            self.telemetry = self._root.Frame2(io, self, self._root)
        elif _on == 3:
            self._raw_telemetry = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_telemetry))
            self.telemetry = self._root.Frame4(io, self, self._root)
        elif _on == 2:
            self._raw_telemetry = self._io.read_bytes(4)
            io = KaitaiStream(BytesIO(self._raw_telemetry))
            self.telemetry = self._root.Frame3(io, self, self._root)
        else:
            self.telemetry = self._io.read_bytes(4)
        self.reserved1 = self._io.read_bytes(9)
        self.framecounterplaceholder = self._io.read_u1()
        self.reserved2 = self._io.read_bytes(112)

    class Frame1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwr_volt = self._io.read_u1()
            self.pwr_cur = self._io.read_u1()
            self.convert_volt = self._io.read_u1()
            self.convert_cur = self._io.read_u1()


    class Frame2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.obc_temp = self._io.read_u1()
            self.rf_amp_temp = self._io.read_u1()
            self.rcv_agc_volt = self._io.read_u1()
            self.rf_fwd = self._io.read_u1()


    class Frame3(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rf_ref = self._io.read_u1()
            self.obc_volt = self._io.read_u1()
            self.obc_reset = self._io.read_u1()
            self.pkt_cnt = self._io.read_bits_int(4)
            self.sat_num = self._io.read_bits_int(4)


    class Frame4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.op_mode = self._io.read_bits_int(4)
            self.pwr_on_op_mode = self._io.read_bits_int(4)
            self.i2c_watchdog = self._io.read_bits_int(1) != 0
            self.i2c_recon_cnt = self._io.read_bits_int(3)
            self.tc_watchdog = self._io.read_bits_int(1) != 0
            self.tc_reset_cnt = self._io.read_bits_int(3)
            self.adc_watchdog = self._io.read_bits_int(1) != 0
            self.adc_reset_cnt = self._io.read_bits_int(3)
            self.spi_watchdog = self._io.read_bits_int(1) != 0
            self.spi_init_cnt = self._io.read_bits_int(3)
            self.cpu_watchdog = self._io.read_bits_int(1) != 0
            self.cpu_reset_cnt = self._io.read_bits_int(3)


    @property
    def framecounter(self):
        if hasattr(self, '_m_framecounter'):
            return self._m_framecounter if hasattr(self, '_m_framecounter') else None

        _pos = self._io.pos()
        self._io.seek(31)
        self._m_framecounter = self._io.read_u1()
        self._io.seek(_pos)
        return self._m_framecounter if hasattr(self, '_m_framecounter') else None


