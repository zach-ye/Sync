FACTOR_CONFIGS = [
    {
        'name': 'STRATEGIC_LIQUIDITY_BUFFER',
        'expression': '(WC_NORM - CL_NORM) / TA_NORM',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['WC', 'CL', 'TA']
    },
    {
        'name': 'EQUITY_QUALITY_INDEX',
        'expression': '1 - (CR_PS_NORM / NA_PS_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['CR_PS', 'NA_PS']
    },
    {
        'name': 'ASSET_MATURITY_ALIGNMENT',
        'expression': '(FA_NORM / (TA_NORM - CA_NORM)) / (TL_NORM / CL_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['FA', 'TA', 'CA', 'TL', 'CL']
    },
    {
        'name': 'CASH_CONVERSION_QUALITY',
        'expression': 'NCFOA_NORM / (OP_NORM - NON_OP_NORM + NON_OE_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['NCFOA', 'OP', 'NON_OP', 'NON_OE']
    },
    {
        'name': 'GROWTH_FINANCING_MIX',
        'expression': '(NCFFA_NORM - ABS(NCFIA_NORM)) / TA_GRATE_YOY_NORM',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['NCFFA', 'NCFIA', 'TA_GRATE_YOY']
    },
    {
        'name': 'LIABILITY_EFFICIENCY',
        'expression': 'TL_NORM / (NP_SHAREHOLDER_NORM + TSE_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['TL', 'NP_SHAREHOLDER', 'TSE']
    },
    {
        'name': 'DISTRESS_BUFFER',
        'expression': '(TSE_NORM - FA_NORM) / (TA_NORM - TL_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['TSE', 'FA', 'TA', 'TL']
    },
    {
        'name': 'NET_LIQUIDITY_POWER',
        'expression': '(WC_NORM - CL_NORM) / TA_NORM',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['WC', 'CL', 'TA']
    },
    {
        'name': 'FIXED_ASSET_GEARING',
        'expression': 'FA_NORM / (TA_NORM - CA_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['FA', 'TA', 'CA']
    },
    {
        'name': 'EQUITY_RESILIENCE',
        'expression': '(TSE_NORM - FA_NORM) / TL_NORM',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['TSE', 'FA', 'TL']
    },
    {
        'name': 'LIABILITY_ALIGNMENT',
        'expression': 'TL_NORM / (CL_NORM + NP_SHAREHOLDER_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['TL', 'CL', 'NP_SHAREHOLDER']
    },
    {
        'name': 'GROWTH_COMMITMENT',
        'expression': '(TA_NORM - LAG(TA_NORM,4)) / TSE_NORM',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['TA', 'TSE']
    },
    {
        'name': 'CASH_CONVERSION_TIER',
        'expression': 'NCFOA_NORM / (OP_NORM - NON_OP_NORM)',
        'normalize': True,
        'normalize_method': 'mad_10',
        'base_fields': ['NCFOA', 'OP', 'NON_OP']
    }
]
