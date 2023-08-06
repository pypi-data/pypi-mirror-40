# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cubebel1(KaitaiStruct):
    """:field cubebel1_dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field cubebel1_src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field cubebel1_src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field cubebel1_dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field cubebel1_ctl: ax25_frame.ax25_header.ctl
    :field cubebel1_pid: ax25_frame.payload.pid
    :field cubebel1_rf_id: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_rf_id
    :field cubebel1_opr_time: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_opr_time
    :field cubebel1_reboot_cnt: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_reboot_cnt
    :field cubebel1_mcusr: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_mcusr
    :field cubebel1_pamp_temp: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_pamp_temp
    :field cubebel1_pamp_voltage: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_pamp_voltage
    :field cubebel1_tx_attenuator: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_tx_attenuator
    :field cubebel1_battery_voltage: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_battery_voltage
    :field cubebel1_system_voltage: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_header.cubebel1_system_voltage
    :field cubebel1_seq_number: ax25_frame.payload.ax25_info.cubebel1_header.
    :field cubebel1_pwr_save_state: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_pwr_save_state
    :field cubebel1_modem_on_period: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_modem_on_period
    :field cubebel1_obc_can_status: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_obc_can_status
    :field cubebel1_eps_can_status: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_eps_can_status
    :field cubebel1_info_size: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_info_size
    :field cubebel1_data_type: ax25_frame.payload.ax25_info.cubebel1_header.cubebel1_data_type
    :field cubebel1_fec_crc_status: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_fec_crc_status
    :field cubebel1_rx_msg_state: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_rx_msg_state
    :field cubebel1_rssi: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_rssi
    :field cubebel1_rf_msg: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_rf_msg
    :field cubebel1_current_to_gamma: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_gamma
    :field cubebel1_current_to_irsensor: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_irsensor
    :field cubebel1_current_to_extflash: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_extflash
    :field cubebel1_current_to_solarsens: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_solarsens
    :field cubebel1_current_to_magnetcoils: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_magnetcoils
    :field cubebel1_current_to_coil_x: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_coil_x
    :field cubebel1_current_to_coil_y: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_coil_y
    :field cubebel1_current_to_coil_pz: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_coil_pz
    :field cubebel1_current_to_coil_nz: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_current_to_coil_nz
    :field cubebel1_battery1_temp: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_battery1_temp
    :field cubebel1_battery2_temp: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_battery2_temp
    :field cubebel1_numb_oc_obc: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_obc
    :field cubebel1_numb_oc_out_gamma: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_out_gamma
    :field cubebel1_numb_oc_out_rf1: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_out_rf1
    :field cubebel1_numb_oc_out_rf2: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_out_rf2
    :field cubebel1_numb_oc_out_flash: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_out_flash
    :field cubebel1_numb_oc_out_irsens: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_out_irsens
    :field cubebel1_numb_oc_coil_x: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_coil_x
    :field cubebel1_numb_oc_coil_y: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_coil_y
    :field cubebel1_numb_oc_coil_pz: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_coil_pz
    :field cubebel1_numb_oc_coil_nz: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_coil_nz
    :field cubebel1_numb_oc_magnetcoils: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_magnetcoils
    :field cubebel1_numb_oc_solarsens: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_numb_oc_solarsens
    :field cubebel1_reset_num: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_reset_num
    :field cubebel1_reset_reason: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_reset_reason
    :field cubebel1_pwr_sat: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_sat
    :field cubebel1_pwr_rf1: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_rf1
    :field cubebel1_pwr_rf2: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_rf2
    :field cubebel1_pwr_sunsensor: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_sunsensor
    :field cubebel1_pwr_gamma: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_gamma
    :field cubebel1_pwr_irsensor: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_irsensor
    :field cubebel1_pwr_flash: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_flash
    :field cubebel1_pwr_magnet_x: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_magnet_x
    :field cubebel1_pwr_magnet_y: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_magnet_y
    :field cubebel1_pwr_magnet_z: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_pwr_magnet_z
    :field cubebel1_sys_time: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_sys_time
    :field cubebel1_adc_correctness: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_adc_correctness
    :field cubebel1_t_adc1: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_t_adc1
    :field cubebel1_t_adc2: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_t_adc2
    :field cubebel1_stepup_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_stepup_current
    :field cubebel1_stetup_voltage: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_stetup_voltage
    :field cubebel1_afterbq_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_afterbq_current
    :field cubebel1_battery_voltage: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_battery_voltage
    :field cubebel1_sys_voltage_50: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_sys_voltage_50
    :field cubebel1_sys_voltage_33: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_sys_voltage_33
    :field cubebel1_eps_uc_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_eps_uc_current
    :field cubebel1_obc_uc_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_obc_uc_current
    :field cubebel1_rf1_uc_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_rf1_uc_current
    :field cubebel1_rf2_uc_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_rf2_uc_current
    :field cubebel1_solar_voltage: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_solar_voltage
    :field cubebel1_side_x_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_side_x_current
    :field cubebel1_side_py_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_side_py_current
    :field cubebel1_side_ny_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_side_ny_current
    :field cubebel1_side_pz_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_side_pz_current
    :field cubebel1_side_nz_current: ax25_frame.payload.ax25_info.cubebel1_data.cubebel1_side_nz_current
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
            self.ax25_info = self._root.Cubebel1Frame(io, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class Cubebel1Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_header = self._root.Cubebel1Header(self._io, self, self._root)
            if self.cubebel1_header.cubebel1_info_size > 0:
                _on = self.cubebel1_header.cubebel1_data_type
                if _on == 1:
                    self.cubebel1_data = self._root.RfResponse(self._io, self, self._root)
                elif _on == 3:
                    self.cubebel1_data = self._root.RfMessage(self._io, self, self._root)
                elif _on == 254:
                    self.cubebel1_data = self._root.EpsFullTel(self._io, self, self._root)
                elif _on == 255:
                    self.cubebel1_data = self._root.EpsShortTel(self._io, self, self._root)



    class RfMessage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_rf_msg = self._io.read_bytes((self._parent.cubebel1_header.cubebel1_info_size - 1))


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


    class EpsShortTel(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_sys_time = self._io.read_u2le()
            self.cubebel1_adc_correctness = self._io.read_bits_int(2)
            self.cubebel1_t_adc1 = self._io.read_bits_int(12)
            self.cubebel1_t_adc2 = self._io.read_bits_int(12)
            self.cubebel1_stepup_current = self._io.read_bits_int(12)
            self.cubebel1_stetup_voltage = self._io.read_bits_int(12)
            self.cubebel1_afterbq_current = self._io.read_bits_int(12)
            self.cubebel1_battery_voltage = self._io.read_bits_int(12)
            self.cubebel1_sys_voltage_50 = self._io.read_bits_int(12)
            self.cubebel1_sys_voltage_33 = self._io.read_bits_int(12)
            self.cubebel1_eps_uc_current = self._io.read_bits_int(12)
            self.cubebel1_obc_uc_current = self._io.read_bits_int(10)
            self.cubebel1_rf1_uc_current = self._io.read_bits_int(10)
            self.cubebel1_rf2_uc_current = self._io.read_bits_int(12)
            self.cubebel1_solar_voltage = self._io.read_bits_int(12)
            self.cubebel1_side_x_current = self._io.read_bits_int(12)
            self.cubebel1_side_py_current = self._io.read_bits_int(12)
            self.cubebel1_side_ny_current = self._io.read_bits_int(12)
            self.cubebel1_side_pz_current = self._io.read_bits_int(12)
            self.cubebel1_side_nz_current = self._io.read_bits_int(12)


    class RfResponse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_fec_crc_status = self._io.read_bits_int(1) != 0
            self.cubebel1_rx_msg_state = self._io.read_bits_int(7)
            self._io.align_to_byte()
            self.cubebel1_rssi = self._io.read_u1()


    class EpsFullTel(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.eps_short_tel = self._root.EpsShortTel(self._io, self, self._root)
            self.cubebel1_current_to_gamma = self._io.read_bits_int(12)
            self.cubebel1_current_to_irsensor = self._io.read_bits_int(12)
            self.cubebel1_current_to_extflash = self._io.read_bits_int(12)
            self.cubebel1_current_to_solarsens = self._io.read_bits_int(12)
            self.cubebel1_current_to_magnetcoils = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_x = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_y = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_pz = self._io.read_bits_int(12)
            self.cubebel1_current_to_coil_nz = self._io.read_bits_int(12)
            self.cubebel1_battery1_temp = self._io.read_bits_int(12)
            self.cubebel1_battery2_temp = self._io.read_bits_int(12)
            self._io.align_to_byte()
            self.cubebel1_numb_oc_obc = self._io.read_u1()
            self.cubebel1_numb_oc_out_gamma = self._io.read_u1()
            self.cubebel1_numb_oc_out_rf1 = self._io.read_u1()
            self.cubebel1_numb_oc_out_rf2 = self._io.read_u1()
            self.cubebel1_numb_oc_out_flash = self._io.read_u1()
            self.cubebel1_numb_oc_out_irsens = self._io.read_u1()
            self.cubebel1_numb_oc_coil_x = self._io.read_u1()
            self.cubebel1_numb_oc_coil_y = self._io.read_u1()
            self.cubebel1_numb_oc_coil_pz = self._io.read_u1()
            self.cubebel1_numb_oc_coil_nz = self._io.read_u1()
            self.cubebel1_numb_oc_magnetcoils = self._io.read_u1()
            self.cubebel1_numb_oc_solarsens = self._io.read_u1()
            self.cubebel1_reset_num = self._io.read_u2le()
            self.cubebel1_reset_reason = self._io.read_u1()
            self.cubebel1_pwr_sat = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_rf1 = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_rf2 = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_sunsensor = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_gamma = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_irsensor = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_flash = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_magnet_x = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_magnet_y = self._io.read_bits_int(1) != 0
            self.cubebel1_pwr_magnet_z = self._io.read_bits_int(1) != 0


    class Cubebel1Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.cubebel1_rf_id = self._io.read_u1()
            self.cubebel1_opr_time = self._io.read_u2le()
            self.cubebel1_reboot_cnt = self._io.read_u1()
            self.cubebel1_mcusr = self._io.read_u1()
            self.cubebel1_pamp_temp = self._io.read_u2le()
            self.cubebel1_pamp_voltage = self._io.read_u1()
            self.cubebel1_tx_attenuator = self._io.read_u1()
            self.cubebel1_battery_voltage = self._io.read_u2le()
            self.cubebel1_system_voltage = self._io.read_u2le()
            self.cubebel1_seq_number = self._io.read_u2le()
            self.cubebel1_pwr_save_state = self._io.read_u1()
            self.cubebel1_modem_on_period = self._io.read_u2le()
            self.cubebel1_obc_can_status = self._io.read_u1()
            self.cubebel1_eps_can_status = self._io.read_u1()
            self.cubebel1_info_size = self._io.read_u1()
            self.cubebel1_data_type = self._io.read_u1()


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



