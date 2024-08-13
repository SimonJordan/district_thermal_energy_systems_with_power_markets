import pyomo.environ as py

def add_ates_equations(m=None):
    
    def ates_feed_in_max_bound(m, s, y, t):
        return m.v_ates_q_thermal_in[s, y, t] <= m.v_ates_Q_thermal_max[s, y]

    def ates_storage_max_bound(m, s, y, t):
        return m.v_ates_q_thermal_out[s, y, t] <= m.v_ates_hp_Q_max[s, y]

    def ates_soc_max_bound(m, s, y, t):
        return m.v_ates_k_thermal[s, y, t] <= m.v_ates_k_thermal_max[s, y]

    def ates_soc(m, s, y, t):
        if t == 0:
            return m.v_ates_k_thermal[s, y, 0] == m.v_ates_k_thermal_max[s, y] * m.p_ates_losses[s, y] * m.p_ates_init[s, y] + m.v_ates_q_thermal_out[s, y, 0] * m.p_ates_eta[s, y] - m.v_ates_q_thermal_in[s, y, 0] / m.p_ates_eta[s, y]
        else:
            return m.v_ates_k_thermal[s, y, t] == m.v_ates_k_thermal[s, y, t-1] * m.p_ates_losses[s, y] + m.v_ates_q_thermal_out[s, y, t] * m.p_ates_eta[s, y] - m.v_ates_q_thermal_in[s, y, t] / m.p_ates_eta[s, y]
    
    def ates_soc_final(m, s, y, t):
        return m.v_ates_k_thermal[s, y, 8759] == m.v_ates_k_thermal_max[s, y] * m.p_ates_end[s, y]

    def ates_elec_heat(m, s, y, t):
        return m.v_ates_q_thermal_in[s, y, t] == m.v_ates_q_elec_consumption[s, y, t] * m.p_ates_cop[s, y]
    
    def ates_k_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ates_k_inv[s, y] == (m.v_ates_k_thermal_max[s, y] - m.v_ates_k_thermal_max[s, y-5])
        else:
            return m.v_ates_k_inv[s, y] == m.v_ates_k_thermal_max[s, y]
    
    def ates_hp_Q_inv(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ates_hp_Q_inv[s, y] == (m.v_ates_hp_Q_max[s, y] - m.v_ates_hp_Q_max[s, y-5])
        else:
            return m.v_ates_hp_Q_inv[s, y] == m.v_ates_hp_Q_max[s, y]
   
    def ates_c_inv(m, s, y):
        return m.v_ates_c_inv[s, y] == m.v_ates_k_inv[s, y] * m.p_ates_c_inv[s, y] + m.v_ates_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]
    
    def ates_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ates_c_fix[s, y] == m.v_ates_c_fix[s, y-5] + (m.v_ates_k_inv[s, y] * m.p_ates_c_inv[s, y] + m.v_ates_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]) * 0.02 + (m.v_ates_k_thermal_max[s, y] - m.v_ates_k_thermal_max[s, y-5]) * m.p_c_mean_elec[s, y] * m.p_ates_elec[s, y]
        else:
            return m.v_ates_c_fix[s, y] == (m.v_ates_k_inv[s, y] * m.p_ates_c_inv[s, y] + m.v_ates_hp_Q_inv[s, y] * m.p_hp_c_inv[s, y]) * 0.02 + m.v_ates_k_thermal_max[s, y] * m.p_c_mean_elec[s, y] * m.p_ates_elec[s, y]
    
    def ates_c_var(m, s, y, t):
        return m.v_ates_c_var[s, y, t] == m.v_ates_q_elec_consumption[s, y, t] * m.p_c_elec[s, y, t] + (m.v_ates_q_thermal_in[s, y, t] + m.v_ates_q_thermal_out[s, y, t]) * m.p_ates_c_charge_discharge[s, y]

    m.con_ates_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                 rule = ates_feed_in_max_bound)
    
    m.con_ates_storage_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                 rule = ates_storage_max_bound)
    
    m.con_ates_elec_heat = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = ates_elec_heat)
    
    m.con_ates_soc_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                             rule = ates_soc_max_bound)
    
    m.con_ates_soc = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                   rule = ates_soc)
        
    m.con_ates_soc_final = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = ates_soc_final)
        
    m.con_ates_k_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ates_k_inv)
    
    m.con_ates_hp_Q_inv = py.Constraint(m.set_scenarios, m.set_years,
                                        rule = ates_hp_Q_inv)
    
    m.con_ates_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ates_c_inv)
    
    m.con_ates_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                     rule = ates_c_fix)
    
    m.con_ates_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                     rule = ates_c_var)

def add_ates_variables(m=None):
    """This section defines the variables for ATES"""
    m.v_ates_q_thermal_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                   domain = py.NonNegativeReals,
                                   doc = 'thermal energy feed in per scenario, year and hour')
    
    m.v_ates_q_thermal_out = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                    domain = py.NonNegativeReals,
                                    doc = 'thermal energy storing per scenario, year and hour')
    
    m.v_ates_Q_thermal_max = py.Var(m.set_scenarios, m.set_years,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum thermal energy feed in per scenario and year')
    
    m.v_ates_hp_Q_max = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'maximum thermal energy storing per scenario and year')
    
    m.v_ates_k_thermal = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                domain = py.NonNegativeReals,
                                doc = 'state of charge per scenario, year and hour')
    
    m.v_ates_k_thermal_max = py.Var(m.set_scenarios, m.set_years,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum state of charge per scenario, year and hour')
    
    m.v_ates_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                         domain = py.NonNegativeReals,
                                         doc = 'electricity input of heat pump per scenario, year and hour')
   
    m.v_ates_k_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'new installed capacity of ATES per scenario and year in EUR')
   
    m.v_ates_hp_Q_inv = py.Var(m.set_scenarios, m.set_years,
                               domain = py.NonNegativeReals,
                               doc = 'new installed capacity of hp for ATES per scenario and year in EUR')
    
    m.v_ates_c_inv = py.Var(m.set_scenarios, m.set_years,
                            domain = py.NonNegativeReals,
                            doc = 'inv costs of ATES per scenario and year in EUR')
    
    m.v_ates_c_fix = py.Var(m.set_scenarios, m.set_years,
                            domain = py.Reals,
                            doc = 'fix costs of ATES per scenario and year in EUR')
    
    m.v_ates_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                            domain = py.Reals,
                            doc = 'var costs of ATES per scenario, year and hour in EUR')
    
def add_ates_parameters(m=None):
    """This section defines the parameters for ATES"""
    
    def init_ates_losses(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_losses']
    
    def init_ates_eta(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_eta']
    
    def init_ates_init(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_init']
    
    def init_ates_end(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_end']
    
    def init_ates_c_inv(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_c_inv']

    def init_ates_elec(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_elec']
    
    def init_ates_cop(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_cop']
    
    def init_ates_c_charge_discharge(m, s, y):
        return m.data_values[s]['ates'][y]['p_ates_c_charge_discharge']
    
    m.p_ates_losses = py.Param(m.set_scenarios, m.set_years,
                               initialize = init_ates_losses,
                               within = py.NonNegativeReals,
                               doc = 'losses of the storage')
    
    m.p_ates_eta = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ates_eta,
                            within = py.NonNegativeReals,
                            doc = 'efficiency of the storage')
    
    m.p_ates_init = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_ates_init,
                             within = py.NonNegativeReals,
                             doc = 'initial soc of the storage')
    
    m.p_ates_end = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ates_end,
                            within = py.NonNegativeReals,
                            doc = 'final soc of the storage')
    
    m.p_ates_c_inv = py.Param(m.set_scenarios, m.set_years,
                              initialize = init_ates_c_inv,
                              within = py.NonNegativeReals,
                              doc = 'specific investment costs of ATES')
    
    m.p_ates_elec = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_ates_elec,
                             within = py.NonNegativeReals,
                             doc = 'electricity share of thermal energy')
    
    m.p_ates_cop = py.Param(m.set_scenarios, m.set_years,
                            initialize = init_ates_cop,
                            within = py.NonNegativeReals,
                            doc = 'cop of the storage')
    
    m.p_ates_c_charge_discharge = py.Param(m.set_scenarios, m.set_years,
                                           initialize = init_ates_c_charge_discharge,
                                           within = py.NonNegativeReals,
                                           doc = 'charge/discharge price per scenario, year and hour')
    