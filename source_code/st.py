import pyomo.environ as py

def add_st_equations(m=None):

    def st_feed_in_max_bound(m, s, y, t):
        return m.v_st_q_heat_in[s, y, t] <= m.v_st_Q_heat_max[s, y]
    
    # def st_limit(m, s, y):
    #     return m.v_st_Q_heat_max[s, y] <= 200
    
    # def st_eta(m, s, y):
    #     if (y - 5) in m.set_years:
    #         return m.v_st_eta_avg[s, y] == (m.v_st_eta_avg[y-5, s] * m.v_st_P_max[y-5, s] + m.p_st_eta[s, y] * m.v_st_P_inv[s, y]) / (m.v_st_P_max[y-5, s] + m.v_st_P_inv[s, y])
    #     else:
    #         return m.v_st_eta_avg[s, y] == m.p_st_eta[s, y]
    
    def st_solar_radiation(m, s, y, t):
        return m.v_st_q_heat_in[s, y, t] == m.p_st_solar_radiation[s, y, t] * m.v_st_p[s, y, t] / 1000 * m.p_st_eta[s, y]
    
    def st_elec_heat(m, s, y, t):
        return m.v_st_q_heat_in[s, y, t] == m.v_st_q_elec_consumption[s, y, t] * m.p_st_cop[s, y]
     
    def st_p_max_bound(m, s, y, t):
        return m.v_st_p[s, y, t] <= m.v_st_P_max[s, y]
     
    def st_P_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_st_P_inv[s, y] == (m.v_st_P_max[s, y] - m.v_st_P_max[s, y-5])
        else:
            return m.v_st_P_inv[s, y] == m.v_st_P_max[s, y]
        
    def st_hp_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_st_hp_Q_inv[s, y] == (m.v_st_Q_heat_max[s, y] - m.v_st_Q_heat_max[s, y-5])
        else:
            return m.v_st_hp_Q_inv[s, y] == m.v_st_Q_heat_max[s, y]
       
    def st_c_inv(m, s, y):
        return m.v_st_c_inv[s, y] == m.v_st_P_inv[s, y] * m.p_st_c_inv[s, y] + m.v_st_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]
   
    def st_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_st_c_fix[s, y] == m.v_st_c_fix[s, y-5] + (m.v_st_P_inv[s, y] * m.p_st_c_inv[s, y] + m.v_st_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]) * 0.02
        else:
            return m.v_st_c_fix[s, y] == (m.v_st_P_inv[s, y] * m.p_st_c_inv[s, y] + m.v_st_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]) * 0.02
    
    def st_c_var(m, s, y, t): # OPAM = operational and maintanance, förderung?
        return m.v_st_c_var[s, y, t] == m.v_st_q_elec_consumption[s, y, t] * (m.p_c_elec[s, y, t] + m.p_elec_co2_share[s, y, t] * m.p_c_co2[s, y])
    
    m.con_st_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                               rule = st_feed_in_max_bound)
    
    # m.con_st_eta = py.Constraint(m.set_scenarios, m.set_years,
    #                              rule = st_eta)
    
    m.con_st_solar_radiation = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                             rule = st_solar_radiation)
    
    m.con_st_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                       rule = st_elec_heat)
    
    m.con_st_p_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = st_p_max_bound)
    
    m.con_st_P_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = st_P_inv)
    
    m.con_st_hp_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = st_hp_Q_inv)
    
    m.con_st_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = st_c_inv)
    
    m.con_st_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                   rule = st_c_fix)
    
    m.con_st_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = st_c_var)
    
    # m.con_st_limit = py.Constraint(m.set_scenarios, m.set_years,
    #                                rule = st_limit)
    
     
def add_st_variables(m=None):
    
    m.v_st_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from solar thermal per scenario, year and hour')
    
    m.v_st_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                       domain = py.NonNegativeReals,
                                       doc = 'electricity input of solar thermal per scenario, year and hour')
    
    # m.v_st_eta_avg = py.Var(m.set_scenarios, m.set_years,
    #                         domain = py.NonNegativeReals,
    #                         doc = 'average eta of solar thermal per scenario and year')
    
    m.v_st_p = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                      domain = py.NonNegativeReals,
                      doc = 'power of solar thermal per scenario, year and hour')
    
    m.v_st_P_max = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'installed power of solar thermal per scenario and year')
    
    m.v_st_P_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'new installed power of solar thermal per scenario and year')
   
    m.v_st_hp_Q_inv = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'new installed capacity of hp for st per scenario and year')
    
    m.v_st_Q_heat_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from solar thermal for district heating')
    
    m.v_st_c_inv = py.Var(m.set_scenarios, m.set_years,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of st per scenario and year in USD')

    m.v_st_c_fix = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'fix costs of st per scenario and year in USD')
    
    m.v_st_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                            domain = py.Reals,
                            doc = 'var costs of st per scenario, year and hour in USD')

def add_st_parameters(m=None):
    
    def init_st_eta(m, s, y):
        return m.data_values[s]['st'][y]['p_st_eta']
    
    def init_st_c_inv(m, s, y):
        return m.data_values[s]['st'][y]['p_st_c_inv']
            
    # def init_st_c_fix(m, s, y):
    #     return m.data_values[s]['st'][y]['p_st_c_fix']
    
    def init_st_cop(m, s, y):
        return m.data_values[s]['st'][y]['p_st_cop']

    def init_solar_radiation(m, s, y, t):
        return m.data_values[s]['st'][y]['p_st_solar_radiation'][t]
    
    m.p_st_eta = py.Param(m.set_scenarios, m.set_years,
                          initialize = init_st_eta,
                          within = py.NonNegativeReals,
                          doc = 'efficiency of the st')

    m.p_st_cop = py.Param(m.set_scenarios, m.set_years,
                          initialize = init_st_cop,
                          within = py.NonNegativeReals,
                          doc = 'coefficient of performance of the hp for the st')
    
    # m.p_st_c_fix = py.Param(m.set_scenarios, m.set_years,
    #                         initialize = init_st_c_fix,
    #                         within = py.NonNegativeReals,
    #                         doc = 'fixed cost of st')
    
    m.p_st_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_st_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of st')
    
    m.p_st_solar_radiation = py.Param(m.set_scenarios, m.set_years, m.set_hours,
                                      initialize = init_solar_radiation,
                                      within = py.NonNegativeReals,
                                      doc = 'solar radiation in W/m2')
    