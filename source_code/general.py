import pyomo.environ as py

def add_general_parameters(m=None):
    
    def init_c_elec(m, s, y, t):
        return m.data_values[s]['electricity_price'][y][t]
    
    def init_c_mean_elec(m, s, y):
        return m.data_values[s]['electricity_mean_price'][y]
    
    def init_electricity_co2_share(m, s, y, t):
        return m.data_values[s]['electricity_co2_share'][y][t]
    
    def init_electricity_co2_share_mean(m, s, y):
        return m.data_values[s]['electricity_mean_co2_share'][y]
    
    def init_c_gas(m, s, y, t):
        return m.data_values[s]['gas_price'][y][t]
     
    def init_c_co2(m, s, y):
        return m.data_values[s]['co2_price'][y]
    
    m.p_c_elec = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                          initialize = init_c_elec,
                          within = py.Reals,
                          doc = 'specific electricity prices per year, hour and scenario')
    
    m.p_c_mean_elec = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_c_mean_elec,
                               within = py.Reals,
                               doc = 'mean electriyity prices per year and scenario')
        
    m.p_elec_co2_share = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                                  initialize = init_electricity_co2_share,
                                  within = py.Reals,
                                  doc = 'CO2 share of electricity per year, hour and scenario')
    
    m.p_mean_elec_co2_share = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_electricity_co2_share_mean,
                               within = py.Reals,
                               doc = 'mean CO2 share of electricity per year and scenario')
    
    m.p_c_gas = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                         initialize = init_c_gas,
                         within = py.Reals,
                         doc = 'specific gas prices per year, hour and scenario')

    m.p_c_co2 = py.Param(m.set_scenarios, m.set_years,
                         initialize = init_c_co2,
                         within = py.NonNegativeReals,
                         doc = 'CO2 price')