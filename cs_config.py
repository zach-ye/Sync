REG_CONFIGS = [
    {
        "name": "CASH_DEBT_COVERAGE",
        "y": "NCFOA_CL_RATIO",
        "x": ["CD_RATIO", "CUR_RATIO"],
        "normalize": {
            "NCFOA_CL_RATIO": "mad_10",
            "CD_RATIO": "mad_10"
        }
    },
    {
        "name": "QUALITY_GROWTH",
        "y": "NP_GRATE_YOY",
        "x": ["ICFOA_OR_RATIO_TTM", "GP_RATIO"],
        "normalize": {
            "NP_GRATE_YOY": "mad_10",
            "ICFOA_OR_RATIO_TTM": "mad_10"
        }
    },
    {
        "name": "LIGHT_ASSET_EFFICIENCY",
        "y": "FA_TURNOVER",
        "x": ["UDP_PS", "CR_PS"],
        "normalize": {
            "FA_TURNOVER": "mad_10",
            "UDP_PS": "mad_10"
        }
    },
    {
        "name": "SAFE_LEVERAGE",
        "y": "INT_MULTIPLIER",
        "x": ["DEBT_AS_RATIO", "TA_GRATE_YOY"],
        "normalize": {
            "INT_MULTIPLIER": "mad_10",
            "DEBT_AS_RATIO": "mad_10"
        }
    },
    {
        "name": "CORE_EARNINGS_PERSISTENCE",
        "y": "OP_GRATE_QOQ",
        "x": ["TA_TURNOVER", "EXP_RATIO"],
        "normalize": {
            "OP_GRATE_QOQ": "mad_10",
            "TA_TURNOVER": "mad_10"
        }
    },
    {
        "name": "SHAREHOLDER_YIELD_QUALITY",
        "y": "UDP_PS",
        "x": ["ROE_EXEAL", "NCFOA_PS"],
        "normalize": {
            "UDP_PS": "mad_10",
            "ROE_EXEAL": "mad_10"
        }
    },
    {
        "name": "WORKING_CAPITAL_ALPHA",
        "y": "WC_TURNOVER",
        "x": ["INV_TURNOVER", "AR_TURNOVER"],
        "normalize": {
            "WC_TURNOVER": "mad_10",
            "INV_TURNOVER": "mad_10"
        }
    },
    {
        "name": "EXPANSION_QUALITY",
        "y": "TA_GRATE_YOY",
        "x": ["NCFOA_TL_RATIO", "ROA_EXEAL"],
        "normalize": {
            "TA_GRATE_YOY": "mad_10",
            "NCFOA_TL_RATIO": "mad_10"
        }
    }
]
