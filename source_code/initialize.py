import os
import numpy as np
import pandas as pd

def initialize_parameters(years=[]):
    heating_demand = {}
    cooling_demand = {}
    electricity_price = {}
    electricity_mean_price = {}
    electricity_co2_share = {}
    electricity_mean_co2_share = {}
    gas_price = {}
    co2_price = {}
    data_eb = {}
    data_hp = {}
    data_st = {}
    data_wi = {}
    data_gt = {}
    data_dgt = {}
    data_ieh = {}
    data_chp = {}
    data_ac = {}
    data_ab = {}
    data_cp = {}
    data_ates = {}
    data_ttes = {}
    data_ites = {}
    
    cur_dir = os.path.dirname(__file__)
    path_to_input_folder = os.path.join(cur_dir, '..', 'inputs')
    path_to_file_demand = os.path.join(path_to_input_folder, 'demand.xlsx')
    path_to_file_electricity_price = os.path.join(path_to_input_folder, 'electricity_price.xlsx')
    path_to_file_gas_price = os.path.join(path_to_input_folder, 'gas_price.xlsx')
    path_to_file_co2_price = os.path.join(path_to_input_folder, 'co2_price.xlsx')
    path_to_file_hp_cop = os.path.join(path_to_input_folder, 'temperature_washington_dc.xlsx')
    path_to_file_solar_radiation = os.path.join(path_to_input_folder, 'solar_radiation_washington_dc.xlsx')
    path_to_file_ieh_profile = os.path.join(path_to_input_folder, 'ieh_profile.xlsx')
    path_to_file_ac_eer = os.path.join(path_to_input_folder, 'ac_eer.xlsx')
    path_to_file_eb = os.path.join(path_to_input_folder, 'eb.xlsx')
    path_to_file_hp = os.path.join(path_to_input_folder, 'hp.xlsx')
    path_to_file_st = os.path.join(path_to_input_folder, 'st.xlsx')
    path_to_file_wi = os.path.join(path_to_input_folder, 'wi.xlsx')
    path_to_file_gt = os.path.join(path_to_input_folder, 'gt.xlsx')
    path_to_file_dgt = os.path.join(path_to_input_folder, 'dgt.xlsx')
    path_to_file_ieh = os.path.join(path_to_input_folder, 'ieh.xlsx')
    path_to_file_chp = os.path.join(path_to_input_folder, 'chp.xlsx')
    path_to_file_ac = os.path.join(path_to_input_folder, 'ac.xlsx')
    path_to_file_ab = os.path.join(path_to_input_folder, 'ab.xlsx')
    path_to_file_cp = os.path.join(path_to_input_folder, 'cp.xlsx')
    path_to_file_ates = os.path.join(path_to_input_folder, 'ates.xlsx')
    path_to_file_ttes = os.path.join(path_to_input_folder, 'ttes.xlsx')
    path_to_file_ites = os.path.join(path_to_input_folder, 'ites.xlsx')
    
    for year in years:
        df_demand = pd.read_excel(path_to_file_demand, sheet_name=str(year))
        df_electricity_price = pd.read_excel(path_to_file_electricity_price, sheet_name=str(year))
        df_gas_price = pd.read_excel(path_to_file_gas_price, sheet_name=str(year))
        df_co2_price = pd.read_excel(path_to_file_co2_price, sheet_name=str(year))
        df_hp_cop = pd.read_excel(path_to_file_hp_cop, sheet_name=str(year))
        df_solar_radiation = pd.read_excel(path_to_file_solar_radiation, sheet_name=str(year))
        df_ieh_profile = pd.read_excel(path_to_file_ieh_profile, sheet_name=str(year))
        df_ac_eer = pd.read_excel(path_to_file_ac_eer, sheet_name=str(year))
        df_eb = pd.read_excel(path_to_file_eb, sheet_name=str(year))
        df_hp = pd.read_excel(path_to_file_hp, sheet_name=str(year))
        df_st = pd.read_excel(path_to_file_st, sheet_name=str(year))
        df_wi = pd.read_excel(path_to_file_wi, sheet_name=str(year))
        df_gt = pd.read_excel(path_to_file_gt, sheet_name=str(year))
        df_dgt = pd.read_excel(path_to_file_dgt, sheet_name=str(year))
        df_ieh = pd.read_excel(path_to_file_ieh, sheet_name=str(year))
        df_chp = pd.read_excel(path_to_file_chp, sheet_name=str(year))
        df_ac = pd.read_excel(path_to_file_ac, sheet_name=str(year))
        df_ab = pd.read_excel(path_to_file_ab, sheet_name=str(year))
        df_cp = pd.read_excel(path_to_file_cp, sheet_name=str(year))
        df_ates = pd.read_excel(path_to_file_ates, sheet_name=str(year))
        df_ttes = pd.read_excel(path_to_file_ttes, sheet_name=str(year))
        df_ites = pd.read_excel(path_to_file_ites, sheet_name=str(year))
        heating_demand[year] = df_demand['heating_demand_districts_building'].tolist()
        cooling_demand[year] = df_demand['cooling_demand_districts_building'].tolist()
        electricity_price[year] = df_electricity_price['electricity_price'].tolist()
        electricity_mean_price[year] = np.mean(electricity_price[year])
        electricity_co2_share[year] = df_electricity_price['electricity_co2_share'].tolist()
        electricity_mean_co2_share[year] = np.mean(electricity_co2_share[year])
        gas_price[year] = df_gas_price['gas_price'].tolist()
        co2_price[year] = df_co2_price['co2_price'].tolist()[0]
        p_eb_eta = df_eb['p_eb_eta'].tolist()[0]
        p_eb_c_inv = df_eb['p_eb_c_inv'].tolist()[0]
        data_eb[year] = {'p_eb_eta': p_eb_eta, 'p_eb_c_inv': p_eb_c_inv}
        p_hp_c_inv = df_hp['p_hp_c_inv'].tolist()[0]
        p_hp_cop = df_hp_cop['p_hp_cop'].tolist()
        data_hp[year] = {'p_hp_c_inv': p_hp_c_inv, 'p_hp_cop': p_hp_cop}
        p_st_eta = df_st['p_st_eta'].tolist()[0]
        p_st_c_inv = df_st['p_st_c_inv'].tolist()[0]
        p_st_cop = df_st['p_st_cop'].tolist()[0]
        p_st_solar_radiation = df_solar_radiation['p_st_solar_radiation'].tolist()
        data_st[year] = {'p_st_eta': p_st_eta, 'p_st_c_inv': p_st_c_inv, 'p_st_cop': p_st_cop, 'p_st_solar_radiation': p_st_solar_radiation}
        p_wi_eta = df_wi['p_wi_eta'].tolist()[0]
        p_wi_q_waste = df_wi['p_wi_q_waste'].tolist()[0]
        p_wi_c_waste = df_wi['p_wi_c_waste'].tolist()[0]
        p_wi_h_waste = df_wi['p_wi_h_waste'].tolist()[0]
        p_wi_heat = df_wi['p_wi_heat'].tolist()[0]
        p_wi_elec = df_wi['p_wi_elec'].tolist()[0]    
        p_wi_co2_share = df_wi['p_wi_co2_share'].tolist()[0]
        p_wi_c_inv = df_wi['p_wi_c_inv'].tolist()[0]
        data_wi[year] = {'p_wi_eta': p_wi_eta, 'p_wi_q_waste': p_wi_q_waste, 'p_wi_c_waste': p_wi_c_waste, 'p_wi_h_waste': p_wi_h_waste, 'p_wi_heat': p_wi_heat, 'p_wi_elec': p_wi_elec, 'p_wi_co2_share': p_wi_co2_share, 'p_wi_c_inv': p_wi_c_inv}
        p_gt_c_inv = df_gt['p_gt_c_inv'].tolist()[0]
        p_gt_cop = df_gt['p_gt_cop'].tolist()[0]
        data_gt[year] = {'p_gt_c_inv': p_gt_c_inv, 'p_gt_cop': p_gt_cop}
        p_dgt_elec = df_dgt['p_dgt_elec'].tolist()[0]
        p_dgt_c_inv = df_dgt['p_dgt_c_inv'].tolist()[0]
        data_dgt[year] = {'p_dgt_elec': p_dgt_elec, 'p_dgt_c_inv': p_dgt_c_inv}
        p_ieh_c_inv = df_ieh['p_ieh_c_inv'].tolist()[0]
        p_ieh_c_in = df_ieh['p_ieh_c_in'].tolist()[0]
        p_ieh_elec = df_ieh['p_ieh_elec'].tolist()[0]
        p_ieh_in = df_ieh_profile['p_ieh_in'].tolist()
        data_ieh[year] = {'p_ieh_c_inv': p_ieh_c_inv, 'p_ieh_c_in': p_ieh_c_in, 'p_ieh_elec': p_ieh_elec, 'p_ieh_in': p_ieh_in}
        p_chp_eta = df_chp['p_chp_eta'].tolist()[0]
        p_chp_h_gas = df_chp['p_chp_h_gas'].tolist()[0]
        p_chp_heat = df_chp['p_chp_heat'].tolist()[0]
        p_chp_elec = df_chp['p_chp_elec'].tolist()[0]
        p_chp_co2_share = df_chp['p_chp_co2_share'].tolist()[0]
        p_chp_c_inv = df_chp['p_chp_c_inv'].tolist()[0]
        data_chp[year] = {'p_chp_eta': p_chp_eta, 'p_chp_h_gas': p_chp_h_gas, 'p_chp_heat': p_chp_heat, 'p_chp_elec': p_chp_elec, 'p_chp_co2_share': p_chp_co2_share, 'p_chp_c_inv': p_chp_c_inv}
        p_ac_eer = df_ac_eer['p_ac_eer'].tolist()
        p_ac_c_inv = df_ac['p_ac_c_inv'].tolist()[0]
        data_ac[year] = {'p_ac_eer': p_ac_eer, 'p_ac_c_inv': p_ac_c_inv}
        p_ab_eer = df_ab['p_ab_eer'].tolist()[0]
        p_ab_hp_cop = df_ab['p_ab_hp_cop'].tolist()[0]
        p_ab_c_inv = df_ab['p_ab_c_inv'].tolist()[0]
        p_ct_ab_c_inv = df_ab['p_ct_ab_c_inv'].tolist()[0]
        data_ab[year] = {'p_ab_eer': p_ab_eer, 'p_ab_hp_cop': p_ab_hp_cop, 'p_ab_c_inv': p_ab_c_inv, 'p_ct_ab_c_inv': p_ct_ab_c_inv}
        p_cp_ct_seer = df_cp['p_cp_ct_seer'].tolist()[0]
        p_cp_hp_seer = df_cp['p_cp_hp_seer'].tolist()[0]
        p_cp_hp_cop = df_cp['p_cp_hp_cop'].tolist()[0]
        p_cp_c_inv = df_cp['p_cp_c_inv'].tolist()[0]
        p_ct_cp_c_inv = df_cp['p_ct_cp_c_inv'].tolist()[0]
        data_cp[year] = {'p_cp_ct_seer': p_cp_ct_seer, 'p_cp_hp_seer': p_cp_hp_seer, 'p_cp_hp_cop': p_cp_hp_cop, 'p_cp_c_inv': p_cp_c_inv, 'p_ct_cp_c_inv': p_ct_cp_c_inv}
        p_ates_losses = df_ates['p_ates_losses'].tolist()[0]
        p_ates_eta = df_ates['p_ates_eta'].tolist()[0]
        p_ates_init = df_ates['p_ates_init'].tolist()[0]
        p_ates_end = df_ates['p_ates_end'].tolist()[0]
        p_ates_c_inv = df_ates['p_ates_c_inv'].tolist()[0]
        p_ates_elec = df_ates['p_ates_elec'].tolist()[0]
        p_ates_cop = df_ates['p_ates_cop'].tolist()[0]
        p_ates_c_charge_discharge = df_ates['p_ates_c_charge_discharge'].tolist()[0]
        data_ates[year] = {'p_ates_losses': p_ates_losses, 'p_ates_eta': p_ates_eta, 'p_ates_init': p_ates_init, 'p_ates_end': p_ates_end, 'p_ates_c_inv': p_ates_c_inv, 'p_ates_elec': p_ates_elec, 'p_ates_cop': p_ates_cop, 'p_ates_c_charge_discharge': p_ates_c_charge_discharge}
        p_ttes_losses = df_ttes['p_ttes_losses'].tolist()[0]
        p_ttes_eta = df_ttes['p_ttes_eta'].tolist()[0]
        p_ttes_init = df_ttes['p_ttes_init'].tolist()[0]
        p_ttes_end = df_ttes['p_ttes_end'].tolist()[0]
        p_ttes_c_inv = df_ttes['p_ttes_c_inv'].tolist()[0]
        p_ttes_elec = df_ttes['p_ttes_elec'].tolist()[0]
        p_ttes_cop = df_ttes['p_ttes_cop'].tolist()[0]
        p_ttes_c_charge_discharge = df_ttes['p_ttes_c_charge_discharge'].tolist()[0]
        data_ttes[year] = {'p_ttes_losses': p_ttes_losses, 'p_ttes_eta': p_ttes_eta, 'p_ttes_init': p_ttes_init, 'p_ttes_end': p_ttes_end, 'p_ttes_c_inv': p_ttes_c_inv, 'p_ttes_elec': p_ttes_elec, 'p_ttes_cop': p_ttes_cop, 'p_ttes_c_charge_discharge': p_ttes_c_charge_discharge}
        p_ites_losses = df_ites['p_ites_losses'].tolist()[0]
        p_ites_eta = df_ites['p_ites_eta'].tolist()[0]
        p_ites_init = df_ites['p_ites_init'].tolist()[0]
        p_ites_end = df_ites['p_ites_end'].tolist()[0]
        p_ites_c_inv = df_ites['p_ites_c_inv'].tolist()[0]
        p_ites_elec = df_ites['p_ites_elec'].tolist()[0]
        p_ites_seer = df_ites['p_ites_seer'].tolist()[0]
        p_ites_c_charge_discharge = df_ites['p_ites_c_charge_discharge'].tolist()[0]
        data_ites[year] = {'p_ites_losses': p_ites_losses, 'p_ites_eta': p_ites_eta, 'p_ites_init': p_ites_init, 'p_ites_end': p_ites_end, 'p_ites_c_inv': p_ites_c_inv, 'p_ites_elec': p_ites_elec, 'p_ites_seer': p_ites_seer, 'p_ites_c_charge_discharge': p_ites_c_charge_discharge}

    return heating_demand, cooling_demand, electricity_price, electricity_mean_price, electricity_co2_share, electricity_mean_co2_share, gas_price, co2_price, data_eb, data_hp, data_st, data_wi, data_gt, data_dgt, data_ieh, data_chp, data_ac, data_ab, data_cp, data_ates, data_ttes, data_ites