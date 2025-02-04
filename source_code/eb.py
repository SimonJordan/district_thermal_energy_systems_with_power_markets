import pyomo.environ as py

def add_eb_equations(m=None):
    """This section defines the equations of the electric boiler"""
    def eb_feed_in_max_bound(m, s, y, h):
        return m.v_eb_q_heat_in[s, y, h] <= m.v_eb_Q_heat_max[s, y]
    
    # def eb_limit(m, s, y):
    #     return m.v_eb_Q_heat_max[s, y] <= 0
    
    def eb_elec_heat(m, s, y, h):
        return m.v_eb_q_heat_in[s, y, h] == m.v_eb_q_elec_consumption[s, y, h] * m.p_eb_eta[s, y]
    
    def eb_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_eb_Q_inv[s, y] == m.v_eb_Q_heat_max[s, y] - m.v_eb_Q_heat_max[s, y-5]
        else:
            return m.v_eb_Q_inv[s, y] == m.v_eb_Q_heat_max[s, y]
    
    def eb_c_inv(m, s, y):
        return m.v_eb_c_inv[s, y] == m.v_eb_Q_inv[s, y] * m.p_eb_c_inv[s, y]
    
    def eb_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_eb_c_fix[s, y] == m.v_eb_c_fix[s, y-5] +  m.p_year_expansion_range[s, y] * m.v_eb_c_inv[s, y] * 0.02
        else:
            return m.v_eb_c_fix[s, y] == m.p_year_expansion_range[s, y] * m.v_eb_c_inv[s, y] * 0.02
    
    def eb_c_var(m, s, y, h):
        return m.v_eb_c_var[s, y, h] == m.p_year_expansion_range[s, y] * (m.v_eb_q_elec_consumption[s, y, h] * (m.p_c_elec[s, y, h] + m.p_elec_co2_share[s, y, h] * m.p_c_co2[s, y]))
        
    m.con_eb_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                               rule = eb_feed_in_max_bound)
    
    m.con_eb_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                       rule = eb_elec_heat)
    
    m.con_eb_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = eb_Q_inv)
    
    m.con_eb_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = eb_c_inv)
    
    m.con_eb_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = eb_c_fix)
    
    m.con_eb_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = eb_c_var)
    
    # m.con_eb_limit = py.Constraint(m.set_scenarios, m.set_years,
    #                                rule = eb_limit)

def add_eb_variables(m=None):
    """This section defines the variables of the electric boiler"""
    m.v_eb_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from electric boiler per scenario, year, and hour')
    
    m.v_eb_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                       domain = py.NonNegativeReals,
                                       doc = 'electricity input of electric boiler per scenario, year, and hour')
    
    m.v_eb_Q_heat_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from electric boiler for district heating')
    
    m.v_eb_Q_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'new istalled eb capacity per scenario and year')
   
    m.v_eb_c_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of eb per scenario and year in USD')
    
    m.v_eb_c_fix = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'fix costs of eb per scenario and year in USD')
    
    m.v_eb_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                          domain = py.Reals,
                          doc = 'var costs of eb per scenario, year and hour in USD')

def add_eb_parameters(m=None):
    """This section defines the parameters of the electric boiler"""
    def init_eb_eta(m, s, y):
        return m.data_values[s]['eb'][y]['p_eb_eta']
    
    def init_eb_c_inv(m, s, y):
        return m.data_values[s]['eb'][y]['p_eb_c_inv']
    
    m.p_eb_eta = py.Param(m.set_scenarios, m.set_years,
                          initialize = init_eb_eta,
                          within = py.NonNegativeReals,
                          doc = 'electrical efficiency of the eb')
    
    m.p_eb_c_inv = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_eb_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv cost of eb')
