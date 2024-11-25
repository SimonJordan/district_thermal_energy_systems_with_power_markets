import os
import pandas as pd
import pyomo.environ as py

def export_result(m=None, data={}, scenarios=[], years=[], hours=[]):
    cur_dir = os.path.dirname(__file__)
    path_to_result_folder = os.path.join(cur_dir, '..', 'results')
    path_to_file_scenarios = os.path.join(path_to_result_folder, 'scenarios.txt')
    
    with open(path_to_file_scenarios, 'w') as file:
        for scenario in scenarios:
            file.write(scenario + '\n')
    
    for scenario in scenarios:
        path_to_heat_supply = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_heat_supply.xlsx')
        path_to_cool_supply = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_cool_supply.xlsx')
        path_to_inv_capacity = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_capacity.xlsx')
        path_to_inv_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_cost.xlsx')
        path_to_fix_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_fix_cost.xlsx')
        path_to_var_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_var_cost.xlsx')
        path_to_elec_consumption = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_consumption.xlsx')
        path_to_elec_gas_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_price_gas_price.xlsx')
        path_to_co2_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_co2_price.xlsx')
        path_to_storage_soc = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_storage_soc.xlsx')
        
        df_0 = []
        df_1 = []
        df_2 = []
        df_3 = []
        df_4 = []
        df_5 = []
        df_6 = []
        df_7 = []
        df_8 = []
        df_9 = []
        
        for year in years:
            eb_heat_in = []
            hp_heat_in = []
            st_heat_in = []
            wi_heat_in = []
            ieh_heat_in = []
            chp_heat_in = []
            ab_ct_heat_out = []
            ab_hp_heat_in = []
            ab_hp_heat_out = []
            cp_hp_heat_in = []
            ttes_heat_in = []
            ttes_heat_out = []
            
            ac_cool_in = []
            ab_ct_cool_in = []
            ab_hp_cool_in = []
            cp_ct_cool_in = []
            cp_hp_cool_in = []
            ites_cool_in = []
            ites_cool_out = []
            
            eb_inv = []
            hp_inv = []
            st_inv = []
            wi_inv = []
            ieh_inv = []
            chp_inv = []
            ac_inv = []
            ab_ct_inv = []
            ab_hp_inv = []
            cp_ct_inv = []
            cp_hp_inv = []
            ttes_inv = []
            ites_inv = []
            
            eb_c_inv = []
            hp_c_inv = []
            st_c_inv = []
            wi_c_inv = []
            ieh_c_inv = []
            chp_c_inv = []
            ac_c_inv = []
            ab_ct_c_inv = []
            ab_hp_c_inv = []
            cp_ct_c_inv = []
            cp_hp_c_inv = []
            ttes_c_inv = []
            ites_c_inv = []
            
            eb_c_fix = []
            hp_c_fix = []
            st_c_fix = []
            wi_c_fix = []
            ieh_c_fix = []
            chp_c_fix = []
            ac_c_fix = []
            ab_ct_c_fix = []
            ab_hp_c_fix = []
            cp_ct_c_fix = []
            cp_hp_c_fix = []
            ttes_c_fix = []
            ites_c_fix = []
            
            eb_c_var = []
            hp_c_var = []
            st_c_var = []
            wi_c_var = []
            ieh_c_var = []
            chp_c_var = []
            ac_c_var = []
            ab_ct_c_var = []
            ab_hp_c_var = []
            cp_ct_c_var = []
            cp_hp_c_var = []
            ttes_c_var = []
            ites_c_var = []
            
            eb_elec = []
            hp_elec = []
            st_elec = []
            ieh_elec = []
            ac_elec = []
            ab_ct_elec = []
            ab_hp_elec = []
            cp_ct_elec = []
            cp_hp_elec = []
            ttes_elec = []
            ites_elec = []
            
            ttes_soc = []
            ites_soc = []
    
            eb_inv.append(py.value(m.v_eb_Q_inv[scenario, year]))
            hp_inv.append(py.value(m.v_hp_Q_inv[scenario, year]))
            st_inv.append(py.value(m.v_st_P_inv[scenario, year]))
            wi_inv.append(py.value(m.v_wi_Q_inv[scenario, year]))
            ieh_inv.append(py.value(m.v_ieh_Q_inv[scenario, year]))
            chp_inv.append(py.value(m.v_chp_Q_inv[scenario, year]))
            ac_inv.append(py.value(m.v_ac_Q_inv[scenario, year]))
            ab_ct_inv.append(py.value(m.v_ab_ct_Q_inv[scenario, year]))
            ab_hp_inv.append(py.value(m.v_ab_hp_Q_inv[scenario, year]))
            cp_ct_inv.append(py.value(m.v_cp_ct_Q_inv[scenario, year]))
            cp_hp_inv.append(py.value(m.v_cp_hp_Q_inv[scenario, year]))
            ttes_inv.append(py.value(m.v_ttes_k_inv[scenario, year]))
            ites_inv.append(py.value(m.v_ites_k_inv[scenario, year]))
            
            eb_c_inv.append(py.value(m.v_eb_c_inv[scenario, year]))
            hp_c_inv.append(py.value(m.v_hp_c_inv[scenario, year]))
            st_c_inv.append(py.value(m.v_st_c_inv[scenario, year]))
            wi_c_inv.append(py.value(m.v_wi_c_inv[scenario, year]))
            ieh_c_inv.append(py.value(m.v_ieh_c_inv[scenario, year]))
            chp_c_inv.append(py.value(m.v_chp_c_inv[scenario, year]))
            ac_c_inv.append(py.value(m.v_ac_c_inv[scenario, year]))
            ab_ct_c_inv.append(py.value(m.v_ab_ct_c_inv[scenario, year]))
            ab_hp_c_inv.append(py.value(m.v_ab_hp_c_inv[scenario, year]))
            cp_ct_c_inv.append(py.value(m.v_cp_ct_c_inv[scenario, year]))
            cp_hp_c_inv.append(py.value(m.v_cp_hp_c_inv[scenario, year]))
            ttes_c_inv.append(py.value(m.v_ttes_c_inv[scenario, year]))
            ites_c_inv.append(py.value(m.v_ites_c_inv[scenario, year]))
            
            eb_c_fix.append(py.value(m.v_eb_c_fix[scenario, year]))
            hp_c_fix.append(py.value(m.v_hp_c_fix[scenario, year]))
            st_c_fix.append(py.value(m.v_st_c_fix[scenario, year]))
            wi_c_fix.append(py.value(m.v_wi_c_fix[scenario, year]))
            ieh_c_fix.append(py.value(m.v_ieh_c_fix[scenario, year]))
            chp_c_fix.append(py.value(m.v_chp_c_fix[scenario, year]))
            ac_c_fix.append(py.value(m.v_ac_c_fix[scenario, year]))
            ab_ct_c_fix.append(py.value(m.v_ab_ct_c_fix[scenario, year]))
            ab_hp_c_fix.append(py.value(m.v_ab_hp_c_fix[scenario, year]))
            cp_ct_c_fix.append(py.value(m.v_cp_ct_c_fix[scenario, year]))
            cp_hp_c_fix.append(py.value(m.v_cp_hp_c_fix[scenario, year]))
            ttes_c_fix.append(py.value(m.v_ttes_c_fix[scenario, year]))
            ites_c_fix.append(py.value(m.v_ites_c_fix[scenario, year]))
            
            for hour in hours:
                eb_heat_in.append(py.value(m.v_eb_q_heat_in[scenario, year, hour]))
                hp_heat_in.append(py.value(m.v_hp_q_heat_in[scenario, year, hour]))
                st_heat_in.append(py.value(m.v_st_q_heat_in[scenario, year, hour]))
                wi_heat_in.append(py.value(m.v_wi_q_heat_in[scenario, year, hour]))
                ieh_heat_in.append(py.value(m.v_ieh_q_heat_in[scenario, year, hour]))
                chp_heat_in.append(py.value(m.v_chp_q_heat_in[scenario, year, hour]))
                ab_ct_heat_out.append(py.value(m.v_ab_ct_q_heat_out[scenario, year, hour]))
                ab_hp_heat_in.append(py.value(m.v_ab_hp_q_heat_in[scenario, year, hour]))
                ab_hp_heat_out.append(py.value(m.v_ab_hp_q_heat_out[scenario, year, hour]))
                cp_hp_heat_in.append(py.value(m.v_cp_hp_q_heat_in[scenario, year, hour]))
                ttes_heat_in.append(py.value(m.v_ttes_q_heat_in[scenario, year, hour]))
                ttes_heat_out.append(-py.value(m.v_ttes_q_heat_out[scenario, year, hour]))

                ac_cool_in.append(py.value(m.v_ac_q_cool_in[scenario, year, hour]))
                ab_ct_cool_in.append(py.value(m.v_ab_ct_q_cool_in[scenario, year, hour]))
                ab_hp_cool_in.append(py.value(m.v_ab_hp_q_cool_in[scenario, year, hour]))
                cp_ct_cool_in.append(py.value(m.v_cp_ct_q_cool_in[scenario, year, hour]))
                cp_hp_cool_in.append(py.value(m.v_cp_hp_q_cool_in[scenario, year, hour]))
                ites_cool_in.append(py.value(m.v_ites_q_cool_in[scenario, year, hour]))
                ites_cool_out.append(-py.value(m.v_ites_q_cool_out[scenario, year, hour]))
                
                eb_c_var.append(py.value(m.v_eb_c_var[scenario, year, hour]))
                hp_c_var.append(py.value(m.v_hp_c_var[scenario, year, hour]))
                st_c_var.append(py.value(m.v_st_c_var[scenario, year, hour]))
                wi_c_var.append(py.value(m.v_wi_c_var[scenario, year, hour]))
                ieh_c_var.append(py.value(m.v_ieh_c_var[scenario, year, hour]))
                chp_c_var.append(py.value(m.v_chp_c_var[scenario, year, hour]))
                ac_c_var.append(py.value(m.v_ac_c_var[scenario, year, hour]))
                ab_ct_c_var.append(py.value(m.v_ab_ct_c_var[scenario, year, hour]))
                ab_hp_c_var.append(py.value(m.v_ab_hp_c_var[scenario, year, hour]))
                cp_ct_c_var.append(py.value(m.v_cp_ct_c_var[scenario, year, hour]))
                cp_hp_c_var.append(py.value(m.v_cp_hp_c_var[scenario, year, hour]))
                ttes_c_var.append(py.value(m.v_ttes_c_var[scenario, year, hour]))
                ites_c_var.append(py.value(m.v_ites_c_var[scenario, year, hour]))
                
                eb_elec.append(py.value(m.v_eb_q_elec_consumption[scenario, year, hour]))
                hp_elec.append(py.value(m.v_hp_q_elec_consumption[scenario, year, hour]))
                st_elec.append(py.value(m.v_st_q_elec_consumption[scenario, year, hour]))
                ieh_elec.append(py.value(m.v_ieh_q_elec_consumption[scenario, year, hour]))
                ac_elec.append(py.value(m.v_ac_q_elec_consumption[scenario, year, hour]))
                ab_ct_elec.append(py.value(m.v_ab_ct_q_elec_consumption[scenario, year, hour]))
                ab_hp_elec.append(py.value(m.v_ab_hp_q_elec_consumption[scenario, year, hour]))
                cp_ct_elec.append(py.value(m.v_cp_ct_q_elec_consumption[scenario, year, hour]))
                cp_hp_elec.append(py.value(m.v_cp_hp_q_elec_consumption[scenario, year, hour]))
                ttes_elec.append(py.value(m.v_ttes_q_elec_consumption[scenario, year, hour]))
                ites_elec.append(py.value(m.v_ites_q_elec_consumption[scenario, year, hour]))
                
                ttes_soc.append(py.value(m.v_ttes_k_heat[scenario, year, hour]))
                ites_soc.append(py.value(m.v_ites_k_cool[scenario, year, hour]))
            
            df_0.append(pd.DataFrame({'hour': hours, 'heating': data[scenario]['heating'][year], 'eb': eb_heat_in, 'hp': hp_heat_in, 'st': st_heat_in, 'wi': wi_heat_in, 'ieh': ieh_heat_in, 'chp': chp_heat_in, 'ab_ct-': ab_ct_heat_out, 'ab_hp+': ab_hp_heat_in, 'ab_hp-': ab_hp_heat_out, 'cp_hp+': cp_hp_heat_in, 'ttes+': ttes_heat_in, 'ttes-': ttes_heat_out}))
            df_1.append(pd.DataFrame({'hour': hours, 'cooling': data[scenario]['cooling'][year], 'ac': ac_cool_in, 'ab_ct': ab_ct_cool_in, 'ab_hp': ab_hp_cool_in, 'cp_ct': cp_ct_cool_in, 'cp_hp': cp_hp_cool_in, 'ites+': ites_cool_in, 'ites-': ites_cool_out}))
            df_2.append(pd.DataFrame({'eb': eb_inv, 'hp': hp_inv, 'st': st_inv, 'wi': wi_inv, 'ieh': ieh_inv, 'chp': chp_inv, 'ac': ac_inv, 'ab_ct': ab_ct_inv, 'ab_hp': ab_hp_inv, 'cp_ct': cp_ct_inv, 'cp_hp': cp_hp_inv, 'ttes': ttes_inv, 'ites': ites_inv}))
            df_3.append(pd.DataFrame({'eb': eb_c_inv, 'hp': hp_c_inv, 'st': st_c_inv, 'wi': wi_c_inv, 'ieh': ieh_c_inv, 'chp': chp_c_inv, 'ac': ac_c_inv, 'ab_ct': ab_ct_c_inv, 'ab_hp': ab_hp_c_inv, 'cp_ct': cp_ct_c_inv, 'cp_hp': cp_hp_c_inv, 'ttes': ttes_c_inv, 'ites': ites_c_inv}))
            df_4.append(pd.DataFrame({'eb': eb_c_fix, 'hp': hp_c_fix, 'st': st_c_fix, 'wi': wi_c_fix, 'ieh': ieh_c_fix, 'chp': chp_c_fix, 'ac': ac_c_fix, 'ab_ct': ab_ct_c_fix, 'ab_hp': ab_hp_c_fix, 'cp_ct': cp_ct_c_fix, 'cp_hp': cp_hp_c_fix, 'ttes': ttes_c_fix, 'ites': ites_c_fix}))
            df_5.append(pd.DataFrame({'eb': eb_c_var, 'hp': hp_c_var, 'st': st_c_var, 'wi': wi_c_var, 'ieh': ieh_c_var, 'chp': chp_c_var, 'ac': ac_c_var, 'ab_ct': ab_ct_c_var, 'ab_hp': ab_hp_c_var, 'cp_ct': cp_ct_c_var, 'cp_hp': cp_hp_c_var, 'ttes': ttes_c_var, 'ites': ites_c_var}))
            df_6.append(pd.DataFrame({'eb': eb_elec, 'hp': hp_elec, 'st': st_elec, 'ieh': ieh_elec, 'ac': ac_elec, 'ab_ct': ab_ct_elec, 'ab_hp': ab_hp_elec, 'cp_ct': cp_ct_elec, 'cp_hp': cp_hp_elec, 'ttes': ttes_elec, 'ites': ites_elec}))
            df_7.append(pd.DataFrame({'hour': hours, 'elec': data[scenario]['electricity_price'][year], 'gas': data[scenario]['gas_price'][year]}))
            df_8.append(pd.DataFrame({'co2': [data[scenario]['co2_price'][year]]}, index=[year]))
            df_9.append(pd.DataFrame({'hour': hours, 'ttes': ttes_soc, 'ites': ites_soc}))
        
        with pd.ExcelWriter(path_to_heat_supply) as writer:
            for df, year in zip(df_0, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_cool_supply) as writer:
            for df, year in zip(df_1, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_inv_capacity) as writer:
            for df, year in zip(df_2, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_inv_cost) as writer:
            for df, year in zip(df_3, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_fix_cost) as writer:
            for df, year in zip(df_4, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                        
        with pd.ExcelWriter(path_to_var_cost) as writer:
            for df, year in zip(df_5, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
    
        with pd.ExcelWriter(path_to_elec_consumption) as writer:
            for df, year in zip(df_6, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
    
        with pd.ExcelWriter(path_to_elec_gas_price) as writer:
            for df, year in zip(df_7, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_co2_price) as writer:
            for df, year in zip(df_8, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_storage_soc) as writer:
            for df, year in zip(df_9, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
