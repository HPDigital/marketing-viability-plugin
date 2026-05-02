# Esquemas de Handoff entre Skills

Cada parte produce un YAML estructurado que la parte siguiente consume como input obligatorio. Esta referencia define el contrato de cada handoff.

## handoff_part1.yaml — Output de Diagnóstico de Mercado

```yaml
handoff_part1:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  evidence_level: "primary" | "modeled" | "secondary" | "modeled-inherited"

  business_definition:
    product_service: <string>
    customer_final: <string>
    customer_intermediate: <string>
    customer_codistributor: <string | null>
    geography: <string>
    horizon_years: <integer>
    economic_unit: <string>
    perimeter_in: [<string>]
    perimeter_out: [<string>]

  market_sizing:
    tam:
      value_units: {min: <number>, max: <number>}
      value_currency: {min: <number>, max: <number>, currency: <string>}
      methodology: <string>
      sources: [<string>]
    sam:
      value_units: {min: <number>, max: <number>}
      value_currency: {min: <number>, max: <number>, currency: <string>}
      restrictions_applied: [<string>]
    som:
      value_units: {min: <number>, max: <number>, year_steady_state: <integer>}
      value_currency: {min: <number>, max: <number>, currency: <string>}
      construction_method: "bottom-up" | "top-down" | "hybrid"
      capacity_constraints: [<string>]

  market_dynamics:
    cagr_by_segment: {<segment_id>: <percent>}
    structural_growth_drivers: [<string>]
    cyclical_growth_drivers: [<string>]
    seasonality_pattern: <string>
    macro_cyclicality: "low" | "medium" | "high"
    regulatory_trends: [<string>]

  competitive_landscape:
    direct_competitors: [{name: <string>, category: <string>, share_estimate: <percent>}]
    indirect_competitors: [{name: <string>, category: <string>}]
    non_obvious_competitors: [{name: <string>, category: <string>}]
    non_consumption: {description: <string>, magnitude_estimate: <string>}
    porter_five_forces: {rivalry: <1-5>, new_entrants: <1-5>, substitutes: <1-5>, suppliers: <1-5>, buyers: <1-5>, structural_profitability: "low" | "medium" | "high"}
    price_benchmark: [{category: <string>, range_low: <number>, range_high: <number>, currency: <string>}]

  customer_understanding:
    job_statement:
      when: <string>
      motivation: <string>
      functional_outcome: <string>
      emotional_outcome: <string>
      social_outcome: <string>
    jobs_functional: [{id: <string>, description: <string>, importance: <1-5>}]
    jobs_emotional: [{id: <string>, description: <string>}]
    jobs_social: [{id: <string>, description: <string>}]
    four_forces:
      push: {score: <1-5>, components: [<string>]}
      pull: {score: <1-5>, components: [<string>]}
      anxiety: {score: <1-5>, components: [<string>]}
      habit: {score: <1-5>, components: [<string>]}
      verdict: "switch_likely" | "switch_fragile" | "switch_blocked"
    outcomes_prioritized:
      - {id: <string>, description: <string>, importance: <1-5>, satisfaction: <1-5>, opportunity_score: <number>}
    willingness_to_pay_declared:
      - {segment_id: <string>, range_low: <number>, range_high: <number>, currency: <string>, financing_terms: <string>}
    declared_to_revealed_correction_factor: <0.5-1.0>
    primary_validation:
      done: <boolean>
      sample_size: <integer | null>
      method: <string | null>
      pending_actions: [<string>]

  preliminary_segments:
    - id: <string>
      name: <string>
      circumstance: <string>
      size_estimate: <string>
      capacity_to_pay: <string>

  diagnosis_synthesis:
    opportunity_verifiable: <string>
    accionable_size: <string>
    preliminary_competitive_position: <string>
    upstream_risks: [<string>]

  required_fields_for_part2:
    - business_definition
    - market_sizing.sam
    - market_sizing.som
    - customer_understanding.job_statement
    - customer_understanding.jobs_functional
    - customer_understanding.four_forces
    - customer_understanding.outcomes_prioritized
    - customer_understanding.willingness_to_pay_declared
    - preliminary_segments
    - competitive_landscape.price_benchmark
```

## handoff_part2.yaml — Output de Marketing Estratégico

```yaml
handoff_part2:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  source_handoff: "handoff_part1.yaml"

  segmentation:
    segments_evaluated:
      - id: <string>
        name: <string>
        atractiveness_score: <1-5>
        capacity_fit_score: <1-5>
        product_atract_x_fit: <number>
        quality_test:
          measurable: <boolean>
          substantial: <boolean>
          accessible: <boolean>
          differentiable: <boolean>
          actionable: <boolean>
    segments_discarded: [{id: <string>, reason: <string>}]
    entry_segment_id: <string>
    secondary_segment_ids: [<string>]

  targeting:
    coverage_decision: "concentrated" | "differentiated" | "undifferentiated" | "micromarketing"
    economic_justification: <string>
    operational_justification: <string>
    icp:
      segment_id: <string>
      descriptors: {<key>: <value>}
    buyer_personas:
      - role: "decisor" | "iniciador" | "pagador" | "influenciador"
        description: <string>
        jobs: [<string>]
        pains: [<string>]
        gains: [<string>]
    targeting_roadmap:
      year_1: <string>
      year_2: <string>
      year_3: <string>
      year_4: <string>
      year_5: <string>

  positioning:
    positioning_statement: <string>
    tagline: <string>
    tagline_validation: {word_count: <integer>, validates_canonical_rules: <boolean>}
    perceptual_dimensions: [<string>]
    competitor_perceptual_position: [{competitor: <string>, scores_by_dimension: {<dim>: <1-5>}}]
    proposal_perceptual_position: {<dim>: <1-5>}
    saturated_zones: [<string>]
    empty_zones: [<string>]
    reason_to_believe_assets: [{asset: <string>, status: "existing" | "to_build", cost_estimate: <string>, timeline: <string>}]

  blue_ocean:
    factors_buyer_side: [{id: <string>, statement: <string>, eric_action: "raise" | "create" | "reduce" | "eliminate", to_be_score: <1-5>}]
    eliminate: [<string>]
    reduce: [<string>]
    raise: [<string>]
    create: [<string>]
    cost_savings_estimated: [{action: <string>, magnitude: <string>}]

  competitive_strategy:
    generic_strategy: "cost_leadership" | "differentiation" | "focus_cost" | "focus_differentiation"
    ansoff_vector: "penetration" | "market_development" | "product_development" | "diversification"
    blue_ocean_six_paths_active: [<string>]
    non_clients_tiers_activated: [<string>]

  value_proposition:
    main_statement: <string>
    sub_propositions_by_segment:
      - segment_id: <string>
        statement: <string>
    products_services: [{id: <string>, name: <string>, segment_target: [<string>], category: "essential" | "secondary" | "support"}]
    pain_relievers: [{id: <string>, description: <string>, pain_target: <string>}]
    gain_creators: [{id: <string>, description: <string>, gain_target: <string>}]

  required_fields_for_part3:
    - segmentation.entry_segment_id
    - targeting.icp
    - positioning.positioning_statement
    - positioning.reason_to_believe_assets
    - blue_ocean.factors_buyer_side
    - blue_ocean.eliminate
    - blue_ocean.create
    - value_proposition.main_statement
    - value_proposition.products_services
```

## handoff_part3.yaml — Output de Marketing Operativo

```yaml
handoff_part3:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  source_handoffs: ["handoff_part1.yaml", "handoff_part2.yaml"]

  product_plan:
    mvp_definition: <string>
    initial_portfolio:
      - line_id: <string>
        line_name: <string>
        references: [{ref_id: <string>, name: <string>, regulatory_status: <string>}]
    backlog_24m:
      - month: <integer>
        increment: <string>
        cost_estimate: <number>
        currency: <string>
    product_kpis: [{kpi: <string>, target: <string>}]

  pricing_plan:
    pricing_structure: "linear" | "tiered" | "value_based" | "hybrid"
    payment_modality: "one_time" | "recurring_monthly" | "recurring_annual" | "mixed"
    tariff_by_line:
      - line_id: <string>
        segment_id: <string>
        price_low: <number>
        price_mid: <number>
        price_high: <number>
        currency: <string>
        financing_terms: <string>
    discount_policy: <string>
    annual_review_policy: <string>
    launch_promotion: <string | "none">
    unit_economics_test:
      avg_price: <number>
      avg_variable_cost: <number>
      avg_gross_margin_percent: <number>
      avg_contribution_margin: <number>

  channels_plan:
    journey_map:
      awareness: {primary: <string>, secondary: <string>}
      evaluation: {primary: <string>, secondary: <string>}
      purchase: {primary: <string>, secondary: <string>}
      delivery: {primary: <string>, secondary: <string>}
      after_sales: {primary: <string>, secondary: <string>}
    channel_operations:
      - channel_id: <string>
        channel_name: <string>
        monthly_budget: <number>
        currency: <string>
        target_volume_year1: <integer>
        cac_estimate: <number>
        actions: [<string>]
    cac_blended:
      year_1: <number>
      year_2: <number>
      year_3_5: <number>
      currency: <string>

  communication_plan:
    promise_central: <string>
    secondary_messages: [<string>]
    tone_style: <string>
    visual_identity_minimum: [<string>]
    editorial_calendar_year_1:
      - month: <integer>
        actions: [<string>]
    launch_campaign:
      window_days: <integer>
      milestones: [{milestone: <string>, month: <integer>}]
      budget: {amount: <number>, currency: <string>}
    funnel:
      stages: [{name: <string>, conversion_rate_low: <percent>, conversion_rate_high: <percent>}]
      total_conversion: {low: <percent>, high: <percent>}
    operational_tools: [{tool: <string>, monthly_cost: <number>}]
    retention_actions: [<string>]

  capacity_plan:
    bottlenecks_sequential: [<string>]
    max_capacity_phase_1:
      big_hire_per_year: {min: <integer>, max: <integer>}
      little_hire_per_year: {min: <integer>, max: <integer>}
      b2b_contracts_active: {min: <integer>, max: <integer>}
    unit_cost_structure:
      - line_id: <string>
        cif_component: <number>
        labor: <number>
        materials: <number>
        financial: <number>
        service_included: <number>
        total_unit_cost: <number>
        currency: <string>
    capacity_jumps:
      - year: <integer>
        action: <string>
        capex_estimate: <number>
        opex_increment: <number>
        currency: <string>

  operational_calendar:
    year_1_monthly_milestones: [{month: <integer>, milestone: <string>, owner: <string>}]
    year_2_3_quarterly: [{quarter: <string>, milestone: <string>}]
    year_4_5_semestral: [{semester: <string>, milestone: <string>}]
    critical_path: [<string>]
    review_rituals: [<string>]

  required_fields_for_part4:
    - pricing_plan.tariff_by_line
    - pricing_plan.unit_economics_test
    - channels_plan.cac_blended
    - capacity_plan.max_capacity_phase_1
    - capacity_plan.unit_cost_structure
    - capacity_plan.capacity_jumps
    - communication_plan.launch_campaign.budget
    - operational_calendar.year_1_monthly_milestones
```

## handoff_part4.yaml — Output de Análisis Financiero

```yaml
handoff_part4:
  version: "1.0"
  case_name: <string>
  date: <ISO-8601>
  source_handoffs: ["handoff_part1.yaml", "handoff_part2.yaml", "handoff_part3.yaml"]

  financial_model:
    horizon_years: <integer>
    granularity: {year_1: "monthly", years_2_3: "quarterly", years_4_5: "semestral"}
    macro_assumptions:
      inflation_annual: <percent>
      exchange_rate: <number>
      discount_rate: <percent>

  revenue_projection:
    by_line_by_year:
      - line_id: <string>
        scenario: "base" | "pessimistic" | "optimistic"
        years: [<number>]
        currency: <string>
    total_by_year:
      base: [<number>]
      pessimistic: [<number>]
      optimistic: [<number>]

  cost_structure:
    variable_costs_by_year: {base: [<number>], pessimistic: [<number>], optimistic: [<number>]}
    fixed_costs_operational_by_year: [<number>]
    fixed_costs_commercial_marketing_by_year: [<number>]
    corporate_structure_by_year: [<number>]
    financial_costs_by_year: [<number>]
    blue_ocean_savings_by_year: [<number>]

  capex_plan:
    initial_capex: {workshop: <number>, stock: <number>, regulatory: <number>, commercial: <number>, total: <number>}
    expansion_capex_by_year: [<number>]
    working_capital_permanent: <number>

  cash_flow:
    operating_cf_year_1_monthly: [<number>]
    operating_cf_years_2_5_quarterly: [<number>]
    investment_cf_by_year: [<number>]
    financing_cf_by_year: [<number>]
    free_cash_flow_by_year: [<number>]
    cumulative_fcf_by_year: [<number>]
    cash_inflection_month: <integer>
    seasonal_tensions: [{period: <string>, magnitude: <number>}]

  viability_indicators:
    npv: {base: <number>, pessimistic: <number>, optimistic: <number>, currency: <string>}
    irr: {base: <percent>, pessimistic: <percent>, optimistic: <percent>}
    payback_simple_months: {base: <integer>, pessimistic: <integer>, optimistic: <integer>}
    payback_discounted_months: {base: <integer>, pessimistic: <integer>, optimistic: <integer>}
    breakeven_volume: <integer>
    breakeven_value: <number>
    breakeven_month: <integer>

  unit_economics:
    cac_blended: <number>
    ltv_blended: <number>
    ltv_cac_ratio: <number>
    payback_cac_months: <integer>
    gross_margin_per_line: {<line_id>: <percent>}
    contribution_margin_per_unit: <number>
    little_hire_retention_rate_year_1: <percent>

  sensitivity_analysis:
    critical_variables: [<string>]
    sensitivity_npv:
      - variable: <string>
        delta_minus_20: <number>
        delta_plus_20: <number>
    tornado_data: [{variable: <string>, impact_low: <number>, impact_high: <number>}]
    npv_invalidation_thresholds: [{variable: <string>, threshold: <string>}]

  risk_analysis:
    market_risks: [{risk: <string>, probability: "low" | "medium" | "high", impact: "low" | "medium" | "high", mitigation: <string>}]
    operational_risks: [{...}]
    regulatory_risks: [{...}]
    financial_risks: [{...}]
    partnership_risks: [{...}]
    pivot_triggers: [{trigger: <string>, action: <string>, cost: <number>}]

  validation_program:
    critical_hypotheses: [{id: <string>, hypothesis: <string>, validation_method: <string>, budget: <number>, duration_weeks: <integer>, threshold: <string>}]
    quarter_1_deseability_budget: <number>
    quarter_2_feasibility_budget: <number>
    quarter_3_operational_viability_budget: <number>
    total_validation_budget: <number>
    pass_no_pass_thresholds: [{hypothesis_id: <string>, threshold: <string>}]

  final_verdict:
    veredict: "viable" | "viable_with_observations" | "marginal" | "not_viable"
    conditional_on: [<string>]
    capital_needed_total: <number>
    capital_structure_proposed: {equity: <number>, debt: <number>, partnership: <number>}
    disbursement_calendar: [{milestone: <string>, amount: <number>}]
    continuation_pivot_abandonment_triggers: [<string>]
```
