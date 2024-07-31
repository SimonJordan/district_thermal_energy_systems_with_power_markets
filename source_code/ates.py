import pyomo.environ as py

def add_ates_equations(m=None):
    
    def ates_feed_in_max_bound(m, y, t, s):
        return m.v_ates_q_thermal_in[y, t, s] <= m.v_ates_Q_thermal_max[y, s]

    def ates_storage_max_bound(m, y, t, s):
        return m.v_ates_q_thermal_out[y, t, s] <= m.v_ates_hp_Q_max[y, s]

    def ates_soc_max_bound(m, y, t, s):
        return m.v_ates_k_thermal[y, t, s] <= m.v_ates_k_thermal_max[y, s]

    def ates_soc(m, y, t, s):
        if t == 0:
            return m.v_ates_k_thermal[y, 0, s] == m.v_ates_k_thermal_max[y, s] * m.p_ates_losses[y, s] * m.p_ates_init[y, s] + m.v_ates_q_thermal_out[y, 0, s] * m.p_ates_eta[y, s] - m.v_ates_q_thermal_in[y, 0, s] / m.p_ates_eta[y, s]
        else:
            return m.v_ates_k_thermal[y, t, s] == m.v_ates_k_thermal[y, t-1, s] * m.p_ates_losses[y, s] + m.v_ates_q_thermal_out[y, t, s] * m.p_ates_eta[y, s] - m.v_ates_q_thermal_in[y, t, s] / m.p_ates_eta[y, s]
    
    def ates_soc_final(m, y, t, s):
        return m.v_ates_k_thermal[y, 8759, s] == m.v_ates_k_thermal_max[y, s] * m.p_ates_end[y, s]

    def ates_elec_heat(m, y, t, s):
        return m.v_ates_q_thermal_in[y, t, s] == m.v_ates_q_elec_consumption[y, t, s] * m.p_ates_cop[y, s]
    
    def ates_k_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ates_k_inv[y, s] == (m.v_ates_k_thermal_max[y, s] - m.v_ates_k_thermal_max[y-5, s])
        else:
            return m.v_ates_k_inv[y, s] == m.v_ates_k_thermal_max[y, s]
    
    def ates_hp_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ates_hp_Q_inv[y, s] == (m.v_ates_hp_Q_max[y, s] - m.v_ates_hp_Q_max[y-5, s])
        else:
            return m.v_ates_hp_Q_inv[y, s] == m.v_ates_hp_Q_max[y, s]
   
    def ates_c_inv(m, y, s):
        return m.v_ates_c_inv[y, s] == m.v_ates_k_inv[y, s] * m.p_ates_c_inv[y, s] + m.v_ates_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]
    
    def ates_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_ates_c_fix[y, s] == m.v_ates_c_fix[y-5, s] + (m.v_ates_k_inv[y, s] * m.p_ates_c_inv[y, s] + m.v_ates_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]) * 0.02 + (m.v_ates_k_thermal_max[y, s] - m.v_ates_k_thermal_max[y-5, s]) * m.p_c_mean_elec[y, s] * m.p_ates_elec[y, s]
        else:
            return m.v_ates_c_fix[y, s] == (m.v_ates_k_inv[y, s] * m.p_ates_c_inv[y, s] + m.v_ates_hp_Q_inv[y, s] * m.p_hp_c_inv[y, s]) * 0.02 + m.v_ates_k_thermal_max[y, s] * m.p_c_mean_elec[y, s] * m.p_ates_elec[y, s]
    
    def ates_c_var(m, y, t, s):
        return m.v_ates_c_var[y, t, s] == m.v_ates_q_elec_consumption[y, t, s] * m.p_c_elec[y, t, s] + (m.v_ates_q_thermal_in[y, t, s] + m.v_ates_q_thermal_out[y, t, s]) * m.p_ates_c_charge_discharge[y, s] # + m.v_c_opam[y, s]

    m.con_ates_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                 rule = ates_feed_in_max_bound)
    
    m.con_ates_storage_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                 rule = ates_storage_max_bound)
    
    m.con_ates_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                         rule = ates_elec_heat)
    
    m.con_ates_soc_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                             rule = ates_soc_max_bound)
    
    m.con_ates_soc = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = ates_soc)
        
    m.con_ates_soc_final = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                         rule = ates_soc_final)
        
    m.con_ates_k_inv = py.Constraint(m.set_years, m.set_scenarios,
                                     rule = ates_k_inv)
    
    m.con_ates_hp_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                        rule = ates_hp_Q_inv)
    
    m.con_ates_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                     rule = ates_c_inv)
    
    m.con_ates_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                     rule = ates_c_fix)
    
    m.con_ates_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                     rule = ates_c_var)

def add_ates_variables(m=None):
    """This section defines the variables for ATES"""
    m.v_ates_q_thermal_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                   domain = py.NonNegativeReals,
                                   doc = 'thermal energy feed in per scenario, year and hour')
    
    m.v_ates_q_thermal_out = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                    domain = py.NonNegativeReals,
                                    doc = 'thermal energy storing per scenario, year and hour')
    
    m.v_ates_Q_thermal_max = py.Var(m.set_years, m.set_scenarios,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum thermal energy feed in per scenario and year')
    
    m.v_ates_hp_Q_max = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'maximum thermal energy storing per scenario and year')
    
    m.v_ates_k_thermal = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                domain = py.NonNegativeReals,
                                doc = 'state of charge per scenario, year and hour')
    
    m.v_ates_k_thermal_max = py.Var(m.set_years, m.set_scenarios,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum state of charge per scenario, year and hour')
    
    m.v_ates_q_elec_consumption = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                         domain = py.NonNegativeReals,
                                         doc = 'electricity input of heat pump per scenario, year and hour')
   
    m.v_ates_k_inv = py.Var(m.set_years, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'new installed capacity of ATES per scenario and year in EUR')
   
    m.v_ates_hp_Q_inv = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'new installed capacity of hp for ATES per scenario and year in EUR')
    
    m.v_ates_c_inv = py.Var(m.set_years, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'inv costs of ATES per scenario and year in EUR')
    
    m.v_ates_c_fix = py.Var(m.set_years, m.set_scenarios,
                            domain = py.Reals,
                            doc = 'fix costs of ATES per scenario and year in EUR')
    
    m.v_ates_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                            domain = py.Reals,
                            doc = 'var costs of ATES per scenario, year and hour in EUR')
    
def add_ates_parameters(m=None):
    """This section defines the parameters for ATES"""
    
    def init_ates_losses(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_losses']
    
    def init_ates_eta(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_eta']
    
    def init_ates_init(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_init']
    
    def init_ates_end(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_end']
    
    def init_ates_c_inv(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_c_inv']

    def init_ates_elec(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_elec']
    
    def init_ates_cop(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_cop']
    
    def init_ates_c_charge_discharge(m, y, s):
        return m.data_values[s]['ates'][y]['p_ates_c_charge_discharge']
    
    m.p_ates_losses = py.Param(m.set_years, m.set_scenarios,
                               initialize = init_ates_losses,
                               within = py.NonNegativeReals,
                               doc = 'losses of the storage')
    
    m.p_ates_eta = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_ates_eta,
                            within = py.NonNegativeReals,
                            doc = 'efficiency of the storage')
    
    m.p_ates_init = py.Param(m.set_years, m.set_scenarios,
                             initialize = init_ates_init,
                             within = py.NonNegativeReals,
                             doc = 'initial soc of the storage')
    
    m.p_ates_end = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_ates_end,
                            within = py.NonNegativeReals,
                            doc = 'final soc of the storage')
    
    m.p_ates_c_inv = py.Param(m.set_years, m.set_scenarios,
                              initialize = init_ates_c_inv,
                              within = py.NonNegativeReals,
                              doc = 'specific investment costs of ATES')
    
    m.p_ates_elec = py.Param(m.set_years, m.set_scenarios,
                             initialize = init_ates_elec,
                             within = py.NonNegativeReals,
                             doc = 'electricity share of thermal energy')
    
    m.p_ates_cop = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_ates_cop,
                            within = py.NonNegativeReals,
                            doc = 'cop of the storage')
    
    m.p_ates_c_charge_discharge = py.Param(m.set_years, m.set_scenarios,
                                           initialize = init_ates_c_charge_discharge,
                                           within = py.NonNegativeReals,
                                           doc = 'charge/discharge price per scenario, year and hour')
    
    # m.p_c_opam = py.Param( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per scenario, year and hour'
    #     )