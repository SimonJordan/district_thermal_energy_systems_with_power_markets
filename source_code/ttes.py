import pyomo.environ as py

def add_ttes_equations(m=None):
    
    def ttes_feed_in_max_bound(m, y, t, s):
        return m.v_ttes_q_thermal_in[y, t, s] <= m.v_ttes_Q_thermal_max[y, s]# * m.b_ttes_in[y, t, s]

    def ttes_storage_max_bound(m, y, t, s):
        return m.v_ttes_q_thermal_out[y, t, s] <= m.v_ttes_Q_thermal_max[y, s]# * m.b_ttes_out[y, t, s]

    # def ttes_balance_penalty(m, y, t, s):
    #     return m.v_ttes_c_penalty[y, t, s] == m.v_ttes_in_out_diff[y, t, s] * 10e12

    # def ttes_abs_diff_1(m, y, t, s):
    #     return m.v_ttes_in_out_diff[y, t, s] >= m.v_ttes_q_thermal_in[y, t, s] - m.v_ttes_q_thermal_out[y, t, s]
    
    # def ttes_abs_diff_2(m, y, t, s):
    #     return m.v_ttes_in_out_diff[y, t, s] >= m.v_ttes_q_thermal_out[y, t, s] - m.v_ttes_q_thermal_in[y, t, s]

    # def ttes_balance_in_out(m, y, t, s):
    #     return m.b_ttes_in[y, t, s] + m.b_ttes_out[y, t, s] <= 1

    def ttes_soc_max_bound_1(m, y, t, s):
        return m.v_ttes_k_thermal[y, t, s] <= m.v_ttes_k_thermal_max[y, s]
    
    def ttes_soc_max_bound_2(m, y, t, s):
        return m.v_ttes_q_thermal_in[y, t, s] <= m.v_ttes_k_thermal_max[y, s]
    
    def ttes_soc_max_bound_3(m, y, t, s):
        return m.v_ttes_q_thermal_out[y, t, s] <= m.v_ttes_k_thermal_max[y, s]

    def ttes_soc(m, y, t, s):#cop abhängig von temp/soc des speichers von 30 bis 90 grad celsius
        if t == 0:
            cop_init = 1#(273.15 + 150)/(273.15 + 150 - (273.15 + 60 * m.v_ttes_k_thermal[y, 0, s] / m.v_ttes_k_thermal_max[y, s] + 30))
            return m.v_ttes_k_thermal[y, 0, s] == m.v_ttes_k_thermal_max[y, s] * m.p_ttes_losses[y, s] * m.p_ttes_init[y, s] + m.v_ttes_q_thermal_out[y, 0, s] * m.p_ttes_eta[y, s] - m.v_ttes_q_thermal_in[y, 0, s] * cop_init / m.p_ttes_eta[y, s]
        else:
            cop_cur = 1#(273.15 + 150)/(273.15 + 150 - (273.15 + 60 * m.v_ttes_k_thermal[y, t-1, s] / m.v_ttes_k_thermal_max[y, s] + 30))
            return m.v_ttes_k_thermal[y, t, s] == m.v_ttes_k_thermal[y, t-1, s] * m.p_ttes_losses[y, s] + m.v_ttes_q_thermal_out[y, t, s] * m.p_ttes_eta[y, s] - m.v_ttes_q_thermal_in[y, t, s] * cop_cur / m.p_ttes_eta[y, s]

    #def ttes_soc_init(m, y, t, s):#cop abhängig von temp/soc des speichers
        
    def ttes_soc_final(m, y, t, s):
        return m.v_ttes_k_thermal[y, 8759, s] == m.v_ttes_k_thermal_max[y, s] * m.p_ttes_end[y, s]

    def ttes_c_fix(m, y, t, s):
        if (y - 5) in m.set_years:
            return m.v_ttes_c_fix[y, s] == (m.v_ttes_k_thermal_max[y, s] - m.v_ttes_k_thermal_max[y-5, s]) * m.p_ttes_c_inv[y, s]
        else:
            return m.v_ttes_c_fix[y, s] == m.v_ttes_k_thermal_max[y, s] * m.p_ttes_c_inv[y, s]
    
    def ttes_c_var(m, y, t, s):
        return m.v_ttes_c_var[y, s] == m.v_ttes_k_thermal_max[y, s] * m.p_c_elec[y, t, s] * m.p_ttes_elec[y, s]# + m.v_c_opam[y, s] + (m.v_ttes_q_thermal_in[y, t, s] + m.v_ttes_q_thermal_out[y, t, s]) * m.p_ttes_c_charge_discharge[y, t, s]

    m.con_ttes_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                 rule = ttes_feed_in_max_bound)
    
    m.con_ttes_storage_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                 rule = ttes_storage_max_bound)
    
    # m.con_ttes_balance_penalty = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
    #                                            rule = ttes_balance_penalty)
    
    # m.con_ttes_abs_diff_1 = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
    #                                       rule = ttes_abs_diff_1)
    
    # m.con_ttes_abs_diff_2 = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
    #                                       rule = ttes_abs_diff_2)
    
    # m.con_ttes_balance_in_out = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
    #                                       rule = ttes_balance_in_out)
    
    m.con_ttes_soc_max_bound_1 = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                             rule = ttes_soc_max_bound_1)
    
    m.con_ttes_soc_max_bound_2 = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                             rule = ttes_soc_max_bound_2)
    
    m.con_ttes_soc_max_bound_3 = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                             rule = ttes_soc_max_bound_3)
    
    m.con_ttes_soc = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = ttes_soc)
    
    # m.con_ttes_soc_init = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
    #                                     rule = ttes_soc_init)
    
    m.con_ttes_soc_final = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                         rule = ttes_soc_final)
    
    m.con_ttes_c_fix = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
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
                                    doc = 'maximum thermal energy feed in/storing per scenario and year')
    
    m.v_ttes_k_thermal = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                                domain = py.NonNegativeReals,
                                doc = 'state of charge per scenario, year and hour')
    
    m.v_ttes_k_thermal_max = py.Var(m.set_years, m.set_scenarios,
                                    domain = py.NonNegativeReals,
                                    doc = 'maximum state of charge per scenario, year and hour')
    
    m.v_ttes_c_fix = py.Var(m.set_years, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'fix costs of TTES per year in EUR')
    
    m.v_ttes_c_var = py.Var(m.set_years, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'var costs of TTES per year in EUR')
    
    # m.v_ttes_c_penalty = py.Var(m.set_years, m.set_hours, m.set_scenarios,
    #                             domain = py.NonNegativeReals,
    #                             doc = 'penalty costs of TTES in EUR')
    
    # m.v_ttes_in_out_diff = py.Var(m.set_years, m.set_hours, m.set_scenarios,
    #                               domain = py.NonNegativeReals,
    #                               doc = 'difference between feed in and storage')
    
    # m.b_ttes_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
    #               domain = py.Binary)
    
    # m.b_ttes_out = py.Var(m.set_years, m.set_hours, m.set_scenarios,
    #                       domain = py.Binary)


def add_ttes_parameters(m=None):
    """This section defines the parameters for TTES"""
    
    def init_ttes_losses(m, y, s):
        return m.data_values[s][3][y]['p_ttes_losses']
    
    def init_ttes_eta(m, y, s):
        return m.data_values[s][3][y]['p_ttes_eta']
    
    def init_ttes_init(m, y, s):
        return m.data_values[s][3][y]['p_ttes_init']
    
    def init_ttes_end(m, y, s):
        return m.data_values[s][3][y]['p_ttes_end']
    
    def init_ttes_c_inv(m, y, s):
        return m.data_values[s][3][y]['p_ttes_c_inv']

    def init_ttes_elec(m, y, s):
        return m.data_values[s][3][y]['p_ttes_elec']
    
    def init_c_elec(m, y, t, s):
        return m.data_values[s][1][y][1][t]    
    
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
                             within = py.Reals,
                             doc = 'electricity share of thermal energy')
    
    # m.p_c_elec = py.Param(m.set_years, m.set_hours, m.set_scenarios,
    #                       initialize = init_c_elec,
    #                       within = py.Reals,
    #                       doc = 'specific electriyity prices year hour and scenario')

    # m.p_ttes_cop = py.Param( #Einlesen von Inputs fehlt! #cop abhängig von temp/soc des speichers
    #     within = py.NonNegativeReals,
    #     doc = 'cop of the storage'
    #     )
    # m.p_c_opam = py.Param( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per scenario, year and hour'
    #     )
    # m.p_ttes_c_charge_discharge = py.Param( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios * m.set_hours,
    #     within = py.Reals,
    #     doc = 'charge/discharge price per scenario, year and hour'
    #     )