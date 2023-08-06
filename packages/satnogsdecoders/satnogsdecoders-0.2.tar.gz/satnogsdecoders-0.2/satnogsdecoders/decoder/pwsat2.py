# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Pwsat2(KaitaiStruct):
    """:field pwsat2_dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field pwsat2_dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field pwsat2_src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field pwsat2_src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field pwsat2_ctl: ax25_frame.ax25_header.ctl
    :field pwsat2_pid: ax25_frame.payload.pid
    :field pwsat2_apid: ax25_frame.payload.ax25_info.pwsat2_hdr.pwsat2_apid
    :field pwsat2_periodic_msg_data: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_periodic_msg_data
    :field pwsat2_obc_boot_ctr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_boot_ctr
    :field pwsat2_obc_boot_idx: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_boot_idx
    :field pwsat2_obc_reboot_reason: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_reboot_reason
    :field pwsat2_obc_code_crc: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_code_crc
    :field pwsat2_obc_mission_time: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_mission_time
    :field pwsat2_obc_ext_time: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_ext_time
    :field pwsat2_obc_comm_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_comm_err
    :field pwsat2_obc_eps_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_eps_err
    :field pwsat2_obc_rtc_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_rtc_err
    :field pwsat2_obc_imtq_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_imtq_err
    :field pwsat2_obc_n25qflash1_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_n25qflash1_err
    :field pwsat2_obc_n25qflash2_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_n25qflash2_err
    :field pwsat2_obc_n25qflash3_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_n25qflash3_err
    :field pwsat2_obc_n25q_tmr_corr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_n25q_tmr_corr
    :field pwsat2_obc_fram_tmr_corr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_fram_tmr_corr
    :field pwsat2_obc_payload_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_payload_err
    :field pwsat2_obc_cam_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_cam_err
    :field pwsat2_obc_suns_exp_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_suns_exp_err
    :field pwsat2_obc_ant_prim_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_ant_prim_err
    :field pwsat2_obc_ant_sec_err: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_ant_sec_err
    :field pwsat2_obc_prim_flash_scrbg_ptr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_prim_flash_scrbg_ptr
    :field pwsat2_obc_sec_flash_scrbg_ptr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_sec_flash_scrbg_ptr
    :field pwsat2_obc_ram_scrbg_ptr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_ram_scrbg_ptr
    :field pwsat2_obc_system_uptime: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_system_uptime
    :field pwsat2_obc_system_flash_free: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_obc.pwsat2_obc_system_flash_free
    :field pwsat2_antennas_ant1_depl_sw_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_depl_sw_ch_a
    :field pwsat2_antennas_ant2_depl_sw_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_depl_sw_ch_a
    :field pwsat2_antennas_ant3_depl_sw_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_depl_sw_ch_a
    :field pwsat2_antennas_ant4_depl_sw_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_depl_sw_ch_a
    :field pwsat2_antennas_ant1_depl_sw_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_depl_sw_ch_b
    :field pwsat2_antennas_ant2_depl_sw_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_depl_sw_ch_b
    :field pwsat2_antennas_ant3_depl_sw_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_depl_sw_ch_b
    :field pwsat2_antennas_ant4_depl_sw_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_depl_sw_ch_b
    :field pwsat2_antennas_ant1_last_timed_stop_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_last_timed_stop_ch_a
    :field pwsat2_antennas_ant2_last_timed_stop_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_last_timed_stop_ch_a
    :field pwsat2_antennas_ant3_last_timed_stop_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_last_timed_stop_ch_a
    :field pwsat2_antennas_ant4_last_timed_stop_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_last_timed_stop_ch_a
    :field pwsat2_antennas_ant1_last_timed_stop_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_last_timed_stop_ch_b
    :field pwsat2_antennas_ant2_last_timed_stop_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_last_timed_stop_ch_b
    :field pwsat2_antennas_ant3_last_timed_stop_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_last_timed_stop_ch_b
    :field pwsat2_antennas_ant4_last_timed_stop_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_last_timed_stop_ch_b
    :field pwsat2_antennas_ant1_burn_active_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_burn_active_ch_a
    :field pwsat2_antennas_ant2_burn_active_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_burn_active_ch_a
    :field pwsat2_antennas_ant3_burn_active_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_burn_active_ch_a
    :field pwsat2_antennas_ant4_burn_active_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_burn_active_ch_a
    :field pwsat2_antennas_ant1_burn_active_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_burn_active_ch_b
    :field pwsat2_antennas_ant2_burn_active_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_burn_active_ch_b
    :field pwsat2_antennas_ant3_burn_active_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_burn_active_ch_b
    :field pwsat2_antennas_ant4_burn_active_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_burn_active_ch_b
    :field pwsat2_antennas_sys_indep_burn_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_sys_indep_burn_ch_a
    :field pwsat2_antennas_sys_indep_burn_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_sys_indep_burn_ch_b
    :field pwsat2_antennas_ant_ignoring_sw_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant_ignoring_sw_ch_a
    :field pwsat2_antennas_ant_ignoring_sw_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant_ignoring_sw_ch_b
    :field pwsat2_antennas_armed_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_armed_ch_a
    :field pwsat2_antennas_armed_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_armed_ch_b
    :field pwsat2_antennas_ant1_activation_cnt_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_activation_cnt_ch_a
    :field pwsat2_antennas_ant2_activation_cnt_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_activation_cnt_ch_a
    :field pwsat2_antennas_ant3_activation_cnt_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_activation_cnt_ch_a
    :field pwsat2_antennas_ant4_activation_cnt_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_activation_cnt_ch_a
    :field pwsat2_antennas_ant1_activation_cnt_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_activation_cnt_ch_b
    :field pwsat2_antennas_ant2_activation_cnt_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_activation_cnt_ch_b
    :field pwsat2_antennas_ant3_activation_cnt_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_activation_cnt_ch_b
    :field pwsat2_antennas_ant4_activation_cnt_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_activation_cnt_ch_b
    :field pwsat2_antennas_ant1_activation_time_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_activation_time_ch_a
    :field pwsat2_antennas_ant2_activation_time_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_activation_time_ch_a
    :field pwsat2_antennas_ant3_activation_time_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_activation_time_ch_a
    :field pwsat2_antennas_ant4_activation_time_ch_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_activation_time_ch_a
    :field pwsat2_antennas_ant1_activation_time_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant1_activation_time_ch_b
    :field pwsat2_antennas_ant2_activation_time_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant2_activation_time_ch_b
    :field pwsat2_antennas_ant3_activation_time_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant3_activation_time_ch_b
    :field pwsat2_antennas_ant4_activation_time_ch_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_antennas.pwsat2_antennas_ant4_activation_time_ch_b
    :field pwsat2_experiments_curr_exp_code: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_experiments.pwsat2_experiments_curr_exp_code
    :field pwsat2_experiments_exp_startup_res: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_experiments.pwsat2_experiments_exp_startup_res
    :field pwsat2_experiments_last_exp_iter_stat_status: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_experiments.pwsat2_experiments_last_exp_iter_stat_status
    :field pwsat2_gyroscope_x_meas: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_gyroscope.pwsat2_gyroscope_x_meas
    :field pwsat2_gyroscope_y_meas: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_gyroscope.pwsat2_gyroscope_y_meas
    :field pwsat2_gyroscope_z_meas: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_gyroscope.pwsat2_gyroscope_z_meas
    :field pwsat2_gyroscope_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_gyroscope.pwsat2_gyroscope_temp
    :field pwsat2_comm_tx_trsmtr_uptime: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_trsmtr_uptime
    :field pwsat2_comm_tx_bitrate: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_bitrate
    :field pwsat2_comm_tx_last_tx_rf_refl_pwr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_last_tx_rf_refl_pwr
    :field pwsat2_comm_tx_last_tx_pamp_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_last_tx_pamp_temp
    :field pwsat2_comm_tx_last_tx_last_tx_rf_fwd_pwr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_last_tx_last_tx_rf_fwd_pwr
    :field pwsat2_comm_tx_last_tx_curr_consmpt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_last_tx_curr_consmpt
    :field pwsat2_comm_tx_now_tx_fwd_pwr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_now_tx_fwd_pwr
    :field pwsat2_comm_tx_now_tx_curr_consmpt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_now_tx_curr_consmpt
    :field pwsat2_comm_tx_state_when_idle: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_state_when_idle
    :field pwsat2_comm_tx_beacon_state: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_tx_beacon_state
    :field pwsat2_comm_rx_uptime: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_uptime
    :field pwsat2_comm_rx_last_rx_doppler_offs: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_last_rx_doppler_offs
    :field pwsat2_comm_rx_last_rx_rssi: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_last_rx_rssi
    :field pwsat2_comm_rx_now_doppler_offs: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_now_doppler_offs
    :field pwsat2_comm_rx_now_rx_curr_consmpt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_now_rx_curr_consmpt
    :field pwsat2_comm_rx_supply_voltage: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_supply_voltage
    :field pwsat2_comm_rx_osc_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_osc_temp
    :field pwsat2_comm_rx_now_pamp_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_now_pamp_temp
    :field pwsat2_comm_rx_now_rssi: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_comm.pwsat2_comm_rx_now_rssi
    :field pwsat2_hardware_state_gpio_sail_deployed: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_hardware_state.pwsat2_hardware_state_gpio_sail_deployed
    :field pwsat2_hardware_state_mcu_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_hardware_state.pwsat2_hardware_state_mcu_temp
    :field pwsat2_eps_controller_a_mpptx_sol_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mpptx_sol_volt
    :field pwsat2_eps_controller_a_mpptx_sol_curr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mpptx_sol_curr
    :field pwsat2_eps_controller_a_mpptx_out_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mpptx_out_volt
    :field pwsat2_eps_controller_a_mpptx_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mpptx_temp
    :field pwsat2_eps_controller_a_mpptx_state: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mpptx_state
    :field pwsat2_eps_controller_a_mppty_pos_sol_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_pos_sol_volt
    :field pwsat2_eps_controller_a_mppty_pos_sol_curr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_pos_sol_curr
    :field pwsat2_eps_controller_a_mppty_pos_out_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_pos_out_volt
    :field pwsat2_eps_controller_a_mppty_pos_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_pos_temp
    :field pwsat2_eps_controller_a_mppty_pos_state: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_pos_state
    :field pwsat2_eps_controller_a_mppty_neg_sol_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_neg_sol_volt
    :field pwsat2_eps_controller_a_mppty_neg_sol_curr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_neg_sol_curr
    :field pwsat2_eps_controller_a_mppty_neg_out_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_neg_out_volt
    :field pwsat2_eps_controller_a_mppty_neg_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_neg_temp
    :field pwsat2_eps_controller_a_mppty_neg_state: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_mppty_neg_state
    :field pwsat2_eps_controller_a_distr_volt_3v3: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_volt_3v3
    :field pwsat2_eps_controller_a_distr_curr_3v3: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_curr_3v3
    :field pwsat2_eps_controller_a_distr_volt_5v: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_volt_5v
    :field pwsat2_eps_controller_a_distr_curr_5v: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_curr_5v
    :field pwsat2_eps_controller_a_distr_volt_vbat: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_volt_vbat
    :field pwsat2_eps_controller_a_distr_curr_vbat: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_curr_vbat
    :field pwsat2_eps_controller_a_distr_lcl_state: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_lcl_state
    :field pwsat2_eps_controller_a_distr_lcl_flagb: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_distr_lcl_flagb
    :field pwsat2_eps_controller_a_batc_volta: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_batc_volta
    :field pwsat2_eps_controller_a_batc_chrg_curr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_batc_chrg_curr
    :field pwsat2_eps_controller_a_batc_dchrg_curr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_batc_dchrg_curr
    :field pwsat2_eps_controller_a_batc_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_batc_temp
    :field pwsat2_eps_controller_a_batc_state: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_batc_state
    :field pwsat2_eps_controller_a_bp_temp_a: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_bp_temp_a
    :field pwsat2_eps_controller_a_bp_temp_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_bp_temp_b
    :field pwsat2_eps_controller_a_safety_ctr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_safety_ctr
    :field pwsat2_eps_controller_a_pwr_cycles: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_pwr_cycles
    :field pwsat2_eps_controller_a_uptime: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_uptime
    :field pwsat2_eps_controller_a_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_temp
    :field pwsat2_eps_controller_a_supp_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_supp_temp
    :field pwsat2_eps_controller_b_3v3d_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_b_3v3d_volt
    :field pwsat2_eps_controller_a_dcdc_3v3_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_dcdc_3v3_temp
    :field pwsat2_eps_controller_a_dcdc_5v_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_a.pwsat2_eps_controller_a_dcdc_5v_temp
    :field pwsat2_eps_controller_b_bptemp_c: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_b_bptemp_c
    :field pwsat2_eps_controller_b_battc_volt_b: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_b_battc_volt_b
    :field pwsat2_eps_controller_b_safety_ctr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_b_safety_ctr
    :field pwsat2_eps_controller_b_pwr_cycles: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_b_pwr_cycles
    :field pwsat2_eps_controller_b_uptime: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_b_uptime
    :field pwsat2_eps_controller_b_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_b_temp
    :field pwsat2_eps_controller_b_supp_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_b_supp_temp
    :field pwsat2_eps_controller_a_3v3d_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_eps_controller_b.pwsat2_eps_controller_a_3v3d_volt
    :field pwsat2_imtq_mag_meas_1: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq.pwsat2_imtq_mag_meas_1
    :field pwsat2_imtq_mag_meas_2: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq.pwsat2_imtq_mag_meas_2
    :field pwsat2_imtq_mag_meas_3: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq.pwsat2_imtq_mag_meas_3
    :field pwsat2_imtq_coil_active_in_meas: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_coil_active.pwsat2_imtq_coil_active_in_meas
    :field pwsat2_imtq_dipole_1: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_dipole.pwsat2_imtq_dipole_1
    :field pwsat2_imtq_dipole_2: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_dipole.pwsat2_imtq_dipole_2
    :field pwsat2_imtq_dipole_3: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_dipole.pwsat2_imtq_dipole_3
    :field pwsat2_imtq_bdot_x: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_bdot.pwsat2_imtq_bdot_x
    :field pwsat2_imtq_bdot_y: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_bdot.pwsat2_imtq_bdot_y
    :field pwsat2_imtq_bdot_z: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_bdot.pwsat2_imtq_bdot_z
    :field pwsat2_imtq_hskp_dig_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_hskp.pwsat2_imtq_hskp_dig_volt
    :field pwsat2_imtq_hskp_ana_volt: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_hskp.pwsat2_imtq_hskp_ana_volt
    :field pwsat2_imtq_hskp_dig_curr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_hskp.pwsat2_imtq_hskp_dig_curr
    :field pwsat2_imtq_hskp_ana_curr: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_hskp.pwsat2_imtq_hskp_ana_curr
    :field pwsat2_imtq_hskp_mcu_temp: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_hskp.pwsat2_imtq_hskp_mcu_temp
    :field pwsat2_imtq_coil_current_x: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_coil.pwsat2_imtq_coil_current_x
    :field pwsat2_imtq_coil_current_y: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_coil.pwsat2_imtq_coil_current_y
    :field pwsat2_imtq_coil_current_z: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_coil.pwsat2_imtq_coil_current_z
    :field pwsat2_imtq_temp_coil_x: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_temp.pwsat2_imtq_temp_coil_x
    :field pwsat2_imtq_temp_coil_y: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_temp.pwsat2_imtq_temp_coil_y
    :field pwsat2_imtq_temp_coil_z: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_temp.pwsat2_imtq_temp_coil_z
    :field pwsat2_imtq_state_status: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_state.pwsat2_imtq_state_status
    :field pwsat2_imtq_state_mode: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_state.pwsat2_imtq_state_mode
    :field pwsat2_imtq_err_prev_iter: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_state.pwsat2_imtq_err_prev_iter
    :field pwsat2_imtq_conf_changed: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_state.pwsat2_imtq_conf_changed
    :field pwsat2_imtq_state_uptime: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_state.pwsat2_imtq_state_uptime
    :field pwsat2_adcs_imtq_slftst_err_initial: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_initial
    :field pwsat2_adcs_imtq_slftst_err_pos_x: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_pos_x
    :field pwsat2_adcs_imtq_slftst_err_neg_x: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_neg_x
    :field pwsat2_adcs_imtq_slftst_err_pos_y: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_pos_y
    :field pwsat2_adcs_imtq_slftst_err_neg_y: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_neg_y
    :field pwsat2_adcs_imtq_slftst_err_pos_z: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_pos_z
    :field pwsat2_adcs_imtq_slftst_err_neg_z: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_neg_z
    :field pwsat2_adcs_imtq_slftst_err_final: ax25_frame.payload.ax25_info.pwsat2_payload.pwsat2_imtq_selftest.pwsat2_adcs_imtq_slftst_err_final
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


    class Pwsat2Telemetry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_obc = self._root.Pwsat2Obc(self._io, self, self._root)
            self.pwsat2_antennas = self._root.Pwsat2Antennas(self._io, self, self._root)
            self.pwsat2_experiments = self._root.Pwsat2Experiments(self._io, self, self._root)
            self.pwsat2_gyroscope = self._root.Pwsat2Gyroscope(self._io, self, self._root)
            self.pwsat2_comm = self._root.Pwsat2Comm(self._io, self, self._root)
            self.pwsat2_hardware_state = self._root.Pwsat2HardwareState(self._io, self, self._root)
            self.pwsat2_eps_controller_a = self._root.Pwsat2EpsControllerA(self._io, self, self._root)
            self.pwsat2_eps_controller_b = self._root.Pwsat2EpsControllerB(self._io, self, self._root)
            self.pwsat2_imtq = self._root.Pwsat2Imtq(self._io, self, self._root)
            self.pwsat2_imtq_coil_active = self._root.Pwsat2ImtqCoilActive(self._io, self, self._root)
            self.pwsat2_imtq_dipole = self._root.Pwsat2ImtqDipole(self._io, self, self._root)
            self.pwsat2_imtq_bdot = self._root.Pwsat2ImtqBdot(self._io, self, self._root)
            self.pwsat2_imtq_hskp = self._root.Pwsat2ImtqHskp(self._io, self, self._root)
            self.pwsat2_imtq_coil = self._root.Pwsat2ImtqCoil(self._io, self, self._root)
            self.pwsat2_imtq_temp = self._root.Pwsat2ImtqTemp(self._io, self, self._root)
            self.pwsat2_imtq_state = self._root.Pwsat2ImtqState(self._io, self, self._root)
            self.pwsat2_imtq_selftest = self._root.Pwsat2ImtqSelftest(self._io, self, self._root)


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


    class Pwsat2ImtqCoilActive(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_coil_active_in_meas = self._io.read_bits_int(1) != 0


    class Pwsat2Antennas(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_antennas_ant1_depl_sw_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant2_depl_sw_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant3_depl_sw_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant4_depl_sw_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant1_depl_sw_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant2_depl_sw_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant3_depl_sw_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant4_depl_sw_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant1_last_timed_stop_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant2_last_timed_stop_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant3_last_timed_stop_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant4_last_timed_stop_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant1_last_timed_stop_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant2_last_timed_stop_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant3_last_timed_stop_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant4_last_timed_stop_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant1_burn_active_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant2_burn_active_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant3_burn_active_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant4_burn_active_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant1_burn_active_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant2_burn_active_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant3_burn_active_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant4_burn_active_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_sys_indep_burn_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_sys_indep_burn_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant_ignoring_sw_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant_ignoring_sw_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_armed_ch_a = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_armed_ch_b = self._io.read_bits_int(1) != 0
            self.pwsat2_antennas_ant1_activation_cnt_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant2_activation_cnt_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant3_activation_cnt_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant4_activation_cnt_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant1_activation_cnt_ch_b = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant2_activation_cnt_ch_b = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant3_activation_cnt_ch_b = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant4_activation_cnt_ch_b = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant1_activation_time_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant2_activation_time_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant3_activation_time_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant4_activation_time_ch_a = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant1_activation_time_ch_b = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant2_activation_time_ch_b = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant3_activation_time_ch_b = self._io.read_bits_int(3)
            self.pwsat2_antennas_ant4_activation_time_ch_b = self._io.read_bits_int(3)


    class Pwsat2ImtqTemp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_temp_coil_x = self._io.read_u2le()
            self.pwsat2_imtq_temp_coil_y = self._io.read_u2le()
            self.pwsat2_imtq_temp_coil_z = self._io.read_u2le()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            _on = self.pid
            if _on == 240:
                self._raw_ax25_info = self._io.read_bytes_full()
                io = KaitaiStream(BytesIO(self._raw_ax25_info))
                self.ax25_info = self._root.Pwsat2Frame(io, self, self._root)
            else:
                self.ax25_info = self._io.read_bytes_full()


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class Pwsat2PeriodicMsg(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_periodic_msg_data = (self._io.read_bytes((self._io.size() - 1))).decode(u"ASCII")


    class Pwsat2HardwareState(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_hardware_state_gpio_sail_deployed = self._io.read_bits_int(1) != 0
            self.pwsat2_hardware_state_mcu_temp = self._io.read_bits_int(12)


    class Pwsat2EpsControllerA(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_eps_controller_a_mpptx_sol_volt = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mpptx_sol_curr = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mpptx_out_volt = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mpptx_temp = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mpptx_state = self._io.read_bits_int(3)
            self.pwsat2_eps_controller_a_mppty_pos_sol_volt = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_pos_sol_curr = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_pos_out_volt = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_pos_temp = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_pos_state = self._io.read_bits_int(3)
            self.pwsat2_eps_controller_a_mppty_neg_sol_volt = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_neg_sol_curr = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_neg_out_volt = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_neg_temp = self._io.read_bits_int(12)
            self.pwsat2_eps_controller_a_mppty_neg_state = self._io.read_bits_int(3)
            self.pwsat2_eps_controller_a_distr_volt_3v3 = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_distr_curr_3v3 = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_distr_volt_5v = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_distr_curr_5v = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_distr_volt_vbat = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_distr_curr_vbat = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_distr_lcl_state = self._io.read_bits_int(7)
            self.pwsat2_eps_controller_a_distr_lcl_flagb = self._io.read_bits_int(6)
            self.pwsat2_eps_controller_a_batc_volta = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_batc_chrg_curr = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_batc_dchrg_curr = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_batc_temp = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_batc_state = self._io.read_bits_int(3)
            self.pwsat2_eps_controller_a_bp_temp_a = self._io.read_bits_int(13)
            self.pwsat2_eps_controller_a_bp_temp_b = self._io.read_bits_int(13)
            self._io.align_to_byte()
            self.pwsat2_eps_controller_a_safety_ctr = self._io.read_u1()
            self.pwsat2_eps_controller_a_pwr_cycles = self._io.read_u2le()
            self.pwsat2_eps_controller_a_uptime = self._io.read_u4le()
            self.pwsat2_eps_controller_a_temp = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_supp_temp = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_b_3v3d_volt = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_dcdc_3v3_temp = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_dcdc_5v_temp = self._io.read_bits_int(10)


    class Pwsat2ImtqBdot(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_bdot_x = self._io.read_u4le()
            self.pwsat2_imtq_bdot_y = self._io.read_u4le()
            self.pwsat2_imtq_bdot_z = self._io.read_u4le()


    class Pwsat2Experiments(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_experiments_curr_exp_code = self._io.read_bits_int(4)
            self._io.align_to_byte()
            self.pwsat2_experiments_exp_startup_res = self._io.read_u1()
            self.pwsat2_experiments_last_exp_iter_stat_status = self._io.read_u1()


    class Pwsat2Obc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_obc_boot_ctr = self._io.read_u4le()
            self.pwsat2_obc_boot_idx = self._io.read_u1()
            self.pwsat2_obc_reboot_reason = self._io.read_u2le()
            self.pwsat2_obc_code_crc = self._io.read_u2le()
            self.pwsat2_obc_mission_time = self._io.read_u8le()
            self.pwsat2_obc_ext_time = self._io.read_u4le()
            self.pwsat2_obc_comm_err = self._io.read_u1()
            self.pwsat2_obc_eps_err = self._io.read_u1()
            self.pwsat2_obc_rtc_err = self._io.read_u1()
            self.pwsat2_obc_imtq_err = self._io.read_u1()
            self.pwsat2_obc_n25qflash1_err = self._io.read_u1()
            self.pwsat2_obc_n25qflash2_err = self._io.read_u1()
            self.pwsat2_obc_n25qflash3_err = self._io.read_u1()
            self.pwsat2_obc_n25q_tmr_corr = self._io.read_u1()
            self.pwsat2_obc_fram_tmr_corr = self._io.read_u1()
            self.pwsat2_obc_payload_err = self._io.read_u1()
            self.pwsat2_obc_cam_err = self._io.read_u1()
            self.pwsat2_obc_suns_exp_err = self._io.read_u1()
            self.pwsat2_obc_ant_prim_err = self._io.read_u1()
            self.pwsat2_obc_ant_sec_err = self._io.read_u1()
            self.pwsat2_obc_prim_flash_scrbg_ptr = self._io.read_bits_int(3)
            self.pwsat2_obc_sec_flash_scrbg_ptr = self._io.read_bits_int(3)
            self._io.align_to_byte()
            self.pwsat2_obc_ram_scrbg_ptr = self._io.read_u4le()
            self.pwsat2_obc_system_uptime = self._io.read_bits_int(22)
            self._io.align_to_byte()
            self.pwsat2_obc_system_flash_free = self._io.read_u4le()


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.ax25_info = self._io.read_bytes_full()


    class Pwsat2Comm(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_comm_tx_trsmtr_uptime = self._io.read_bits_int(17)
            self.pwsat2_comm_tx_bitrate = self._io.read_bits_int(2)
            self.pwsat2_comm_tx_last_tx_rf_refl_pwr = self._io.read_bits_int(12)
            self.pwsat2_comm_tx_last_tx_pamp_temp = self._io.read_bits_int(12)
            self.pwsat2_comm_tx_last_tx_last_tx_rf_fwd_pwr = self._io.read_bits_int(12)
            self.pwsat2_comm_tx_last_tx_curr_consmpt = self._io.read_bits_int(12)
            self.pwsat2_comm_tx_now_tx_fwd_pwr = self._io.read_bits_int(12)
            self.pwsat2_comm_tx_now_tx_curr_consmpt = self._io.read_bits_int(12)
            self.pwsat2_comm_tx_state_when_idle = self._io.read_bits_int(1) != 0
            self.pwsat2_comm_tx_beacon_state = self._io.read_bits_int(1) != 0
            self.pwsat2_comm_rx_uptime = self._io.read_bits_int(17)
            self.pwsat2_comm_rx_last_rx_doppler_offs = self._io.read_bits_int(12)
            self.pwsat2_comm_rx_last_rx_rssi = self._io.read_bits_int(12)
            self.pwsat2_comm_rx_now_doppler_offs = self._io.read_bits_int(12)
            self.pwsat2_comm_rx_now_rx_curr_consmpt = self._io.read_bits_int(12)
            self.pwsat2_comm_rx_supply_voltage = self._io.read_bits_int(12)
            self.pwsat2_comm_rx_osc_temp = self._io.read_bits_int(12)
            self.pwsat2_comm_rx_now_pamp_temp = self._io.read_bits_int(12)
            self.pwsat2_comm_rx_now_rssi = self._io.read_bits_int(12)


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


    class Pwsat2ImtqDipole(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_dipole_1 = self._io.read_u2le()
            self.pwsat2_imtq_dipole_2 = self._io.read_u2le()
            self.pwsat2_imtq_dipole_3 = self._io.read_u2le()


    class Pwsat2Hdr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_apid = self._io.read_u1()


    class Pwsat2Gyroscope(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_gyroscope_x_meas = self._io.read_u2le()
            self.pwsat2_gyroscope_y_meas = self._io.read_u2le()
            self.pwsat2_gyroscope_z_meas = self._io.read_u2le()
            self.pwsat2_gyroscope_temp = self._io.read_u2le()


    class Pwsat2Imtq(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_mag_meas_1 = self._io.read_u4le()
            self.pwsat2_imtq_mag_meas_2 = self._io.read_u4le()
            self.pwsat2_imtq_mag_meas_3 = self._io.read_u4le()


    class Pwsat2ImtqCoil(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_coil_current_x = self._io.read_u2le()
            self.pwsat2_imtq_coil_current_y = self._io.read_u2le()
            self.pwsat2_imtq_coil_current_z = self._io.read_u2le()


    class Pwsat2ImtqHskp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_hskp_dig_volt = self._io.read_u2le()
            self.pwsat2_imtq_hskp_ana_volt = self._io.read_u2le()
            self.pwsat2_imtq_hskp_dig_curr = self._io.read_u2le()
            self.pwsat2_imtq_hskp_ana_curr = self._io.read_u2le()
            self.pwsat2_imtq_hskp_mcu_temp = self._io.read_u2le()


    class Pwsat2ImtqSelftest(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_adcs_imtq_slftst_err_initial = self._io.read_u1()
            self.pwsat2_adcs_imtq_slftst_err_pos_x = self._io.read_u1()
            self.pwsat2_adcs_imtq_slftst_err_neg_x = self._io.read_u1()
            self.pwsat2_adcs_imtq_slftst_err_pos_y = self._io.read_u1()
            self.pwsat2_adcs_imtq_slftst_err_neg_y = self._io.read_u1()
            self.pwsat2_adcs_imtq_slftst_err_pos_z = self._io.read_u1()
            self.pwsat2_adcs_imtq_slftst_err_neg_z = self._io.read_u1()
            self.pwsat2_adcs_imtq_slftst_err_final = self._io.read_u1()


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


    class Pwsat2EpsControllerB(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_eps_controller_b_bptemp_c = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_b_battc_volt_b = self._io.read_bits_int(10)
            self._io.align_to_byte()
            self.pwsat2_eps_controller_b_safety_ctr = self._io.read_u1()
            self.pwsat2_eps_controller_b_pwr_cycles = self._io.read_u2le()
            self.pwsat2_eps_controller_b_uptime = self._io.read_u4le()
            self.pwsat2_eps_controller_b_temp = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_b_supp_temp = self._io.read_bits_int(10)
            self.pwsat2_eps_controller_a_3v3d_volt = self._io.read_bits_int(10)


    class Pwsat2Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_hdr = self._root.Pwsat2Hdr(self._io, self, self._root)
            _on = (self.pwsat2_hdr.pwsat2_apid & 63)
            if _on == 5:
                self.pwsat2_payload = self._root.Pwsat2PeriodicMsg(self._io, self, self._root)
            elif _on == 13:
                self.pwsat2_payload = self._root.Pwsat2Telemetry(self._io, self, self._root)


    class Pwsat2ImtqState(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pwsat2_imtq_state_status = self._io.read_u1()
            self.pwsat2_imtq_state_mode = self._io.read_bits_int(2)
            self._io.align_to_byte()
            self.pwsat2_imtq_err_prev_iter = self._io.read_u1()
            self.pwsat2_imtq_conf_changed = self._io.read_bits_int(1) != 0
            self._io.align_to_byte()
            self.pwsat2_imtq_state_uptime = self._io.read_u4le()



