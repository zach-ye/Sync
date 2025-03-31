REG_CONFIGS = [
    {   # 1. Core Cost Efficiency Anomaly
        "name": "core_cost_anomaly",
        "y": "CostRatio1",
        "x": ["CostRatio9", "CostRatio10", "CostRatio11", "CostRatio12"],
        "normalize": {
            "CostRatio1": "mad_10",
            "CostRatio9": "mad_10",
            "CostRatio10": "mad_10",
            "CostRatio11": "mad_10",
            "CostRatio12": "mad_10"
        }
    },
    {   # 2. Sustainable Profit Filter
        "name": "sustainable_profit",
        "y": "NetProfitRatio",
        "x": ["InvestmentProfitRatio"],
        "normalize": {
            "NetProfitRatio": "mad_10",
            "InvestmentProfitRatio": "mad_10"
        }
    },
    {   # 3. Tax Efficiency Signal
        "name": "tax_efficiency",
        "y": "CostRatio9",
        "x": ["CostRatio1", "NetProfitRatio"],
        "normalize": {
            "CostRatio9": "mad_10",
            "CostRatio1": "mad_10",
            "NetProfitRatio": "mad_10"
        }
    },
    {   # 4. Structural Cost Risk
        "name": "structural_cost_risk",
        "y": "TotalCostToNetProfit",
        "x": ["CostRatio1", "CostRatio9", "CostRatio10", "CostRatio11", "CostRatio12"],
        "normalize": {
            "TotalCostToNetProfit": "mad_10",
            "CostRatio1": "mad_10",
            "CostRatio9": "mad_10",
            "CostRatio10": "mad_10",
            "CostRatio11": "mad_10",
            "CostRatio12": "mad_10"
        }
    },
    {   # 5. Financial Cost Justification
        "name": "financial_cost_justified",
        "y": "CostRatio12",
        "x": ["NetProfitRatio", "InvestmentProfitRatio"],
        "normalize": {
            "CostRatio12": "mad_10",
            "NetProfitRatio": "mad_10",
            "InvestmentProfitRatio": "mad_10"
        }
    }
]
