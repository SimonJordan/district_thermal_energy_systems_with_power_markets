import pyomo.environ as py

def add_gt_equations(m=None):

    def gt_feed_in_max_bound(m, y, t, s):
        return m.v_gt_q_heat_in[y, t, s] <= m.v_gt_Q_heat_max[y, s]
    
    # def gt_limit(m, y, s):
    #     return m.v_gt_Q_heat_max[y, s] <= 300
    
    def gt_elec_heat(m, y, t, s): 
        return m.v_gt_q_heat_in[y, t, s] == m.v_gt_q_elec_consumption[y, t, s] * m.p_gt_cop[y, s]
     
    def gt_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_gt_Q_inv[y, s] == (m.v_gt_Q_heat_max[y, s] - m.v_gt_Q_heat_max[y-5, s])
        else:
            return m.v_gt_Q_inv[y, s] == m.v_gt_Q_heat_max[y, s]
    
    def gt_c_inv(m, y, s):
        return m.v_gt_c_inv[y, s] == m.v_gt_Q_inv[y, s] * (m.p_gt_c_inv[y, s] + m.p_hp_c_inv[y, s])
  
    def gt_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_gt_c_fix[y, s] == m.v_gt_c_fix[y-5, s] + m.v_gt_Q_inv[y, s] * (m.p_gt_c_inv[y, s] + m.p_hp_c_inv[y, s]) * 0.02
        else:
            return m.v_gt_c_fix[y, s] == m.v_gt_Q_inv[y, s] * (m.p_gt_c_inv[y, s] + m.p_hp_c_inv[y, s]) * 0.02

    def gt_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_gt_c_var[y, t, s] == m.v_gt_q_elec_consumption[y, t, s] * m.p_c_elec[y, t, s]

    m.con_gt_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = gt_feed_in_max_bound)
    
    m.con_gt_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                       rule = gt_elec_heat)
    
    m.con_gt_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = gt_Q_inv)
    
    m.con_gt_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = gt_c_inv)
    
    m.con_gt_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = gt_c_fix)
    
    m.con_gt_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = gt_c_var)
    
    # m.con_gt_limit = py.Constraint(m.set_years, m.set_scenarios,
    #                                rule = gt_limit)

def add_gt_variables(m=None):
    
    m.v_gt_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from large-scale geothermal per scenario, year, and hour')
    
    m.v_gt_q_elec_consumption = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                       domain = py.NonNegativeReals,
                                       doc = 'electricity input of large-scale geothermal per scenario, year, and hour')
    
    m.v_gt_Q_heat_max = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from large-scale geothermal for district heating')
    
    m.v_gt_Q_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'new istalled gt capacity per scenario and year in EUR')

    m.v_gt_c_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of gt per scenario and year in EUR')
    
    m.v_gt_c_fix = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'fix costs of gt per scenario and year in EUR')
    
    m.v_gt_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'var costs of gt per scenario, year and hour in EUR')

def add_gt_parameters(m=None):
       
    def init_gt_c_inv(m, y, s):
        return m.data_values[s]['gt'][y]['p_gt_c_inv']
    
    def init_gt_cop(m, y, s):
        return m.data_values[s]['gt'][y]['p_gt_cop']
    
    # def init_gt_c_fix(m, y, s):
    #     return m.data_values[s]['gt'][y]['p_gt_c_fix']

    m.p_gt_c_inv =py.Param(m.set_years, m.set_scenarios,
                           initialize = init_gt_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of geothermal')
    
    m.p_gt_cop = py.Param(m.set_years, m.set_scenarios,
                          initialize = init_gt_cop,
                          within = py.NonNegativeReals,
                          doc = 'coefficient of performance of the hp for the gt')
    
    # m.p_gt_c_fix = py.Param(m.set_years, m.set_scenarios,
    #                         initialize = init_gt_c_fix,
    #                         within = py.NonNegativeReals,
    #                         doc = 'fixed cost of gt')
    
    # m.p_c_opam( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )