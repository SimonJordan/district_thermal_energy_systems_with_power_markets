import pyomo.environ as py

def add_wi_equations(m=None):

    def wi_feed_in_max_bound(m, y, t, s):
        return m.v_wi_q_heat_in[y, t, s] + m.v_wi_q_elec_in[y, t, s] <= m.v_wi_Q_mix_max[y, s]
    
    def wi_waste_heat(m, y, t, s):
        return m.v_wi_q_heat_in[y, t, s] == m.p_wi_q_waste[y, s] * m.p_wi_eta[y, s] * m.p_wi_h_waste[y, s] * m.p_wi_heat[y, s] * m.v_wi_p_scale[y, t, s]
        
    def wi_waste_elec(m, y, t, s):
        return m.v_wi_q_elec_in[y, t, s] == m.p_wi_q_waste[y, s] * m.p_wi_eta[y, s] * m.p_wi_h_waste[y, s] * m.p_wi_elec[y, s] * m.v_wi_p_scale[y, t, s]
    
    def wi_p_scale(m, y, t, s):
        return m.v_wi_p_scale[y, t, s] <= 1
    
    def wi_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_wi_Q_inv[y, s] == (m.v_wi_Q_mix_max[y, s] - m.v_wi_Q_mix_max[y-5, s])
        else:
            return m.v_wi_Q_inv[y, s] == m.v_wi_Q_mix_max[y, s]
    
    def wi_c_inv(m, y, s):
        return m.v_wi_c_inv[y, s] == m.v_wi_Q_inv[y, s] * m.p_wi_c_inv[y, s]
   
    def wi_c_fix(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_wi_c_fix[y, s] == m.v_wi_c_fix[y-5, s] + m.v_wi_Q_inv[y, s] * m.p_wi_c_inv[y, s] * 0.02
        else:
            return m.v_wi_c_fix[y, s] == m.v_wi_Q_inv[y, s] * m.p_wi_c_inv[y, s] * 0.02
    
    def wi_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_wi_c_var[y, t, s] == m.p_wi_q_waste[y, s] * m.p_wi_c_waste[y, s] * m.v_wi_p_scale[y, t, s] + m.p_wi_q_waste[y, s] * m.p_wi_co2_share[y, s] * m.p_c_co2[y, s] * m.v_wi_p_scale[y, t, s] - m.v_wi_q_elec_in[y, t, s] * m.p_c_elec[y, t, s]
    
    m.con_wi_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = wi_feed_in_max_bound)
    
    m.con_wi_waste_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                        rule = wi_waste_heat)
    
    m.con_wi_waste_elec = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                        rule = wi_waste_elec)
    
    m.con_wi_p_scale = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                     rule = wi_p_scale)
        
    m.con_wi_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = wi_Q_inv)
    
    m.con_wi_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = wi_c_inv)
    
    m.con_wi_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = wi_c_fix)
    
    m.con_wi_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = wi_c_var)

def add_wi_variables(m=None):
    
    m.v_wi_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from waste incineration per scenario, year and hour')

    m.v_wi_q_elec_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'electricity feed in from waste incineration per scenario, year and hour')
    
    m.v_wi_p_scale = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                            domain = py.NonNegativeReals,
                            doc = 'scale size of waste incineration per scenario, year and hour')

    m.v_wi_Q_mix_max = py.Var(m.set_years, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'max energy feed in from waste incineration per scenario, year and hour')
    
    m.v_wi_Q_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'new installed power of waste incineration per scenario and year')
   
    m.v_wi_c_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of wi per scenario and year in EUR')

    m.v_wi_c_fix = py.Var(m.set_years, m.set_scenarios,
                         domain = py.NonNegativeReals,
                         doc = 'fix costs of wi per scenario and year in EUR')
    
    m.v_wi_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                          domain = py.Reals,
                          doc = 'var costs of wi per scenario, year and hour in EUR')
    
def add_wi_parameters(m=None):

    def init_wi_eta(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_eta']
    
    def init_wi_q_waste(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_q_waste']
    
    def init_wi_c_waste(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_c_waste']
    
    def init_wi_h_waste(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_h_waste']
    
    def init_wi_heat(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_heat']
    
    def init_wi_elec(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_elec']
    
    def init_wi_co2_share(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_co2_share']
        
    def init_wi_c_inv(m, y, s):
        return m.data_values[s]['wi'][y]['p_wi_c_inv']
    
    m.p_wi_eta = py.Param(m.set_years, m.set_scenarios,
                          initialize = init_wi_eta,
                          within = py.NonNegativeReals,
                          doc = 'efficiency of the wi')
    
    m.p_wi_q_waste = py.Param(m.set_years, m.set_scenarios,
                              initialize = init_wi_q_waste,
                              within = py.NonNegativeReals,
                              doc = 'amount of waste for wi')
    
    m.p_wi_c_waste = py.Param(m.set_years, m.set_scenarios,
                              initialize = init_wi_c_waste,
                              within = py.NonNegativeReals,
                              doc = 'price of waste for wi')
    
    m.p_wi_h_waste = py.Param(m.set_years, m.set_scenarios,
                              initialize = init_wi_h_waste,
                              within = py.NonNegativeReals,
                              doc = 'calorific value of waste for wi')
    
    m.p_wi_heat = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_wi_heat,
                            within = py.NonNegativeReals,
                            doc = 'share of heat output of the wi')
    
    m.p_wi_elec = py.Param(m.set_years, m.set_scenarios,
                           initialize = init_wi_elec,
                           within = py.NonNegativeReals,
                           doc = 'share of electric output of the wi')
    
    m.p_wi_co2_share = py.Param(m.set_years, m.set_scenarios,
                                initialize = init_wi_co2_share,
                                within = py.NonNegativeReals,
                                doc = 'share of CO2 of the waste for wi')
        
    m.p_wi_c_inv = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_wi_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv cost of wi')
    
    # m.p_c_opam=py.Param( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )