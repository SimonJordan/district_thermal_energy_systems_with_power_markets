import pyomo.environ as py

def add_ieh_equations(m=None):

    def ieh_feed_in_max_bound(m, y, t, s):
        return m.v_ieh_q_heat_in[y, t, s] <= m.v_ieh_Q_heat_max[y, s]
    
    def ieh_limit(m, y, t, s):
        return m.v_ieh_q_heat_in[y, t, s] <= m.p_ieh_in[y, t, s]
    
    def ieh_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ieh_Q_inv[y, s] == (m.v_ieh_Q_heat_max[y, s] - m.v_ieh_Q_heat_max[y-5, s])
        else:
            return m.v_ieh_Q_inv[y, s] == m.v_ieh_Q_heat_max[y, s]
        
    def ieh_c_inv(m, y, s):
        return m.v_ieh_c_inv[y, s] == m.v_ieh_Q_inv[y, s] * m.p_ieh_c_inv[y, s]
   
    def ieh_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ieh_c_fix[y, s] == m.v_ieh_c_fix[y-5, s] + m.v_ieh_Q_inv[y, s] * m.p_ieh_c_inv[y, s] * 0.02
        else:
            return m.v_ieh_c_fix[y, s] == m.v_ieh_Q_inv[y, s] * m.p_ieh_c_inv[y, s] * 0.02
    
    def ieh_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_ieh_c_var[y, t, s] == m.v_ieh_q_heat_in[y, t, s] * m.p_ieh_elec[y, s] * m.p_c_elec[y, t, s] + m.v_ieh_q_heat_in[y, t, s] * m.p_ieh_c_in[y, s]
    
    m.con_ieh_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                 rule = ieh_feed_in_max_bound)
    
    m.con_ieh_limit = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                     rule = ieh_limit)
    
    m.con_ieh_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                     rule = ieh_Q_inv)   
        
    m.con_ieh_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = ieh_c_inv)
    
    m.con_ieh_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = ieh_c_fix)
    
    m.con_ieh_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = ieh_c_var)
    
def add_ieh_variables(m=None):
    
    m.v_ieh_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'heat energy feed in from industrial excess heat per scenario, year and hour')
    
    m.v_ieh_Q_heat_max = py.Var(m.set_years, m.set_scenarios,
                                domain = py.NonNegativeReals,
                                doc = 'max heat feed in from industrial excess heat for diiehrict heating')
    
    m.v_ieh_Q_inv = py.Var(m.set_years, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'installed power of industrial excess heat per scenario and year')
    
    m.v_ieh_c_inv = py.Var(m.set_years, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'inv costs of ieh per scenario and year in EUR')

    m.v_ieh_c_fix = py.Var(m.set_years, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'fix costs of ieh per scenario and year in EUR')
    
    m.v_ieh_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'var costs of ieh per scenario, year and hour in EUR')

def add_ieh_parameters(m=None):
    
    def init_ieh_c_inv(m, y, s):
        return m.data_values[s]['ieh'][y]['p_ieh_c_inv']
                
    # def init_ieh_c_fix(m, y, s):
    #     return m.data_values[s]['ieh'][y]['p_ieh_c_fix']
    
    def init_ieh_c_in(m, y, s):
        return m.data_values[s]['ieh'][y]['p_ieh_c_in']
    
    def init_ieh_elec(m, y, s):
        return m.data_values[s]['ieh'][y]['p_ieh_elec']
    
    def init_ieh_in(m, y, t, s):
        return m.data_values[s]['ieh'][y]['p_ieh_in'][t]
    
    
    m.p_ieh_c_inv =py.Param(m.set_years, m.set_scenarios,
                            initialize = init_ieh_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv costs of ieh')
    
    # m.p_ieh_c_fix = py.Param(m.set_years, m.set_scenarios,
    #                          initialize = init_ieh_c_fix,
    #                          within = py.NonNegativeReals,
    #                          doc = 'fixed coieh of ieh')
    
    m.p_ieh_c_in =py.Param(m.set_years, m.set_scenarios,
                           initialize = init_ieh_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'heat costs of ieh')
    
    m.p_ieh_elec =py.Param(m.set_years, m.set_scenarios,
                           initialize = init_ieh_elec,
                           within = py.NonNegativeReals,
                           doc = 'electricity share of ieh')
    
    m.p_ieh_in = py.Param(m.set_years, m.set_hours, m.set_scenarios,
                          initialize = init_ieh_in,
                          within = py.NonNegativeReals,
                          doc = 'feed in from ieh')
    
    # m.p_c_opam( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance coieh per year and scenario'
    #     )