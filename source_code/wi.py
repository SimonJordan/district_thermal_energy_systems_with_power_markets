import pyomo.environ as py

def add_wi_equations(m=None):
    #max waste per year
    def wi_feed_in_max_bound(m, y, t, s):
        m.v_wi_q_heat_in[y, t, s] <= m.v_wi_Q_heat_max[y, s]
    
    def wi_waste_heat(m, y, t, s):
        m.v_wi_q_heat_in[y, t, s] == m.v_wi_q_waste_in[y, t, s] * m.f_wi_eta
        
    def wi_q_co2(m, y, t, s):
        m.v_wi_q_co2[y, t, s] == m.v_wi_q_waste_in[y, t, s] * m.f_wi_eta_co2
    
    def wi_elec(m, y, t, s):
        m.v_wi_q_elec_in[y, t, s] ==  m.v_wi_q_heat_in[y, t, s] * m.f_wi_eta_el[t]
    
    def wi_c_fix(m, y, t, s): 
        m.v_wi_c_fix(y, s) == (m.v_wi_Q_heat_max[y, s] - m.v_wi_Q_heat_max[y-1, s]) * m.v_wi_c_inv(y, s)
        
    def wi_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        m.v_wi_c_var(y, s) == m.v_wi_q_waste_in[y, t, s] * m.v_c_waste[y, t, s] + m.v_c_opam[y, s] 
        + m.v_wi_q_elec_in[y, t, s] * m.v_c_elec[y, t, s] + m.v_wi_q_co2[y, t, s] * m.v_c_co2[y, t, s]

def add_wi_variables(m=None):
    
    m.v_wi_q_heat_in = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'heat energy feed in from WI per scenario, year, and hour'
    )
    m.v_wi_q_waste_in = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'wast input of WI per scenario, year, and hour'
    )
    m.v_wi_Q_heat_max = py.Variable(
        m.set_scenarios * m.set_years,
        domain = py.NonNegativeReals,
        doc = 'max heat feed in from WI for district heating'
    ) 
    m.v_wi_c_fix = py.Variable(
        m.set_years[1:] * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'Fix cost wi per heat in EUR'
    )
    m.v_wi_c_var = py.Variable(
        m.set_years * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'var cost wi per heat in EUR'
    )
    m.v_wi_q_co2= py.Variable(
        m.set_years * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'var quantity of co2 for wi per ton waste in EUR'
    )
def add_wi_parameters(m=None):
    m.f_wi_eta_el = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_hours,
        within = py.NonNegativeReals,
        doc = 'electric efficiency of the wi'
    )
    m.f_wi_eta = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'efficiency of the wi'
    )
    m.f_wi_eta_co2 = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'co2 output for waste input of the wi'
    )
    m.v_wi_c_inv =py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'specific inv cost of wi'
        )
    m.v_c_elec=py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'specific electrisity prices year hour and scenario'
        )
    m.v_c_waste=py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'specific waste prices year hour and scenario'
        )
    m.v_c_co2=py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'specific co2 prices year hour and scenario'
        )
    m.v_c_opam=py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'Operational and Maintanance cost per year and scenario'
        )