import pyomo.environ as py

def add_dgt_equations(m=None):

    def dgt_feed_in_max_bound(m, y, t, s):
        return m.v_dgt_q_heat_in[y, t, s] <= m.v_dgt_Q_heat_max[y, s]
    
    # def dgt_limit(m, y, s):
    #     return m.v_dgt_Q_heat_max[y, s] <= 50
     
    def dgt_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_dgt_Q_inv[y, s] == (m.v_dgt_Q_heat_max[y, s] - m.v_dgt_Q_heat_max[y-5, s])
        else:
            return m.v_dgt_Q_inv[y, s] == m.v_dgt_Q_heat_max[y, s]
    
    def dgt_c_inv(m, y, s):
        return m.v_dgt_c_inv[y, s] == m.v_dgt_Q_inv[y, s] * m.p_dgt_c_inv[y, s]
  
    def dgt_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_dgt_c_fix[y, s] == m.v_dgt_c_fix[y-5, s] + m.v_dgt_Q_inv[y, s] * m.p_dgt_c_inv[y, s] * 0.02
        else:
            return m.v_dgt_c_fix[y, s] == m.v_dgt_Q_inv[y, s] * m.p_dgt_c_inv[y, s] * 0.02

    def dgt_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_dgt_c_var[y, t, s] == m.v_dgt_q_heat_in[y, t, s] * 0.1 * m.p_c_elec[y, t, s]

    m.con_dgt_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                rule = dgt_feed_in_max_bound)
    
    m.con_dgt_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                    rule = dgt_Q_inv)
    
    m.con_dgt_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                    rule = dgt_c_inv)
    
    m.con_dgt_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                    rule = dgt_c_fix)
    
    m.con_dgt_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                    rule = dgt_c_var)
    
    # m.con_dgt_limit = py.Constraint(m.set_years, m.set_scenarios,
    #                                 rule = dgt_limit)

def add_dgt_variables(m=None):
    
    m.v_dgt_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'heat energy feed in from large-scale deep geothermal per scenario, year, and hour')
    
    m.v_dgt_Q_heat_max = py.Var(m.set_years, m.set_scenarios,
                                domain = py.NonNegativeReals,
                                doc = 'max heat feed in from large-scale deep geothermal for district heating')
    
    m.v_dgt_Q_inv = py.Var(m.set_years, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'new istalled dgt capacity per scenario and year in EUR')

    m.v_dgt_c_inv = py.Var(m.set_years, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'inv costs of dgt per scenario and year in EUR')
    
    m.v_dgt_c_fix = py.Var(m.set_years, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'fix costs of dgt per scenario and year in EUR')
    
    m.v_dgt_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'var costs of dgt per scenario, year and hour in EUR')

def add_dgt_parameters(m=None):
       
    def init_dgt_c_inv(m, y, s):
        return m.data_values[s]['dgt'][y]['p_dgt_c_inv']
    
    # def init_dgt_c_fix(m, y, s):
    #     return m.data_values[s]['dgt'][y]['p_dgt_c_fix']

    m.p_dgt_c_inv =py.Param(m.set_years, m.set_scenarios,
                            initialize = init_dgt_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv cost of deep geothermal')
    
    # m.p_dgt_c_fix = py.Param(m.set_years, m.set_scenarios,
    #                          initialize = init_dgt_c_fix,
    #                          within = py.NonNegativeReals,
    #                          doc = 'fixed cost of dgt')
    
    # m.p_c_opam( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )