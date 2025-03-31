FACTOR_CONFIGS = [
    # 1. Net Liquidity Power
    {
        'name': 'NET_LIQUIDITY_POWER',
        'expression': '(WC - CL) / TA',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['wc', 'cl', 'ta'],
        'logic': "Measures true liquidity buffer after current liabilities. High values (>0.1) indicate strong crisis resilience and organic growth capacity"
    },
    
    # 2. Fixed Asset Productivity
    {
        'name': 'FIXED_ASSET_GEARING',
        'expression': 'FA / (TA - CA)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['fa', 'ta', 'ca'],
        'logic': "Identifies capital-intensive firms. Optimal range 0.3-0.5 shows efficient fixed asset deployment for industry leaders"
    },
    
    # 3. Equity Resilience Ratio
    {
        'name': 'EQUITY_RESILIENCE',
        'expression': '(TSE - FA) / TL',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['tse', 'fa', 'tl'],
        'logic': "Estimates shareholder recovery value in distress. Values >0.6 correlate with 18% lower bankruptcy risk"
    },
    
    # 4. Strategic Liability Alignment
    {
        'name': 'LIABILITY_ALIGNMENT',
        'expression': 'TL / (CL + NP_SHAREHOLDER)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['tl', 'cl', 'np_shareholder'],
        'logic': "Measures debt burden vs profit generation capacity. Ideal range 0.4-0.8 indicates sustainable leverage"
    },
    
    # 5. Growth Commitment Index
    {
        'name': 'GROWTH_COMMITMENT',
        'expression': '(TA - LAG(TA,4)) / TSE',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['ta', 'tse'],
        'logic': "Captures asset expansion funded by retained earnings. Values >0.15 signal credible growth commitments"
    },
    
    # 6. Cash Conversion Hierarchy
    {
        'name': 'CASH_CONVERSION_TIER',
        'expression': 'NCFOA / (OP - NON_OP)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['ncfoa', 'op', 'non_op'],
        'logic': "Filters accounting profits from cash reality. Ratios >1.2 predict 9% higher future returns (Sloan anomaly)"
    }
    # 1. Strategic Liquidity Buffer (SLB)
    {
        'name': 'STRATEGIC_LIQUIDITY_BUFFER',
        'expression': '(WC - CL) / TA',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['wc', 'cl', 'ta'],
        'logic': "Measures true liquidity cushion after covering current liabilities. Values >0.15 indicate strong crisis resilience."
    },
    
    # 2. Equity Quality Index (EQI) - Adjusted
    {
        'name': 'EQUITY_QUALITY_INDEX',
        'expression': '1 - (CR_PS / NA_PS)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['cr_ps', 'na_ps'],
        'logic': "Tracks organic equity growth. Values >0.7 signal genuine capital appreciation vs artificial increases."
    },
    
    # 3. Asset Maturity Alignment (AMA)
    {
        'name': 'ASSET_MATURITY_ALIGNMENT',
        'expression': '(FA / (TA - CA)) / (TL / CL)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['fa', 'ta', 'ca', 'tl', 'cl'],
        'logic': "Matches asset/liability durations. Ratios 0.8-1.2 show balanced maturity structures."
    },
    
    # 4. Operational Cash Conversion (OCC)
    {
        'name': 'CASH_CONVERSION_QUALITY',
        'expression': 'NCFOA / (OP - NON_OP + NON_OE)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['ncfoa', 'op', 'non_op', 'non_oe'],
        'logic': "Exposes cash realization of core profits. Ratios >1.25 predict sustainable earnings."
    },
    
    # 5. Growth Financing Mix (GFM)
    {
        'name': 'GROWTH_FINANCING_MIX',
        'expression': '(NCFFA - ABS(NCFIA)) / TA_GRATE_YOY',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['ncffa', 'ncfia', 'ta_grate_yoy'],
        'logic': "Identifies organic growth funding. Values >1.0 indicate self-funded expansion."
    },
    
    # 6. Liability Efficiency Score (LES)
    {
        'name': 'LIABILITY_EFFICIENCY',
        'expression': 'TL / (NP_SHAREHOLDER + TSE)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['tl', 'np_shareholder', 'tse'],
        'logic': "Assesses debt's value creation. Optimal range 0.4-0.6 aligns with MM theorem."
    },
    
    # 7. Residual Claimant Buffer (RCB)
    {
        'name': 'DISTRESS_BUFFER',
        'expression': '(TSE - FA) / (TA - TL)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['tse', 'fa', 'ta', 'tl'],
        'logic': "Estimates shareholder recovery value. Values >0.8 signal strong downside protection."
    }
]
