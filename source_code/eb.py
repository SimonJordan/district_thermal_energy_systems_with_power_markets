import pyomo.environ as py

def add_eb_equations(m=None):

    def eb_feed_in_max_bound(m, y, t, s):
        return m.v_eb_q_heat_in[y, t, s] <= m.v_eb_Q_heat_max[y, s]
    
    # def test(m, y, s):
    #     return m.v_eb_Q_heat_max[y, s] <= 800
    
    def eb_elec_heat(m, y, t, s):
        return m.v_eb_q_heat_in[y, t, s] == m.v_eb_q_elec_in[y, t, s] * m.p_eb_eta[y, s]
    
    def eb_Q_inv(m, y, s):
        if (y - 5) in m.set_years:
            return m.v_eb_Q_inv[y, s] == (m.v_eb_Q_heat_max[y, s] - m.v_eb_Q_heat_max[y-5, s])
        else:
            return m.v_eb_Q_inv[y, s] == m.v_eb_Q_heat_max[y, s]
    
    def eb_c_inv(m, y, s):
        return m.v_eb_c_inv[y, s] == m.v_eb_Q_inv[y, s] * m.p_eb_c_inv[y, s]
    
    def eb_c_fix(m, y, s):
        return m.v_eb_c_fix[y, s] == m.v_eb_Q_heat_max[y, s] * m.p_eb_c_fix[y, s]
        
    def eb_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        return m.v_eb_c_var[y, t, s] == m.v_eb_q_elec_in[y, t, s] * m.p_c_elec[y, t, s]
        
    m.con_eb_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = eb_feed_in_max_bound)
    
    m.con_eb_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                       rule = eb_elec_heat)
    
    m.con_eb_Q_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = eb_Q_inv)
    
    m.con_eb_c_inv = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = eb_c_inv)
    
    m.con_eb_c_fix = py.Constraint(m.set_years, m.set_scenarios,
                                   rule = eb_c_fix)
    
    m.con_eb_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                   rule = eb_c_var)
    
    # m.con_test = py.Constraint(m.set_years, m.set_scenarios,
    #                            rule = test)

def add_eb_variables(m=None):
    
    m.v_eb_q_heat_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'heat energy feed in from electric boiler per scenario, year, and hour')
    
    m.v_eb_q_elec_in = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                              domain = py.NonNegativeReals,
                              doc = 'electricity input of electric boiler per scenario, year, and hour')
    
    m.v_eb_Q_heat_max = py.Var(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'max heat feed in from electric boiler for district heating')
    
    m.v_eb_Q_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'istalled TTES capacity per scenario and year in EUR')
   
    m.v_eb_c_inv = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'inv costs of eb per scenario and year in EUR')
    
    m.v_eb_c_fix = py.Var(m.set_years, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'fix costs of eb per scenario and year in EUR')
    
    m.v_eb_c_var = py.Var(m.set_years, m.set_hours, m.set_scenarios,
                          domain = py.NonNegativeReals,
                          doc = 'var costs of eb per scenario, year and hour in EUR')

def add_eb_parameters(m=None):
    
    def init_eb_eta(m, y, s):
        return m.data_values[s]['eb'][y]['p_eb_eta']
    
    def init_eb_c_inv(m, y, s):
        return m.data_values[s]['eb'][y]['p_eb_c_inv']
    
    def init_eb_c_fix(m, y, s):
        return m.data_values[s]['eb'][y]['p_eb_c_fix']
    
    def init_c_elec(m, y, t, s):
        return m.data_values[s]['electricity_price'][y][t]
    
    def init_c_mean_elec(m, y, s):
        return m.data_values[s]['electricity_mean_price'][y]
    
    m.p_eb_eta = py.Param(m.set_years, m.set_scenarios,
                          initialize = init_eb_eta,
                          within = py.NonNegativeReals,
                          doc = 'electrical efficiency of the eb')
    
    m.p_eb_c_inv = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_eb_c_inv,
                            within = py.NonNegativeReals,
                            doc = 'specific inv cost of eb')
    
    m.p_eb_c_fix = py.Param(m.set_years, m.set_scenarios,
                            initialize = init_eb_c_fix,
                            within = py.NonNegativeReals,
                            doc = 'fixed cost of eb')
    
    m.p_c_elec = py.Param(m.set_years, m.set_hours, m.set_scenarios,
                          initialize = init_c_elec,
                          within = py.Reals,
                          doc = 'specific electriyity prices year hour and scenario')

    m.p_c_mean_elec = py.Param(m.set_years, m.set_scenarios,
                               initialize = init_c_mean_elec,
                               within = py.Reals,
                               doc = 'mean electriyity prices year and scenario')

    # m.p_c_opam = py.Param( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )