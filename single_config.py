[
    // 核心盈利能力指标
    {
        "name": "GrossProfitMargin",
        "expression": "(TOR1_NORM - TOC1_NORM) / TOR1_NORM",
        "base_fields": ["TOR1", "TOC1"]
    },
    {
        "name": "CashEarningQuality",
        "expression": "NCF_OA_NORM / NP_NORM",
        "base_fields": ["NCF_OA", "NP"]
    },

    // 现金流分析指标
    {
        "name": "StrategicCAPEX",
        "expression": "NCF_IA21_NORM / NCF_OA_NORM",
        "base_fields": ["NCF_IA21", "NCF_OA"]
    },
    {
        "name": "DividendSustainability",
        "expression": "NCF_FA22_NORM / NP_SHAREHOLDER_NORM",
        "base_fields": ["NCF_FA22", "NP_SHAREHOLDER"]
    },

    // 运营效率指标
    {
        "name": "RevenueCashRatio",
        "expression": "NCF_OA11_NORM / TOR1_NORM",
        "base_fields": ["NCF_OA11", "TOR1"]
    },
    {
        "name": "TaxEfficiency",
        "expression": "NCF_OA23_NORM / TP_NORM",
        "base_fields": ["NCF_OA23", "TP"]
    },

    // 资本结构指标
    {
        "name": "DebtServiceCoverage",
        "expression": "NCF_OA_NORM / NCF_FA21_NORM",
        "base_fields": ["NCF_OA", "NCF_FA21"]
    },
    {
        "name": "EquityGrowthRate",
        "expression": "(TCI_PARENT_NORM - LAG(TCI_PARENT_NORM,1)) / ABS(LAG(TCI_PARENT_NORM,1))",
        "base_fields": ["TCI_PARENT"]
    },

    // 创新复合指标
    {
        "name": "CFROI",
        "expression": "(NCF_OA_NORM + NCF_IA21_NORM) / (NCF_IA21_NORM + 0.1*TA_NCA6_NORM)",
        "base_fields": ["NCF_OA", "NCF_IA21", "TA_NCA6"]
    },
    {
        "name": "HumanCapitalROI",
        "expression": "OP_NORM / NCF_OA22_NORM",
        "base_fields": ["OP", "NCF_OA22"]
    }
]
