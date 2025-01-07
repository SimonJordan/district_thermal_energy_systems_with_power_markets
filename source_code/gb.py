import pyomo.environ as py

def add_gb_equations(m=None):
    
    def gb_feed_in_max_bound(m, s, y, h):
        return m.v_gb_q_heat_in[s, y, h] <= m.v_gb_Q_heat_max[y]
    
    # def gb_limit(m, y):
    #     return m.v_gb_Q_heat_max[y] <= 0
    
    def gb_gas_heat(m, s, y, h):
        return m.v_gb_q_heat_in[s, y, h] == m.v_gb_q_gas[s, y, h] * m.p_gb_eta[s, y]
    
    def gb_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_gb_Q_inv[y] == m.v_gb_Q_heat_max[y] - m.v_gb_Q_heat_max[y-5]
        else:
            return m.v_gb_Q_inv[y] == m.v_gb_Q_heat_max[y]
    
    def gb_c_inv(m, s, y):
        return m.v_gb_c_inv[s, y] == m.v_gb_Q_inv[y] * m.p_gb_c_inv[s, y]
   
    def gb_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_gb_c_fix[s, y] == m.v_gb_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * m.v_gb_c_inv[s, y] * 0.02
        else:
            return m.v_gb_c_fix[s, y] == m.p_year_expansion_range[s, y] * m.v_gb_c_inv[s, y] * 0.02
    
    def gb_c_var(m, s, y, h):
        return m.v_gb_c_var[s, y, h] == m.p_year_expansion_range[s, y] * (m.v_gb_q_gas[s, y, h] * m.p_c_gas[s, y, h] + m.v_gb_q_gas[s, y, h] / m.p_gb_h_gas[s, y] * m.p_gb_co2_share[s, y] * m.p_c_co2[s, y])
    
    m.con_gb_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                rule = gb_feed_in_max_bound)
    
    m.con_gb_gas_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                       rule = gb_gas_heat)
            
    m.con_gb_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                    rule = gb_Q_inv)
    
    m.con_gb_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                    rule = gb_c_inv)
    
    m.con_gb_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                    rule = gb_c_fix)
    
    m.con_gb_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                    rule = gb_c_var)
    
    # m.con_gb_limit = py.Constraint(m.set_years,
    #                                rule = gb_limit)

def add_gb_variables(m=None):
    
    m.v_gb_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from gas boiler per scenario, year and hour')

    m.v_gb_q_gas = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                           domain = py.NonNegativeReals,
                           doc = 'gas consumption from gas boiler per scenario, year and hour')

    m.v_gb_Q_heat_max = py.Var(m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'max energy feed in from gas boiler per scenario, year and hour')
    
    m.v_gb_Q_inv = py.Var(m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'new installed power of gas boiler per scenario and year')
   
    m.v_gb_c_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of gb per scenario and year in USD')

    m.v_gb_c_fix = py.Var(m.set_scenarios, m.set_years,
                         domain = py.NonNegativeReals,
                         doc = 'fix costs of gb per scenario and year in USD')
    
    m.v_gb_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                          domain = py.Reals,
                          doc = 'var costs of gb per scenario, year and hour in USD')
    
def add_gb_parameters(m=None):

    def init_gb_eta(m, s, y):
        return m.data_values[s]['gb'][y]['p_gb_eta']
       
    def init_gb_h_gas(m, s, y):
        return m.data_values[s]['gb'][y]['p_gb_h_gas']
    
    def init_gb_co2_share(m, s, y):
        return m.data_values[s]['gb'][y]['p_gb_co2_share']
        
    def init_gb_c_inv(m, s, y):
        return m.data_values[s]['gb'][y]['p_gb_c_inv']
    
    m.p_gb_eta = py.Param(m.set_scenarios, m.set_years,
                           initialize = init_gb_eta,
                           within = py.NonNegativeReals,
                           doc = 'efficiency of the gb')
    
    m.p_gb_h_gas = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_gb_h_gas,
                             within = py.NonNegativeReals,
                             doc = 'calorific value of gas for gb')
    
    m.p_gb_co2_share = py.Param(m.set_scenarios, m.set_years,
                                initialize = init_gb_co2_share,
                                within = py.NonNegativeReals,
                                doc = 'share of CO2 of the gas for gb')
        
    m.p_gb_c_inv = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_gb_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv cost of gb')
    