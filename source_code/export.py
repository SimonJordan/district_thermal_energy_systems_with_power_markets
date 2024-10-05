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
        path_to_inv_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_inv_cost.xlsx')
        path_to_fix_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_fix_cost.xlsx')
        path_to_var_cost = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_var_cost.xlsx')
        path_to_elec_consumption = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_consumption.xlsx')
        path_to_elec_gas_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_elec_price_co2_share_gas_price.xlsx')
        path_to_co2_price = os.path.join(path_to_result_folder, f'[{str(scenario)}]_#_co2_price.xlsx')
        
        df_0 = []
        df_1 = []
        df_2 = []
        df_3 = []
        df_4 = []
        df_5 = []
        df_6 = []
        df_7 = []
        
        for year in years:
            eb_in = []
            hp_in = []
            st_in = []
            wi_in = []
            gt_in = []
            dgt_in = []
            ieh_in = []
            chp_in = []
            ates_in = []
            ates_out = []
            ttes_in = []
            ttes_out = []
                    
            eb_c_inv = []
            hp_c_inv = []
            st_c_inv = []
            wi_c_inv = []
            gt_c_inv = []
            dgt_c_inv = []
            ieh_c_inv = []
            chp_c_inv = []
            ates_c_inv = []
            ttes_c_inv = []
            
            eb_c_fix = []
            hp_c_fix = []
            st_c_fix = []
            wi_c_fix = []
            gt_c_fix = []
            dgt_c_fix = []
            ieh_c_fix = []
            chp_c_fix = []
            ates_c_fix = []
            ttes_c_fix = []
            
            eb_c_var = []
            hp_c_var = []
            st_c_var = []
            wi_c_var = []
            gt_c_var = []
            dgt_c_var = []
            ieh_c_var = []
            chp_c_var = []
            ates_c_var = []
            ttes_c_var = []
            
            eb_elec = []
            hp_elec = []
            st_elec = []
            gt_elec = []
            ates_elec = []
            ttes_elec = []
            
            eb_c_inv.append(py.value(m.v_eb_c_inv[scenario, year]))
            hp_c_inv.append(py.value(m.v_hp_c_inv[scenario, year]))
            st_c_inv.append(py.value(m.v_st_c_inv[scenario, year]))
            wi_c_inv.append(py.value(m.v_wi_c_inv[scenario, year]))
            gt_c_inv.append(py.value(m.v_gt_c_inv[scenario, year]))
            dgt_c_inv.append(py.value(m.v_dgt_c_inv[scenario, year]))
            ieh_c_inv.append(py.value(m.v_ieh_c_inv[scenario, year]))
            chp_c_inv.append(py.value(m.v_chp_c_inv[scenario, year]))
            ates_c_inv.append(py.value(m.v_ates_c_inv[scenario, year]))
            ttes_c_inv.append(py.value(m.v_ttes_c_inv[scenario, year]))
            
            eb_c_fix.append(py.value(m.v_eb_c_fix[scenario, year]))
            hp_c_fix.append(py.value(m.v_hp_c_fix[scenario, year]))
            st_c_fix.append(py.value(m.v_st_c_fix[scenario, year]))
            wi_c_fix.append(py.value(m.v_wi_c_fix[scenario, year]))
            gt_c_fix.append(py.value(m.v_gt_c_fix[scenario, year]))
            dgt_c_fix.append(py.value(m.v_dgt_c_fix[scenario, year]))
            ieh_c_fix.append(py.value(m.v_ieh_c_fix[scenario, year]))
            chp_c_fix.append(py.value(m.v_chp_c_fix[scenario, year]))
            ates_c_fix.append(py.value(m.v_ates_c_fix[scenario, year]))
            ttes_c_fix.append(py.value(m.v_ttes_c_fix[scenario, year]))
            
            for hour in hours:
                eb_in.append(py.value(m.v_eb_q_heat_in[scenario, year, hour]))
                hp_in.append(py.value(m.v_hp_q_heat_in[scenario, year, hour]))
                st_in.append(py.value(m.v_st_q_heat_in[scenario, year, hour]))
                wi_in.append(py.value(m.v_wi_q_heat_in[scenario, year, hour]))
                gt_in.append(py.value(m.v_gt_q_heat_in[scenario, year, hour]))
                dgt_in.append(py.value(m.v_dgt_q_heat_in[scenario, year, hour]))
                ieh_in.append(py.value(m.v_ieh_q_heat_in[scenario, year, hour]))
                chp_in.append(py.value(m.v_chp_q_heat_in[scenario, year, hour]))
                ates_in.append(py.value(m.v_ates_q_heat_in[scenario, year, hour]))
                ates_out.append(-py.value(m.v_ates_q_heat_out[scenario, year, hour]))
                ttes_in.append(py.value(m.v_ttes_q_heat_in[scenario, year, hour]))
                ttes_out.append(-py.value(m.v_ttes_q_heat_out[scenario, year, hour]))
                
                eb_c_var.append(py.value(m.v_eb_c_var[scenario, year, hour]))
                hp_c_var.append(py.value(m.v_hp_c_var[scenario, year, hour]))
                st_c_var.append(py.value(m.v_st_c_var[scenario, year, hour]))
                wi_c_var.append(py.value(m.v_wi_c_var[scenario, year, hour]))
                gt_c_var.append(py.value(m.v_gt_c_var[scenario, year, hour]))
                dgt_c_var.append(py.value(m.v_dgt_c_var[scenario, year, hour]))
                ieh_c_var.append(py.value(m.v_ieh_c_var[scenario, year, hour]))
                chp_c_var.append(py.value(m.v_chp_c_var[scenario, year, hour]))
                ates_c_var.append(py.value(m.v_ates_c_var[scenario, year, hour]))
                ttes_c_var.append(py.value(m.v_ttes_c_var[scenario, year, hour]))
                
                eb_elec.append(py.value(m.v_eb_q_elec_consumption[scenario, year, hour]))
                hp_elec.append(py.value(m.v_hp_q_elec_consumption[scenario, year, hour]))
                st_elec.append(py.value(m.v_st_q_elec_consumption[scenario, year, hour]))
                gt_elec.append(py.value(m.v_gt_q_elec_consumption[scenario, year, hour]))
                ates_elec.append(py.value(m.v_ates_q_elec_consumption[scenario, year, hour]))
                ttes_elec.append(py.value(m.v_ttes_q_elec_consumption[scenario, year, hour]))
                
            df_0.append(pd.DataFrame({'hour': hours, 'heating': data[scenario]['heating'][year], 'eb': eb_in, 'hp': hp_in, 'st': st_in, 'wi': wi_in, 'gt': gt_in, 'dgt': dgt_in, 'ieh': ieh_in, 'chp': chp_in, 'ates+': ates_in, 'ates-': ates_out, 'ttes+': ttes_in, 'ttes-': ttes_out}))
            df_2.append(pd.DataFrame({'eb': eb_c_inv, 'hp': hp_c_inv, 'st': st_c_inv, 'wi': wi_c_inv, 'gt': gt_c_inv, 'dgt': dgt_c_inv, 'ieh': ieh_c_inv, 'chp': chp_c_inv, 'ates': ates_c_inv, 'ttes': ttes_c_inv}))
            df_3.append(pd.DataFrame({'eb': eb_c_fix, 'hp': hp_c_fix, 'st': st_c_fix, 'wi': wi_c_fix, 'gt': gt_c_fix, 'dgt': dgt_c_fix, 'ieh': ieh_c_fix, 'chp': chp_c_fix, 'ates': ates_c_fix, 'ttes': ttes_c_fix}))
            df_4.append(pd.DataFrame({'eb': eb_c_var, 'hp': hp_c_var, 'st': st_c_var, 'wi': wi_c_var, 'gt': gt_c_var, 'dgt': dgt_c_var, 'ieh': ieh_c_var, 'chp': chp_c_var, 'ates': ates_c_var, 'ttes': ttes_c_var}))
            df_5.append(pd.DataFrame({'eb': eb_elec, 'hp': hp_elec, 'st': st_elec, 'gt': gt_elec, 'ates': ates_elec, 'ttes': ttes_elec}))
            df_6.append(pd.DataFrame({'elec': data[scenario]['electricity_price'][year], 'co2': data[scenario]['electricity_co2_share'][year], 'gas': data[scenario]['gas_price'][year]}))
            df_7.append(pd.DataFrame({'co2': [data[scenario]['co2_price'][year]]}, index=[year]))
        
        with pd.ExcelWriter(path_to_heat_supply) as writer:
            for df, year in zip(df_0, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                       
        with pd.ExcelWriter(path_to_inv_cost) as writer:
            for df, year in zip(df_2, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_fix_cost) as writer:
            for df, year in zip(df_3, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                        
        with pd.ExcelWriter(path_to_var_cost) as writer:
            for df, year in zip(df_4, years):
                df.to_excel(writer, sheet_name=str(year), index=False)

        with pd.ExcelWriter(path_to_elec_consumption) as writer:
            for df, year in zip(df_5, years):
                df.to_excel(writer, sheet_name=str(year), index=False)

        with pd.ExcelWriter(path_to_elec_gas_price) as writer:
            for df, year in zip(df_6, years):
                df.to_excel(writer, sheet_name=str(year), index=False)
                
        with pd.ExcelWriter(path_to_co2_price) as writer:
            for df, year in zip(df_7, years):
                df.to_excel(writer, sheet_name=str(year), index=False)

    path_to_inv_capacity = os.path.join(path_to_result_folder, '[all]_#_inv_capacity.xlsx')

    for year in years:
        eb_inv = []
        hp_inv = []
        st_inv = []
        wi_inv = []
        gt_inv = []
        dgt_inv = []
        ieh_inv = []
        chp_inv = []
        ates_inv = []
        ttes_inv = []
        
        eb_inv.append(py.value(m.v_eb_Q_inv[year]))
        hp_inv.append(py.value(m.v_hp_Q_inv[year]))
        st_inv.append(py.value(m.v_st_P_inv[year]))
        wi_inv.append(py.value(m.v_wi_Q_inv[year]))
        gt_inv.append(py.value(m.v_gt_Q_inv[year]))
        dgt_inv.append(py.value(m.v_dgt_Q_inv[year]))
        ieh_inv.append(py.value(m.v_ieh_Q_inv[year]))
        chp_inv.append(py.value(m.v_chp_Q_inv[year]))
        ates_inv.append(py.value(m.v_ates_k_inv[year]))
        ttes_inv.append(py.value(m.v_ttes_k_inv[year]))

        df_1.append(pd.DataFrame({'eb': eb_inv, 'hp': hp_inv, 'st': st_inv, 'wi': wi_inv, 'gt': gt_inv, 'dgt': dgt_inv, 'ieh': ieh_inv, 'chp': chp_inv, 'ates': ates_inv, 'ttes': ttes_inv}))

    with pd.ExcelWriter(path_to_inv_capacity) as writer:
        for df, year in zip(df_1, years):
            df.to_excel(writer, sheet_name=str(year), index=False)
            