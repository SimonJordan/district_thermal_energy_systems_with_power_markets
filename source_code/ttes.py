import pyomo.environ as py

def add_ttes_equations(m=None):
    
    def ttes_feed_in_max_bound(m, s, y, t):
        return m.v_ttes_q_heat_out[s, y, t] <= m.v_ttes_hp_Q_max[s, y]
    
    # def ttes_limit_1(m, s, y):
    #     return m.v_ttes_hp_Q_max[s, y] <= 0
    
    # def ttes_limit_2(m, s, y):
    #     return m.v_ttes_k_heat_max[s, y] <= 0
    
    def ttes_soc_max_bound(m, s, y, t):
        return m.v_ttes_k_heat[s, y, t] <= m.v_ttes_k_heat_max[s, y]

    def ttes_soc(m, s, y, t):
        if t == 0:
            return m.v_ttes_k_heat[s, y, t] == m.v_ttes_k_heat_max[s, y] * m.p_ttes_losses[s, y] * m.p_ttes_init[s, y] + m.v_ttes_q_heat_out[s, y, t] * m.p_ttes_eta[s, y] - m.v_ttes_q_heat_in[s, y, t] / m.p_ttes_eta[s, y]
        elif t == 8759:
            return m.v_ttes_k_heat[s, y, t] ==  m.v_ttes_k_heat_max[s, y] * m.p_ttes_end[s, y]
        else:
            return m.v_ttes_k_heat[s, y, t] == m.v_ttes_k_heat[s, y, t-1] * m.p_ttes_losses[s, y] + m.v_ttes_q_heat_out[s, y, t] * m.p_ttes_eta[s, y] - m.v_ttes_q_heat_in[s, y, t] / m.p_ttes_eta[s, y]
    
    def ttes_elec_heat(m, s, y, t):
        return m.v_ttes_q_heat_out[s, y, t] == m.v_ttes_q_elec_consumption[s, y, t] * m.p_ttes_cop[s, y]
    
    def ttes_k_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ttes_k_inv[s, y] == m.v_ttes_k_heat_max[s, y] - m.v_ttes_k_heat_max[s, y-5]
        else:
            return m.v_ttes_k_inv[s, y] == m.v_ttes_k_heat_max[s, y]
    
    def ttes_hp_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ttes_hp_Q_inv[s, y] == m.v_ttes_hp_Q_max[s, y] - m.v_ttes_hp_Q_max[s, y-5]
        else:
            return m.v_ttes_hp_Q_inv[s, y] == m.v_ttes_hp_Q_max[s, y]
   
    def ttes_c_inv(m, s, y):
        return m.v_ttes_c_inv[s, y] == m.v_ttes_k_inv[s, y] * m.p_ttes_c_inv[s, y] + m.v_ttes_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]
    
    def ttes_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ttes_c_fix[s, y] == m.v_ttes_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * (m.v_ttes_c_inv[s, y] * 0.02 + m.v_ttes_k_inv[s, y] * (m.p_c_mean_elec[s, y] + m.p_mean_elec_co2_share[s, y] * m.p_c_co2[s, y]) * m.p_ttes_elec[s, y])
        else:
            return m.v_ttes_c_fix[s, y] == m.p_year_expansion_range[s, y] * (m.v_ttes_c_inv[s, y] * 0.02 + m.v_ttes_k_inv[s, y] * (m.p_c_mean_elec[s, y] + m.p_mean_elec_co2_share[s, y] * m.p_c_co2[s, y]) * m.p_ttes_elec[s, y])
    
    def ttes_c_var(m, s, y, t):
        return m.v_ttes_c_var[s, y, t] == m.p_year_expansion_range[s, y] * (m.v_ttes_q_elec_consumption[s, y, t] * (m.p_c_elec[s, y, t] + m.p_elec_co2_share[s, y, t] * m.p_c_co2[s, y]) + (m.v_ttes_q_heat_in[s, y, t] + m.v_ttes_q_heat_out[s, y, t]) * m.p_ttes_c_charge_discharge[s, y])

    m.con_ttes_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                 rule = ttes_feed_in_max_bound)
    
    m.con_ttes_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = ttes_elec_heat)
    
    m.con_ttes_soc_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                             rule = ttes_soc_max_bound)
    
    m.con_ttes_soc = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = ttes_soc)
        
    m.con_ttes_k_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ttes_k_inv)
    
    m.con_ttes_hp_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                        rule = ttes_hp_Q_inv)
    
    m.con_ttes_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ttes_c_inv)
    
    m.con_ttes_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ttes_c_fix)
    
    m.con_ttes_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                     rule = ttes_c_var)
    
    # m.con_ttes_limit_1 = py.Constraint(m.set_scenarios, m.set_years,
    #                                   rule = ttes_limit_1)
    
    # m.con_ttes_limit_2 = py.Constraint(m.set_scenarios, m.set_years,
    #                                   rule = ttes_limit_2)

def add_ttes_variables(m=None):
    """This section defines the variables for TTES"""
    m.v_ttes_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                domain = py.NonNegativeReals,
                                doc = 'heat energy feed in per scenario, year and hour')
    
    m.v_ttes_q_heat_out = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                 domain = py.NonNegativeReals,
                                 doc = 'heat energy storing per scenario, year and hour')
    
    m.v_ttes_hp_Q_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'maximum heat energy storing per scenario and year')
    
    m.v_ttes_k_heat = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                             domain = py.NonNegativeReals,
                             doc = 'state of charge per scenario, year and hour')
    
    m.v_ttes_k_heat_max = py.Var(m.set_scenarios, m.set_years,
                                 domain = py.NonNegativeReals,
                                 doc = 'maximum state of charge per scenario, year and hour')
    
    m.v_ttes_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                         domain = py.NonNegativeReals,
                                         doc = 'electricity input of heat pump per scenario, year and hour')
   
    m.v_ttes_k_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'new installed capacity of TTES per scenario and year')
   
    m.v_ttes_hp_Q_inv = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'new installed capacity of hp for TTES per scenario and year')
    
    m.v_ttes_c_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'inv costs of TTES per scenario and year in USD')
    
    m.v_ttes_c_fix = py.Var(m.set_scenarios, m.set_years,
                            domain = py.Reals,
                            doc = 'fix costs of TTES per scenario and year in USD')
    
    m.v_ttes_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                            domain = py.Reals,
                            doc = 'var costs of TTES per scenario, year and hour in USD')
    
def add_ttes_parameters(m=None):
    """This section defines the parameters for TTES"""
    
    def init_ttes_losses(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_losses']
    
    def init_ttes_eta(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_eta']
    
    def init_ttes_init(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_init']
    
    def init_ttes_end(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_end']
    
    def init_ttes_c_inv(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_c_inv']

    def init_ttes_elec(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_elec']
    
    def init_ttes_cop(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_cop']
    
    def init_ttes_c_charge_discharge(m, s, y):
        return m.data_values[s]['ttes'][y]['p_ttes_c_charge_discharge']
    
    m.p_ttes_losses = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_ttes_losses,
                               within = py.NonNegativeReals,
                               doc = 'losses of the storage')
    
    m.p_ttes_eta = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ttes_eta,
                            within = py.NonNegativeReals,
                            doc = 'efficiency of the storage')
    
    m.p_ttes_init = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_ttes_init,
                             within = py.NonNegativeReals,
                             doc = 'initial soc of the storage')
    
    m.p_ttes_end = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ttes_end,
                            within = py.NonNegativeReals,
                            doc = 'final soc of the storage')
    
    m.p_ttes_c_inv = py.Param(m.set_scenarios, m.set_years,
                              initialize = init_ttes_c_inv,
                              within = py.NonNegativeReals,
                              doc = 'specific investment costs of TTES')
    
    m.p_ttes_elec = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_ttes_elec,
                             within = py.NonNegativeReals,
                             doc = 'electricity share of heat energy')
    
    m.p_ttes_cop = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ttes_cop,
                            within = py.NonNegativeReals,
                            doc = 'cop of the storage')
    
    m.p_ttes_c_charge_discharge = py.Param(m.set_scenarios, m.set_years,
                                           initialize = init_ttes_c_charge_discharge,
                                           within = py.NonNegativeReals,
                                           doc = 'charge/discharge price per scenario, year and hour')
