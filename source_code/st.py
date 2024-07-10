import pyomo.environ as py

def add_st_equations(m=None):

    def st_feed_in_max_bound(m, y, t, s):
        return m.v_st_q_heat_in[y, t, s] <= m.v_st_Q_heat_max[y, s]
    
    # def test(m, y, s):
    #     return m.v_eb_Q_heat_max[y, s] <= 800
    
    def st_elec_heat(m, y, t, s): 
        return m.v_st_q_heat_in[y, t, s] == m.v_st_q_elec_in[y, t, s] * m.p_st_cop[y, s, t]
     
    def st_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_st_Q_diff[y, s] == (m.v_st_Q_heat_max[y, s] - m.v_st_Q_heat_max[y-5, s])
        else:
            return m.v_st_Q_diff[y, s] == m.v_st_Q_heat_max[y, s]
    
    def st_c_fix(m, y, s):
        return m.v_st_c_fix[y, s] == m.v_st_Q_diff[y, s] * m.p_st_c_inv[y, s] + m.p_st_c_fix[y, s] * m.v_st_Q_heat_max[y, s]        
    
    def st_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_st_c_var(y, t, s) == m.v_st_q_elec_in[y, t, s] * m.p_c_elec[y, t, s]


    m.con_st_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = st_feed_in_max_bound)
    
    m.con_st_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                       rule = st_elec_heat)
    
    m.con_st_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = st_Q_inv)
    
    m.con_st_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = st_c_fix)
    
    m.con_st_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = st_c_var)
     
def add_st_variables(m=None):
    
    m.v_st_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from solar thermal per scenario, year, and hour')
    
    m.v_st_q_elec_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'electricity input of solar thermal per scenario, year, and hour')
    
    m.v_st_Q_heat_max = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from solar thermal for district heating')
    
    m.v_st_Q_diff = py.Var(m.set_years, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'difference of capacity for investments')
    
    m.v_st_c_fix = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'Fix cost st per hear in EUR')
    
    m.v_st_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'var cost st per hear in EUR')   

def add_st_parameters(m=None):
    
    def init_st_cop(m, y, t, s):
        return m.data_values[s]['st'][y]['p_st_cop'][t]
    
    def init_st_c_inv(m, y, s):
        return m.data_values[s]['st'][y]['p_st_c_inv']
    
    def init_st_c_fix(m, y, s):
        return m.data_values[s]['st'][y]['p_st_c_fix']

    m.p_st_cop = py.Parameter(m.set_years, m.set_hours, m.set_scenarios,
                              initialize = init_st_cop,
                              within = py.NonNegativeReals,
                              doc = 'coefficient of performance of the st')

    m.p_st_c_inv =py.Parameter(m.set_years, m.set_scenarios,
                               initialize = init_st_c_inv,
                               within = py.NonNegativeReals,
                               doc = 'specific inv cost of st')
    
    m.p_st_c_fix = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_st_c_fix,
                            within = py.NonNegativeReals,
                            doc = 'fixed cost of st')
    
    # m.p_c_opam( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )