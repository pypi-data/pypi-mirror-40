# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
import satnogsdecoders.process


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Elfin(KaitaiStruct):
    """:field elfin_dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field elfin_src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field elfin_src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field elfin_dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field elfin_ctl: ax25_frame.ax25_header.ctl
    :field elfin_pid: ax25_frame.payload.pid
    :field elfin_frame_start: ax25_frame.payload.ax25_info.elfin_frame_start
    :field elfin_beacon_setting: ax25_frame.payload.ax25_info.elfin_beacon_setting
    :field elfin_status_1_safe_mode: ax25_frame.payload.ax25_info.elfin_status_1_safe_mode
    :field elfin_status_1_reserved: ax25_frame.payload.ax25_info.elfin_status_1_reserved
    :field elfin_status_1_early_orbit: ax25_frame.payload.ax25_info.elfin_status_1_early_orbit
    :field elfin_status_2_payload_power: ax25_frame.payload.ax25_info.elfin_status_2_payload_power
    :field elfin_status_2_9v_boost: ax25_frame.payload.ax25_info.elfin_status_2_9v_boost
    :field elfin_status_2_bat_htr_allow: ax25_frame.payload.ax25_info.
    :field elfin_status_2_htr_force: ax25_frame.payload.ax25_info.elfin_status_2_htr_force
    :field elfin_status_2_htr_alert: ax25_frame.payload.ax25_info.elfin_status_2_htr_alert
    :field elfin_status_2_reserved: ax25_frame.payload.ax25_info.elfin_status_2_reserved
    :field elfin_reserved: ax25_frame.payload.ax25_info.elfin_reserved
    :field elfin_hskp_pwr1_rtcc_year: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_year
    :field elfin_hskp_pwr1_rtcc_month: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_month
    :field elfin_hskp_pwr1_rtcc_day: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_day
    :field elfin_hskp_pwr1_rtcc_hour: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_hour
    :field elfin_hskp_pwr1_rtcc_minute: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_minute
    :field elfin_hskp_pwr1_rtcc_second: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_second
    :field elfin_hskp_pwr1_adc_data_adc_sa_volt_12: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_adc_sa_volt_12
    :field elfin_hskp_pwr1_adc_data_adc_sa_volt_34: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_adc_sa_volt_34
    :field elfin_hskp_pwr1_adc_data_adc_sa_volt_56: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_adc_sa_volt_56
    :field elfin_hskp_pwr1_adc_data_sa_short_circuit_current: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_sa_short_circuit_current
    :field elfin_hskp_pwr1_adc_data_bat_2_volt: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_bat_2_volt
    :field elfin_hskp_pwr1_adc_data_bat_1_volt: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_bat_1_volt
    :field elfin_hskp_pwr1_adc_data_reg_sa_volt_1: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_reg_sa_volt_1
    :field elfin_hskp_pwr1_adc_data_reg_sa_volt_2: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_reg_sa_volt_2
    :field elfin_hskp_pwr1_adc_data_reg_sa_volt_3: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_reg_sa_volt_3
    :field elfin_hskp_pwr1_adc_data_power_bus_current_1: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_power_bus_current_1
    :field elfin_hskp_pwr1_adc_data_power_bus_current_2: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_power_bus_current_2
    :field elfin_hskp_pwr1_bat_mon_1_avg_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_avg_cur_reg
    :field elfin_hskp_pwr1_bat_mon_1_temperature_register: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_temperature_register
    :field elfin_hskp_pwr1_bat_mon_1_volt_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_volt_reg
    :field elfin_hskp_pwr1_bat_mon_1_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_cur_reg
    :field elfin_hskp_pwr1_bat_mon_1_acc_curr_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_acc_curr_reg
    :field elfin_hskp_pwr1_bat_mon_2_avg_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_avg_cur_reg
    :field elfin_hskp_pwr1_bat_mon_2_temperature_register: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_temperature_register
    :field elfin_hskp_pwr1_bat_mon_2_volt_reg: ax2_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_volt_reg
    :field elfin_hskp_pwr1_bat_mon_2_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_cur_reg
    :field elfin_hskp_pwr1_bat_mon_2_acc_curr_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_acc_curr_reg
    :field elfin_hskp_pwr1_bv_mon: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bv_mon
    :field elfin_hskp_pwr1_tmps_tmp1: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp1
    :field elfin_hskp_pwr1_tmps_tmp2: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp2
    :field elfin_hskp_pwr1_tmps_tmp3: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp3
    :field elfin_hskp_pwr1_tmps_tmp4: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp4
    :field elfin_hskp_pwr1_accumulated_curr_bat1_rarc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat1_rarc
    :field elfin_hskp_pwr1_accumulated_curr_bat1_rsrc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat1_rsrc
    :field elfin_hskp_pwr1_accumulated_curr_bat2_rarc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat2_rarc
    :field elfin_hskp_pwr1_accumulated_curr_bat2_rsrc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat2_rsrc
    :field elfin_hskp_pwr2_rtcc_year: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_rtcc_year
    :field elfin_hskp_pwr2_rtcc_month: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_rtcc_month
    :field elfin_hskp_pwr2_rtcc_day: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_rtcc_day
    :field elfin_hskp_pwr2_rtcc_hour: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_rtcc_hour
    :field elfin_hskp_pwr2_rtcc_minute: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_rtcc_minute
    :field elfin_hskp_pwr2_rtcc_second: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_rtcc_second
    :field elfin_hskp_pwr2_adc_data_adc_sa_volt_12: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_adc_sa_volt_12
    :field elfin_hskp_pwr2_adc_data_adc_sa_volt_34: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_adc_sa_volt_34
    :field elfin_hskp_pwr2_adc_data_adc_sa_volt_56: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_adc_sa_volt_56
    :field elfin_hskp_pwr2_adc_data_sa_short_circuit_current: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_sa_short_circuit_current
    :field elfin_hskp_pwr2_adc_data_bat_2_volt: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_bat_2_volt
    :field elfin_hskp_pwr2_adc_data_bat_1_volt: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_bat_1_volt
    :field elfin_hskp_pwr2_adc_data_reg_sa_volt_1: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_reg_sa_volt_1
    :field elfin_hskp_pwr2_adc_data_reg_sa_volt_2: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_reg_sa_volt_2
    :field elfin_hskp_pwr2_adc_data_reg_sa_volt_3: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_reg_sa_volt_3
    :field elfin_hskp_pwr2_adc_data_power_bus_current_1: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_power_bus_current_1
    :field elfin_hskp_pwr2_adc_data_power_bus_current_2: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_adc_data_power_bus_current_2
    :field elfin_hskp_pwr2_bat_mon_1_avg_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_1_avg_cur_reg
    :field elfin_hskp_pwr2_bat_mon_1_temperature_register: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_1_temperature_register
    :field elfin_hskp_pwr2_bat_mon_1_volt_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_1_volt_reg
    :field elfin_hskp_pwr2_bat_mon_1_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_1_cur_reg
    :field elfin_hskp_pwr2_bat_mon_1_acc_curr_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_1_acc_curr_reg
    :field elfin_hskp_pwr2_bat_mon_2_avg_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_2_avg_cur_reg
    :field elfin_hskp_pwr2_bat_mon_2_temperature_register: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_2_temperature_register
    :field elfin_hskp_pwr2_bat_mon_2_volt_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_2_volt_reg
    :field elfin_hskp_pwr2_bat_mon_2_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_2_cur_reg
    :field elfin_hskp_pwr2_bat_mon_2_acc_curr_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bat_mon_2_acc_curr_reg
    :field elfin_hskp_pwr2_bv_mon: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_bv_mon
    :field elfin_hskp_pwr2_tmps_tmp1: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_tmps_tmp1
    :field elfin_hskp_pwr2_tmps_tmp2: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_tmps_tmp2
    :field elfin_hskp_pwr2_tmps_tmp3: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_tmps_tmp3
    :field elfin_hskp_pwr2_tmps_tmp4: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_tmps_tmp4
    :field elfin_hskp_pwr2_accumulated_curr_bat1_rarc: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_accumulated_curr_bat1_rarc
    :field elfin_hskp_pwr2_accumulated_curr_bat1_rsrc: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_accumulated_curr_bat1_rsrc
    :field elfin_hskp_pwr2_accumulated_curr_bat2_rarc: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_accumulated_curr_bat2_rarc
    :field elfin_hskp_pwr2_accumulated_curr_bat2_rsrc: ax25_frame.payload.ax25_info.elfin_hskp_pwr2_accumulated_curr_bat2_rsrc
    :field elfin_acb_pc_data1_rtcc_year: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_rtcc_year
    :field elfin_acb_pc_data1_rtcc_month: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_rtcc_month
    :field elfin_acb_pc_data1_rtcc_day: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_rtcc_day
    :field elfin_acb_pc_data1_rtcc_hour: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_rtcc_hour
    :field elfin_acb_pc_data1_rtcc_minute: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_rtcc_minute
    :field elfin_acb_pc_data1_rtcc_second: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_rtcc_second
    :field elfin_acb_pc_data1_acb_mrm_x: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_acb_mrm_x
    :field elfin_acb_pc_data1_acb_mrm_y: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_acb_mrm_y
    :field elfin_acb_pc_data1_acb_mrm_z: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_acb_mrm_z
    :field elfin_acb_pc_data1_ipdu_mrm_x: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_ipdu_mrm_x
    :field elfin_acb_pc_data1_ipdu_mrm_y: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_ipdu_mrm_y
    :field elfin_acb_pc_data1_ipdu_mrm_z: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_ipdu_mrm_z
    :field elfin_acb_pc_data1_tmps_tmp1: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_tmps_tmp1
    :field elfin_acb_pc_data1_tmps_tmp2: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_tmps_tmp2
    :field elfin_acb_pc_data1_tmps_tmp3: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_tmps_tmp3
    :field elfin_acb_pc_data1_tmps_tmp4: ax25_frame.payload.ax25_info.elfin_acb_pc_data1_tmps_tmp4
    :field elfin_acb_pc_data2_rtcc_year: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_rtcc_year
    :field elfin_acb_pc_data2_rtcc_month: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_rtcc_month
    :field elfin_acb_pc_data2_rtcc_day: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_rtcc_day
    :field elfin_acb_pc_data2_rtcc_hour: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_rtcc_hour
    :field elfin_acb_pc_data2_rtcc_minute: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_rtcc_minute
    :field elfin_acb_pc_data2_rtcc_second: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_rtcc_second
    :field elfin_acb_pc_data2_acb_mrm_x: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_acb_mrm_x
    :field elfin_acb_pc_data2_acb_mrm_y: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_acb_mrm_y
    :field elfin_acb_pc_data2_acb_mrm_z: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_acb_mrm_z
    :field elfin_acb_pc_data2_ipdu_mrm_x: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_ipdu_mrm_x
    :field elfin_acb_pc_data2_ipdu_mrm_y: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_ipdu_mrm_y
    :field elfin_acb_pc_data2_ipdu_mrm_z: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_ipdu_mrm_z
    :field elfin_acb_pc_data2_tmps_tmp1: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_tmps_tmp1
    :field elfin_acb_pc_data2_tmps_tmp2: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_tmps_tmp2
    :field elfin_acb_pc_data2_tmps_tmp3: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_tmps_tmp3
    :field elfin_acb_pc_data2_tmps_tmp4: ax25_frame.payload.ax25_info.elfin_acb_pc_data2_tmps_tmp4
    :field elfin_acb_sense_adc_data_current: ax25_frame.payload.ax25_info.elfin_acb_sense_adc_data_current
    :field elfin_acb_sense_adc_data_voltage: ax25_frame.payload.ax25_info.elfin_acb_sense_adc_data_voltage
    :field elfin_fc_counters_cmds_recv: ax25_frame.payload.ax25_info.elfin_fc_counters_cmds_recv
    :field elfin_fc_counters_badcmds_recv: ax25_frame.payload.ax25_info.elfin_fc_counters_badcmds_recv
    :field elfin_fc_counters_badpkts_fm_radio: ax25_frame.payload.ax25_info.elfin_fc_counters_badpkts_fm_radio
    :field elfin_fc_counters_fcpkts_fm_radio: ax25_frame.payload.ax25_info.elfin_fc_counters_fcpkts_fm_radio
    :field elfin_fc_counters_errors: ax25_frame.payload.ax25_info.elfin_fc_counters_errors
    :field elfin_fc_counters_reboots: ax25_frame.payload.ax25_info.elfin_fc_counters_reboots
    :field elfin_fc_counters_intrnl_wdttmout: ax25_frame.payload.ax25_info.elfin_fc_counters_intrnl_wdttmout
    :field elfin_fc_counters_brwnouts: ax25_frame.payload.ax25_info.elfin_fc_counters_brwnouts
    :field elfin_fc_counters_wdpicrst: ax25_frame.payload.ax25_info.elfin_fc_counters_wdpicrst
    :field elfin_fc_counters_porst: ax25_frame.payload.ax25_info.elfin_fc_counters_porst
    :field elfin_fc_counters_uart1_recvpkts: ax25_frame.payload.ax25_info.elfin_fc_counters_uart1_recvpkts
    :field elfin_fc_counters_uart1_parseerrs: ax25_frame.payload.ax25_info.elfin_fc_counters_uart1_parseerrs
    :field elfin_fc_counters_sips_ovcur_evts: ax25_frame.payload.ax25_info.elfin_fc_counters_sips_ovcur_evts
    :field elfin_fc_counters_vu1_on: ax25_frame.payload.ax25_info.elfin_fc_counters_vu1_on
    :field elfin_fc_counters_vu1_off: ax25_frame.payload.ax25_info.elfin_fc_counters_vu1_off
    :field elfin_fc_counters_vu2_on: ax25_frame.payload.ax25_info.elfin_fc_counters_vu2_on
    :field elfin_fc_counters_vu2_off: ax25_frame.payload.ax25_info.elfin_fc_counters_vu2_off
    :field elfin_radio_tlm_rssi: ax25_frame.payload.ax25_info.elfin_radio_tlm_rssi
    :field elfin_radio_tlm_bytes_rx: ax25_frame.payload.ax25_info.elfin_radio_tlm_bytes_rx
    :field elfin_radio_tlm_bytes_tx: ax25_frame.payload.ax25_info.elfin_radio_tlm_bytes_tx
    :field elfin_radio_cfg_read_radio_palvl: ax25_frame.payload.ax25_info.elfin_radio_cfg_read_radio_palvl
    :field elfin_errors_error1_day: ax25_frame.payload.ax25_info.elfin_errors_error1_day
    :field elfin_errors_error1_hour: ax25_frame.payload.ax25_info.elfin_errors_error1_hour
    :field elfin_errors_error1_minute: ax25_frame.payload.ax25_info.elfin_errors_error1_minute
    :field elfin_errors_error1_second: ax25_frame.payload.ax25_info.elfin_errors_error1_second
    :field elfin_errors_error1_error: ax25_frame.payload.ax25_info.elfin_errors_error1_error
    :field elfin_errors_error2_day: ax25_frame.payload.ax25_info.elfin_errors_error2_day
    :field elfin_errors_error2_hour: ax25_frame.payload.ax25_info.elfin_errors_error2_hour
    :field elfin_errors_error2_minute: ax25_frame.payload.ax25_info.elfin_errors_error2_minute
    :field elfin_errors_error2_second: ax25_frame.payload.ax25_info.elfin_errors_error2_second
    :field elfin_errors_error2_error: ax25_frame.payload.ax25_info.elfin_errors_error2_error
    :field elfin_errors_error3_day: ax25_frame.payload.ax25_info.elfin_errors_error3_day
    :field elfin_errors_error3_hour: ax25_frame.payload.ax25_info.elfin_errors_error3_hour
    :field elfin_errors_error3_minute: ax25_frame.payload.ax25_info.elfin_errors_error3_minute
    :field elfin_errors_error3_second: ax25_frame.payload.ax25_info.elfin_errors_error3_second
    :field elfin_errors_error3_error: ax25_frame.payload.ax25_info.elfin_errors_error3_error
    :field elfin_errors_error4_day: ax25_frame.payload.ax25_info.elfin_errors_error4_day
    :field elfin_errors_error4_hour: ax25_frame.payload.ax25_info.elfin_errors_error4_hour
    :field elfin_errors_error4_minute: ax25_frame.payload.ax25_info.elfin_errors_error4_minute
    :field elfin_errors_error4_second: ax25_frame.payload.ax25_info.elfin_errors_error4_second
    :field elfin_errors_error4_error: ax25_frame.payload.ax25_info.elfin_errors_error4_error
    :field elfin_errors_error5_day: ax25_frame.payload.ax25_info.elfin_errors_error5_day
    :field elfin_errors_error5_hour: ax25_frame.payload.ax25_info.elfin_errors_error5_hour
    :field elfin_errors_error5_minute: ax25_frame.payload.ax25_info.elfin_errors_error5_minute
    :field elfin_errors_error5_second: ax25_frame.payload.ax25_info.elfin_errors_error5_second
    :field elfin_errors_error5_error: ax25_frame.payload.ax25_info.elfin_errors_error5_error
    :field elfin_errors_error6_day: ax25_frame.payload.ax25_info.elfin_errors_error6_day
    :field elfin_errors_error6_hour: ax25_frame.payload.ax25_info.elfin_errors_error6_hour
    :field elfin_errors_error6_minute: ax25_frame.payload.ax25_info.elfin_errors_error6_minute
    :field elfin_errors_error6_second: ax25_frame.payload.ax25_info.elfin_errors_error6_second
    :field elfin_errors_error6_error: ax25_frame.payload.ax25_info.elfin_errors_error6_error
    :field elfin_errors_error7_day: ax25_frame.payload.ax25_info.elfin_errors_error7_day
    :field elfin_errors_error7_hour: ax25_frame.payload.ax25_info.elfin_errors_error7_hour
    :field elfin_errors_error7_minute: ax25_frame.payload.ax25_info.elfin_errors_error7_minute
    :field elfin_errors_error7_second: ax25_frame.payload.ax25_info.elfin_errors_error7_second
    :field elfin_errors_error7_error: ax25_frame.payload.ax25_info.elfin_errors_error7_error
    :field elfin_fc_salt: ax25_frame.payload.ax25_info.elfin_fc_salt
    :field elfin_fc_crc: ax25_frame.payload.ax25_info.elfin_fc_crc
    :field elfin_frame_end: ax25_frame.payload.ax25_info.elfin_frame_end
    :field elfin_hskp_pwr1_rtcc_year: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_year
    :field elfin_hskp_pwr1_rtcc_month: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_month
    :field elfin_hskp_pwr1_rtcc_day: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_day
    :field elfin_hskp_pwr1_rtcc_hour: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_hour
    :field elfin_hskp_pwr1_rtcc_minute: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_minute
    :field elfin_hskp_pwr1_rtcc_second: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_rtcc_second
    :field elfin_hskp_pwr1_pwr_board_id: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_pwr_board_id
    :field elfin_hskp_pwr1_adc_data_adc_sa_volt_12: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_adc_sa_volt_12
    :field elfin_hskp_pwr1_adc_data_adc_sa_volt_34: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_adc_sa_volt_34
    :field elfin_hskp_pwr1_adc_data_adc_sa_volt_56: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_adc_sa_volt_56
    :field elfin_hskp_pwr1_adc_data_sa_short_circuit_current: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_sa_short_circuit_current
    :field elfin_hskp_pwr1_adc_data_bat_2_volt: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_bat_2_volt
    :field elfin_hskp_pwr1_adc_data_bat_1_volt: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_bat_1_volt
    :field elfin_hskp_pwr1_adc_data_reg_sa_volt_1: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_reg_sa_volt_1
    :field elfin_hskp_pwr1_adc_data_reg_sa_volt_2: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_reg_sa_volt_2
    :field elfin_hskp_pwr1_adc_data_reg_sa_volt_3: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_reg_sa_volt_3
    :field elfin_hskp_pwr1_adc_data_power_bus_current_1: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_power_bus_current_1
    :field elfin_hskp_pwr1_adc_data_power_bus_current_2: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_adc_data_power_bus_current_2
    :field elfin_hskp_pwr1_bat_mon_1_avg_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_avg_cur_reg
    :field elfin_hskp_pwr1_bat_mon_1_temperature_register: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_temperature_register
    :field elfin_hskp_pwr1_bat_mon_1_volt_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_volt_reg
    :field elfin_hskp_pwr1_bat_mon_1_cur_reg: ax25_frame.payload.ax25_info.
    :field elfin_hskp_pwr1_bat_mon_1_acc_curr_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_1_acc_curr_reg
    :field elfin_hskp_pwr1_bat_mon_2_avg_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_avg_cur_reg
    :field elfin_hskp_pwr1_bat_mon_2_temperature_register: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_temperature_register
    :field elfin_hskp_pwr1_bat_mon_2_volt_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_volt_reg
    :field elfin_hskp_pwr1_bat_mon_2_cur_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_cur_reg
    :field elfin_hskp_pwr1_bat_mon_2_acc_curr_reg: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bat_mon_2_acc_curr_reg
    :field elfin_hskp_pwr1_bv_mon: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_bv_mon
    :field elfin_hskp_pwr1_tmps_tmp1: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp1
    :field elfin_hskp_pwr1_tmps_tmp2: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp2
    :field elfin_hskp_pwr1_tmps_tmp3: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp3
    :field elfin_hskp_pwr1_tmps_tmp4: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_tmps_tmp4
    :field elfin_hskp_pwr1_accumulated_curr_bat1_rsrc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat1_rsrc
    :field elfin_hskp_pwr1_accumulated_curr_bat2_rsrc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat2_rsrc
    :field elfin_hskp_pwr1_accumulated_curr_bat1_rarc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat1_rarc
    :field elfin_hskp_pwr1_accumulated_curr_bat2_rarc: ax25_frame.payload.ax25_info.elfin_hskp_pwr1_accumulated_curr_bat2_rarc
    :field elfin_fc_status_safe_mode: ax25_frame.payload.ax25_info.elfin_fc_status_safe_mode
    :field elfin_fc_status_reserved: ax25_frame.payload.ax25_info.elfin_fc_status_reserved
    :field elfin_fc_status_early_orbit: ax25_frame.payload.ax25_info.elfin_fc_status_early_orbit
    :field elfin_frame_start: ax25_frame.payload.ax25_info.elfin_frame_start
    :field elfin_opcode: ax25_frame.payload.ax25_info.elfin_opcode
    :field elfin_fc_crc: ax25_frame.payload.ax25_info.elfin_fc_crc
    :field elfin_frame_end: ax25_frame.payload.ax25_info.elfin_frame_end
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


    class ElfinCmdResponse(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.elfin_frame_start = self._io.read_u1()
            self.elfin_opcode = self._io.read_u1()
            _on = self.elfin_opcode
            if _on == 48:
                self.cmd_response = self._root.ElfinHskpPacket(self._io, self, self._root)
            self.elfin_fc_crc = self._io.read_u1()
            self.elfin_frame_end = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            _on = self._io.size()
            if _on == 269:
                self._raw__raw_ax25_info = self._io.read_bytes_full()
                _process = satnogsdecoders.process.ElfinPp()
                self._raw_ax25_info = _process.decode(self._raw__raw_ax25_info)
                io = KaitaiStream(BytesIO(self._raw_ax25_info))
                self.ax25_info = self._root.ElfinTlmData(io, self, self._root)
            else:
                self._raw__raw_ax25_info = self._io.read_bytes_full()
                _process = satnogsdecoders.process.ElfinPp()
                self._raw_ax25_info = _process.decode(self._raw__raw_ax25_info)
                io = KaitaiStream(BytesIO(self._raw_ax25_info))
                self.ax25_info = self._root.ElfinCmdResponse(io, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


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


    class ElfinTlmData(KaitaiStruct):
        """
        .. seealso::
           Source - https://elfin.igpp.ucla.edu/s/Beacon-Format_v2.xlsx
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.elfin_frame_start = self._io.read_u1()
            self.elfin_beacon_setting = self._io.read_u1()
            self.elfin_status_1_safe_mode = self._io.read_bits_int(1) != 0
            self.elfin_status_1_reserved = self._io.read_bits_int(3)
            self.elfin_status_1_early_orbit = self._io.read_bits_int(4)
            self.elfin_status_2_payload_power = self._io.read_bits_int(1) != 0
            self.elfin_status_2_9v_boost = self._io.read_bits_int(1) != 0
            self.elfin_status_2_bat_htr_allow = self._io.read_bits_int(1) != 0
            self.elfin_status_2_htr_force = self._io.read_bits_int(1) != 0
            self.elfin_status_2_htr_alert = self._io.read_bits_int(1) != 0
            self.elfin_status_2_reserved = self._io.read_bits_int(3)
            self._io.align_to_byte()
            self.elfin_reserved = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_year = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_month = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_day = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_hour = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_minute = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_second = self._io.read_u1()
            self.elfin_hskp_pwr1_adc_data_adc_sa_volt_12 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_adc_sa_volt_34 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_adc_sa_volt_56 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_sa_short_circuit_current = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_bat_2_volt = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_bat_1_volt = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_reg_sa_volt_1 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_reg_sa_volt_2 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_reg_sa_volt_3 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_power_bus_current_1 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_power_bus_current_2 = self._io.read_u2be()
            self.elfin_hskp_pwr1_bat_mon_1_avg_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_temperature_register = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_volt_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_acc_curr_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_avg_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_temperature_register = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_volt_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_acc_curr_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bv_mon = self._io.read_u2be()
            self.elfin_hskp_pwr1_tmps_tmp1 = self._io.read_s2be()
            self.elfin_hskp_pwr1_tmps_tmp2 = self._io.read_s2be()
            self.elfin_hskp_pwr1_tmps_tmp3 = self._io.read_s2be()
            self.elfin_hskp_pwr1_tmps_tmp4 = self._io.read_s2be()
            self.elfin_hskp_pwr1_accumulated_curr_bat1_rarc = self._io.read_u1()
            self.elfin_hskp_pwr1_accumulated_curr_bat1_rsrc = self._io.read_u1()
            self.elfin_hskp_pwr1_accumulated_curr_bat2_rarc = self._io.read_u1()
            self.elfin_hskp_pwr1_accumulated_curr_bat2_rsrc = self._io.read_u1()
            self.elfin_hskp_pwr2_rtcc_year = self._io.read_u1()
            self.elfin_hskp_pwr2_rtcc_month = self._io.read_u1()
            self.elfin_hskp_pwr2_rtcc_day = self._io.read_u1()
            self.elfin_hskp_pwr2_rtcc_hour = self._io.read_u1()
            self.elfin_hskp_pwr2_rtcc_minute = self._io.read_u1()
            self.elfin_hskp_pwr2_rtcc_second = self._io.read_u1()
            self.elfin_hskp_pwr2_adc_data_adc_sa_volt_12 = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_adc_sa_volt_34 = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_adc_sa_volt_56 = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_sa_short_circuit_current = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_bat_2_volt = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_bat_1_volt = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_reg_sa_volt_1 = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_reg_sa_volt_2 = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_reg_sa_volt_3 = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_power_bus_current_1 = self._io.read_u2be()
            self.elfin_hskp_pwr2_adc_data_power_bus_current_2 = self._io.read_u2be()
            self.elfin_hskp_pwr2_bat_mon_1_avg_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_1_temperature_register = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_1_volt_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_1_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_1_acc_curr_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_2_avg_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_2_temperature_register = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_2_volt_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_2_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bat_mon_2_acc_curr_reg = self._io.read_s2be()
            self.elfin_hskp_pwr2_bv_mon = self._io.read_s2be()
            self.elfin_hskp_pwr2_tmps_tmp1 = self._io.read_s2be()
            self.elfin_hskp_pwr2_tmps_tmp2 = self._io.read_s2be()
            self.elfin_hskp_pwr2_tmps_tmp3 = self._io.read_s2be()
            self.elfin_hskp_pwr2_tmps_tmp4 = self._io.read_s2be()
            self.elfin_hskp_pwr2_accumulated_curr_bat1_rarc = self._io.read_u1()
            self.elfin_hskp_pwr2_accumulated_curr_bat1_rsrc = self._io.read_u1()
            self.elfin_hskp_pwr2_accumulated_curr_bat2_rarc = self._io.read_u1()
            self.elfin_hskp_pwr2_accumulated_curr_bat2_rsrc = self._io.read_u1()
            self.elfin_acb_pc_data1_rtcc_year = self._io.read_u1()
            self.elfin_acb_pc_data1_rtcc_month = self._io.read_u1()
            self.elfin_acb_pc_data1_rtcc_day = self._io.read_u1()
            self.elfin_acb_pc_data1_rtcc_hour = self._io.read_u1()
            self.elfin_acb_pc_data1_rtcc_minute = self._io.read_u1()
            self.elfin_acb_pc_data1_rtcc_second = self._io.read_u1()
            self.elfin_acb_pc_data1_acb_mrm_x = self._io.read_s2be()
            self.elfin_acb_pc_data1_acb_mrm_y = self._io.read_s2be()
            self.elfin_acb_pc_data1_acb_mrm_z = self._io.read_s2be()
            self.elfin_acb_pc_data1_ipdu_mrm_x = self._io.read_s2be()
            self.elfin_acb_pc_data1_ipdu_mrm_y = self._io.read_s2be()
            self.elfin_acb_pc_data1_ipdu_mrm_z = self._io.read_s2be()
            self.elfin_acb_pc_data1_tmps_tmp1 = self._io.read_u2be()
            self.elfin_acb_pc_data1_tmps_tmp2 = self._io.read_u2be()
            self.elfin_acb_pc_data1_tmps_tmp3 = self._io.read_u2be()
            self.elfin_acb_pc_data1_tmps_tmp4 = self._io.read_u2be()
            self.elfin_acb_pc_data2_rtcc_year = self._io.read_u1()
            self.elfin_acb_pc_data2_rtcc_month = self._io.read_u1()
            self.elfin_acb_pc_data2_rtcc_day = self._io.read_u1()
            self.elfin_acb_pc_data2_rtcc_hour = self._io.read_u1()
            self.elfin_acb_pc_data2_rtcc_minute = self._io.read_u1()
            self.elfin_acb_pc_data2_rtcc_second = self._io.read_u1()
            self.elfin_acb_pc_data2_acb_mrm_x = self._io.read_s2be()
            self.elfin_acb_pc_data2_acb_mrm_y = self._io.read_s2be()
            self.elfin_acb_pc_data2_acb_mrm_z = self._io.read_s2be()
            self.elfin_acb_pc_data2_ipdu_mrm_x = self._io.read_s2be()
            self.elfin_acb_pc_data2_ipdu_mrm_y = self._io.read_s2be()
            self.elfin_acb_pc_data2_ipdu_mrm_z = self._io.read_s2be()
            self.elfin_acb_pc_data2_tmps_tmp1 = self._io.read_u2be()
            self.elfin_acb_pc_data2_tmps_tmp2 = self._io.read_u2be()
            self.elfin_acb_pc_data2_tmps_tmp3 = self._io.read_u2be()
            self.elfin_acb_pc_data2_tmps_tmp4 = self._io.read_u2be()
            self.elfin_acb_sense_adc_data_current = self._io.read_u2le()
            self.elfin_acb_sense_adc_data_voltage = self._io.read_u2le()
            self.elfin_fc_counters_cmds_recv = self._io.read_u1()
            self.elfin_fc_counters_badcmds_recv = self._io.read_u1()
            self.elfin_fc_counters_badpkts_fm_radio = self._io.read_u1()
            self.elfin_fc_counters_fcpkts_fm_radio = self._io.read_u1()
            self.elfin_fc_counters_errors = self._io.read_u1()
            self.elfin_fc_counters_reboots = self._io.read_u1()
            self.elfin_fc_counters_intrnl_wdttmout = self._io.read_u1()
            self.elfin_fc_counters_brwnouts = self._io.read_u1()
            self.elfin_fc_counters_wdpicrst = self._io.read_u1()
            self.elfin_fc_counters_porst = self._io.read_u1()
            self.elfin_fc_counters_uart1_recvpkts = self._io.read_u1()
            self.elfin_fc_counters_uart1_parseerrs = self._io.read_u1()
            self.elfin_fc_counters_sips_ovcur_evts = self._io.read_u1()
            self.elfin_fc_counters_vu1_on = self._io.read_u1()
            self.elfin_fc_counters_vu1_off = self._io.read_u1()
            self.elfin_fc_counters_vu2_on = self._io.read_u1()
            self.elfin_fc_counters_vu2_off = self._io.read_u1()
            self.elfin_radio_tlm_rssi = self._io.read_u1()
            self.elfin_radio_tlm_bytes_rx = self._io.read_u4be()
            self.elfin_radio_tlm_bytes_tx = self._io.read_u4be()
            self.elfin_radio_cfg_read_radio_palvl = self._io.read_u1()
            self.elfin_errors_error1_day = self._io.read_u1()
            self.elfin_errors_error1_hour = self._io.read_u1()
            self.elfin_errors_error1_minute = self._io.read_u1()
            self.elfin_errors_error1_second = self._io.read_u1()
            self.elfin_errors_error1_error = self._io.read_u1()
            self.elfin_errors_error2_day = self._io.read_u1()
            self.elfin_errors_error2_hour = self._io.read_u1()
            self.elfin_errors_error2_minute = self._io.read_u1()
            self.elfin_errors_error2_second = self._io.read_u1()
            self.elfin_errors_error2_error = self._io.read_u1()
            self.elfin_errors_error3_day = self._io.read_u1()
            self.elfin_errors_error3_hour = self._io.read_u1()
            self.elfin_errors_error3_minute = self._io.read_u1()
            self.elfin_errors_error3_second = self._io.read_u1()
            self.elfin_errors_error3_error = self._io.read_u1()
            self.elfin_errors_error4_day = self._io.read_u1()
            self.elfin_errors_error4_hour = self._io.read_u1()
            self.elfin_errors_error4_minute = self._io.read_u1()
            self.elfin_errors_error4_second = self._io.read_u1()
            self.elfin_errors_error4_error = self._io.read_u1()
            self.elfin_errors_error5_day = self._io.read_u1()
            self.elfin_errors_error5_hour = self._io.read_u1()
            self.elfin_errors_error5_minute = self._io.read_u1()
            self.elfin_errors_error5_second = self._io.read_u1()
            self.elfin_errors_error5_error = self._io.read_u1()
            self.elfin_errors_error6_day = self._io.read_u1()
            self.elfin_errors_error6_hour = self._io.read_u1()
            self.elfin_errors_error6_minute = self._io.read_u1()
            self.elfin_errors_error6_second = self._io.read_u1()
            self.elfin_errors_error6_error = self._io.read_u1()
            self.elfin_errors_error7_day = self._io.read_u1()
            self.elfin_errors_error7_hour = self._io.read_u1()
            self.elfin_errors_error7_minute = self._io.read_u1()
            self.elfin_errors_error7_second = self._io.read_u1()
            self.elfin_errors_error7_error = self._io.read_u1()
            self.elfin_fc_salt = self._io.read_bytes(4)
            self.elfin_fc_crc = self._io.read_u1()
            self.elfin_frame_end = self._io.read_u1()


    class ElfinHskpPacket(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.elfin_hskp_pwr1_rtcc_year = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_month = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_day = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_hour = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_minute = self._io.read_u1()
            self.elfin_hskp_pwr1_rtcc_second = self._io.read_u1()
            self.elfin_hskp_pwr1_pwr_board_id = self._io.read_u1()
            self.elfin_hskp_pwr1_adc_data_adc_sa_volt_12 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_adc_sa_volt_34 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_adc_sa_volt_56 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_sa_short_circuit_current = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_bat_2_volt = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_bat_1_volt = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_reg_sa_volt_1 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_reg_sa_volt_2 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_reg_sa_volt_3 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_power_bus_current_1 = self._io.read_u2be()
            self.elfin_hskp_pwr1_adc_data_power_bus_current_2 = self._io.read_u2be()
            self.elfin_hskp_pwr1_bat_mon_1_avg_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_temperature_register = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_volt_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_1_acc_curr_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_avg_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_temperature_register = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_volt_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_cur_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bat_mon_2_acc_curr_reg = self._io.read_s2be()
            self.elfin_hskp_pwr1_bv_mon = self._io.read_u2be()
            self.elfin_hskp_pwr1_tmps_tmp1 = self._io.read_s2be()
            self.elfin_hskp_pwr1_tmps_tmp2 = self._io.read_s2be()
            self.elfin_hskp_pwr1_tmps_tmp3 = self._io.read_s2be()
            self.elfin_hskp_pwr1_tmps_tmp4 = self._io.read_s2be()
            self.elfin_hskp_pwr1_accumulated_curr_bat1_rsrc = self._io.read_u1()
            self.elfin_hskp_pwr1_accumulated_curr_bat2_rsrc = self._io.read_u1()
            self.elfin_hskp_pwr1_accumulated_curr_bat1_rarc = self._io.read_u1()
            self.elfin_hskp_pwr1_accumulated_curr_bat2_rarc = self._io.read_u1()
            self.elfin_fc_status_safe_mode = self._io.read_bits_int(1) != 0
            self.elfin_fc_status_reserved = self._io.read_bits_int(3)
            self.elfin_fc_status_early_orbit = self._io.read_bits_int(4)


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



