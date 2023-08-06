# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Minxss(KaitaiStruct):
    """:field minxss_dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field minxss_src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field minxss_src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field minxss_dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field minxss_ctl: ax25_frame.ax25_header.ctl
    :field minxss_pid: ax25_frame.payload.pid
    :field minxss_spacecraft_flags: ax25_frame.payload.ax25_info.minxss_beacon.minxss_spacecraft_flags
    :field minxss_pointing_mode: ax25_frame.payload.ax25_info.minxss_beacon.minxss_pointing_mode
    :field minxss_cmd_accept_cnt: ax25_frame.payload.ax25_info.minxss_beacon.minxss_cmd_accept_cnt
    :field minxss_flight_model: ax25_frame.payload.ax25_info.minxss_beacon.minxss_flight_model
    :field minxss_cdh_board_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_cdh_board_temp
    :field minxss_enable_flags: ax25_frame.payload.ax25_info.minxss_beacon.minxss_enable_flags
    :field minxss_comm_brd_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_comm_brd_temp
    :field minxss_mbrd_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_mbrd_temp
    :field minxss_eps_brd_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_eps_brd_temp
    :field minxss_battery_voltage: ax25_frame.payload.ax25_info.minxss_beacon.minxss_battery_voltage
    :field minxss_solar_panel_minus_y_curr: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_minus_y_curr
    :field minxss_solar_panel_minus_y_volt: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_minus_y_volt
    :field minxss_solar_panel_plus_x_curr: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_plus_x_curr
    :field minxss_solar_panel_plus_x_volt: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_plus_x_volt
    :field minxss_solar_panel_plus_y_curr: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_plus_y_curr
    :field minxss_solar_panel_plus_y_volt: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_plus_y_volt
    :field minxss_solar_panel_minus_y_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_minus_y_temp
    :field minxss_solar_panel_plus_x_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_plus_x_temp
    :field minxss_solar_panel_plus_y_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_solar_panel_plus_y_temp
    :field minxss_battery_chrg_curr: ax25_frame.payload.ax25_info.minxss_beacon.minxss_battery_chrg_curr
    :field minxss_battery_dchrg_curr: ax25_frame.payload.ax25_info.minxss_beacon.minxss_battery_dchrg_curr
    :field minxss_battery_temp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_battery_temp
    :field minxss_xp: ax25_frame.payload.ax25_info.minxss_beacon.minxss_xp
    :field minxss_sps_x: ax25_frame.payload.ax25_info.minxss_beacon.minxss_sps_x
    :field minxss_sps_y: ax25_frame.payload.ax25_info.minxss_beacon.minxss_sps_y
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = self._root.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = self._root.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = self._root.IFrame(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            self.ctl = self._io.read_u1()


    class MinxssTelemetry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.minxss_start_sync_flag = self._io.read_u2be()
            _on = self.minxss_start_sync_flag
            if _on == 2073:
                self._raw_minxss_beacon = self._io.read_bytes((self._io.size() - 4))
                io = KaitaiStream(BytesIO(self._raw_minxss_beacon))
                self.minxss_beacon = self._root.MinxssHskpData(io, self, self._root)
            elif _on == 2077:
                self._raw_minxss_beacon = self._io.read_bytes((self._io.size() - 4))
                io = KaitaiStream(BytesIO(self._raw_minxss_beacon))
                self.minxss_beacon = self._root.MinxssRtData(io, self, self._root)
            else:
                self.minxss_beacon = self._io.read_bytes((self._io.size() - 4))
            self.minxss_stop_sync_flag = self._io.ensure_fixed_contents(b"\xA5\xA5")


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            io = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = self._root.MinxssTelemetry(io, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class MinxssRtData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.minxss_rt_data_raw = self._io.read_bytes((self._io.size() - 4))


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.ax25_info = self._io.read_bytes_full()


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return self._m_ssid if hasattr(self, '_m_ssid') else None


    class MinxssHskpData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.minxss_res_1 = [None] * (10)
            for i in range(10):
                self.minxss_res_1[i] = self._io.read_u1()

            self.minxss_spacecraft_flags = self._io.read_u1()
            self.minxss_pointing_mode = self._io.read_u1()
            self.minxss_res_2 = self._io.read_u2be()
            self.minxss_cmd_accept_cnt = self._io.read_u2le()
            self.minxss_res_3 = [None] * (33)
            for i in range(33):
                self.minxss_res_3[i] = self._io.read_u1()

            self.minxss_flight_model = self._io.read_u1()
            self.minxss_res_4 = [None] * (34)
            for i in range(34):
                self.minxss_res_4[i] = self._io.read_u1()

            self.minxss_cdh_board_temp = self._io.read_s2le()
            self.minxss_enable_flags = self._io.read_u2be()
            self.minxss_res_5 = [None] * (32)
            for i in range(32):
                self.minxss_res_5[i] = self._io.read_u1()

            self.minxss_comm_brd_temp = self._io.read_s2le()
            self.minxss_mbrd_temp = self._io.read_s2le()
            self.minxss_res_6 = self._io.read_u2be()
            self.minxss_eps_brd_temp = self._io.read_s2le()
            self.minxss_res_7 = self._io.read_u2be()
            self.minxss_battery_voltage = self._io.read_u2le()
            self.minxss_res_8 = self._io.read_u2be()
            self.minxss_solar_panel_minus_y_curr = self._io.read_u2le()
            self.minxss_solar_panel_minus_y_volt = self._io.read_u2le()
            self.minxss_solar_panel_plus_x_curr = self._io.read_u2le()
            self.minxss_solar_panel_plus_x_volt = self._io.read_u2le()
            self.minxss_solar_panel_plus_y_curr = self._io.read_u2le()
            self.minxss_solar_panel_plus_y_volt = self._io.read_u2le()
            self.minxss_res_9 = [None] * (12)
            for i in range(12):
                self.minxss_res_9[i] = self._io.read_u1()

            self.minxss_solar_panel_minus_y_temp = self._io.read_u2le()
            self.minxss_solar_panel_plus_x_temp = self._io.read_u2le()
            self.minxss_solar_panel_plus_y_temp = self._io.read_u2le()
            self.minxss_res_0 = self._io.read_u2be()
            self.minxss_battery_chrg_curr = self._io.read_u2le()
            self.minxss_res_a = self._io.read_u2be()
            self.minxss_battery_dchrg_curr = self._io.read_u2le()
            self.minxss_battery_temp = self._io.read_u2le()
            self.minxss_res_b = [None] * (16)
            for i in range(16):
                self.minxss_res_b[i] = self._io.read_u1()

            self.minxss_xp = self._io.read_u4le()
            self.minxss_res_c = [None] * (10)
            for i in range(10):
                self.minxss_res_c[i] = self._io.read_u1()

            self.minxss_sps_x = self._io.read_u2le()
            self.minxss_sps_y = self._io.read_u2le()


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            io = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = self._root.Callsign(io, self, self._root)



