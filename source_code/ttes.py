import pyomo.environ as py

def add_ttes_equations(m=None):
    
    def ttes_feed_in_max_bound(m, y, t, s):
        return m.v_ttes_q_thermal_in[y, t, s] <= m.v_ttes_Q_thermal_max[y, s]

    def ttes_storage_max_bound(m, y, t, s):
        return m.v_ttes_q_thermal_out[y, t, s] <= m.v_ttes_hp_Q_max[y, s]

    def ttes_soc_max_bound(m, y, t, s):
        return m.v_ttes_k_thermal[y, t, s] <= m.v_ttes_k_thermal_max[y, s]

    def ttes_soc(m, y, t, s):
        if t == 0:
            return m.v_ttes_k_thermal[y, 0, s] == m.v_ttes_k_thermal_max[y, s] * m.p_ttes_losses[y, s] * m.p_ttes_init[y, s] + m.v_ttes_q_thermal_out[y, 0, s] * m.p_ttes_eta[y, s] - m.v_ttes_q_thermal_in[y, 0, s] / m.p_ttes_eta[y, s]
        else:
            return m.v_ttes_k_thermal[y, t, s] == m.v_ttes_k_thermal[y, t-1, s] * m.p_ttes_losses[y, s] + m.v_ttes_q_thermal_out[y, t, s] * m.p_ttes_eta[y, s] - m.v_ttes_q_thermal_in[y, t, s] / m.p_ttes_eta[y, s]
    
    def ttes_soc_final(m, y, t, s):
        return m.v_ttes_k_thermal[y, 8759, s] == m.v_ttes_k_thermal_max[y, s] * m.p_ttes_end[y, s]

    def ttes_elec_heat(m, y, t, s):
        return m.v_ttes_q_thermal_in[y, t, s] == m.v_ttes_q_elec_consumption[y, t, s] * m.p_ttes_cop[y, s]
    
    def ttes_k_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ttes_k_inv[y, s] == (m.v_ttes_k_thermal_max[y, s] - m.v_ttes_k_thermal_max[y-5, s])
        else:
            return m.v_ttes_k_inv[y, s] == m.v_ttes_k_thermal_max[y, s]
    
    def ttes_hp_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ttes_hp_Q_inv[y, s] == (m.v_ttes_hp_Q_max[y, s] - m.v_ttes_hp_Q_max[y-5, s])
        else:
            return m.v_ttes_hp_Q_inv[y, s] == m.v_ttes_hp_Q_max[y, s]
   
    def ttes_c_inv(m, y, s):
        return m.v_ttes_c_inv[y, s] == m.v_ttes_k_inv[y, s] * m.p_ttes_c_inv[y, s] + m.v_ttes_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]
    
    def ttes_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ttes_c_fix[y, s] == m.v_ttes_c_fix[y-5, s] + (m.v_ttes_k_inv[y, s] * m.p_ttes_c_inv[y, s] + m.v_ttes_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]) * 0.02 + (m.v_ttes_k_thermal_max[y, s] - m.v_ttes_k_thermal_max[y-5, s]) * m.p_c_mean_elec[y, s] * m.p_ttes_elec[y, s]
        else:
            return m.v_ttes_c_fix[y, s] == (m.v_ttes_k_inv[y, s] * m.p_ttes_c_inv[y, s] + m.v_ttes_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]) * 0.02 + m.v_ttes_k_thermal_max[y, s] * m.p_c_mean_elec[y, s] * m.p_ttes_elec[y, s]
    
    def ttes_c_var(m, y, t, s):
        return m.v_ttes_c_var[y, t, s] == m.v_ttes_q_elec_consumption[y, t, s] * m.p_c_elec[y, t, s] + (m.v_ttes_q_thermal_in[y, t, s] + m.v_ttes_q_thermal_out[y, t, s]) * m.p_ttes_c_charge_discharge[y, s] # + m.v_c_opam[y, s]

    m.con_ttes_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                 rule = ttes_feed_in_max_bound)
    
    m.con_ttes_storage_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                 rule = ttes_storage_max_bound)
    
    m.con_ttes_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                         rule = ttes_elec_heat)
    
    m.con_ttes_soc_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                             rule = ttes_soc_max_bound)
    
    m.con_ttes_soc = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = ttes_soc)
        
    m.con_ttes_soc_final = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                         rule = ttes_soc_final)
        
    m.con_ttes_k_inv = py.Constraint(m.set_years, m.set_scenarios,
                                     rule = ttes_k_inv)
    
    m.con_ttes_hp_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                        rule = ttes_hp_Q_inv)
    
    m.con_ttes_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                     rule = ttes_c_inv)
    
    m.con_ttes_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                     rule = ttes_c_fix)
    
    m.con_ttes_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                     rule = ttes_c_var)

def add_ttes_variables(m=None):
    """This section defines the variables for TTES"""
    m.v_ttes_q_thermal_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                   domain = py.NonNegativeReals,
                                   doc = 'thermal energy feed in per scenario, year and hour')
    
    m.v_ttes_q_thermal_out = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                    domain = py.NonNegativeReals,
                                    doc = 'thermal energy storing per scenario, year and hour')
    
    m.v_ttes_Q_thermal_max = py.Var(m.set_years, m.set_scenarios,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum thermal energy feed in per scenario and year')
    
    m.v_ttes_hp_Q_max = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'maximum thermal energy storing per scenario and year')
    
    m.v_ttes_k_thermal = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                domain = py.NonNegativeReals,
                                doc = 'state of charge per scenario, year and hour')
    
    m.v_ttes_k_thermal_max = py.Var(m.set_years, m.set_scenarios,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum state of charge per scenario, year and hour')
    
    m.v_ttes_q_elec_consumption = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                         domain = py.NonNegativeReals,
                                         doc = 'electricity input of heat pump per scenario, year and hour')
   
    m.v_ttes_k_inv = py.Var(m.set_years, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'new installed capacity of TTES per scenario and year in EUR')
   
    m.v_ttes_hp_Q_inv = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'new installed capacity of hp for TTES per scenario and year in EUR')
    
    m.v_ttes_c_inv = py.Var(m.set_years, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'inv costs of TTES per scenario and year in EUR')
    
    m.v_ttes_c_fix = py.Var(m.set_years, m.set_scenarios,
                            domain = py.Reals,
                            doc = 'fix costs of TTES per scenario and year in EUR')
    
    m.v_ttes_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                            domain = py.Reals,
                            doc = 'var costs of TTES per scenario, year and hour in EUR')
    
def add_ttes_parameters(m=None):
    """This section defines the parameters for TTES"""
    
    def init_ttes_losses(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_losses']
    
    def init_ttes_eta(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_eta']
    
    def init_ttes_init(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_init']
    
    def init_ttes_end(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_end']
    
    def init_ttes_c_inv(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_c_inv']

    def init_ttes_elec(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_elec']
    
    def init_ttes_cop(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_cop']
    
    def init_ttes_c_charge_discharge(m, y, s):
        return m.data_values[s]['ttes'][y]['p_ttes_c_charge_discharge']
    
    m.p_ttes_losses = py.Param(m.set_years, m.set_scenarios,
                               initialize = init_ttes_losses,
                               within = py.NonNegativeReals,
                               doc = 'losses of the storage')
    
    m.p_ttes_eta = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_ttes_eta,
                            within = py.NonNegativeReals,
                            doc = 'efficiency of the storage')
    
    m.p_ttes_init = py.Param(m.set_years, m.set_scenarios,
                             initialize = init_ttes_init,
                             within = py.NonNegativeReals,
                             doc = 'initial soc of the storage')
    
    m.p_ttes_end = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_ttes_end,
                            within = py.NonNegativeReals,
                            doc = 'final soc of the storage')
    
    m.p_ttes_c_inv = py.Param(m.set_years, m.set_scenarios,
                              initialize = init_ttes_c_inv,
                              within = py.NonNegativeReals,
                              doc = 'specific investment costs of TTES')
    
    m.p_ttes_elec = py.Param(m.set_years, m.set_scenarios,
                             initialize = init_ttes_elec,
                             within = py.NonNegativeReals,
                             doc = 'electricity share of thermal energy')
    
    m.p_ttes_cop = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_ttes_cop,
                            within = py.NonNegativeReals,
                            doc = 'cop of the storage')
    
    m.p_ttes_c_charge_discharge = py.Param(m.set_years, m.set_scenarios,
                                           initialize = init_ttes_c_charge_discharge,
                                           within = py.NonNegativeReals,
                                           doc = 'charge/discharge price per scenario, year and hour')
    
    # m.p_c_opam = py.Param( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per scenario, year and hour'
    #     )