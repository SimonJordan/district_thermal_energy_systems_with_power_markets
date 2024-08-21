import pyomo.environ as py

def add_dgt_equations(m=None):

    def dgt_feed_in_max_bound(m, s, y, t):
        return m.v_dgt_q_heat_in[s, y, t] <= m.v_dgt_Q_heat_max[y]
    
    def dgt_limit(m, s, y):
        return m.v_dgt_Q_heat_max[y] <= 0
     
    def dgt_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_dgt_Q_inv[y] == (m.v_dgt_Q_heat_max[y] - m.v_dgt_Q_heat_max[y-5])
        else:
            return m.v_dgt_Q_inv[y] == m.v_dgt_Q_heat_max[y]
    
    def dgt_c_inv(m, s, y):
        return m.v_dgt_c_inv[s, y] == m.p_scenario_weighting[s] * (m.v_dgt_Q_inv[y] * m.p_dgt_c_inv[s, y])
  
    def dgt_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_dgt_c_fix[s, y] == m.v_dgt_c_fix[s, y-5] + m.p_scenario_weighting[s] * m.p_year_expansion_range[s, y] * (m.v_dgt_Q_inv[y] * m.p_dgt_c_inv[s, y] * 0.02)
        else:
            return m.v_dgt_c_fix[s, y] == m.p_scenario_weighting[s] * m.p_year_expansion_range[s, y] * (m.v_dgt_Q_inv[y] * m.p_dgt_c_inv[s, y] * 0.02)
    def dgt_c_var(m, s, y, t):
        return m.v_dgt_c_var[s, y, t] == m.p_scenario_weighting[s] * m.p_year_expansion_range[s, y] * (m.v_dgt_q_heat_in[s, y, t] * 0.1 * (m.p_c_elec[s, y, t] + m.p_elec_co2_share[s, y, t] * m.p_c_co2[s, y]))

    m.con_dgt_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                rule = dgt_feed_in_max_bound)
    
    m.con_dgt_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                    rule = dgt_Q_inv)
    
    m.con_dgt_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                    rule = dgt_c_inv)
    
    m.con_dgt_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                    rule = dgt_c_fix)
    
    m.con_dgt_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                    rule = dgt_c_var)
    
    m.con_dgt_limit = py.Constraint(m.set_scenarios, m.set_years,
                                    rule = dgt_limit)

def add_dgt_variables(m=None):
    
    m.v_dgt_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                               domain = py.NonNegativeReals,
                               doc = 'heat energy feed in from large-scale deep geothermal per scenario, year, and hour')
    
    m.v_dgt_Q_heat_max = py.Var(m.set_years,
                                domain = py.NonNegativeReals,
                                doc = 'max heat feed in from large-scale deep geothermal for district heating')
    
    m.v_dgt_Q_inv = py.Var(m.set_years,
                           domain = py.NonNegativeReals,
                           doc = 'new istalled dgt capacity per scenario and year')

    m.v_dgt_c_inv = py.Var(m.set_scenarios, m.set_years,
                           domain = py.NonNegativeReals,
                           doc = 'inv costs of dgt per scenario and year in USD')
    
    m.v_dgt_c_fix = py.Var(m.set_scenarios, m.set_years,
                           domain = py.NonNegativeReals,
                           doc = 'fix costs of dgt per scenario and year in USD')
    
    m.v_dgt_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                           domain = py.Reals,
                           doc = 'var costs of dgt per scenario, year and hour in USD')

def add_dgt_parameters(m=None):
       
    def init_dgt_c_inv(m, s, y):
        return m.data_values[s]['dgt'][y]['p_dgt_c_inv']
    
    # def init_dgt_c_fix(m, s, y):
    #     return m.data_values[s]['dgt'][y]['p_dgt_c_fix']

    m.p_dgt_c_inv =py.Param(m.set_scenarios, m.set_years,
                            initialize = init_dgt_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv cost of deep geothermal')
    
    # m.p_dgt_c_fix = py.Param(m.set_scenarios, m.set_years,
    #                          initialize = init_dgt_c_fix,
    #                          within = py.NonNegativeReals,
    #                          doc = 'fixed cost of dgt')
