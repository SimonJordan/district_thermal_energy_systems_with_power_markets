import pyomo.environ as py

def add_gt_equations(m=None):

    def gt_feed_in_max_bound(m, s, y, t):
        return m.v_gt_q_heat_in[s, y, t] <= m.v_gt_Q_heat_max[s, y]
    
    # def gt_limit(m, s, y):
    #     return m.v_gt_Q_heat_max[s, y] <= 300
    
    def gt_elec_heat(m, s, y, t): 
        return m.v_gt_q_heat_in[s, y, t] == m.v_gt_q_elec_consumption[s, y, t] * m.p_gt_cop[s, y]
     
    def gt_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_gt_Q_inv[s, y] == (m.v_gt_Q_heat_max[s, y] - m.v_gt_Q_heat_max[s, y-5])
        else:
            return m.v_gt_Q_inv[s, y] == m.v_gt_Q_heat_max[s, y]
    
    def gt_c_inv(m, s, y):
        return m.v_gt_c_inv[s, y] == m.v_gt_Q_inv[s, y] * (m.p_gt_c_inv[s, y] + m.p_hp_c_inv[s, y])
  
    def gt_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_gt_c_fix[s, y] == m.v_gt_c_fix[s, y-5] + m.v_gt_Q_inv[s, y] * (m.p_gt_c_inv[s, y] + m.p_hp_c_inv[s, y]) * 0.02
        else:
            return m.v_gt_c_fix[s, y] == m.v_gt_Q_inv[s, y] * (m.p_gt_c_inv[s, y] + m.p_hp_c_inv[s, y]) * 0.02

    def gt_c_var(m, s, y, t): # OPAM = operational and maintanance, förderung?
        return m.v_gt_c_var[s, y, t] == m.v_gt_q_elec_consumption[s, y, t] * m.p_c_elec[s, y, t]

    m.con_gt_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                               rule = gt_feed_in_max_bound)
    
    m.con_gt_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                       rule = gt_elec_heat)
    
    m.con_gt_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = gt_Q_inv)
    
    m.con_gt_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = gt_c_inv)
    
    m.con_gt_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = gt_c_fix)
    
    m.con_gt_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = gt_c_var)
    
    # m.con_gt_limit = py.Constraint(m.set_scenarios, m.set_years,
    #                                rule = gt_limit)

def add_gt_variables(m=None):
    
    m.v_gt_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from large-scale geothermal per scenario, year, and hour')
    
    m.v_gt_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                       domain = py.NonNegativeReals,
                                       doc = 'electricity input of large-scale geothermal per scenario, year, and hour')
    
    m.v_gt_Q_heat_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from large-scale geothermal for district heating')
    
    m.v_gt_Q_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'new istalled gt capacity per scenario and year in EUR')

    m.v_gt_c_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of gt per scenario and year in EUR')
    
    m.v_gt_c_fix = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'fix costs of gt per scenario and year in EUR')
    
    m.v_gt_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                          domain = py.Reals,
                          doc = 'var costs of gt per scenario, year and hour in EUR')

def add_gt_parameters(m=None):
       
    def init_gt_c_inv(m, s, y):
        return m.data_values[s]['gt'][y]['p_gt_c_inv']
    
    def init_gt_cop(m, s, y):
        return m.data_values[s]['gt'][y]['p_gt_cop']
    
    # def init_gt_c_fix(m, s, y):
    #     return m.data_values[s]['gt'][y]['p_gt_c_fix']

    m.p_gt_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_gt_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of geothermal')
    
    m.p_gt_cop = py.Param(m.set_scenarios, m.set_years,
                          initialize = init_gt_cop,
                          within = py.NonNegativeReals,
                          doc = 'coefficient of performance of the hp for the gt')
    
    # m.p_gt_c_fix = py.Param(m.set_scenarios, m.set_years,
    #                         initialize = init_gt_c_fix,
    #                         within = py.NonNegativeReals,
    #                         doc = 'fixed cost of gt')
