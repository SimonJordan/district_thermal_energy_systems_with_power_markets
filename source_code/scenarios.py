def define_scenarios(year_expansion_range, heating_demand, cooling_demand, electricity_price, electricity_mean_price, gas_price, co2_price, data_eb, data_gb, data_hp, data_st, data_wi, data_ieh, data_chp, data_ac, data_ab, data_cp, data_ttes, data_btes, data_ites):
    data = {}
    
    shifted_co2_price = {}
    stored_co2_price = []
    
    for year, value in co2_price.items():
        if year in [2025, 2030]:
            shifted_co2_price[year] = value * 0
            stored_co2_price.append(value)
        else:
            if stored_co2_price == []:
                shifted_co2_price[year] = value
            else:
                shifted_co2_price[year] = stored_co2_price.pop(0)
    
    data['1_reference'] = {'year_expansion_range': year_expansion_range,
                           'heating': heating_demand,
                           'cooling': cooling_demand,
                           'electricity_price': electricity_price,
                           'electricity_mean_price': electricity_mean_price,
                           'gas_price': gas_price,
                           'co2_price': co2_price,
                           'eb': data_eb,
                           'gb': data_gb,
                           'hp': data_hp,
                           'st': data_st,
                           'wi': data_wi,
                           'ieh': data_ieh,
                           'chp': data_chp,
                           'ac': data_ac,
                           'ab': data_ab,
                           'cp': data_cp,
                           'ttes': data_ttes,
                           'btes': data_btes,
                           'ites': data_ites}
    
    data['2_high_electricity_prices'] = {'year_expansion_range': year_expansion_range,
                                         'heating': heating_demand,
                                         'cooling': cooling_demand,
                                         'electricity_price': {year: [value * 1.2 for value in values] for year, values in electricity_price.items()},
                                         'electricity_mean_price': {year: value * 1.2 for year, value in electricity_mean_price.items()},
                                         'gas_price': gas_price,
                                         'co2_price': co2_price,
                                         'eb': data_eb,
                                         'gb': data_gb,
                                         'hp': data_hp,
                                         'st': data_st,
                                         'wi': data_wi,
                                         'ieh': data_ieh,
                                         'chp': data_chp,
                                         'ac': data_ac,
                                         'ab': data_ab,
                                         'cp': data_cp,
                                         'ttes': data_ttes,
                                         'btes': data_btes,
                                         'ites': data_ites}
    
    # data['3_low_electricity_prices'] = {'year_expansion_range': year_expansion_range,
    #                                     'heating': heating_demand,
    #                                     'cooling': cooling_demand,
    #                                     'electricity_price': {year: [value * 0.8 for value in values] for year, values in electricity_price.items()},
    #                                     'electricity_mean_price': {year: value * 0.8 for year, value in electricity_mean_price.items()},
    #                                     'gas_price': gas_price,
    #                                     'co2_price': co2_price,
    #                                     'eb': data_eb,
    #                                     'gb': data_gb,
    #                                     'hp': data_hp,
    #                                     'st': data_st,
    #                                     'wi': data_wi,
    #                                     'ieh': data_ieh,
    #                                     'chp': data_chp,
    #                                     'ac': data_ac,
    #                                     'ab': data_ab,
    #                                     'cp': data_cp,
    #                                     'ttes': data_ttes,
    #                                     'btes': data_btes,
    #                                     'ites': data_ites}
    
    # data['4_flexible_energy_market'] = {'year_expansion_range': year_expansion_range,
    #                                     'heating': heating_demand,
    #                                     'cooling': cooling_demand,
    #                                     'electricity_price': {year: [max(0, value) for value in values] for year, values in electricity_price.items()},
    #                                     'electricity_mean_price': {year: sum(values)/len(values) for year, values in {year: [max(0, value) for value in values] for year, values in electricity_price.items()}.items()},
    #                                     'gas_price': gas_price,
    #                                     'co2_price': co2_price,
    #                                     'eb': data_eb,
    #                                     'gb': data_gb,
    #                                     'hp': data_hp,
    #                                     'st': data_st,
    #                                     'wi': data_wi,
    #                                     'ieh': data_ieh,
    #                                     'chp': data_chp,
    #                                     'ac': data_ac,
    #                                     'ab': data_ab,
    #                                     'cp': data_cp,
    #                                     'ttes': data_ttes,
    #                                     'btes': data_btes,
    #                                     'ites': data_ites}
    
    # data['5_energy_congestion'] = {'year_expansion_range': year_expansion_range,
    #                                'heating': heating_demand,
    #                                'cooling': cooling_demand,
    #                                'electricity_price': {year: [value * 1.1 for value in values] if year in [2035] else values for year, values in electricity_price.items()},
    #                                'electricity_mean_price': {year: value * 1.1 if year in [2035] else value for year, value in electricity_mean_price.items()},
    #                                'gas_price': {year: [value * 1.2 for value in values] if year in [2035] else values for year, values in gas_price.items()},
    #                                'co2_price': co2_price,
    #                                'eb': data_eb,
    #                                'gb': data_gb,
    #                                'hp': data_hp,
    #                                'st': data_st,
    #                                'wi': data_wi,
    #                                'ieh': data_ieh,
    #                                'chp': data_chp,
    #                                'ac': data_ac,
    #                                'ab': data_ab,
    #                                'cp': data_cp,
    #                                'ttes': data_ttes,
    #                                'btes': data_btes,
    #                                'ites': data_ites}
    
    # data['6_green_friendly'] = {'year_expansion_range': year_expansion_range,
    #                             'heating': heating_demand,
    #                             'cooling': cooling_demand,
    #                             'electricity_price': electricity_price,
    #                             'electricity_mean_price': electricity_mean_price,
    #                             'gas_price': gas_price,
    #                             'co2_price': {year: value * 1.1 for year, value in co2_price.items()},
    #                             'eb': {year: {name: (value * 0.8 if name == 'p_eb_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_eb.items()},
    #                             'gb': {year: {name: (value * 0.8 if name == 'p_gb_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_gb.items()},
    #                             'hp': {year: {name: (value * 0.8 if name == 'p_hp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_hp.items()},
    #                             'st': {year: {name: (value * 0.8 if name == 'p_st_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_st.items()},
    #                             'wi': {year: {name: (value * 0.8 if name == 'p_wi_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_wi.items()},
    #                             'ieh': {year: {name: (value * 0.8 if name == 'p_ieh_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ieh.items()},
    #                             'chp': {year: {name: (value * 0.8 if name == 'p_chp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_chp.items()},
    #                             'ac': {year: {name: (value * 0.8 if name == 'p_ac_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ac.items()},
    #                             'ab': {year: {name: (value * 0.8 if name == 'p_ab_c_inv' or 'p_ct_ab_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ab.items()},
    #                             'cp': {year: {name: (value * 0.8 if name == 'p_cp_c_inv' or 'p_ct_cp_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_cp.items()},
    #                             'ttes': {year: {name: (value * 0.8 if name == 'p_ttes_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ttes.items()},
    #                             'btes': {year: {name: (value * 0.8 if name == 'p_btes_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_btes.items()},
    #                             'ites': {year: {name: (value * 0.8 if name == 'p_ites_c_inv' else value) for name, value in dict_items.items()} for year, dict_items in data_ites.items()}}
    
    # data['7_low_gas_demand'] = {'year_expansion_range': year_expansion_range,
    #                             'heating': heating_demand,
    #                             'cooling': cooling_demand,
    #                             'electricity_price': {year: [value * 0.85 for value in values] for year, values in electricity_price.items()},
    #                             'electricity_mean_price': {year: value * 0.85 for year, value in electricity_mean_price.items()},
    #                             'gas_price': {year: [value * 0.95 for value in values] for year, values in gas_price.items()},
    #                             'co2_price': {year: value * 1.25 for year, value in co2_price.items()},
    #                             'eb': data_eb,
    #                             'gb': data_gb,
    #                             'hp': data_hp,
    #                             'st': data_st,
    #                             'wi': data_wi,
    #                             'ieh': data_ieh,
    #                             'chp': data_chp,
    #                             'ac': data_ac,
    #                             'ab': data_ab,
    #                             'cp': data_cp,
    #                             'ttes': data_ttes,
    #                             'btes': data_btes,
    #                             'ites': data_ites}
    
    # data['8_natural_gas_friendly'] = {'year_expansion_range': year_expansion_range,
    #                                   'heating': heating_demand,
    #                                   'cooling': cooling_demand,
    #                                   'electricity_price': electricity_price,
    #                                   'electricity_mean_price': electricity_mean_price,
    #                                   'gas_price': {year: [value * 0.85 for value in values] if year in [2040] else values for year, values in gas_price.items()},
    #                                   'co2_price': {year: value * 0 if year in [2040] else value for year, value in co2_price.items()},
    #                                   'eb': data_eb,
    #                                   'gb': data_gb,
    #                                   'hp': data_hp,
    #                                   'st': data_st,
    #                                   'wi': data_wi,
    #                                   'ieh': data_ieh,
    #                                   'chp': data_chp,
    #                                   'ac': data_ac,
    #                                   'ab': data_ab,
    #                                   'cp': data_cp,
    #                                   'ttes': data_ttes,
    #                                   'btes': data_btes,
    #                                   'ites': data_ites}
    
    # data['9_cold_winters'] = {'year_expansion_range': year_expansion_range,
    #                           'heating': {year: [value * 1.1 for value in values] if year in [2045, 2050] else values for year, values in heating_demand.items()},
    #                           'cooling': cooling_demand,
    #                           'electricity_price': {year: [value * 1.05 for value in values] if year in [2045, 2050] else values for year, values in electricity_price.items()},
    #                           'electricity_mean_price': {year: value * 1.05 if year in [2045, 2050] else value for year, value in electricity_mean_price.items()},
    #                           'gas_price': {year: [value * 1.1 for value in values] if year in [2045, 2050] else values for year, values in gas_price.items()},
    #                           'co2_price': co2_price,
    #                           'eb': data_eb,
    #                           'gb': data_gb,
    #                           'hp': data_hp,
    #                           'st': data_st,
    #                           'wi': data_wi,
    #                           'ieh': data_ieh,
    #                           'chp': data_chp,
    #                           'ac': data_ac,
    #                           'ab': data_ab,
    #                           'cp': data_cp,
    #                           'ttes': data_ttes,
    #                           'btes': data_btes,
    #                           'ites': data_ites}
    
    # data['10_hot_summers'] = {'year_expansion_range': year_expansion_range,
    #                           'heating': heating_demand,
    #                           'cooling': {year: [value * 1.1 for value in values] if year in [2030] else values for year, values in cooling_demand.items()},
    #                           'electricity_price': {year: [value * 1.1 for value in values] if year in [2030] else values for year, values in electricity_price.items()},
    #                           'electricity_mean_price': {year: value * 1.1 if year in [2030] else value for year, value in electricity_mean_price.items()},
    #                           'gas_price': gas_price,
    #                           'co2_price': co2_price,
    #                           'eb': data_eb,
    #                           'gb': data_gb,
    #                           'hp': data_hp,
    #                           'st': data_st,
    #                           'wi': data_wi,
    #                           'ieh': data_ieh,
    #                           'chp': data_chp,
    #                           'ac': data_ac,
    #                           'ab': data_ab,
    #                           'cp': data_cp,
    #                           'ttes': data_ttes,
    #                           'btes': data_btes,
    #                           'ites': data_ites}
    
    # data['11_warm_summers'] = {'year_expansion_range': year_expansion_range,
    #                            'heating': heating_demand,
    #                            'cooling': {year: [value * 1.05 for value in values] if year in [2045, 2050] else values for year, values in cooling_demand.items()},
    #                            'electricity_price': electricity_price,
    #                            'electricity_mean_price': electricity_mean_price,
    #                            'gas_price': gas_price,
    #                            'co2_price': co2_price,
    #                            'eb': data_eb,
    #                            'gb': data_gb,
    #                            'hp': data_hp,
    #                            'st': data_st,
    #                            'wi': data_wi,
    #                            'ieh': data_ieh,
    #                            'chp': data_chp,
    #                            'ac': data_ac,
    #                            'ab': data_ab,
    #                            'cp': data_cp,
    #                            'ttes': data_ttes,
    #                            'btes': data_btes,
    #                            'ites': data_ites}
    
    # data['12_moderate_climate'] = {'year_expansion_range': year_expansion_range,
    #                                'heating': {year: [value * 0.9 for value in values] for year, values in heating_demand.items()},
    #                                'cooling': {year: [value * 0.9 for value in values] for year, values in cooling_demand.items()},
    #                                'electricity_price': {year: [value * 0.9 for value in values] for year, values in electricity_price.items()},
    #                                'electricity_mean_price': {year: value * 0.9 for year, value in electricity_mean_price.items()},
    #                                'gas_price': {year: [value * 0.8 for value in values] for year, values in gas_price.items()},
    #                                'co2_price': co2_price,
    #                                'eb': data_eb,
    #                                'gb': data_gb,
    #                                'hp': data_hp,
    #                                'st': data_st,
    #                                'wi': data_wi,
    #                                'ieh': data_ieh,
    #                                'chp': data_chp,
    #                                'ac': data_ac,
    #                                'ab': data_ab,
    #                                'cp': data_cp,
    #                                'ttes': data_ttes,
    #                                'btes': data_btes,
    #                                'ites': data_ites}
    
    # data['13_zero_co2_price'] = {'year_expansion_range': year_expansion_range,
    #                              'heating': heating_demand,
    #                              'cooling': cooling_demand,
    #                              'electricity_price': electricity_price,
    #                              'electricity_mean_price': electricity_mean_price,
    #                              'gas_price': gas_price,
    #                              'co2_price': {year: value * 0 for year, value in co2_price.items()},
    #                              'eb': data_eb,
    #                              'gb': data_gb,
    #                              'hp': data_hp,
    #                              'st': data_st,
    #                              'wi': data_wi,
    #                              'ieh': data_ieh,
    #                              'chp': data_chp,
    #                              'ac': data_ac,
    #                              'ab': data_ab,
    #                              'cp': data_cp,
    #                              'ttes': data_ttes,
    #                              'btes': data_btes,
    #                              'ites': data_ites}
    
    # data['14_delayed_co2_pricing'] = {'year_expansion_range': year_expansion_range,
    #                                   'heating': heating_demand,
    #                                   'cooling': cooling_demand,
    #                                   'electricity_price': electricity_price,
    #                                   'electricity_mean_price': electricity_mean_price,
    #                                   'gas_price': gas_price,
    #                                   'co2_price': {year: value for year, value in shifted_co2_price.items()},
    #                                   'eb': data_eb,
    #                                   'gb': data_gb,
    #                                   'hp': data_hp,
    #                                   'st': data_st,
    #                                   'wi': data_wi,
    #                                   'ieh': data_ieh,
    #                                   'chp': data_chp,
    #                                   'ac': data_ac,
    #                                   'ab': data_ab,
    #                                   'cp': data_cp,
    #                                   'ttes': data_ttes,
    #                                   'btes': data_btes,
    #                                   'ites': data_ites}
    
    # data['15_ambitious_co2_pricing'] = {'year_expansion_range': year_expansion_range,
    #                                     'heating': heating_demand,
    #                                     'cooling': cooling_demand,
    #                                     'electricity_price': electricity_price,
    #                                     'electricity_mean_price': electricity_mean_price,
    #                                     'gas_price': gas_price,
    #                                     'co2_price': {year: value * 1.25 for year, value in co2_price.items()},
    #                                     'eb': data_eb,
    #                                     'gb': data_gb,
    #                                     'hp': data_hp,
    #                                     'st': data_st,
    #                                     'wi': data_wi,
    #                                     'ieh': data_ieh,
    #                                     'chp': data_chp,
    #                                     'ac': data_ac,
    #                                     'ab': data_ab,
    #                                     'cp': data_cp,
    #                                     'ttes': data_ttes,
    #                                     'btes': data_btes,
    #                                     'ites': data_ites}
    
    # data['16_expiring_support_res'] = {'year_expansion_range': year_expansion_range,
    #                                    'heating': heating_demand,
    #                                    'cooling': cooling_demand,
    #                                    'electricity_price': electricity_price,
    #                                    'electricity_mean_price': electricity_mean_price,
    #                                    'gas_price': gas_price,
    #                                    'co2_price': co2_price,
    #                                    'eb': {year: {name: (value * 0.7 if name == 'p_eb_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_eb.items()},
    #                                    'gb': {year: {name: (value * 0.7 if name == 'p_gb_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_gb.items()},
    #                                    'hp': {year: {name: (value * 0.7 if name == 'p_hp_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_hp.items()},
    #                                    'st': {year: {name: (value * 0.7 if name == 'p_st_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_st.items()},
    #                                    'wi': {year: {name: (value * 0.7 if name == 'p_wi_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_wi.items()},
    #                                    'ieh': {year: {name: (value * 0.7 if name == 'p_ieh_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_ieh.items()},
    #                                    'chp': {year: {name: (value * 0.7 if name == 'p_chp_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_chp.items()},
    #                                    'ac': {year: {name: (value * 0.7 if name == 'p_ac_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_ac.items()},
    #                                    'ab': {year: {name: (value * 0.7 if name == ('p_ab_c_inv' or 'p_ct_ab_c_inv') and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_ab.items()},
    #                                    'cp': {year: {name: (value * 0.7 if name == ('p_cp_c_inv' or 'p_ct_cp_c_inv') and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_cp.items()},
    #                                    'ttes': {year: {name: (value * 0.7 if name == 'p_ttes_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_ttes.items()},
    #                                    'btes': {year: {name: (value * 0.7 if name == 'p_btes_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_btes.items()},
    #                                    'ites': {year: {name: (value * 0.7 if name == 'p_ites_c_inv' and year in [2025, 2030] else value) for name, value in dict_items.items()} for year, dict_items in data_ites.items()}}
    
    return data
    