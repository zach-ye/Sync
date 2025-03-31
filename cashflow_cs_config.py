REG_CONFIGS = [
    {
        "name": "profitability_drivers",
        "y": "NetProfitMargin",  # 净利润率 (NP/OR)
        "x": [
            "CashToRevenueRatio",  # 收入现金比 (NCF_OA11/OR)
            "DebtToAssets",        # 资产负债率 (TL/TA)
            "CAPEXIntensity",      # 资本支出强度 (NCF_IA21/NCF_OA)
            "sw1_dummy"           # 行业哑变量
        ],
        "normalize": {
            "NetProfitMargin": "mad_10",
            "CashToRevenueRatio": "mad_10"
        }
    },
    {
        "name": "fcf_sustainability",
        "y": "FreeCashFlow",       # 自由现金流 (NCF_OA - NCF_IA21)
        "x": [
            "OperatingCashFlowCoverage",  # 经营现金流覆盖率 (NCF_OA/CL)
            "CAPEXIntensity",      # 资本支出强度 
            "DividendPayoutRatio", # 股利支付率 (NCF_FA22/NP)
            "sw1_dummy"
        ],
        "normalize": {
            "FreeCashFlow": "mad_10",
            "CAPEXIntensity": "mad_10"
        }
    },
    {
        "name": "liquidity_risk",
        "y": "LiquidityStrengthIndex",  # 流动性强度 (CA-CL)/(CA+CL)
        "x": [
            "CurrentRatio",        # 流动比率 (CA/CL)
            "CashToNetIncome",     # 现金净利润比 (NCF_OA/NP)
            "DebtToAssets",
            "sw1_dummy"
        ],
        "normalize": {
            "LiquidityStrengthIndex": "mad_10",
            "CurrentRatio": "mad_10"
        }
    },
    {
        "name": "reinvestment_efficiency",
        "y": "CashReinvestmentRatio",  # 现金再投资率 (NCF_OA-NCF_FA22)/(TA-CA)
        "x": [
            "TotalCashGeneration",    # 总现金生成 (NCF_OA+NCF_IA+NCFFA)/TA
            "NetProfitMargin",
            "sw1_dummy"
        ],
        "normalize": {
            "CashReinvestmentRatio": "mad_10",
            "TotalCashGeneration": "mad_10"
        }
    },
    {
        "name": "dividend_policy",
        "y": "DividendPayoutRatio",    # 股利支付率 (NCF_FA22/NP)
        "x": [
            "FreeCashFlow", 
            "CashToNetIncome",         # 现金流质量指标
            "DebtToAssets",
            "sw1_dummy"
