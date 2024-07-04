import pyomo.environ as py #komplett neu machen. nur eb in ieh umgewaNDELT

def add_ieh_equations(m=None):

    def ieh_feed_in_max_bound(m, y, t, s):
        m.v_ieh_q_heat_in[y, t, s] <= m.v_ieh_Q_heat_max[y, s]
    
    def ieh_elec_heat(m, y, t, s):
        m.v_ieh_q_heat_in[y, t, s] == m.v_ieh_q_elec_in[y, t, s] * m.f_ieh_eta
        
    def ieh_c_fix(m, y, t, s): #y=0 berücksichtigen fehlt, größer gleich im vergleich zum vorjahr
        m.v_ieh_c_fix(y, s) == (m.v_ieh_Q_heat_max[y, s] - m.v_ieh_Q_heat_max[y-1, s]) * m.v_ieh_c_inv(y, s)
        
    def ieh_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        m.v_ieh_c_var(y, s) == m.v_ieh_q_elec_in[y, t, s] * m.v_c_elec[y, t, s] + m.v_c_opam[y, s]

def add_ieh_variables(m=None):
    
    m.v_ieh_q_heat_in = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'heat energy feed in from ieh per scenario, year, and hour'
    )
    m.v_ieh_q_elec_in = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'electricity input of ieh per scenario, year, and hour'
    )
    m.v_ieh_Q_heat_max = py.Variable(
        m.set_scenarios * m.set_years,
        domain = py.NonNegativeReals,
        doc = 'max heat feed in from ieh for district heating'
    )
    m.v_ieh_c_fix = py.Variable(
        m.set_years[1:] * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'Fix cost ieh per hear in EUR'
    )
    m.v_ieh_c_var = py.Variable(
        m.set_years * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'var cost ieh per hear in EUR'
    )

def add_ieh_parameters(m=None):
    m.f_ieh_eta = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'electrical efficiency of the ieh'
    )
    m.v_ieh_c_inv =py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'specific inv cost of ieh'
        )
    m.v_c_elec( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'specific electriyity prices year hour and scenario'
        )
    m.v_c_opam( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'Operational and Maintanance cost per year and scenario'
        )