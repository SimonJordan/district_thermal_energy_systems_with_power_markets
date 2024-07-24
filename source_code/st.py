import pyomo.environ as py

def add_st_equations(m=None):

    def st_feed_in_max_bound(m, y, t, s):
        return m.v_st_q_heat_in[y, t, s] <= m.v_st_Q_heat_max[y, s]
    
    # def st_limit(m, y, s):
    #     return m.v_st_Q_heat_max[y, s] <= 200
    
    # def st_eta(m, y, s):
    #     if (y - 5) in m.set_years:
    #         return m.v_st_eta_avg[y, s] == (m.v_st_eta_avg[y-5, s] * m.v_st_P_max[y-5, s] + m.p_st_eta[y, s] * m.v_st_P_inv[y, s]) / (m.v_st_P_max[y-5, s] + m.v_st_P_inv[y, s])
    #     else:
    #         return m.v_st_eta_avg[y, s] == m.p_st_eta[y, s]
    
    def st_solar_radiation(m, y, t, s):
        return m.v_st_q_heat_in[y, t, s] == m.p_st_solar_radiation[y, t, s] * m.v_st_p[y, t, s] / 1000 * m.p_st_eta[y, s]
    
    def st_elec_heat(m, y, t, s):
        return m.v_st_q_heat_in[y, t, s] == m.v_st_q_elec_in[y, t, s] * m.p_st_cop[y, s]
     
    def st_p_max_bound(m, y, t, s):
        return m.v_st_p[y, t, s] <= m.v_st_P_max[y, s]
     
    def st_P_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_st_P_inv[y, s] == (m.v_st_P_max[y, s] - m.v_st_P_max[y-5, s])
        else:
            return m.v_st_P_inv[y, s] == m.v_st_P_max[y, s]
        
    def st_hp_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_st_hp_Q_inv[y, s] == (m.v_st_Q_heat_max[y, s] - m.v_st_Q_heat_max[y-5, s])
        else:
            return m.v_st_hp_Q_inv[y, s] == m.v_st_Q_heat_max[y, s]
       
    def st_c_inv(m, y, s):
        return m.v_st_c_inv[y, s] == m.v_st_P_inv[y, s] * m.p_st_c_inv[y, s] + m.v_st_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]
   
    def st_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_st_c_fix[y, s] == m.v_st_c_fix[y-5, s] + (m.v_st_P_inv[y, s] * m.p_st_c_inv[y, s] + m.v_st_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]) * 0.02
        else:
            return m.v_st_c_fix[y, s] == (m.v_st_P_inv[y, s] * m.p_st_c_inv[y, s] + m.v_st_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]) * 0.02
    
    def st_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_st_c_var[y, t, s] == m.v_st_q_elec_in[y, t, s] * m.p_c_elec[y, t, s]
    
    m.con_st_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = st_feed_in_max_bound)
    
    # m.con_st_eta = py.Constraint(m.set_years, m.set_scenarios,
    #                              rule = st_eta)
    
    m.con_st_solar_radiation = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                             rule = st_solar_radiation)
    
    m.con_st_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                       rule = st_elec_heat)
    
    m.con_st_p_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                         rule = st_p_max_bound)
    
    m.con_st_P_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = st_P_inv)
    
    m.con_st_hp_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                      rule = st_hp_Q_inv)
    
    m.con_st_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = st_c_inv)
    
    m.con_st_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = st_c_fix)
    
    m.con_st_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = st_c_var)
    
    # m.con_st_limit = py.Constraint(m.set_years, m.set_scenarios,
    #                                rule = st_limit)
    
     
def add_st_variables(m=None):
    
    m.v_st_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from solar thermal per scenario, year and hour')
    
    m.v_st_q_elec_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'electricity input of solar thermal per scenario, year and hour')
    
    # m.v_st_eta_avg = py.Var(m.set_years, m.set_scenarios,
    #                         domain = py.NonNegativeReals,
    #                         doc = 'average eta of solar thermal per scenario and year')
    
    m.v_st_p = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                      domain = py.NonNegativeReals,
                      doc = 'power of solar thermal per scenario, year and hour')
    
    m.v_st_P_max = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'installed power of solar thermal per scenario and year')
    
    m.v_st_P_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'new installed power of solar thermal per scenario and year')
   
    m.v_st_hp_Q_inv = py.Var(m.set_years, m.set_scenarios,
                             domain = py.NonNegativeReals,
                             doc = 'new installed capacity of hp for st per scenario and year in EUR')
    
    m.v_st_Q_heat_max = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from solar thermal for district heating')
    
    m.v_st_c_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of st per scenario and year in EUR')

    m.v_st_c_fix = py.Var(m.set_years, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'fix costs of st per scenario and year in EUR')
    
    m.v_st_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'var costs of st per scenario, year and hour in EUR')

def add_st_parameters(m=None):
    
    def init_st_eta(m, y, s):
        return m.data_values[s]['st'][y]['p_st_eta']
    
    def init_st_c_inv(m, y, s):
        return m.data_values[s]['st'][y]['p_st_c_inv']
            
    # def init_st_c_fix(m, y, s):
    #     return m.data_values[s]['st'][y]['p_st_c_fix']
    
    def init_st_cop(m, y, s):
        return m.data_values[s]['st'][y]['p_st_cop']

    def init_solar_radiation(m, y, t, s):
        return m.data_values[s]['st'][y]['p_st_solar_radiation'][t]
    
    m.p_st_eta = py.Param(m.set_years, m.set_scenarios,
                          initialize = init_st_eta,
                          within = py.NonNegativeReals,
                          doc = 'efficiency of the st')

    m.p_st_cop = py.Param(m.set_years, m.set_scenarios,
                          initialize = init_st_cop,
                          within = py.NonNegativeReals,
                          doc = 'coefficient of performance of the hp for the st')
    
    # m.p_st_c_fix = py.Param(m.set_years, m.set_scenarios,
    #                         initialize = init_st_c_fix,
    #                         within = py.NonNegativeReals,
    #                         doc = 'fixed cost of st')
    
    m.p_st_c_inv =py.Param(m.set_years, m.set_scenarios,
                           initialize = init_st_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of st')
    
    m.p_st_solar_radiation = py.Param(m.set_years, m.set_hours, m.set_scenarios,
                                      initialize = init_solar_radiation,
                                      within = py.NonNegativeReals,
                                      doc = 'solar radiation in W/m2')
    
    # m.p_c_opam( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )