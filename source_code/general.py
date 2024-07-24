import pyomo.environ as py

def add_general_parameters(m=None):
    
    def init_c_elec(m, y, t, s):
        return m.data_values[s]['electricity_price'][y][t]
    
    def init_c_mean_elec(m, y, s):
        return m.data_values[s]['electricity_mean_price'][y]
    
    def init_c_co2(m, y, s):
        return m.data_values[s]['co2_price'][y]
    
    m.p_c_elec = py.Param(m.set_years, m.set_hours, m.set_scenarios,
                          initialize = init_c_elec,
                          within = py.Reals,
                          doc = 'specific electriyity prices year hour and scenario')

    m.p_c_mean_elec = py.Param(m.set_years, m.set_scenarios,
                               initialize = init_c_mean_elec,
                               within = py.Reals,
                               doc = 'mean electriyity prices year and scenario')
    
    m.p_c_co2 = py.Param(m.set_years, m.set_scenarios,
                         initialize = init_c_co2,
                         within = py.NonNegativeReals,
                         doc = 'CO2 price')