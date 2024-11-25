import pyomo.environ as py

def add_general_parameters(m=None):
    
    def init_year_expansion_range(m, s, y):
        return m.data_values[s]['year_expansion_range'][y]
    
    def init_c_elec(m, s, y, h):
        return m.data_values[s]['electricity_price'][y][h]
    
    def init_c_mean_elec(m, s, y):
        return m.data_values[s]['electricity_mean_price'][y]
    
    def init_c_gas(m, s, y, h):
        return m.data_values[s]['gas_price'][y][h]
     
    def init_c_co2(m, s, y):
        return m.data_values[s]['co2_price'][y]
    
    m.p_year_expansion_range = py.Param(m.set_scenarios, m.set_years,
                                        initialize = init_year_expansion_range,
                                        within = py.Reals,
                                        doc = 'scaling the years')
    
    m.p_c_elec = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                          initialize = init_c_elec,
                          within = py.Reals,
                          doc = 'specific electricity prices per year, hour and scenario')
    
    m.p_c_mean_elec = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_c_mean_elec,
                               within = py.Reals,
                               doc = 'mean electriyity prices per year and scenario')
    
    m.p_c_gas = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                         initialize = init_c_gas,
                         within = py.Reals,
                         doc = 'specific gas prices per year, hour and scenario')

    m.p_c_co2 = py.Param(m.set_scenarios, m.set_years,
                         initialize = init_c_co2,
                         within = py.NonNegativeReals,
                         doc = 'CO2 price')
    