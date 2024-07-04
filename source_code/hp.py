import pyomo.environ as py

def add_hp_equations(m=None):

    def hp_feed_in_max_bound(m, y, t, s):
        m.v_hp_q_heat_in[y, t, s] <= m.v_hp_Q_heat_max[y, s]
    
    def hp_elec_cop_heat(m, y, t, s):
        m.v_hp_q_heat_in[y, t, s] == m.v_hp_q_elec_in[y, t, s] * m.f_hp_cop[t] *m.f_hp_eta
        
    def hp_c_fix(m, y, t, s):
        m.v_hp_c_fix(y, s) == (m.v_hp_Q_heat_max[y, s] - m.v_hp_Q_heat_max[y-1, s]) * m.v_hp_c_inv(y, s)
        
    def hp_c_var(m, y, t, s): # OPAM = operational and maintanance, förderung?
        m.v_hp_c_var(y, s) == m.v_hp_q_elec_in[y, t, s] * m.v_c_elec[y, t, s] + m.v_c_opam[y, s]

def add_hp_variables(m=None):
    
    m.v_hp_q_heat_in = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'heat energy feed in from large-scale heat pump per scenario, year, and hour'
    )
    m.v_hp_q_elec_in = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'electricity input of large-scale heat pump per scenario, year, and hour'
    )
    m.v_hp_Q_heat_max = py.Variable(
        m.set_scenarios * m.set_years,
        domain = py.NonNegativeReals,
        doc = 'max heat feed in from large-scale heat pump for district heating'
    ) 
    m.v_hp_c_fix = py.Variable(
        m.set_years[1:] * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'Fix cost hp per hear in EUR'
    )
    m.v_hp_c_var = py.Variable(
        m.set_years * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'var cost hp per hear in EUR'
    )

def add_hp_parameters(m=None):
    m.f_hp_cop = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_hours,
        within = py.NonNegativeReals,
        doc = 'coefficient of performance of the large-scale heat pump'
    )
    m.f_hp_min_ratio_hp = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'ratio of min cap around 10-20%'
    )
    m.f_hp_eta = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'electrical efficiency of the hp'
    )
    m.v_hp_c_inv =py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'specific inv cost of heatpumps'
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