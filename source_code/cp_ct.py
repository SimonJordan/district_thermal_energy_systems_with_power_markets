import pyomo.environ as py

def add_cp_ct_equations(m=None):

    def cp_ct_feed_in_max_bound(m, s, y, t):
        return m.v_cp_ct_q_cool_in[s, y, t] <= m.v_cp_ct_Q_cool_max[s, y]
    
    # def cp_ct_limit(m, s, y):
    #     return m.v_cp_ct_Q_cool_max[s, y] <= 0
    
    def cp_ct_elec_cool(m, s, y, t):
        return m.v_cp_ct_q_elec_consumption[s, y, t] == m.v_cp_ct_q_cool_in[s, y, t]  / m.p_cp_ct_seer[s, y] + m.v_cp_ct_q_cool_in[s, y, t] * 0.05
    
    def cp_ct_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_cp_ct_Q_inv[s, y] == m.v_cp_ct_Q_cool_max[s, y] - m.v_cp_ct_Q_cool_max[s, y-5]
        else:
            return m.v_cp_ct_Q_inv[s, y] == m.v_cp_ct_Q_cool_max[s, y]
    
    def cp_ct_c_inv(m, s, y):
        return m.v_cp_ct_c_inv[s, y] == m.v_cp_ct_Q_inv[s, y] * (m.p_cp_c_inv[s, y] + m.p_ct_cp_c_inv[s, y])
  
    def cp_ct_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_cp_ct_c_fix[s, y] == m.v_cp_ct_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * m.v_cp_ct_c_inv[s, y] * 0.02
        else:
            return m.v_cp_ct_c_fix[s, y] == m.p_year_expansion_range[s, y] * m.v_cp_ct_c_inv[s, y] * 0.02

    def cp_ct_c_var(m, s, y, t):
        return m.v_cp_ct_c_var[s, y, t] == m.p_year_expansion_range[s, y] * (m.v_cp_ct_q_elec_consumption[s, y, t] * (m.p_c_elec[s, y, t] + m.p_elec_co2_share[s, y, t] * m.p_c_co2[s, y]))

    m.con_cp_ct_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                  rule = cp_ct_feed_in_max_bound)
    
    m.con_cp_ct_elec_cool = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                          rule = cp_ct_elec_cool)
    
    m.con_cp_ct_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = cp_ct_Q_inv)
    
    m.con_cp_ct_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = cp_ct_c_inv)
    
    m.con_cp_ct_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = cp_ct_c_fix)
    
    m.con_cp_ct_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                      rule = cp_ct_c_var)
    
    # m.con_cp_ct_limit = py.Constraint(m.set_scenarios, m.set_years,
    #                                   rule = cp_ct_limit)

def add_cp_ct_variables(m=None):
    
    m.v_cp_ct_q_cool_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                 domain = py.NonNegativeReals,
                                 doc = 'cool energy feed in from large-scale compressor with cooling tower per scenario, year, and hour')
    
    m.v_cp_ct_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                          domain = py.NonNegativeReals,
                                          doc = 'electricity input of large-scale compressor with cooling tower per scenario, year, and hour')
    
    m.v_cp_ct_Q_cool_max = py.Var(m.set_scenarios, m.set_years,
                                  domain = py.NonNegativeReals,
                                  doc = 'max cool feed in from large-scale compressor with cooling tower for district cooling')
    
    m.v_cp_ct_Q_inv = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'new istalled cp_ct capacity per scenario and year')

    m.v_cp_ct_c_inv = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'inv costs of cp_ct per scenario and year in USD')
    
    m.v_cp_ct_c_fix = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'fix costs of cp_ct per scenario and year in USD')
    
    m.v_cp_ct_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                             domain = py.Reals,
                             doc = 'var costs of cp_ct per scenario, year and hour in USD')

def add_cp_ct_parameters(m=None):
    
    def init_cp_ct_seer(m, s, y):
        return m.data_values[s]['cp'][y]['p_cp_ct_seer']
    
    def init_cp_c_inv(m, s, y):
        return m.data_values[s]['cp'][y]['p_cp_c_inv']
    
    def init_ct_cp_c_inv(m, s, y):
        return m.data_values[s]['cp'][y]['p_ct_cp_c_inv']

    m.p_cp_ct_seer = py.Param(m.set_scenarios, m.set_years,
                           initialize = init_cp_ct_seer,
                           within = py.NonNegativeReals,
                           doc = 'seasonal energy efficiency ratio of the large-scale compressor with cooling tower')

    m.p_cp_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_cp_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of the large-scale compressor')
    
    m.p_ct_cp_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_ct_cp_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of the large-scale cooling tower')
    