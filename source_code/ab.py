import pyomo.environ as py

def add_ab_equations(m=None):

    def ab_ct_feed_in_max_bound(m, s, y, h):
        return m.v_ab_ct_q_cool_in[s, y, h] <= m.v_ab_ct_Q_cool_max[y]
    
    # def ab_ct_limit(m, y):
    #     return m.v_ab_ct_Q_cool_max[y] <= 0
    
    def ab_ct_heat_out(m, s, y, h):
        return m.v_ab_ct_q_cool_in[s, y, h] == m.v_ab_ct_q_heat_out[s, y, h] * m.p_ab_eer[s, y]
    
    def ab_ct_elec_cool(m, s, y, h):
        return m.v_ab_ct_q_elec_consumption[s, y, h] == m.v_ab_ct_q_heat_out[s, y, h] * 0.01 + (m.v_ab_ct_q_heat_out[s, y, h] + m.v_ab_ct_q_cool_in[s, y, h]) * 0.05
     
    def ab_ct_Q_inv(m, y):
        if (y - 5) in m.set_years:
            return m.v_ab_ct_Q_inv[y] == m.v_ab_ct_Q_cool_max[y] - m.v_ab_ct_Q_cool_max[y-5]
        else:
            return m.v_ab_ct_Q_inv[y] == m.v_ab_ct_Q_cool_max[y]
    
    def ab_ct_c_inv(m, s, y):
        return m.v_ab_ct_c_inv[s, y] == m.p_scenario_weighting[s] * (m.v_ab_ct_Q_inv[y] * m.p_ab_c_inv[s, y] + m.v_ab_ct_Q_inv[y] * (1 + 1 / m.p_ab_eer[s, y]) * m.p_ct_ab_c_inv[s, y])
    
    def ab_ct_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ab_ct_c_fix[s, y] == m.v_ab_ct_c_fix[s, y-5] + m.p_scenario_weighting[s] * m.p_year_expansion_range[s, y] * m.v_ab_ct_c_inv[s, y] * 0.02
        else:
            return m.v_ab_ct_c_fix[s, y] == m.p_scenario_weighting[s] * m.p_year_expansion_range[s, y] * m.v_ab_ct_c_inv[s, y] * 0.02

    def ab_ct_c_var(m, s, y, h):
        return m.v_ab_ct_c_var[s, y, h] == m.p_scenario_weighting[s] * m.p_year_expansion_range[s, y] * (m.v_ab_ct_q_elec_consumption[s, y, h] * (m.p_c_elec[s, y, h] + m.p_elec_co2_share[s, y, h] * m.p_c_co2[s, y]))

    def ab_hp_feed_in_max_bound(m, s, y, h):
        return m.v_ab_hp_q_cool_in[s, y, h] <= m.v_ab_hp_Q_cool_max[y]
    
    # def ab_hp_limit(m, y):
    #     return m.v_ab_hp_Q_cool_max[y] <= 0
    
    def ab_hp_heat_out(m, s, y, h):
        return m.v_ab_hp_q_cool_in[s, y, h] == m.v_ab_hp_q_heat_out[s, y, h] * m.p_ab_eer[s, y]
    
    def ab_hp_heat_in(m, s, y, h):
        return m.v_ab_hp_q_heat_in[s, y, h] == m.v_ab_hp_q_heat_out[s, y, h] + m.v_ab_hp_q_cool_in[s, y, h]
    
    def ab_hp_elec_cool(m, s, y, h):
        return m.v_ab_hp_q_elec_consumption[s, y, h] == m.v_ab_hp_q_heat_out[s, y, h] * 0.01 + m.v_ab_hp_q_heat_in[s, y, h] / m.p_ab_hp_cop[s, y]
     
    def ab_hp_Q_inv(m, y):
        if (y - 5) in m.set_years:
            return m.v_ab_hp_Q_inv[y] == m.v_ab_hp_Q_cool_max[y] - m.v_ab_hp_Q_cool_max[y-5]
        else:
            return m.v_ab_hp_Q_inv[y] == m.v_ab_hp_Q_cool_max[y]
    
    def ab_hp_c_inv(m, s, y):
        return m.v_ab_hp_c_inv[s, y] == m.v_ab_hp_Q_inv[y] * m.p_ab_c_inv[s, y] + m.v_ab_hp_Q_inv[y] * (1 + 1 / m.p_ab_eer[s, y]) * m.p_hp_c_inv[s, y]
  
    def ab_hp_c_fix(m, s, y):
        if (y - 5) in m.set_years:
            return m.v_ab_hp_c_fix[s, y] == m.v_ab_hp_c_fix[s, y-5] + m.p_year_expansion_range[s, y] * m.v_ab_hp_c_inv[s, y] * 0.02
        else:
            return m.v_ab_hp_c_fix[s, y] == m.p_year_expansion_range[s, y] * m.v_ab_hp_c_inv[s, y] * 0.02

    def ab_hp_c_var(m, s, y, h):
        return m.v_ab_hp_c_var[s, y, h] == m.p_year_expansion_range[s, y] * (m.v_ab_hp_q_elec_consumption[s, y, h] * (m.p_c_elec[s, y, h] + m.p_elec_co2_share[s, y, h] * m.p_c_co2[s, y]))
    
    m.con_ab_ct_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                  rule = ab_ct_feed_in_max_bound)
    
    m.con_ab_ct_heat_out = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = ab_ct_heat_out)
    
    m.con_ab_ct_elec_cool = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                          rule = ab_ct_elec_cool)
    
    m.con_ab_ct_Q_inv = py.Constraint(m.set_years,
                                      rule = ab_ct_Q_inv)
    
    m.con_ab_ct_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = ab_ct_c_inv)
    
    m.con_ab_ct_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = ab_ct_c_fix)
    
    m.con_ab_ct_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                      rule = ab_ct_c_var)
    
    # m.con_ab_ct_limit = py.Constraint(m.set_years,
    #                                   rule = ab_ct_limit)
    
    m.con_ab_hp_feed_in_max_bound = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                                  rule = ab_hp_feed_in_max_bound)
    
    m.con_ab_hp_heat_out = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                         rule = ab_hp_heat_out)
    
    m.con_ab_hp_heat_in = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                        rule = ab_hp_heat_in)
    
    m.con_ab_hp_elec_cool = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                          rule = ab_hp_elec_cool)
    
    m.con_ab_hp_Q_inv = py.Constraint(m.set_years,
                                      rule = ab_hp_Q_inv)
    
    m.con_ab_hp_c_inv = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = ab_hp_c_inv)
    
    m.con_ab_hp_c_fix = py.Constraint(m.set_scenarios, m.set_years,
                                      rule = ab_hp_c_fix)
    
    m.con_ab_hp_c_var = py.Constraint(m.set_scenarios, m.set_years, m.set_hours,
                                      rule = ab_hp_c_var)
    
    # m.con_ab_hp_limit = py.Constraint(m.set_years,
    #                                   rule = ab_hp_limit)

def add_ab_variables(m=None):
    
    m.v_ab_ct_q_cool_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                 domain = py.NonNegativeReals,
                                 doc = 'cool energy feed in from large-scale absorber with cooling tower per scenario, year, and hour')
    
    m.v_ab_ct_q_heat_out = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                  domain = py.NonNegativeReals,
                                  doc = 'heat energy take out from large-scale absorber with cooling tower per scenario, year, and hour')
    
    m.v_ab_ct_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                          domain = py.NonNegativeReals,
                                          doc = 'electricity input of large-scale absorber with cooling tower per scenario, year, and hour')
    
    m.v_ab_ct_Q_cool_max = py.Var(m.set_years,
                                  domain = py.NonNegativeReals,
                                  doc = 'max cool feed in from large-scale absorber with cooling tower for district cooling')
    
    m.v_ab_ct_Q_inv = py.Var(m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'new istalled ab_ct capacity per scenario and year')

    m.v_ab_ct_c_inv = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'inv costs of ab_ct per scenario and year in USD')
    
    m.v_ab_ct_c_fix = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'fix costs of ab_ct per scenario and year in USD')
    
    m.v_ab_ct_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                             domain = py.Reals,
                             doc = 'var costs of ab_ct per scenario, year and hour in USD')
    
    m.v_ab_hp_q_cool_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                 domain = py.NonNegativeReals,
                                 doc = 'cool energy feed in from large-scale absorber with heat pump per scenario, year, and hour')
    
    m.v_ab_hp_q_heat_out = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                  domain = py.NonNegativeReals,
                                  doc = 'heat energy take out from large-scale absorber with heat pump per scenario, year, and hour')
    
    m.v_ab_hp_q_heat_in = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                 domain = py.NonNegativeReals,
                                 doc = 'heat energy feed in from large-scale absorber with heat pump per scenario, year, and hour')
    
    m.v_ab_hp_q_elec_consumption = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                                          domain = py.NonNegativeReals,
                                          doc = 'electricity input of large-scale absorber with heat pump tower per scenario, year, and hour')
    
    m.v_ab_hp_Q_cool_max = py.Var(m.set_years,
                                  domain = py.NonNegativeReals,
                                  doc = 'max cool feed in from large-scale absorber with heat pump for district cooling')
    
    m.v_ab_hp_Q_inv = py.Var(m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'new istalled ab_hp capacity per scenario and year')

    m.v_ab_hp_c_inv = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'inv costs of ab_hp per scenario and year in USD')
    
    m.v_ab_hp_c_fix = py.Var(m.set_scenarios, m.set_years,
                             domain = py.NonNegativeReals,
                             doc = 'fix costs of ab_hp per scenario and year in USD')
    
    m.v_ab_hp_c_var = py.Var(m.set_scenarios, m.set_years, m.set_hours,
                             domain = py.Reals,
                             doc = 'var costs of ab_hp per scenario, year and hour in USD')

def add_ab_parameters(m=None):
    
    def init_ab_eer(m, s, y):
        return m.data_values[s]['ab'][y]['p_ab_eer']
    
    def init_ab_hp_cop(m, s, y):
        return m.data_values[s]['ab'][y]['p_ab_hp_cop']
    
    def init_ab_c_inv(m, s, y):
        return m.data_values[s]['ab'][y]['p_ab_c_inv']
    
    def init_ct_ab_c_inv(m, s, y):
        return m.data_values[s]['ab'][y]['p_ct_ab_c_inv']
    
    m.p_ab_eer = py.Param(m.set_scenarios, m.set_years,
                          initialize = init_ab_eer,
                          within = py.NonNegativeReals,
                          doc = 'seasonal energy efficiency ratio of the large-scale absorber with cooling tower')
    
    m.p_ab_hp_cop = py.Param(m.set_scenarios, m.set_years,
                             initialize = init_ab_hp_cop,
                             within = py.NonNegativeReals,
                             doc = 'coeffiecent of perfomance of the heat pump for the large-scale absorber')

    m.p_ab_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_ab_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of the large-scale absorber')
    
    m.p_ct_ab_c_inv =py.Param(m.set_scenarios, m.set_years,
                           initialize = init_ct_ab_c_inv,
                           within = py.NonNegativeReals,
                           doc = 'specific inv cost of the large-scale cooling tower')
