import pyomo.environ as py

def add_st_equations(m=None):

    def st_feed_in_max_bound(m, y, t, s):
        return m.v_st_q_heat_in[y, t, s] <= m.v_st_Q_heat_max[y, s]
    
    def st_elec_cop_heat(m, y, t, s):
        return m.v_st_q_heat_in[y, t, s] == m.v_st_q_elec_in[y, t, s] * m.p_st_cop[t] *m.p_st_eta #2 wirkungsgrade beachten (WP und LT el verbrauch)
    
    def st_c_fix(m, y, t, s): #y=0 berücksichtigen fehlt, größer gleich im vergleich zum vorjahr
        if (y - 5) in m.set_years:
            return m.v_st_c_fix[y, s] == (m.v_st_Q_heat_max[y, s] - m.v_st_Q_heat_max[y-5, s]) * m.p_st_c_inv[y, s]
        else:
            return m.v_st_c_fix[y, s] == m.v_st_Q_heat_max[y, s] * m.p_st_c_inv[y, s]
        
    def st_c_var(m, y, t, s): 
        return m.v_st_c_var(y, s) == m.v_st_q_elec_in[y, t, s] * m.v_st_q_elec_in[y, t, s]
      
    m.con_st_feed_in_max_bound = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = st_feed_in_max_bound)
    m.con_st_elec_heat = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = st_elec_cop_heat)
    m.con_st_c_fix = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = st_c_fix)
    m.con_st_c_var = py.Constraint(m.set_years, m.set_hours, m.set_scenarios,
                                               rule = st_c_var)
       
        

def add_st_variables(m=None):
    
    m.v_st_q_heat_in = py.Variable(m.set_scenarios, m.set_years, m.set_hours,
                                   domain = py.NonNegativeReals,
                                   doc = 'heat energy feed in from solar thermal per scenario, year, and hour')
    m.v_st_q_elec_in = py.Variable(m.set_scenarios, m.set_years, m.set_hours,
                                   domain = py.NonNegativeReals,
                                   doc = 'electricity input of solar thermal per scenario, year, and hour')
    m.v_st_Q_heat_max = py.Variable(m.set_scenarios, m.set_years,
                                    domain = py.NonNegativeReals,
                                    doc = 'max heat feed in from solar thermal for district heating') 
    m.v_st_c_fix = py.Variable(m.set_years[1:], m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'Fix cost st per heat in EUR')
    m.v_st_c_var = py.Variable(m.set_years, m.set_scenarios,
                               domain = py.NonNegativeReals,
                               doc = 'var cost st per heat in EUR')

def add_st_parameters(m=None):
    
    def init_st_cop(m, y, s):
        return m.data_values[s][2][y]['p_st_cop'] #Genaues einlesen muss noch geändert werden
    
    def init_st_c_inv(m, y, s):
        return m.data_values[s][2][y]['p_st_c_inv'] #Genaues einlesen muss noch geändert werden
    
    def init_c_elec(m, y, t, s):
        return m.data_values[s][1][y][1][t]
    
    m.p_st_cop = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_hours,
        within = py.NonNegativeReals,
        doc = 'coefficient of performance of the solar thermal'
    )
    m.p_st_eta = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'electrical efficiency of the st'
    )
    m.p_st_c_inv =py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'specific inv cost of st'
        )
    m.p_c_elec=py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'specific electriyity prices year hour and scenario'
        )
    # m.v_c_opam=py.Parameter( #Einlesen von Inputs fehlt!
    #     m.set_years * m.set_scenarios,
    #     within = py.NonNegativeReals,
    #     doc = 'Operational and Maintanance cost per year and scenario'
    #     )