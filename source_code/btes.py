import pyomo.environ as py

def add_btes_equations(m=None):
    
    def btes_feed_in_max_bound(m, s, y, h):
        return m.v_wi_q_heat_out[s, y, h] <= m.v_btes_hp_Q_max[s, y]
    
    # def btes_limit_1(m, s, y):
    #     return m.v_btes_hp_Q_max[s, y] <= 0
    
    # def btes_limit_2(m, s, y):
    #     return m.v_btes_k_heat_max[s, y] <= 0
    
    def btes_soc_max_bound(m, s, y, h):
        return m.v_btes_k_heat[s, y, h] <= m.v_btes_k_heat_max[s, y]

    def btes_soc(m, s, y, h):
        if h == 0:
            if y == 2025:
                return m.v_btes_k_heat[s, y, h] == m.v_btes_k_heat_max[s, y] * m.p_btes_losses[s, y] * m.p_btes_init[s, y] + m.v_wi_q_heat_out[s, y, h] * m.p_btes_eta[s, y] - m.v_btes_q_heat_in[s, y, h] / m.p_btes_eta[s, y]
            else:
                return m.v_btes_k_heat[s, y, h] == m.v_btes_k_heat[s, y-5, 8759] * m.p_btes_losses[s, y] + m.v_wi_q_heat_out[s, y, h] * m.p_btes_eta[s, y] - m.v_btes_q_heat_in[s, y, h] / m.p_btes_eta[s, y]
        elif h == 8759 and y == 2050:
            return m.v_btes_k_heat[s, y, h] == m.v_btes_k_heat_max[s, y] * m.p_btes_end[s, y]
        else:
            return m.v_btes_k_heat[s, y, h] == m.v_btes_k_heat[s, y, h-1] * m.p_btes_losses[s, y] + m.v_wi_q_heat_out[s, y, h] * m.p_btes_eta[s, y] - m.v_btes_q_heat_in[s, y, h] / m.p_btes_eta[s, y]
    
    def btes_elec_heat(m, s, y, h):
        return m.v_wi_q_heat_out[s, y, h] == m.v_btes_q_elec_consumption[s, y, h] * m.p_btes_cop[s, y]
    
    def btes_k_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_btes_k_inv[s, y] == m.v_btes_k_heat_max[s, y] - m.v_btes_k_heat_max[s, y-5]
        else:
            return m.v_btes_k_inv[s, y] == m.v_btes_k_heat_max[s, y]
    
    def btes_hp_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_btes_hp_Q_inv[s, y] == m.v_btes_hp_Q_max[s, y] - m.v_btes_hp_Q_max[s, y-5]
        else:
            return m.v_btes_hp_Q_inv[s, y] == m.v_btes_hp_Q_max[s, y]
   
    def btes_c_inv(m, s, y):
        return m.v_btes_c_inv[s, y] == m.v_btes_k_inv[s, y] * m.p_btes_c_inv[s, y] + m.v_btes_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]
    
    def btes_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_btes_c_fix[s, y] == m.v_btes_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * (m.v_btes_c_inv[s, y] * 0.02 + m.v_btes_k_inv[s, y] * m.p_c_mean_elec[s, y] * m.p_btes_elec[s, y])
        else:
            return m.v_btes_c_fix[s, y] == m.p_year_expansion_range[s, y] * (m.v_btes_c_inv[s, y] * 0.02 + m.v_btes_k_inv[s, y] * m.p_c_mean_elec[s, y] * m.p_btes_elec[s, y])
    
    def btes_c_var(m, s, y, h):
        return m.v_btes_c_var[s, y, h] == m.p_year_expansion_range[s, y] * (m.v_btes_q_elec_consumption[s, y, h] * m.p_c_elec[s, y, h] + (m.v_btes_q_heat_in[s, y, h] + m.v_wi_q_heat_out[s, y, h]) * m.p_btes_c_charge_discharge[s, y])

    m.con_btes_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                 rule = btes_feed_in_max_bound)
    
    m.con_btes_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = btes_elec_heat)
    
    m.con_btes_soc_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                             rule = btes_soc_max_bound)
    
    m.con_btes_soc = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = btes_soc)
        
    m.con_btes_k_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = btes_k_inv)
    
    m.con_btes_hp_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                        rule = btes_hp_Q_inv)
    
    m.con_btes_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = btes_c_inv)
    
    m.con_btes_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = btes_c_fix)
    
    m.con_btes_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                     rule = btes_c_var)
    
    # m.con_btes_limit_1 = py.Constraint(m.set_scenarios, m.set_years,
    #                                   rule = btes_limit_1)
    
    # m.con_btes_limit_2 = py.Constraint(m.set_scenarios, m.set_years,
    #                                   rule = btes_limit_2)

def add_btes_variables(m=None):
    """This section defines the variables for BTES"""
    m.v_btes_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                domain = py.NonNegativeReals,
                                doc = 'heat energy feed in per scenario, year and hour')
    
    m.v_btes_hp_Q_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'maximum heat energy storing per scenario and year')
    
    m.v_btes_k_heat = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                             domain = py.NonNegativeReals,
                             doc = 'state of charge per scenario, year and hour')
    
    m.v_btes_k_heat_max = py.Var(m.set_scenarios, m.set_years,
                                 domain = py.NonNegativeReals,
                                 doc = 'maximum state of charge per scenario, year and hour')
    
    m.v_btes_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                         domain = py.NonNegativeReals,
                                         doc = 'electricity input of heat pump per scenario, year and hour')
   
    m.v_btes_k_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'new installed capacity of BTES per scenario and year')
   
    m.v_btes_hp_Q_inv = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'new installed capacity of hp for BTES per scenario and year')
    
    m.v_btes_c_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'inv costs of BTES per scenario and year in USD')
    
    m.v_btes_c_fix = py.Var(m.set_scenarios, m.set_years,
                            domain = py.Reals,
                            doc = 'fix costs of BTES per scenario and year in USD')
    
    m.v_btes_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                            domain = py.Reals,
                            doc = 'var costs of BTES per scenario, year and hour in USD')
    
def add_btes_parameters(m=None):
    """This section defines the parameters for BTES"""
    
    def init_btes_losses(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_losses']
    
    def init_btes_eta(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_eta']
    
    def init_btes_init(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_init']
    
    def init_btes_end(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_end']
    
    def init_btes_c_inv(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_c_inv']

    def init_btes_elec(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_elec']
    
    def init_btes_cop(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_cop']
    
    def init_btes_c_charge_discharge(m, s, y):
        return m.data_values[s]['btes'][y]['p_btes_c_charge_discharge']
    
    m.p_btes_losses = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_btes_losses,
                               within = py.NonNegativeReals,
                               doc = 'losses of the storage')
    
    m.p_btes_eta = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_btes_eta,
                            within = py.NonNegativeReals,
                            doc = 'efficiency of the storage')
    
    m.p_btes_init = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_btes_init,
                             within = py.NonNegativeReals,
                             doc = 'initial soc of the storage')
    
    m.p_btes_end = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_btes_end,
                            within = py.NonNegativeReals,
                            doc = 'final soc of the storage')
    
    m.p_btes_c_inv = py.Param(m.set_scenarios, m.set_years,
                              initialize = init_btes_c_inv,
                              within = py.NonNegativeReals,
                              doc = 'specific investment costs of BTES')
    
    m.p_btes_elec = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_btes_elec,
                             within = py.NonNegativeReals,
                             doc = 'electricity share of heat energy')
    
    m.p_btes_cop = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_btes_cop,
                            within = py.NonNegativeReals,
                            doc = 'cop of the storage')
    
    m.p_btes_c_charge_discharge = py.Param(m.set_scenarios, m.set_years,
                                           initialize = init_btes_c_charge_discharge,
                                           within = py.NonNegativeReals,
                                           doc = 'charge/discharge price per scenario, year and hour')
