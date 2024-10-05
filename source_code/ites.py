import pyomo.environ as py

def add_ites_equations(m=None):
    
    def ites_feed_in_max_bound(m, s, y, t):
        return m.v_ites_q_cool_out[s, y, t] <= m.v_ites_ac_Q_max[s, y]
    
    # def ites_limit_1(m, s, y):
    #     return m.v_ites_ac_Q_max[s, y] <= 0
    
    # def ites_limit_2(m, s, y):
    #     return m.v_ites_k_cool_max[s, y] <= 0
    
    def ites_soc_max_bound(m, s, y, t):
        return m.v_ites_k_cool[s, y, t] <= m.v_ites_k_cool_max[s, y]

    def ites_soc(m, s, y, t):
        if t == 0:
            return m.v_ites_k_cool[s, y, t] == m.v_ites_k_cool_max[s, y] * m.p_ites_losses[s, y] * m.p_ites_init[s, y] + m.v_ites_q_cool_out[s, y, t] * m.p_ites_eta[s, y] - m.v_ites_q_cool_in[s, y, t] / m.p_ites_eta[s, y]
        elif t == 8759:
            return m.v_ites_k_cool[s, y, t] ==  m.v_ites_k_cool_max[s, y] * m.p_ites_end[s, y]
        else:
            return m.v_ites_k_cool[s, y, t] == m.v_ites_k_cool[s, y, t-1] * m.p_ites_losses[s, y] + m.v_ites_q_cool_out[s, y, t] * m.p_ites_eta[s, y] - m.v_ites_q_cool_in[s, y, t] / m.p_ites_eta[s, y]
    
    def ites_elec_cool(m, s, y, t):
        return m.v_ites_q_cool_out[s, y, t] == m.v_ites_q_elec_consumption[s, y, t] * m.p_ites_seer[s, y]
    
    def ites_k_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ites_k_inv[s, y] == m.v_ites_k_cool_max[s, y] - m.v_ites_k_cool_max[s, y-5]
        else:
            return m.v_ites_k_inv[s, y] == m.v_ites_k_cool_max[s, y]
    
    def ites_ac_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ites_ac_Q_inv[s, y] == m.v_ites_ac_Q_max[s, y] - m.v_ites_ac_Q_max[s, y-5]
        else:
            return m.v_ites_ac_Q_inv[s, y] == m.v_ites_ac_Q_max[s, y]
   
    def ites_c_inv(m, s, y):
        return m.v_ites_c_inv[s, y] == m.v_ites_k_inv[s, y] * m.p_ites_c_inv[s, y] + m.v_ites_ac_Q_inv[s, y] * m.p_ac_c_inv[s, y]
    
    def ites_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ites_c_fix[s, y] == m.v_ites_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * (m.v_ites_c_inv[s, y] * 0.02 + (m.v_ites_k_cool_max[s, y] - m.v_ites_k_cool_max[s, y-5]) * (m.p_c_mean_elec[s, y] + m.p_mean_elec_co2_share[s, y] * m.p_c_co2[s, y]) * m.p_ites_elec[s, y])
        else:
            return m.v_ites_c_fix[s, y] == m.p_year_expansion_range[s, y] * (m.v_ites_c_inv[s, y] * 0.02 + m.v_ites_k_cool_max[s, y] * (m.p_c_mean_elec[s, y] + m.p_mean_elec_co2_share[s, y] * m.p_c_co2[s, y]) * m.p_ites_elec[s, y])
    
    def ites_c_var(m, s, y, t):
        return m.v_ites_c_var[s, y, t] == m.p_year_expansion_range[s, y] * (m.v_ites_q_elec_consumption[s, y, t] * (m.p_c_elec[s, y, t] + m.p_elec_co2_share[s, y, t] * m.p_c_co2[s, y]) + (m.v_ites_q_cool_in[s, y, t] + m.v_ites_q_cool_out[s, y, t]) * m.p_ites_c_charge_discharge[s, y])

    m.con_ites_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                 rule = ites_feed_in_max_bound)
    
    m.con_ites_elec_cool = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = ites_elec_cool)
    
    m.con_ites_soc_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                             rule = ites_soc_max_bound)
    
    m.con_ites_soc = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = ites_soc)
        
    m.con_ites_k_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ites_k_inv)
    
    m.con_ites_ac_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                        rule = ites_ac_Q_inv)
    
    m.con_ites_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ites_c_inv)
    
    m.con_ites_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ites_c_fix)
    
    m.con_ites_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                     rule = ites_c_var)
    
    # m.con_ites_limit_1 = py.Constraint(m.set_scenarios, m.set_years,
    #                                   rule = ites_limit_1)
    
    # m.con_ites_limit_2 = py.Constraint(m.set_scenarios, m.set_years,
    #                                   rule = ites_limit_2)

def add_ites_variables(m=None):
    """This section defines the variables for ITES"""
    m.v_ites_q_cool_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                   domain = py.NonNegativeReals,
                                   doc = 'cool energy feed in per scenario, year and hour')
    
    m.v_ites_q_cool_out = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                    domain = py.NonNegativeReals,
                                    doc = 'cool energy storing per scenario, year and hour')
    
    m.v_ites_ac_Q_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'maximum cool energy storing per scenario and year')
    
    m.v_ites_k_cool = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                domain = py.NonNegativeReals,
                                doc = 'state of charge per scenario, year and hour')
    
    m.v_ites_k_cool_max = py.Var(m.set_scenarios, m.set_years,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum state of charge per scenario, year and hour')
    
    m.v_ites_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                         domain = py.NonNegativeReals,
                                         doc = 'electricity input of airchiller per scenario, year and hour')
   
    m.v_ites_k_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'new installed capacity of ITES per scenario and year')
   
    m.v_ites_ac_Q_inv = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'new installed capacity of ac for ITES per scenario and year')
    
    m.v_ites_c_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'inv costs of ITES per scenario and year in USD')
    
    m.v_ites_c_fix = py.Var(m.set_scenarios, m.set_years,
                            domain = py.Reals,
                            doc = 'fix costs of ITES per scenario and year in USD')
    
    m.v_ites_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                            domain = py.Reals,
                            doc = 'var costs of ITES per scenario, year and hour in USD')
    
def add_ites_parameters(m=None):
    """This section defines the parameters for ITES"""
    
    def init_ites_losses(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_losses']
    
    def init_ites_eta(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_eta']
    
    def init_ites_init(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_init']
    
    def init_ites_end(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_end']
    
    def init_ites_c_inv(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_c_inv']

    def init_ites_elec(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_elec']
    
    def init_ites_seer(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_seer']
    
    def init_ites_c_charge_discharge(m, s, y):
        return m.data_values[s]['ites'][y]['p_ites_c_charge_discharge']
    
    m.p_ites_losses = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_ites_losses,
                               within = py.NonNegativeReals,
                               doc = 'losses of the storage')
    
    m.p_ites_eta = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ites_eta,
                            within = py.NonNegativeReals,
                            doc = 'efficiency of the storage')
    
    m.p_ites_init = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_ites_init,
                             within = py.NonNegativeReals,
                             doc = 'initial soc of the storage')
    
    m.p_ites_end = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ites_end,
                            within = py.NonNegativeReals,
                            doc = 'final soc of the storage')
    
    m.p_ites_c_inv = py.Param(m.set_scenarios, m.set_years,
                              initialize = init_ites_c_inv,
                              within = py.NonNegativeReals,
                              doc = 'specific investment costs of ITES')
    
    m.p_ites_elec = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_ites_elec,
                             within = py.NonNegativeReals,
                             doc = 'electricity share of cool energy')
    
    m.p_ites_seer = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ites_seer,
                            within = py.NonNegativeReals,
                            doc = 'seer of the storage')
    
    m.p_ites_c_charge_discharge = py.Param(m.set_scenarios, m.set_years,
                                           initialize = init_ites_c_charge_discharge,
                                           within = py.NonNegativeReals,
                                           doc = 'charge/discharge price per scenario, year and hour')
