def define_scenarios(year_expansion_range, heating_demand, cooling_demand, electricity_price, electricity_mean_price, electricity_co2_share, electricity_mean_co2_share, gas_price, co2_price, data_eb, data_hp, data_st, data_wi, data_gt, data_dgt, data_ieh, data_chp, data_ac, data_ab, data_cp, data_ates, data_ttes, data_ites):
def define_scenarios(scenarios_weighting, year_expansion_range, heating_demand, cooling_demand, electricity_price, electricity_mean_price, electricity_co2_share, electricity_mean_co2_share, gas_price, co2_price, data_eb, data_hp, data_st, data_wi, data_gt, data_dgt, data_ieh, data_chp, data_ac, data_ab, data_cp, data_ates, data_ttes):
    data = {}
    
    data['0_basic'] = {'scenario_weighting': scenarios_weighting['0_basic'],
                       'year_expansion_range': year_expansion_range,
                       'heating': heating_demand,
                       'cooling': cooling_demand,
                       'electricity_price': electricity_price,
                       'electricity_mean_price': electricity_mean_price,
                       'electricity_co2_share': electricity_co2_share,
                       'electricity_mean_co2_share': electricity_mean_co2_share,
                       'gas_price': gas_price,
                       'co2_price': co2_price,
                       'eb': data_eb,
                       'hp': data_hp,
                       'st': data_st,
                       'wi': data_wi,
                       'gt': data_gt,
                       'dgt': data_dgt,
                       'ieh': data_ieh,
                       'chp': data_chp,
                       'ac': data_ac,
                       'ab': data_ab,
                       'cp': data_cp,
                       'ates': data_ates,
                       'ttes': data_ttes,
                       'ites': data_ites}
    
    data['1_high_electricity_price'] = {'scenario_weighting': scenarios_weighting['1_high_electricity_price'],
                                        'year_expansion_range': year_expansion_range,
                                        'heating': heating_demand,
                                        'cooling': cooling_demand,
                                        'electricity_price': {year: [value * 1.5 for value in values] for year, values in electricity_price.items()},
                                        'electricity_mean_price': {year: value * 1.5 for year, value in electricity_mean_price.items()},
                                        'electricity_co2_share': electricity_co2_share,
                                        'electricity_mean_co2_share': electricity_mean_co2_share,
                                        'gas_price': gas_price,
                                        'co2_price': co2_price,
                                        'eb': data_eb,
                                        'hp': data_hp,
                                        'st': data_st,
                                        'wi': data_wi,
                                        'gt': data_gt,
                                        'dgt': data_dgt,
                                        'ieh': data_ieh,
                                        'chp': data_chp,
                                        'ac': data_ac,
                                        'ab': data_ab,
                                        'cp': data_cp,
                                        'ates': data_ates,
                                        'ttes': data_ttes,
                                        'ites': data_ites}
    
    # data['2_low_electricity_price'] = {'year_expansion_range': year_expansion_range,
    #                                     'heating': heating_demand,
    #                                     'cooling': cooling_demand,
    #                                     'electricity_price': {year: [value * 0.5 for value in values] for year, values in electricity_price.items()},
    #                                     'electricity_mean_price': {year: value * 0.5 for year, value in electricity_mean_price.items()},
    #                                     'electricity_co2_share': electricity_co2_share,
    #                                     'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                     'gas_price': gas_price,
    #                                     'co2_price': co2_price,
    #                                     'eb': data_eb,
    #                                     'hp': data_hp,
    #                                     'st': data_st,
    #                                     'wi': data_wi,
    #                                     'gt': data_gt,
    #                                     'dgt': data_dgt,
    #                                     'ieh': data_ieh,
    #                                     'chp': data_chp,
    #                                     'ac': data_ac,
    #                                     'ab': data_ab,
    #                                     'cp': data_cp,
    #                                     'ates': data_ates,
    #                                     'ttes': data_ttes,
    #                                     'ites': data_ites}
    # data['2_low_electricity_price'] = {'scenario_weighting': scenarios_weighting['2_low_electricity_price'],
    #                                    'year_expansion_range': year_expansion_range,
    #                                    'heating': heating_demand,
    #                                    'cooling': cooling_demand,
    #                                    'electricity_price': {year: [value * 0.5 for value in values] for year, values in electricity_price.items()},
    #                                    'electricity_mean_price': {year: value * 0.5 for year, value in electricity_mean_price.items()},
    #                                    'electricity_co2_share': electricity_co2_share,
    #                                    'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                    'gas_price': gas_price,
    #                                    'co2_price': co2_price,
    #                                    'eb': data_eb,
    #                                    'hp': data_hp,
    #                                    'st': data_st,
    #                                    'wi': data_wi,
    #                                    'gt': data_gt,
    #                                    'dgt': data_dgt,
    #                                    'ieh': data_ieh,
    #                                    'chp': data_chp,
    #                                    'ac': data_ac,
    #                                    'ab': data_ab,
    #                                    'cp': data_cp,
    #                                    'ates': data_ates,
    #                                    'ttes': data_ttes}
    
    # data['3_non_neg_electricity_price'] = {'year_expansion_range': year_expansion_range,
    #                                         'heating': heating_demand,
    #                                         'cooling': cooling_demand,
    #                                         'electricity_price': {year: [max(0, value) for value in values] for year, values in electricity_price.items()},
    #                                         'electricity_mean_price': {year: sum(values)/len(values) for year, values in {year: [max(0, value) for value in values] for year, values in electricity_price.items()}.items()},
    #                                         'electricity_co2_share': electricity_co2_share,
    #                                         'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                         'gas_price': gas_price,
    #                                         'co2_price': co2_price,
    #                                         'eb': data_eb,
    #                                         'hp': data_hp,
    #                                         'st': data_st,
    #                                         'wi': data_wi,
    #                                         'gt': data_gt,
    #                                         'dgt': data_dgt,
    #                                         'ieh': data_ieh,
    #                                         'chp': data_chp,
    #                                         'ac': data_ac,
    #                                         'ab': data_ab,
    #                                         'cp': data_cp,
    #                                         'ates': data_ates,
    #                                         'ttes': data_ttes,
    #                                         'ites': data_ites}
    # data['3_non_neg_electricity_price'] = {'scenario_weighting': scenarios_weighting['3_non_neg_electricity_price'],
    #                                        'year_expansion_range': year_expansion_range,
    #                                        'heating': heating_demand,
    #                                        'cooling': cooling_demand,
    #                                        'electricity_price': {year: [max(0, value) for value in values] for year, values in electricity_price.items()},
    #                                        'electricity_mean_price': {year: sum(values)/len(values) for year, values in {year: [max(0, value) for value in values] for year, values in electricity_price.items()}.items()},
    #                                        'electricity_co2_share': electricity_co2_share,
    #                                        'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                        'gas_price': gas_price,
    #                                        'co2_price': co2_price,
    #                                        'eb': data_eb,
    #                                        'hp': data_hp,
    #                                        'st': data_st,
    #                                        'wi': data_wi,
    #                                        'gt': data_gt,
    #                                        'dgt': data_dgt,
    #                                        'ieh': data_ieh,
    #                                        'chp': data_chp,
    #                                        'ac': data_ac,
    #                                        'ab': data_ab,
    #                                        'cp': data_cp,
    #                                        'ates': data_ates,
    #                                        'ttes': data_ttes}
    
    # data['4_high_gas_price'] = {'scenario_weighting': scenarios_weighting['4_high_gas_price'],
    #                             'year_expansion_range': year_expansion_range,
    #                             'heating': heating_demand,
    #                             'cooling': cooling_demand,
    #                             'electricity_price': electricity_price,
    #                             'electricity_mean_price': electricity_mean_price,
    #                             'electricity_co2_share': electricity_co2_share,
    #                             'electricity_mean_co2_share': electricity_mean_co2_share,
    #                             'gas_price': {year: [value * 1.3 for value in values] for year, values in gas_price.items()},
    #                             'co2_price': co2_price,
    #                             'eb': data_eb,
    #                             'hp': data_hp,
    #                             'st': data_st,
    #                             'wi': data_wi,
    #                             'gt': data_gt,
    #                             'dgt': data_dgt,
    #                             'ieh': data_ieh,
    #                             'chp': data_chp,
    #                             'ac': data_ac,
    #                             'ab': data_ab,
    #                             'cp': data_cp,
    #                             'ates': data_ates,
    #                             'ttes': data_ttes,
    #                             'ites': data_ites}
    
    # data['5_zero_co2_price'] = {'scenario_weighting': scenarios_weighting['5_zero_co2_price'],
    #                             'year_expansion_range': year_expansion_range,
    #                             'heating': heating_demand,
    #                             'cooling': cooling_demand,
    #                             'electricity_price': electricity_price,
    #                             'electricity_mean_price': electricity_mean_price,
    #                             'electricity_co2_share': electricity_co2_share,
    #                             'electricity_mean_co2_share': electricity_mean_co2_share, 
    #                             'gas_price': gas_price,
    #                             'co2_price': {year: value * 0 for year, value in co2_price.items()},
    #                             'eb': data_eb,
    #                             'hp': data_hp,
    #                             'st': data_st,
    #                             'wi': data_wi,
    #                             'gt': data_gt,
    #                             'dgt': data_dgt,
    #                             'ieh': data_ieh,
    #                             'chp': data_chp,
    #                             'ac': data_ac,
    #                             'ab': data_ab,
    #                             'cp': data_cp,
    #                             'ates': data_ates,
    #                             'ttes': data_ttes,
    #                             'ites': data_ites}
    
    # data['6_high_co2_price'] = {'scenario_weighting': scenarios_weighting['6_high_co2_price'],
    #                             'year_expansion_range': year_expansion_range,
    #                             'heating': heating_demand,
    #                             'cooling': cooling_demand,
    #                             'electricity_price': electricity_price,
    #                             'electricity_mean_price': electricity_mean_price,
    #                             'electricity_co2_share': electricity_co2_share,
    #                             'electricity_mean_co2_share': electricity_mean_co2_share,
    #                             'gas_price': gas_price,
    #                             'co2_price': {year: value * 1.5 for year, value in co2_price.items()},
    #                             'eb': data_eb,
    #                             'hp': data_hp,
    #                             'st': data_st,
    #                             'wi': data_wi,
    #                             'gt': data_gt,
    #                             'dgt': data_dgt,
    #                             'ieh': data_ieh,
    #                             'chp': data_chp,
    #                             'ac': data_ac,
    #                             'ab': data_ab,
    #                             'cp': data_cp,
    #                             'ates': data_ates,
    #                             'ttes': data_ttes,
    #                             'ites': data_ites}
    
    # data['7_half_investment_c'] = {'year_expansion_range': year_expansion_range,
    #                                 'heating': heating_demand,
    #                                 'cooling': cooling_demand,
    #                                 'electricity_price': electricity_price,
    #                                 'electricity_mean_price': electricity_mean_price,
    #                                 'electricity_co2_share': electricity_co2_share,
    #                                 'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                 'gas_price': gas_price,
    #                                 'co2_price': co2_price,
    #                                 'eb': {year: {name: (value * 0.5 if name == 'p_eb_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_eb.items()},
    #                                 'hp': {year: {name: (value * 0.5 if name == 'p_hp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_hp.items()},
    #                                 'st': {year: {name: (value * 0.5 if name == 'p_st_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_st.items()},
    #                                 'wi': {year: {name: (value * 0.5 if name == 'p_wi_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_wi.items()},
    #                                 'gt': {year: {name: (value * 0.5 if name == 'p_gt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_gt.items()},
    #                                 'dgt': {year: {name: (value * 0.5 if name == 'p_dgt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_dgt.items()},
    #                                 'ieh': {year: {name: (value * 0.5 if name == 'p_ieh_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ieh.items()},
    #                                 'chp': {year: {name: (value * 0.5 if name == 'p_chp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_chp.items()},
    #                                 'ac': {year: {name: (value * 0.5 if name == 'p_ac_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ac.items()},
    #                                 'ab': {year: {name: (value * 0.5 if name == 'p_ab_c_inv' or 'p_ct_ab_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ab.items()},
    #                                 'cp': {year: {name: (value * 0.5 if name == 'p_cp_c_inv' or 'p_ct_cp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_cp.items()},
    #                                 'ates': {year: {name: (value * 0.5 if name == 'p_ates_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ates.items()},
    #                                 'ttes': {year: {name: (value * 0.5 if name == 'p_ttes_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ttes.items()},
    #                                 'ites': {year: {name: (value * 0.5 if name == 'p_ites_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ttes.items()}}
    # data['7_half_investment_c'] = {'scenario_weighting': scenarios_weighting['7_half_investment_c'],
    #                                'year_expansion_range': year_expansion_range,
    #                                'heating': heating_demand,
    #                                'cooling': cooling_demand,
    #                                'electricity_price': electricity_price,
    #                                'electricity_mean_price': electricity_mean_price,
    #                                'electricity_co2_share': electricity_co2_share,
    #                                'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                'gas_price': gas_price,
    #                                'co2_price': co2_price,
    #                                'eb': {year: {name: (value * 0.5 if name == 'p_eb_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_eb.items()},
    #                                'hp': {year: {name: (value * 0.5 if name == 'p_hp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_hp.items()},
    #                                'st': {year: {name: (value * 0.5 if name == 'p_st_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_st.items()},
    #                                'wi': {year: {name: (value * 0.5 if name == 'p_wi_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_wi.items()},
    #                                'gt': {year: {name: (value * 0.5 if name == 'p_gt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_gt.items()},
    #                                'dgt': {year: {name: (value * 0.5 if name == 'p_dgt_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_dgt.items()},
    #                                'ieh': {year: {name: (value * 0.5 if name == 'p_ieh_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ieh.items()},
    #                                'chp': {year: {name: (value * 0.5 if name == 'p_chp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_chp.items()},
    #                                'ac': {year: {name: (value * 0.5 if name == 'p_ac_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ac.items()},
    #                                'ab': {year: {name: (value * 0.5 if name == 'p_ab_c_inv' or 'p_ct_ab_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ab.items()},
    #                                'cp': {year: {name: (value * 0.5 if name == 'p_cp_c_inv' or 'p_ct_cp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_cp.items()},
    #                                'ates': {year: {name: (value * 0.5 if name == 'p_ates_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ates.items()},
    #                                'ttes': {year: {name: (value * 0.5 if name == 'p_ttes_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ttes.items()}}
    
    # data['8_low_electricity_price_high_co2_price'] = {'scenario_weighting': scenarios_weighting['8_low_electricity_price_high_co2_price'],
    #                                                   'year_expansion_range': year_expansion_range,
    #                                                   'heating': heating_demand,
    #                                                   'cooling': cooling_demand,
    #                                                   'electricity_price': {year: [value * 0.5 for value in values] for year, values in electricity_price.items()},
    #                                                   'electricity_mean_price': {year: value * 0.5 for year, value in electricity_mean_price.items()},
    #                                                   'electricity_co2_share': electricity_co2_share,
    #                                                   'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                                   'gas_price': gas_price,
    #                                                   'co2_price': {year: value * 1.5 for year, value in co2_price.items()},
    #                                                   'eb': data_eb,
    #                                                   'hp': data_hp,
    #                                                   'st': data_st,
    #                                                   'wi': data_wi,
    #                                                   'gt': data_gt,
    #                                                   'dgt': data_dgt,
    #                                                   'ieh': data_ieh,
    #                                                   'chp': data_chp,
    #                                                   'ac': data_ac,
    #                                                   'ab': data_ab,
    #                                                   'cp': data_cp,
    #                                                   'ates': data_ates,
    #                                                   'ttes': data_ttes,
    #                                                   'ites': data_ites}
    
    # data['9_high_electricity_price_high_gas_price_high_co2_price'] = {'scenario_weighting': scenarios_weighting['9_high_electricity_price_high_gas_price_high_co2_price'],
    #                                                                   'year_expansion_range': year_expansion_range,
    #                                                                   'heating': heating_demand,
    #                                                                   'cooling': cooling_demand,
    #                                                                   'electricity_price': {year: [value * 1.5 for value in values] for year, values in electricity_price.items()},
    #                                                                   'electricity_mean_price': {year: value * 1.5 for year, value in electricity_mean_price.items()},
    #                                                                   'electricity_co2_share': electricity_co2_share,
    #                                                                   'electricity_mean_co2_share': electricity_mean_co2_share,
    #                                                                   'gas_price': {year: [value * 1.3 for value in values] for year, values in gas_price.items()},
    #                                                                   'co2_price': {year: value * 1.5 for year, value in co2_price.items()},
    #                                                                   'eb': data_eb,
    #                                                                   'hp': data_hp,
    #                                                                   'st': data_st,
    #                                                                   'wi': data_wi,
    #                                                                   'gt': data_gt,
    #                                                                   'dgt': data_dgt,
    #                                                                   'ieh': data_ieh,
    #                                                                   'chp': data_chp,
    #                                                                   'ac': data_ac,
    #                                                                   'ab': data_ab,
    #                                                                   'cp': data_cp,
    #                                                                   'ates': data_ates,
    #                                                                   'ttes': data_ttes,
    #                                                                   'ites': data_ites}
    
    return data
    