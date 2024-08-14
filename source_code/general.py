import pyomo.environ as py

def add_general_parameters(m=None):
    
    def init_c_elec(m, s, y, t):
        return m.data_values[s]['electricity_price'][y][t]
    
    def init_c_gas(m, s, y, t):
        return m.data_values[s]['gas_price'][y][t]
    
    def init_c_mean_elec(m, s, y):
        return m.data_values[s]['electricity_mean_price'][y]
    
    def init_c_co2(m, s, y):
        return m.data_values[s]['co2_price'][y]
    
    def init_scenario_weighting(m, s):
        return m.data_values[s]['scenario_weighting']
    
    m.p_c_elec = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                          initialize = init_c_elec,
                          within = py.Reals,
                          doc = 'specific electricity prices per year, hour and scenario')
    
    m.p_c_gas = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                         initialize = init_c_gas,
                         within = py.Reals,
                         doc = 'specific gas prices per year, hour and scenario')

    m.p_c_mean_elec = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_c_mean_elec,
                               within = py.Reals,
                               doc = 'mean electriyity prices per year and scenario')
    
    m.p_c_co2 = py.Param(m.set_scenarios, m.set_years,
                         initialize = init_c_co2,
                         within = py.NonNegativeReals,
                         doc = 'CO2 price')
    
    m.p_scenario_weighting = py.Param(m.set_scenarios,
                                      initialize = init_scenario_weighting,
                                      within = py.NonNegativeReals,
                                      doc = 'weighting of the scenario')