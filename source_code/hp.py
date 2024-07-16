import pyomo.environ as py

def add_hp_equations(m=None):

    def hp_feed_in_max_bound(m, y, t, s):
        return m.v_hp_q_heat_in[y, t, s] <= m.v_hp_Q_heat_max[y, s]
    
    # def test(m, y, s):
    #     return m.v_hp_Q_heat_max[y, s] <= 800
    
    def hp_elec_heat(m, y, t, s): 
        return m.v_hp_q_heat_in[y, t, s] == m.v_hp_q_elec_in[y, t, s] * m.p_hp_cop[y, t, s]
     
    def hp_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_hp_Q_inv[y, s] == (m.v_hp_Q_heat_max[y, s] - m.v_hp_Q_heat_max[y-5, s])
        else:
            return m.v_hp_Q_inv[y, s] == m.v_hp_Q_heat_max[y, s]
    
    def hp_c_inv(m, y, s):
        return m.v_hp_c_inv[y, s] == m.v_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]
  
    def hp_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_hp_c_fix[y, s] == m.v_hp_c_fix[y-5, s] + m.v_hp_Q_inv[y, s] * m.p_hp_c_fix[y, s]
        else:
            return m.v_hp_c_fix[y, s] == m.v_hp_Q_inv[y, s] * m.p_hp_c_fix[y, s]

    def hp_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_hp_c_var[y, t, s] == m.v_hp_q_elec_in[y, t, s] * m.p_c_elec[y, t, s]

    m.con_hp_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = hp_feed_in_max_bound)
    
    m.con_hp_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                       rule = hp_elec_heat)
    
    m.con_hp_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = hp_Q_inv)
    
    m.con_hp_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = hp_c_inv)
    
    m.con_hp_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = hp_c_fix)
    
    m.con_hp_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = hp_c_var)
    
    # m.con_test = py.Constraint(m.set_years, m.set_scenarios,
    #                            rule = test)

def add_hp_variables(m=None):
    
    m.v_hp_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from large-scale heat pump per scenario, year, and hour')
    
    m.v_hp_q_elec_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'electricity input of large-scale heat pump per scenario, year, and hour')
    
    m.v_hp_Q_heat_max = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from large-scale heat pump for district heating')
    
    m.v_hp_Q_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'istalled hp capacity per scenario and year in EUR')

    m.v_hp_c_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of hp per scenario and year in EUR')
    
    m.v_hp_c_fix = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'fix costs of hp per scenario and year in EUR')
    
    m.v_hp_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'var costs of hp per scenario, year and hour in EUR')

def add_hp_parameters(m=None):
    
    def init_hp_cop(m, y, t, s):
        return m.data_values[s]['hp'][y]['p_hp_cop'][t]
    
    def init_hp_c_inv(m, y, s):
        return m.data_values[s]['hp'][y]['p_hp_c_inv']
    
    def init_hp_c_fix(m, y, s):
        return m.data_values[s]['hp'][y]['p_hp_c_fix']

    m.p_hp_cop = py.Param(m.set_years, m.set_hours, m.set_scenarios,
                          initialize = init_hp_cop,
                          within = py.NonNegativeReals,
                          doc = 'coefficient of performance of the large-scale heat pump')

    m.p_hp_c_inv =py.Param(m.set_years, m.set_scenarios,
                           initialize = init_hp_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of heatpumps')
    
    m.p_hp_c_fix = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_hp_c_fix,
                            within = py.NonNegativeReals,
                            doc = 'fixed cost of hp')
    
    # m.p_c_opam( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )