import pyomo.environ as py

def add_ieh_equations(m=None):

    def ieh_feed_in_max_bound(m, s, y, t):
        return m.v_ieh_q_heat_in[s, y, t] <= m.v_ieh_Q_heat_max[s, y]
    
    def ieh_limit(m, s, y, t):
        return m.v_ieh_q_heat_in[s, y, t] <= m.p_ieh_in[s, y, t]
    
    def ieh_elec_heat(m, s, y, t): 
        return m.v_ieh_q_elec_consumption[s, y, t] == m.v_ieh_q_heat_in[s, y, t] * m.p_ieh_elec[s, y]
     
    def ieh_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ieh_Q_inv[s, y] == m.v_ieh_Q_heat_max[s, y] - m.v_ieh_Q_heat_max[s, y-5]
        else:
            return m.v_ieh_Q_inv[s, y] == m.v_ieh_Q_heat_max[s, y]
        
    def ieh_c_inv(m, s, y):
        return m.v_ieh_c_inv[s, y] == m.v_ieh_Q_inv[s, y] * m.p_ieh_c_inv[s, y]
   
    def ieh_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ieh_c_fix[s, y] == m.v_ieh_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * m.v_ieh_c_inv[s, y] * 0.02
        else:
            return m.v_ieh_c_fix[s, y] == m.p_year_expansion_range[s, y] * m.v_ieh_c_inv[s, y] * 0.02
    
    def ieh_c_var(m, s, y, t):
        return m.v_ieh_c_var[s, y, t] == m.p_year_expansion_range[s, y] * (m.v_ieh_q_elec_consumption[s, y, t] * (m.p_c_elec[s, y, t] + m.p_elec_co2_share[s, y, t] * m.p_c_co2[s, y]) + m.v_ieh_q_heat_in[s, y, t] * m.p_ieh_c_in[s, y])
    
    m.con_ieh_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                 rule = ieh_feed_in_max_bound)
    
    m.con_ieh_limit = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                     rule = ieh_limit)
    
    m.con_ieh_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                        rule = ieh_elec_heat)
    
    m.con_ieh_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ieh_Q_inv)   
        
    m.con_ieh_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = ieh_c_inv)
    
    m.con_ieh_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = ieh_c_fix)
    
    m.con_ieh_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = ieh_c_var)
    
def add_ieh_variables(m=None):
    
    m.v_ieh_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                               domain = py.NonNegativeReals,
                               doc = 'heat energy feed in from industrial excess heat per scenario, year and hour')
    
    m.v_ieh_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                        domain = py.NonNegativeReals,
                                        doc = 'electricity input of industrial excess heat per scenario, year and hour')
    
    m.v_ieh_Q_heat_max = py.Var(m.set_scenarios, m.set_years,
                                domain = py.NonNegativeReals,
                                doc = 'max heat feed in from industrial excess heat for district heating')
    
    m.v_ieh_Q_inv = py.Var(m.set_scenarios, m.set_years,
                           domain = py.NonNegativeReals,
                           doc = 'installed power of industrial excess heat per scenario and year')
    
    m.v_ieh_c_inv = py.Var(m.set_scenarios, m.set_years,
                           domain = py.NonNegativeReals,
                           doc = 'inv costs of ieh per scenario and year in USD')

    m.v_ieh_c_fix = py.Var(m.set_scenarios, m.set_years,
                           domain = py.NonNegativeReals,
                           doc = 'fix costs of ieh per scenario and year in USD')
    
    m.v_ieh_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                           domain = py.Reals,
                           doc = 'var costs of ieh per scenario, year and hour in USD')

def add_ieh_parameters(m=None):
    
    def init_ieh_c_inv(m, s, y):
        return m.data_values[s]['ieh'][y]['p_ieh_c_inv']
    
    def init_ieh_c_in(m, s, y):
        return m.data_values[s]['ieh'][y]['p_ieh_c_in']
    
    def init_ieh_elec(m, s, y):
        return m.data_values[s]['ieh'][y]['p_ieh_elec']
    
    def init_ieh_in(m, s, y, t):
        return m.data_values[s]['ieh'][y]['p_ieh_in'][t]
    
    
    m.p_ieh_c_inv =py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ieh_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv costs of ieh')
    
    m.p_ieh_c_in =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_ieh_c_in,
                           within = py.NonNegativeReals,
                           doc = 'heat costs of ieh')
    
    m.p_ieh_elec =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_ieh_elec,
                           within = py.NonNegativeReals,
                           doc = 'electricity share of ieh')
    
    m.p_ieh_in = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                          initialize = init_ieh_in,
                          within = py.NonNegativeReals,
                          doc = 'feed in from ieh')
    