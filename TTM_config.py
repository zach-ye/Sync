[
    {
        "name": "ROE",
        "expression": "NP_NORM / TSE_NORM",
        "base_fields": ["NP", "TSE"]
    },
    {
        "name": "ROA",
        "expression": "NP_NORM / TA_NORM",
        "base_fields": ["NP", "TA"]
    },
    {
        "name": "GrossProfitMargin",
        "expression": "(TOR1_NORM - TOC1_NORM) / TOR1_NORM",
        "base_fields": ["TOR1", "TOC1"]
    },
    {
        "name": "OperatingProfitMargin",
        "expression": "OP_NORM / TOR1_NORM",
        "base_fields": ["OP", "TOR1"]
    },
    {
        "name": "QuickRatio",
        "expression": "(CA_NORM - TA_CA10_NORM) / CL_NORM",
        "base_fields": ["CA", "TA_CA10", "CL"]
    },
    {
        "name": "InterestCoverageRatio",
        "expression": "(OP_NORM + TOC12_NORM) / TOC12_NORM",
        "base_fields": ["OP", "TOC12"]
    },
    {
        "name": "ReceivablesTurnover",
        "expression": "TOR1_NORM / TA_CA4_NORM",
        "base_fields": ["TOR1", "TA_CA4"]
    },
    {
        "name": "InventoryTurnover",
        "expression": "TOC1_NORM / TA_CA10_NORM",
        "base_fields": ["TOC1", "TA_CA10"]
    },
    {
        "name": "TotalAssetTurnover",
        "expression": "TOR1_NORM / TA_NORM",
        "base_fields": ["TOR1", "TA"]
    },
    {
        "name": "EquityMultiplier",
        "expression": "TA_NORM / TSE_NORM",
        "base_fields": ["TA", "TSE"]
    },
    {
        "name": "PretaxProfitMargin",
        "expression": "TP_NORM / TOR1_NORM",
        "base_fields": ["TP", "TOR1"]
    },
    {
        "name": "TaxBurdenRatio",
        "expression": "ITE_NORM / TP_NORM",
        "base_fields": ["ITE", "TP"]
    },
    {
        "name": "OperatingCashFlowToDebt",
        "expression": "NCF_OA_NORM / TL_NORM",
        "base_fields": ["NCF_OA", "TL"]
    },
    {
        "name": "CashFlowMargin",
        "expression": "NCF_OA_NORM / TOR1_NORM",
        "base_fields": ["NCF_OA", "TOR1"]
    },
    {
        "name": "WorkingCapital",
        "expression": "CA_NORM - CL_NORM",
        "base_fields": ["CA", "CL"]
    },
    {
        "name": "DebtToEquity",
        "expression": "TL_NORM / TSE_NORM",
        "base_fields": ["TL", "TSE"]
    },
    {
        "name": "RetainedEarningsToTA",
        "expression": "TSE_PA8_NORM / TA_NORM",
        "base_fields": ["TSE_PA8", "TA"]
    },
    {
        "name": "CAPEXToOperatingCashFlow",
        "expression": "NCF_IA21_NORM / NCF_OA_NORM",
        "base_fields": ["NCF_IA21", "NCF_OA"]
    },
    {
        "name": "FCFToRevenue",
        "expression": "(NCF_OA_NORM - NCF_IA21_NORM) / TOR1_NORM",
        "base_fields": ["NCF_OA", "NCF_IA21", "TOR1"]
    },
    {
        "name": "EBITMargin",
        "expression": "OP_NORM / TOR1_NORM",
        "base_fields": ["OP", "TOR1"]
    }
]
