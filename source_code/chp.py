import pyomo.environ as py

def add_chp_equations(m=None):

    def chp_feed_in_max_bound(m, y, t, s):
        return m.v_chp_q_heat_in[y, t, s] + m.v_chp_q_elec_in[y, t, s] <= m.v_chp_Q_mix_max[y, s]
    
    def chp_gas_heat(m, y, t, s):
        return m.v_chp_q_heat_in[y, t, s] == m.v_chp_q_gas[y, t, s] * m.p_chp_eta[y, s] * m.p_chp_heat[y, s]
        
    def chp_gas_elec(m, y, t, s):
        return m.v_chp_q_elec_in[y, t, s] == m.v_chp_q_gas[y, t, s] * m.p_chp_eta[y, s] * m.p_chp_elec[y, s]
    
    def chp_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_chp_Q_inv[y, s] == (m.v_chp_Q_mix_max[y, s] - m.v_chp_Q_mix_max[y-5, s])
        else:
            return m.v_chp_Q_inv[y, s] == m.v_chp_Q_mix_max[y, s]
    
    def chp_c_inv(m, y, s):
        return m.v_chp_c_inv[y, s] == m.v_chp_Q_inv[y, s] * m.p_chp_c_inv[y, s]
   
    def chp_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_chp_c_fix[y, s] == m.v_chp_c_fix[y-5, s] + m.v_chp_Q_inv[y, s] * m.p_chp_c_inv[y, s] * 0.02
        else:
            return m.v_chp_c_fix[y, s] == m.v_chp_Q_inv[y, s] * m.p_chp_c_inv[y, s] * 0.02
    
    def chp_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_chp_c_var[y, t, s] == m.v_chp_q_gas[y, t, s] * m.p_c_gas[y, t, s] + m.v_chp_q_gas[y, t, s] / m.p_chp_h_gas[y, s] * m.p_chp_co2_share[y, s] * m.p_c_co2[y, s] - m.v_chp_q_elec_in[y, t, s] * m.p_c_elec[y, t, s]
    
    m.con_chp_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                                rule = chp_feed_in_max_bound)
    
    m.con_chp_gas_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                       rule = chp_gas_heat)
    
    m.con_chp_gas_elec = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                       rule = chp_gas_elec)
            
    m.con_chp_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                    rule = chp_Q_inv)
    
    m.con_chp_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                    rule = chp_c_inv)
    
    m.con_chp_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                    rule = chp_c_fix)
    
    m.con_chp_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                    rule = chp_c_var)

def add_chp_variables(m=None):
    
    m.v_chp_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from combined heat and power per scenario, year and hour')

    m.v_chp_q_elec_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'electricity feed in from combined heat and power per scenario, year and hour')

    m.v_chp_q_gas = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                           domain = py.NonNegativeReals,
                           doc = 'gas consumption from combined heat and power per scenario, year and hour')

    m.v_chp_Q_mix_max = py.Var(m.set_years, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'max energy feed in from combined heat and power per scenario, year and hour')
    
    m.v_chp_Q_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'new installed power of combined heat and power per scenario and year')
   
    m.v_chp_c_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of chp per scenario and year in EUR')

    m.v_chp_c_fix = py.Var(m.set_years, m.set_scenarios,
                         domain = py.NonNegativeReals,
                         doc = 'fix costs of chp per scenario and year in EUR')
    
    m.v_chp_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                          domain = py.Reals,
                          doc = 'var costs of chp per scenario, year and hour in EUR')
    
def add_chp_parameters(m=None):

    def init_chp_eta(m, y, s):
        return m.data_values[s]['chp'][y]['p_chp_eta']
       
    def init_chp_h_gas(m, y, s):
        return m.data_values[s]['chp'][y]['p_chp_h_gas']
    
    def init_chp_heat(m, y, s):
        return m.data_values[s]['chp'][y]['p_chp_heat']
    
    def init_chp_elec(m, y, s):
        return m.data_values[s]['chp'][y]['p_chp_elec']
    
    def init_chp_co2_share(m, y, s):
        return m.data_values[s]['chp'][y]['p_chp_co2_share']
        
    def init_chp_c_inv(m, y, s):
        return m.data_values[s]['chp'][y]['p_chp_c_inv']
    
    m.p_chp_eta = py.Param(m.set_years, m.set_scenarios,
                           initialize = init_chp_eta,
                           within = py.NonNegativeReals,
                           doc = 'efficiency of the chp')
    
    m.p_chp_h_gas = py.Param(m.set_years, m.set_scenarios,
                             initialize = init_chp_h_gas,
                             within = py.NonNegativeReals,
                             doc = 'calorific value of gas for chp')
    
    m.p_chp_heat = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_chp_heat,
                            within = py.NonNegativeReals,
                            doc = 'share of heat output of the chp')
    
    m.p_chp_elec = py.Param(m.set_years, m.set_scenarios,
                           initialize = init_chp_elec,
                           within = py.NonNegativeReals,
                           doc = 'share of electric output of the chp')
    
    m.p_chp_co2_share = py.Param(m.set_years, m.set_scenarios,
                                initialize = init_chp_co2_share,
                                within = py.NonNegativeReals,
                                doc = 'share of CO2 of the gas for chp')
        
    m.p_chp_c_inv = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_chp_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv cost of chp')
    
    # m.p_c_opam=py.Param( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )