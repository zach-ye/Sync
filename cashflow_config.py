[
    {
        'name': 'CurrentRatio',
        'expression': 'CA_NORM / CL_NORM',
        'base_fields': ['CA', 'CL']
    },
    {
        'name': 'NetProfitMargin',
        'expression': 'NP_NORM / OR_NORM',
        'base_fields': ['NP', 'OR']
    },
    {
        'name': 'OperatingCashFlowCoverage',
        'expression': 'NCF_OA_NORM / CL_NORM',
        'base_fields': ['NCF_OA', 'CL']
    },
    {
        'name': 'FreeCashFlow',
        'expression': 'NCF_OA_NORM - NCF_IA21_NORM',
        'base_fields': ['NCF_OA', 'NCF_IA21']
    },
    {
        'name': 'DebtToAssets',
        'expression': 'TL_NORM / TA_NORM',
        'base_fields': ['TL', 'TA']
    },
    {
        'name': 'CashToRevenueRatio',
        'expression': 'NCF_OA11_NORM / OR_NORM',
        'base_fields': ['NCF_OA11', 'OR']
    },
    {
        'name': 'DividendPayoutRatio',
        'expression': 'NCF_FA22_NORM / NP_NORM',
        'base_fields': ['NCF_FA22', 'NP']
    },
    {
        'name': 'CashToNetIncome',
        'expression': 'NCF_OA_NORM / NP_NORM',
        'base_fields': ['NCF_OA', 'NP']
    },
    {
        'name': 'CAPEXIntensity',
        'expression': 'NCF_IA21_NORM / NCF_OA_NORM',
        'base_fields': ['NCF_IA21', 'NCF_OA']
    },
    {
        'name': 'LiquidityStrengthIndex',
        'expression': '(CA_NORM - CL_NORM) / (CA_NORM + CL_NORM)',
        'base_fields': ['CA', 'CL']
    },
    {
        'name': 'TotalCashGeneration',
        'expression': '(NCF_OA_NORM + NCF_IA_NORM + NCFFA_NORM) / TA_NORM',
        'base_fields': ['NCF_OA', 'NCF_IA', 'NCFFA', 'TA']
    },
    {
        'name': 'FreeCashFlowPerShare',
        'expression': '(NCF_OA_NORM - NCF_IA21_NORM) / NA_PS_NORM',
        'base_fields': ['NCF_OA', 'NCF_IA21', 'NA_PS']
    },
    {
        'name': 'SelfFundedInvestments',
        'expression': 'NCF_IA_NORM / NCF_OA_NORM',
        'base_fields': ['NCF_IA', 'NCF_OA']
    },
    {
        'name': 'CashReinvestmentRatio',
        'expression': '(NCF_OA_NORM - NCF_FA22_NORM) / (TA_NORM - CA_NORM)',
        'base_fields': ['NCF_OA', 'NCF_FA22', 'TA', 'CA']
    },
    {
        'name': 'CashConversionCycleProxy',
        'expression': '(NCF_OA11_NORM - NCF_OA21_NORM) / OR_NORM',
        'base_fields': ['NCF_OA11', 'NCF_OA21', 'OR']
    }
]
