import pyomo.environ as py

def add_hp_equations(m=None):

    def hp_feed_in_max_bound(m, s, y, h):
        return m.v_hp_q_heat_in[s, y, h] <= m.v_hp_Q_heat_max[y]
    
    # def hp_limit(m, y):
    #     return m.v_hp_Q_heat_max[y] <= 0
    
    def hp_elec_heat(m, s, y, h): 
        return m.v_hp_q_heat_in[s, y, h] == m.v_hp_q_elec_consumption[s, y, h] * m.p_hp_cop[s, y, h]
     
    def hp_Q_inv(m, y):
        if (y - 5) in m.set_years:
            return m.v_hp_Q_inv[y] == m.v_hp_Q_heat_max[y] - m.v_hp_Q_heat_max[y-5]
        else:
            return m.v_hp_Q_inv[y] == m.v_hp_Q_heat_max[y]
    
    def hp_c_inv(m, s, y):
        return m.v_hp_c_inv[s, y] == m.v_hp_Q_inv[y] * m.p_hp_c_inv[s, y]
  
    def hp_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_hp_c_fix[s, y] == m.v_hp_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * m.v_hp_c_inv[s, y] * 0.02
        else:
            return m.v_hp_c_fix[s, y] == m.p_year_expansion_range[s, y] * m.v_hp_c_inv[s, y] * 0.02
            
    def hp_c_var(m, s, y, h):
        return m.v_hp_c_var[s, y, h] == m.p_year_expansion_range[s, y] * (m.v_hp_q_elec_consumption[s, y, h] * m.p_c_elec[s, y, h])

    m.con_hp_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                               rule = hp_feed_in_max_bound)
    
    m.con_hp_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                       rule = hp_elec_heat)
    
    m.con_hp_Q_inv = py.Constraint(m.set_years,
                                   rule = hp_Q_inv)
    
    m.con_hp_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = hp_c_inv)
    
    m.con_hp_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = hp_c_fix)
    
    m.con_hp_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = hp_c_var)
    
    # m.con_hp_limit = py.Constraint(m.set_years,
    #                                rule = hp_limit)

def add_hp_variables(m=None):
    
    m.v_hp_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from large-scale heat pump per scenario, year, and hour')
    
    m.v_hp_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                       domain = py.NonNegativeReals,
                                       doc = 'electricity input of large-scale heat pump per scenario, year, and hour')
    
    m.v_hp_Q_heat_max = py.Var(m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from large-scale heat pump for district heating')
    
    m.v_hp_Q_inv = py.Var(m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'new istalled hp capacity per scenario and year')

    m.v_hp_c_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of hp per scenario and year in USD')
    
    m.v_hp_c_fix = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'fix costs of hp per scenario and year in USD')
    
    m.v_hp_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                          domain = py.Reals,
                          doc = 'var costs of hp per scenario, year and hour in USD')

def add_hp_parameters(m=None):
    
    def init_hp_cop(m, s, y, h):
        return m.data_values[s]['hp'][y]['p_hp_cop'][h]
    
    def init_hp_c_inv(m, s, y):
        return m.data_values[s]['hp'][y]['p_hp_c_inv']

    m.p_hp_cop = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                          initialize = init_hp_cop,
                          within = py.NonNegativeReals,
                          doc = 'coefficient of performance of the large-scale heat pump')

    m.p_hp_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_hp_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of the large-scale heat pump')
