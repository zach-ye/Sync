REGRESSION_CONFIGS = [
    {
        'y': 'NP',
        'x': ['OR'],
        'window_size': 8,
        'factors': [
            {'name': 'residual_np_or', 'type': 'last_residual'},
            {'name': 'r2_np_or', 'type': 'r2'},
            {'name': 'intercept_np_or', 'type': 'intercept'},
            {'name': 'slope_or_np_or', 'type': 'slope', 'var': 'OR'}
        ]
    },
    {
        'y': 'ROA',
        'x': ['TA_TURNOVER'],
        'window_size': 8,
        'factors': [
            {'name': 'residual_roa_ta_turnover', 'type': 'last_residual'},
            {'name': 'r2_roa_ta_turnover', 'type': 'r2'},
            {'name': 'intercept_roa_ta_turnover', 'type': 'intercept'},
            {'name': 'slope_ta_turnover_roa_ta_turnover', 'type': 'slope', 'var': 'TA_TURNOVER'}
        ]
    },
    {
        'y': 'ROE',
        'x': ['EQ_MULTIPLIER'],
        'window_size': 8,
        'factors': [
            {'name': 'residual_roe_eq_multiplier', 'type': 'last_residual'},
            {'name': 'r2_roe_eq_multiplier', 'type': 'r2'},
            {'name': 'intercept_roe_eq_multiplier', 'type': 'intercept'},
            {'name': 'slope_eq_multiplier_roe_eq_multiplier', 'type': 'slope', 'var': 'EQ_MULTIPLIER'}
        ]
    },
    {
        'y': 'OP_GRATE_YOY',
        'x': ['OR_GRATE_YOY'],
        'window_size': 8,
        'factors': [
            {'name': 'residual_op_grate_yoy_or_grate_yoy', 'type': 'last_residual'},
            {'name': 'r2_op_grate_yoy_or_grate_yoy', 'type': 'r2'},
            {'name': 'intercept_op_grate_yoy_or_grate_yoy', 'type': 'intercept'},
            {'name': 'slope_or_grate_yoy_op_grate_yoy_or_grate_yoy', 'type': 'slope', 'var': 'OR_GRATE_YOY'}
        ]
    },
    {
        'y': 'NCFOA',
        'x': ['NP'],
        'window_size': 8,
        'factors': [
            {'name': 'residual_ncfoa_np', 'type': 'last_residual'},
            {'name': 'r2_ncfoa_np', 'type': 'r2'},
            {'name': 'intercept_ncfoa_np', 'type': 'intercept'},
            {'name': 'slope_np_ncfoa_np', 'type': 'slope', 'var': 'NP'}
        ]
    }
]
