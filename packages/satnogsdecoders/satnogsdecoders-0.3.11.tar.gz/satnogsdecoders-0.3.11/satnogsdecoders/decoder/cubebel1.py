# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Cubebel1(KaitaiStruct):
    """:field dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field hdr_rf_id: ax25_frame.payload.ax25_info.header.rf_id
    :field hdr_opr_time: ax25_frame.payload.ax25_info.header.opr_time
    :field hdr_reboot_cnt: ax25_frame.payload.ax25_info.header.reboot_cnt
    :field hdr_mcusr: ax25_frame.payload.ax25_info.header.mcusr
    :field hdr_pamp_temp: ax25_frame.payload.ax25_info.header.pamp_temp
    :field hdr_pamp_voltage: ax25_frame.payload.ax25_info.header.pamp_voltage
    :field hdr_tx_attenuator: ax25_frame.payload.ax25_info.header.tx_attenuator
    :field hdr_battery_voltage: ax25_frame.payload.ax25_info.header.battery_voltage
    :field hdr_system_voltage: ax25_frame.payload.ax25_info.header.system_voltage
    :field hdr_seq_number: ax25_frame.payload.ax25_info.header.
    :field hdr_pwr_save_state: ax25_frame.payload.ax25_info.header.pwr_save_state
    :field hdr_modem_on_period: ax25_frame.payload.ax25_info.header.modem_on_period
    :field hdr_obc_can_status: ax25_frame.payload.ax25_info.header.obc_can_status
    :field hdr_eps_can_status: ax25_frame.payload.ax25_info.header.eps_can_status
    :field hdr_info_size: ax25_frame.payload.ax25_info.header.info_size
    :field hdr_data_type: ax25_frame.payload.ax25_info.header.data_type
    :field fec_crc_status: ax25_frame.payload.ax25_info.data.fec_crc_status
    :field rx_msg_state: ax25_frame.payload.ax25_info.data.rx_msg_state
    :field rssi: ax25_frame.payload.ax25_info.data.rssi
    :field rf_msg: ax25_frame.payload.ax25_info.data.rf_msg
    :field current_to_gamma: ax25_frame.payload.ax25_info.data.current_to_gamma
    :field current_to_irsensor: ax25_frame.payload.ax25_info.data.current_to_irsensor
    :field current_to_extflash: ax25_frame.payload.ax25_info.data.current_to_extflash
    :field current_to_solarsens: ax25_frame.payload.ax25_info.data.current_to_solarsens
    :field current_to_magnetcoils: ax25_frame.payload.ax25_info.data.current_to_magnetcoils
    :field current_to_coil_x: ax25_frame.payload.ax25_info.data.current_to_coil_x
    :field current_to_coil_y: ax25_frame.payload.ax25_info.data.current_to_coil_y
    :field current_to_coil_pz: ax25_frame.payload.ax25_info.data.current_to_coil_pz
    :field current_to_coil_nz: ax25_frame.payload.ax25_info.data.current_to_coil_nz
    :field battery1_temp: ax25_frame.payload.ax25_info.data.battery1_temp
    :field battery2_temp: ax25_frame.payload.ax25_info.data.battery2_temp
    :field numb_oc_obc: ax25_frame.payload.ax25_info.data.numb_oc_obc
    :field numb_oc_out_gamma: ax25_frame.payload.ax25_info.data.numb_oc_out_gamma
    :field numb_oc_out_rf1: ax25_frame.payload.ax25_info.data.numb_oc_out_rf1
    :field numb_oc_out_rf2: ax25_frame.payload.ax25_info.data.numb_oc_out_rf2
    :field numb_oc_out_flash: ax25_frame.payload.ax25_info.data.numb_oc_out_flash
    :field numb_oc_out_irsens: ax25_frame.payload.ax25_info.data.numb_oc_out_irsens
    :field numb_oc_coil_x: ax25_frame.payload.ax25_info.data.numb_oc_coil_x
    :field numb_oc_coil_y: ax25_frame.payload.ax25_info.data.numb_oc_coil_y
    :field numb_oc_coil_pz: ax25_frame.payload.ax25_info.data.numb_oc_coil_pz
    :field numb_oc_coil_nz: ax25_frame.payload.ax25_info.data.numb_oc_coil_nz
    :field numb_oc_magnetcoils: ax25_frame.payload.ax25_info.data.numb_oc_magnetcoils
    :field numb_oc_solarsens: ax25_frame.payload.ax25_info.data.numb_oc_solarsens
    :field reset_num: ax25_frame.payload.ax25_info.data.reset_num
    :field reset_reason: ax25_frame.payload.ax25_info.data.reset_reason
    :field pwr_sat: ax25_frame.payload.ax25_info.data.pwr_sat
    :field pwr_rf1: ax25_frame.payload.ax25_info.data.pwr_rf1
    :field pwr_rf2: ax25_frame.payload.ax25_info.data.pwr_rf2
    :field pwr_sunsensor: ax25_frame.payload.ax25_info.data.pwr_sunsensor
    :field pwr_gamma: ax25_frame.payload.ax25_info.data.pwr_gamma
    :field pwr_irsensor: ax25_frame.payload.ax25_info.data.pwr_irsensor
    :field pwr_flash: ax25_frame.payload.ax25_info.data.pwr_flash
    :field pwr_magnet_x: ax25_frame.payload.ax25_info.data.pwr_magnet_x
    :field pwr_magnet_y: ax25_frame.payload.ax25_info.data.pwr_magnet_y
    :field pwr_magnet_z: ax25_frame.payload.ax25_info.data.pwr_magnet_z
    :field sys_time: ax25_frame.payload.ax25_info.data.sys_time
    :field adc_correctness: ax25_frame.payload.ax25_info.data.adc_correctness
    :field t_adc1: ax25_frame.payload.ax25_info.data.t_adc1
    :field t_adc2: ax25_frame.payload.ax25_info.data.t_adc2
    :field stepup_current: ax25_frame.payload.ax25_info.data.stepup_current
    :field stetup_voltage: ax25_frame.payload.ax25_info.data.stetup_voltage
    :field afterbq_current: ax25_frame.payload.ax25_info.data.afterbq_current
    :field battery_voltage: ax25_frame.payload.ax25_info.data.battery_voltage
    :field sys_voltage_50: ax25_frame.payload.ax25_info.data.sys_voltage_50
    :field sys_voltage_33: ax25_frame.payload.ax25_info.data.sys_voltage_33
    :field eps_uc_current: ax25_frame.payload.ax25_info.data.eps_uc_current
    :field obc_uc_current: ax25_frame.payload.ax25_info.data.obc_uc_current
    :field rf1_uc_current: ax25_frame.payload.ax25_info.data.rf1_uc_current
    :field rf2_uc_current: ax25_frame.payload.ax25_info.data.rf2_uc_current
    :field solar_voltage: ax25_frame.payload.ax25_info.data.solar_voltage
    :field side_x_current: ax25_frame.payload.ax25_info.data.side_x_current
    :field side_py_current: ax25_frame.payload.ax25_info.data.side_py_current
    :field side_ny_current: ax25_frame.payload.ax25_info.data.side_ny_current
    :field side_pz_current: ax25_frame.payload.ax25_info.data.side_pz_current
    :field side_nz_current: ax25_frame.payload.ax25_info.data.side_nz_current
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
            self.ax25_info = self._root.Frame(io, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class RfMessage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rf_msg = self._io.read_bytes((self._parent.header.info_size - 1))


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.ax25_info = self._io.read_bytes_full()


    class Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = self._root.Header(self._io, self, self._root)
            if self.header.info_size > 0:
                _on = self.header.data_type
                if _on == 1:
                    self.data = self._root.RfResponse(self._io, self, self._root)
                elif _on == 3:
                    self.data = self._root.RfMessage(self._io, self, self._root)
                elif _on == 254:
                    self.data = self._root.EpsFullTel(self._io, self, self._root)
                elif _on == 255:
                    self.data = self._root.EpsShortTel(self._io, self, self._root)



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
            self.sys_time = self._io.read_u2le()
            self.adc_correctness = self._io.read_bits_int(2)
            self.t_adc1 = self._io.read_bits_int(12)
            self.t_adc2 = self._io.read_bits_int(12)
            self.stepup_current = self._io.read_bits_int(12)
            self.stetup_voltage = self._io.read_bits_int(12)
            self.afterbq_current = self._io.read_bits_int(12)
            self.battery_voltage = self._io.read_bits_int(12)
            self.sys_voltage_50 = self._io.read_bits_int(12)
            self.sys_voltage_33 = self._io.read_bits_int(12)
            self.eps_uc_current = self._io.read_bits_int(12)
            self.obc_uc_current = self._io.read_bits_int(10)
            self.rf1_uc_current = self._io.read_bits_int(10)
            self.rf2_uc_current = self._io.read_bits_int(12)
            self.solar_voltage = self._io.read_bits_int(12)
            self.side_x_current = self._io.read_bits_int(12)
            self.side_py_current = self._io.read_bits_int(12)
            self.side_ny_current = self._io.read_bits_int(12)
            self.side_pz_current = self._io.read_bits_int(12)
            self.side_nz_current = self._io.read_bits_int(12)


    class RfResponse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.fec_crc_status = self._io.read_bits_int(1) != 0
            self.rx_msg_state = self._io.read_bits_int(7)
            self._io.align_to_byte()
            self.rssi = self._io.read_u1()


    class EpsFullTel(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.eps_short_tel = self._root.EpsShortTel(self._io, self, self._root)
            self.current_to_gamma = self._io.read_bits_int(12)
            self.current_to_irsensor = self._io.read_bits_int(12)
            self.current_to_extflash = self._io.read_bits_int(12)
            self.current_to_solarsens = self._io.read_bits_int(12)
            self.current_to_magnetcoils = self._io.read_bits_int(12)
            self.current_to_coil_x = self._io.read_bits_int(12)
            self.current_to_coil_y = self._io.read_bits_int(12)
            self.current_to_coil_pz = self._io.read_bits_int(12)
            self.current_to_coil_nz = self._io.read_bits_int(12)
            self.battery1_temp = self._io.read_bits_int(12)
            self.battery2_temp = self._io.read_bits_int(12)
            self._io.align_to_byte()
            self.numb_oc_obc = self._io.read_u1()
            self.numb_oc_out_gamma = self._io.read_u1()
            self.numb_oc_out_rf1 = self._io.read_u1()
            self.numb_oc_out_rf2 = self._io.read_u1()
            self.numb_oc_out_flash = self._io.read_u1()
            self.numb_oc_out_irsens = self._io.read_u1()
            self.numb_oc_coil_x = self._io.read_u1()
            self.numb_oc_coil_y = self._io.read_u1()
            self.numb_oc_coil_pz = self._io.read_u1()
            self.numb_oc_coil_nz = self._io.read_u1()
            self.numb_oc_magnetcoils = self._io.read_u1()
            self.numb_oc_solarsens = self._io.read_u1()
            self.reset_num = self._io.read_u2le()
            self.reset_reason = self._io.read_u1()
            self.pwr_sat = self._io.read_bits_int(1) != 0
            self.pwr_rf1 = self._io.read_bits_int(1) != 0
            self.pwr_rf2 = self._io.read_bits_int(1) != 0
            self.pwr_sunsensor = self._io.read_bits_int(1) != 0
            self.pwr_gamma = self._io.read_bits_int(1) != 0
            self.pwr_irsensor = self._io.read_bits_int(1) != 0
            self.pwr_flash = self._io.read_bits_int(1) != 0
            self.pwr_magnet_x = self._io.read_bits_int(1) != 0
            self.pwr_magnet_y = self._io.read_bits_int(1) != 0
            self.pwr_magnet_z = self._io.read_bits_int(1) != 0


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rf_id = self._io.read_u1()
            self.opr_time = self._io.read_u2le()
            self.reboot_cnt = self._io.read_u1()
            self.mcusr = self._io.read_u1()
            self.pamp_temp = self._io.read_u2le()
            self.pamp_voltage = self._io.read_u1()
            self.tx_attenuator = self._io.read_u1()
            self.battery_voltage = self._io.read_u2le()
            self.system_voltage = self._io.read_u2le()
            self.seq_number = self._io.read_u2le()
            self.pwr_save_state = self._io.read_u1()
            self.modem_on_period = self._io.read_u2le()
            self.obc_can_status = self._io.read_u1()
            self.eps_can_status = self._io.read_u1()
            self.info_size = self._io.read_u1()
            self.data_type = self._io.read_u1()


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



