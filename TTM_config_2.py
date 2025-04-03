[
    {
        "name": "CurrentRatio",
        "expression": "TA_CA_NORM / TL_CL_NORM",
        "base_fields": ["ta_ca", "tl_cl"]
    },
    {
        "name": "NetProfitMargin",
        "expression": "NP_NORM / TOR1_NORM",
        "base_fields": ["np", "tor1"]
    },
    {
        "name": "CashFlowLiquidity",
        "expression": "NCF_OA_NORM / TL_CL_NORM",
        "base_fields": ["ncf_oa", "tl_cl"]
    },
    {
        "name": "StrategicCAPEX",
        "expression": "NCF_IA21_NORM / TA_NCA6_NORM",
        "base_fields": ["ncf_ia21", "ta_nca6"]
    },
    {
        "name": "CoreRevenueGrowth",
        "expression": "(TOR1_NORM - LAG(TOR1_NORM,1)) / ABS(LAG(TOR1_NORM,1))",
        "base_fields": ["tor1"]
    },
    {
        "name": "ReceivableQuality",
        "expression": "NCF_OA11_NORM / TA_CA4_NORM",
        "base_fields": ["ncf_oa11", "ta_ca4"]
    },
    {
        "name": "InventoryStress",
        "expression": "TA_CA10_NORM / TOC1_NORM",
        "base_fields": ["ta_ca10", "toc1"]
    },
    {
        "name": "EmployeeEfficiency",
        "expression": "TOR1_NORM / NCF_OA22_NORM",
        "base_fields": ["tor1", "ncf_oa22"]
    },
    {
        "name": "TaxShieldEffect",
        "expression": "ITE_NORM / NCF_OA23_NORM",
        "base_fields": ["ite", "ncf_oa23"]
    },
    {
        "name": "DebtServiceRisk",
        "expression": "TL_CL15_NORM / NCF_FA21_NORM",
        "base_fields": ["tl_cl15", "ncf_fa21"]
    },
    {
        "name": "EquityStability",
        "expression": "TSE_PA8_NORM / TSE_PARENT_NORM",
        "base_fields": ["tse_pa8", "tse_parent"]
    },
    {
        "name": "IntangibleLeverage",
        "expression": "TA_NCA12_NORM / TSE_NORM",
        "base_fields": ["ta_nca12", "tse"]
    },
    {
        "name": "DividendSustainability",
        "expression": "NCF_FA22_NORM / TSE_PA8_NORM",
        "base_fields": ["ncf_fa22", "tse_pa8"]
    },
    {
        "name": "RDEfficiency",
        "expression": "TA_NCA13_NORM / TOC11_NORM",
        "base_fields": ["ta_nca13", "toc11"]
    },
    {
        "name": "FinancialAssetsQuality",
        "expression": "(TA_CA2_NORM + TA_NCA1_NORM) / TA_NORM",
        "base_fields": ["ta_ca2", "ta_nca1", "ta"]
    }
]
