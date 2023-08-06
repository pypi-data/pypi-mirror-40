# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Uwe4(KaitaiStruct):
    """:field uwe4_dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field uwe4_src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field uwe4_src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field uwe4_dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field uwe4_ctl: ax25_frame.ax25_header.ctl
    :field uwe4_pid: ax25_frame.payload.pid
    :field uwe4_beacon_header_flags1: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_flags1
    :field uwe4_beacon_header_flags2: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_flags2
    :field uwe4_beacon_header_packet_id: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_packet_id
    :field uwe4_beacon_header_fm_system_id: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_fm_system_id
    :field uwe4_beacon_header_fm_subsystem_id: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_fm_subsystem_id
    :field uwe4_beacon_header_to_system_id: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_to_system_id
    :field uwe4_beacon_header_to_subsystem_id: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_to_subsystem_id
    :field uwe4_beacon_header_api: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_api
    :field uwe4_beacon_header_payload_size: ax25_frame.payload.ax25_info.uwe4_beacon_header.uwe4_beacon_header_payload_size
    :field uwe4_beacon_payload_command: ax25_frame.payload.ax25_info.uwe4_beacon_payload_command
    :field uwe4_beacon_payload_var_id: ax25_frame.payload.ax25_info.uwe4_beacon_payload_var_id
    :field uwe4_beacon_payload_typeandlength: ax25_frame.payload.ax25_info.uwe4_beacon_payload_typeandlength
    :field uwe4_beacon_payload_timestamp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_timestamp
    :field uwe4_beacon_payload_beacon_rate: ax25_frame.payload.ax25_info.uwe4_beacon_payload_beacon_rate
    :field uwe4_beacon_payload_vals_out_of_range: ax25_frame.payload.ax25_info.uwe4_beacon_payload_vals_out_of_range
    :field uwe4_beacon_payload_uptime: ax25_frame.payload.ax25_info.uwe4_beacon_payload_uptime
    :field uwe4_beacon_payload_subsystem_status_bitmap: ax25_frame.payload.ax25_info.uwe4_beacon_payload_subsystem_status.uwe4_beacon_payload_subsystem_status_bitmap
    :field uwe4_beacon_payload_batt_a_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_a_temp
    :field uwe4_beacon_payload_batt_a_state_of_charge: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_a_state_of_charge
    :field uwe4_beacon_payload_batt_b_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_b_temp
    :field uwe4_beacon_payload_batt_b_state_of_charge: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_b_state_of_charge
    :field uwe4_beacon_payload_batt_a_current: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_a_current
    :field uwe4_beacon_payload_batt_a_voltage: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_a_voltage
    :field uwe4_beacon_payload_batt_b_current: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_b_current
    :field uwe4_beacon_payload_batt_b_voltage: ax25_frame.payload.ax25_info.uwe4_beacon_payload_batt_b_voltage
    :field uwe4_beacon_payload_power_consumption: ax25_frame.payload.ax25_info.uwe4_beacon_payload_power_consumption
    :field uwe4_beacon_payload_obc_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_obc_temp
    :field uwe4_beacon_payload_panel_pos_x_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_panel_pos_x_temp
    :field uwe4_beacon_payload_panel_neg_x_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_panel_neg_x_temp
    :field uwe4_beacon_payload_panel_pos_y_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_panel_pos_y_temp
    :field uwe4_beacon_payload_panel_neg_y_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_panel_neg_y_temp
    :field uwe4_beacon_payload_panel_pos_z_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_panel_pos_z_temp
    :field uwe4_beacon_payload_panel_neg_z_temp: ax25_frame.payload.ax25_info.uwe4_beacon_payload_panel_neg_z_temp
    :field uwe4_beacon_payload_freq: ax25_frame.payload.ax25_info.uwe4_beacon_payload_freq
    :field uwe4_beacon_payload_crc: ax25_frame.payload.ax25_info.uwe4_beacon_payload_crc
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
            self.ax25_info = self._root.Uwe4Beacon(io, self, self._root)


    class Bitmap16SubsystemStatus(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.uwe4_beacon_payload_subsystem_status_bitmap = self._io.read_bytes(2)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class Uwe4Beacon(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_uwe4_beacon_header = self._io.read_bytes(10)
            io = KaitaiStream(BytesIO(self._raw_uwe4_beacon_header))
            self.uwe4_beacon_header = self._root.Uwe4BeaconHeader(io, self, self._root)
            self.uwe4_beacon_payload_command = self._io.read_u1()
            self.uwe4_beacon_payload_var_id = self._io.read_u2le()
            self.uwe4_beacon_payload_typeandlength = self._io.read_u2le()
            self.uwe4_beacon_payload_timestamp = self._io.read_bytes(6)
            self.uwe4_beacon_payload_beacon_rate = self._io.read_u4le()
            self.uwe4_beacon_payload_vals_out_of_range = self._io.read_u2le()
            self.uwe4_beacon_payload_uptime = self._io.read_u4le()
            self._raw_uwe4_beacon_payload_subsystem_status = self._io.read_bytes(2)
            io = KaitaiStream(BytesIO(self._raw_uwe4_beacon_payload_subsystem_status))
            self.uwe4_beacon_payload_subsystem_status = self._root.Bitmap16SubsystemStatus(io, self, self._root)
            self.uwe4_beacon_payload_batt_a_temp = self._io.read_s1()
            self.uwe4_beacon_payload_batt_a_state_of_charge = self._io.read_s1()
            self.uwe4_beacon_payload_batt_b_temp = self._io.read_s1()
            self.uwe4_beacon_payload_batt_b_state_of_charge = self._io.read_s1()
            self.uwe4_beacon_payload_batt_a_current = self._io.read_s2le()
            self.uwe4_beacon_payload_batt_a_voltage = self._io.read_s2le()
            self.uwe4_beacon_payload_batt_b_current = self._io.read_s2le()
            self.uwe4_beacon_payload_batt_b_voltage = self._io.read_s2le()
            self.uwe4_beacon_payload_power_consumption = self._io.read_s2le()
            self.uwe4_beacon_payload_obc_temp = self._io.read_s1()
            self.uwe4_beacon_payload_panel_pos_x_temp = self._io.read_s1()
            self.uwe4_beacon_payload_panel_neg_x_temp = self._io.read_s1()
            self.uwe4_beacon_payload_panel_pos_y_temp = self._io.read_s1()
            self.uwe4_beacon_payload_panel_neg_y_temp = self._io.read_s1()
            self.uwe4_beacon_payload_panel_pos_z_temp = self._io.read_s1()
            self.uwe4_beacon_payload_panel_neg_z_temp = self._io.read_s1()
            self.uwe4_beacon_payload_freq = self._io.read_u2le()
            self.uwe4_beacon_payload_crc = self._io.read_u2le()


    class Uwe4BeaconHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.uwe4_beacon_header_flags1 = self._io.read_u1()
            self.uwe4_beacon_header_flags2 = self._io.read_u1()
            self.uwe4_beacon_header_packet_id = self._io.read_u2le()
            self.uwe4_beacon_header_fm_system_id = self._io.read_u1()
            self.uwe4_beacon_header_fm_subsystem_id = self._io.read_u1()
            self.uwe4_beacon_header_to_system_id = self._io.read_u1()
            self.uwe4_beacon_header_to_subsystem_id = self._io.read_u1()
            self.uwe4_beacon_header_api = self._io.read_u1()
            self.uwe4_beacon_header_payload_size = self._io.read_u1()


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



