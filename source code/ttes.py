import pyomo.environ as py

def add_ttes_equations(m=None):
    def ttes_feed_in_max_bound(m, y, t, s):
        m.v_ttes_q_thermal_in[y, t, s] <= m.v_ttes_Q_thermal_max[y, s]

    def ttes_storage_max_bound(m, y, t, s):
        m.v_ttes_q_thermal_out[y, t, s] <= m.v_ttes_Q_thermal_max[y, s]

    def ttes_soc_max_bound(m, y, t, s):
        m.v_ttes_k_thermal[y, t, s] <= m.v_ttes_k_thermal_max[y, s]

    def ttes_soc(m, y, t, s):#cop abhängig von temp/soc des speichers
        m.v_ttes_k_thermal[y, t, s] == m.v_ttes_k_thermal[y, t-1, s] * m.p_ttes_losses + m.v_ttes_q_thermal_out[y, t, s] * m.p_ttes_eta / m.p_ttes_cop - m.v_ttes_q_thermal_in[y, t, s] * m.p_ttes_cop / m.p_ttes_eta

    def ttes_soc_init(m, y, t, s):#cop abhängig von temp/soc des speichers
        m.v_ttes_k_thermal[y, 0, s] == m.v_ttes_k_thermal_max[y, s] * m.p_ttes_losses * m.p_ttes_init + m.v_ttes_q_thermal_out[y, 0, s] * m.p_ttes_eta / m.p_ttes_cop - m.v_ttes_q_thermal_in[y, 0, s] * m.p_ttes_cop / m.p_ttes_eta

    def ttes_soc_finalt(m, y, t, s):
        m.v_ttes_k_thermal[y, 8760, s] == m.v_ttes_k_thermal_max[y, s] * m.p_ttes_end

    def ttes_c_fix(m, y, t, s):
        m.v_ttes_c_fix(y, s) == (m.v_ttes_k_thermal_max[y, s] - m.v_ttes_k_thermal_max[y-1, s]) * m.p_ttes_c_inv(y, s)
    
    def ttes_c_var(m, y, t, s):
        m.v_ttes_c_var(y, s) == m.v_ttes_k_thermal_max[y, s] * m.p_c_elec[y, t, s] * m.p_ttes_elec + m.v_c_opam[y, s] + (m.v_ttes_q_thermal_in[y, t, s] + m.v_ttes_q_thermal_out[y, t, s]) * m.p_ttes_c_charge_discharge[y, t, s]

def add_hp_variables(m=None):
    m.v_ttes_q_thermal_in = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'thermal energy feed in per scenario, year and hour'
        )
    m.v_ttes_q_thermal_out = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'thermal energy storing per scenario, year and hour'
        )
    m.v_ttes_Q_thermal_max = py.Variable(
        m.set_scenarios * m.set_years,
        domain = py.NonNegativeReals,
        doc = 'maximum thermal energy feed in/storing per scenario and year'
        )
    m.v_ttes_k_thermal = py.Variable(
        m.set_scenarios * m.set_years * m.set_hours,
        domain = py.NonNegativeReals,
        doc = 'state of charge per scenario, year and hour'
        )
    m.v_ttes_k_thermal_max = py.Variable(
        m.set_scenarios * m.set_years,
        domain = py.NonNegativeReals,
        doc = 'maximum state of charge per scenario, year and hour'
        )
    m.v_ttes_c_fix = py.Variable(
        m.set_years[1:] * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'fix costs of TTES per year in EUR'
        )
    m.v_ttes_c_var = py.Variable(
        m.set_years * m.set_scenarios,
        domain = py.NonNegativeReals,
        doc = 'var costs of TTES per year in EUR'
        )

def add_hp_parameters(m=None):
    m.p_ttes_losses = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'losses of the storage'
        )
    m.p_ttes_eta = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'efficiency of the storage'
        )    
    m.p_ttes_cop = py.Parameter( #Einlesen von Inputs fehlt! #cop abhängig von temp/soc des speichers
        within = py.NonNegativeReals,
        doc = 'cop of the storage'
        )
    m.p_ttes_init = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'initial soc of the storage'
        )
    m.p_ttes_end = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.NonNegativeReals,
        doc = 'final soc of the storage'
        )  
    m.p_ttes_c_inv = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'specific investment costs of TTES'
        )   
    m.p_c_elec = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'electricity price per scenario, year and hour'
        )    
    m.p_ttes_elec = py.Parameter( #Einlesen von Inputs fehlt!
        within = py.Reals,
        doc = 'electricity share of thermal energy'
        )
    m.p_c_opam = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios,
        within = py.NonNegativeReals,
        doc = 'Operational and Maintanance cost per scenario, year and hour'
        )
    m.p_ttes_c_charge_discharge = py.Parameter( #Einlesen von Inputs fehlt!
        m.set_years * m.set_scenarios * m.set_hours,
        within = py.Reals,
        doc = 'charge/discharge price per scenario, year and hour'
        ) 