import pyomo.environ as py

def add_hp_equations(m=None):

    def hp_feed_in_max_bound(m, y, t, s):
        m.v_hp_q_heat_in[y, t, s] <= m.v_hp_Q_heat_max[y, s]
    
    def hp_elec_cop_heat(m, y, t, s):
        m.v_hp_q_heat_in[y, t, s] == m.v_hp_q_elec_in[y, t, s] * m.p_hp_cop[t] *m.p_hp_eta
     
    def hp_c_fix(m, y, t, s): #y=0 berücksichtigen fehlt, größer gleich im vergleich zum vorjahr
        if (y - 5) in m.set_years:
            return m.v_hp_c_fix[y, s] == (m.v_hp_Q_heat_max[y, s] - m.v_hp_Q_heat_max[y-5, s]) * m.p_hp_c_inv[y, s]
        else:
            return m.v_hp_c_fix[y, s] == m.v_hp_Q_heat_max[y, s] * m.p_hp_c_inv[y, s]    
          
    def hp_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        m.v_hp_c_var(y, s) == m.v_hp_q_elec_in[y, t, s] * m.p_c_elec[y, t, s] + m.p_c_opam[y, s]


    m.con_hp_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = hp_feed_in_max_bound)
    m.con_hp_elec_cop_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = hp_elec_cop_heat)
    m.con_hp_c_fix = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = hp_c_fix)
    m.con_hp_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = hp_c_var)

def add_hp_variables(m=None):
    
    m.v_hp_q_heat_in = py.Variable(m.set_years, m.set_hours, m.set_scenarios,
                                   domain = py.NonNegativeReals,
                                   doc = 'heat energy feed in from large-scale heat pump per scenario, year, and hour')
    
    m.v_hp_q_elec_in = py.Variable(m.set_scenarios, m.set_years, m.set_hours, 
                                   domain = py.NonNegativeReals,
                                   doc = 'electricity input of large-scale heat pump per scenario, year, and hour')
    
    m.v_hp_Q_heat_max = py.Variable(m.set_scenarios, m.set_years,
                                    domain = py.NonNegativeReals,
                                    doc = 'max heat feed in from large-scale heat pump for district heating') 
    
    m.v_hp_c_fix = py.Variable(m.set_years[1:], m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'Fix cost hp per hear in EUR')
    m.v_hp_c_var = py.Variable(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'var cost hp per hear in EUR')

def add_hp_parameters(m=None):
    
    def init_hp_cop(m, y, s):
        return m.data_values[s][2][y]['p_hp_cop']
    
    def init_hp_eta(m, y, s):
        return m.data_values[s][2][y]['p_hp_eta']
    
    def init_hp_c_inv(m, y, s):
        return m.data_values[s][2][y]['p_hp_c_inv']
    
    def init_c_elec(m, y, t, s):
        return m.data_values[s][1][y][1][t]
    
    m.p_hp_cop = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_hours,
        within = py.NonNegativeReals,
        doc = 'coefficient of performance of the large-scale heat pump'
    )
    # m.p_hp_min_ratio_hp = py.Parameter( #Einlesen von Inputs fehlt!
    #     within = py.NonNegativeReals,
    #     doc = 'ratio of min cap around 10-20%'
    # )
    m.p_hp_eta = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'electrical efficiency of the hp'
    )
    m.p_hp_c_inv =py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'specific inv cost of heatpumps'
        )
    m.p_c_elec( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'specific electriyity prices year hour and scenario'
        )
    # m.p_c_opam( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )