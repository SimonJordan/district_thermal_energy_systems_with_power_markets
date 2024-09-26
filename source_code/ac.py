import pyomo.environ as py

def add_ac_equations(m=None):

    def ac_feed_in_max_bound(m, s, y, t):
        return m.v_ac_q_cool_in[s, y, t] <= m.v_ac_Q_cool_max[s, y]
    
    # def ac_limit(m, s, y):
    #     return m.v_ac_Q_cool_max[s, y] <= 0
    
    def ac_elec_cool(m, s, y, t):
        return m.v_ac_q_cool_in[s, y, t] == m.v_ac_q_elec_consumption[s, y, t] * m.p_ac_eer[s, y, t]
     
    def ac_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ac_Q_inv[s, y] == (m.v_ac_Q_cool_max[s, y] - m.v_ac_Q_cool_max[s, y-5])
        else:
            return m.v_ac_Q_inv[s, y] == m.v_ac_Q_cool_max[s, y]
    
    def ac_c_inv(m, s, y):
        return m.v_ac_c_inv[s, y] == m.v_ac_Q_inv[s, y] * m.p_ac_c_inv[s, y]
  
    def ac_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ac_c_fix[s, y] == m.v_ac_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * (m.v_ac_Q_inv[s, y] * m.p_ac_c_inv[s, y] * 0.02)
        else:
            return m.v_ac_c_fix[s, y] == m.p_year_expansion_range[s, y] * (m.v_ac_Q_inv[s, y] * m.p_ac_c_inv[s, y] * 0.02)

    def ac_c_var(m, s, y, t):
        return m.v_ac_c_var[s, y, t] == m.p_year_expansion_range[s, y] * (m.v_ac_q_elec_consumption[s, y, t] * (m.p_c_elec[s, y, t] + m.p_elec_co2_share[s, y, t] * m.p_c_co2[s, y]))

    m.con_ac_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                               rule = ac_feed_in_max_bound)
    
    m.con_ac_elec_cool = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                       rule = ac_elec_cool)
    
    m.con_ac_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = ac_Q_inv)
    
    m.con_ac_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = ac_c_inv)
    
    m.con_ac_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = ac_c_fix)
    
    m.con_ac_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = ac_c_var)
    
    # m.con_ac_limit = py.Constraint(m.set_scenarios, m.set_years,
    #                                 rule = ac_limit)

def add_ac_variables(m=None):
    
    m.v_ac_q_cool_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                              domain = py.NonNegativeReals,
                              doc = 'cool energy feed in from large-scale airchiller per scenario, year, and hour')
    
    m.v_ac_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                       domain = py.NonNegativeReals,
                                       doc = 'electricity input of large-scale airchiller per scenario, year, and hour')
    
    m.v_ac_Q_cool_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'max cool feed in from large-scale airchiller for district cooling')
    
    m.v_ac_Q_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'new istalled ac capacity per scenario and year')

    m.v_ac_c_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of ac per scenario and year in USD')
    
    m.v_ac_c_fix = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'fix costs of ac per scenario and year in USD')
    
    m.v_ac_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                          domain = py.Reals,
                          doc = 'var costs of ac per scenario, year and hour in USD')

def add_ac_parameters(m=None):
    
    def init_ac_seer(m, s, y, t):
        return m.data_values[s]['ac'][y]['p_ac_eer'][t]
    
    def init_ac_c_inv(m, s, y):
        return m.data_values[s]['ac'][y]['p_ac_c_inv']
    
    # def init_ac_c_fix(m, s, y):
    #     return m.data_values[s]['ac'][y]['p_ac_c_fix']

    m.p_ac_eer = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                          initialize = init_ac_seer,
                          within = py.NonNegativeReals,
                          doc = 'seasonal energy efficiency ratio of the large-scale airchiller')

    m.p_ac_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_ac_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of the large-scale airchiller')
    
    # m.p_ac_c_fix = py.Param(m.set_scenarios, m.set_years,
    #                         initialize = init_ac_c_fix,
    #                         within = py.NonNegativeReals,
    #                         doc = 'fixed cost of ac')
    