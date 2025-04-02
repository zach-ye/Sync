FACTOR_CONFIGS = [
   
    {
        'name': 'RevenueAcceleration',
        'expression': '(TOR1_Q - TOR1_Q_PREV)/TOR1_Q_PREV - (TOR1_TTM - TOR1_TTM_PREV)/TOR1_TTM_PREV',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['TOR1_Q', 'TOR1_Q_PREV', 'TOR1_TTM', 'TOR1_TTM_PREV']
    },
    {
        'name': 'NetProfitQuality',
        'expression': '(NP_Q / NP_TTM * 4) - 1',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['NP_Q', 'NP_TTM']
    },
    {
        'name': 'CostControlEfficiency',
        'expression': '(TOC10_TTM/TOR1_TTM - TOC10_Q/TOR1_Q) + (TOC11_TTM/TOR1_TTM - TOC11_Q/TOR1_Q)',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['TOC10_Q', 'TOC10_TTM', 'TOC11_Q', 'TOC11_TTM', 'TOR1_Q', 'TOR1_TTM']
    },

    {
        'name': 'CoreProfitRatioChange',
        'expression': '(OP_Q/TP_Q) - (OP_TTM/TP_TTM)',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['OP_Q', 'TP_Q', 'OP_TTM', 'TP_TTM']
    },

    {
        'name': 'NetInterestGap',
        'expression': '(TOR2_Q - TOC2_Q) - (TOR2_TTM - TOC2_TTM)/4',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['TOR2_Q', 'TOC2_Q', 'TOR2_TTM', 'TOC2_TTM']
    },
    {
        'name': 'PremiumMomentum',
        'expression': '(TOR3_Q/TOR3_TTM*4) - (TOR1_Q/TOR1_TTM*4)',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['TOR3_Q', 'TOR3_TTM', 'TOR1_Q', 'TOR1_TTM']
    },

    {
        'name': 'ImpairmentSurge',
        'expression': 'TOC13_Q / NP_MAXIMUM(TOC13_TTM, 0.01*TOTAL_ASSETS_TTM)',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['TOC13_Q', 'TOC13_TTM', 'TOTAL_ASSETS_TTM']
    }
]
