import pandas as pd
import numpy as np
from scipy.stats import zscore, rankdata
from scipy.special import ndtri

# 新增标准化方法
def guassian_rank(x):
    ranked = rankdata(x) / len(x)
    return ndtri(ranked)

def cut_mad_10(x):
    median = np.median(x)
    mad = np.median(np.abs(x - median))
    lower = median - 10 * mad
    upper = median + 10 * mad
    return np.clip(x, lower, upper)

def winsorie(x, lower=0.01, upper=0.99):
    q_low = np.quantile(x, lower)
    q_high = np.quantile(x, upper)
    return np.clip(x, q_low, q_high)

def safe_zscore(x):
    x = x.fillna(0)
    std = x.std()
    if std == 0:
        return np.zeros_like(x)
    return (x - x.mean()) / std

# ================== 因子配置 ==================
FACTOR_CONFIGS = [
    # 成本相关因子
    {
        'name': 'CostRatio1',
        'expression': 'toc1_norm / op_norm',
        'category': 'CostAnalysis',
        'normalize': True,
        'normalize_method': 'safe_zscore',
        'winsorize': (0.01, 0.99),
        'base_fields': ['toc1', 'op']
    },
    {
        'name': 'CostRatio9',
        'expression': 'toc9_norm / op_norm',
        'category': 'CostAnalysis',
        'normalize': True,
        'normalize_method': 'guassian_rank',
        'winsorize': (0.01, 0.99),
        'base_fields': ['toc9', 'op']
    },
    {
        'name': 'CostRatio10',
        'expression': 'toc10_norm / op_norm',
        'category': 'CostAnalysis',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['toc10', 'op']
    },
    {
        'name': 'CostRatio11',
        'expression': 'toc11_norm / op_norm',
        'category': 'CostAnalysis',
        'normalize': True,
        'normalize_method': 'winsorie',
        'base_fields': ['toc11', 'op']
    },
    {
        'name': 'CostRatio12',
        'expression': 'toc12_norm / op_norm',
        'category': 'CostAnalysis',
        'normalize': True,
        'normalize_method': 'safe_zscore',
        'base_fields': ['toc12', 'op']
    },
    # 投资收益与营业利润关系
    {
        'name': 'InvestmentProfitRatio',
        'expression': 'inve_income_norm / op_norm',
        'category': 'ProfitAnalysis',
        'normalize': True,
        'normalize_method': 'guassian_rank',
        'base_fields': ['inve_income', 'op']
    },
    # 净利润与营业利润关系
    {
        'name': 'NetProfitRatio',
        'expression': 'np_norm / op_norm',
        'category': 'ProfitAnalysis',
        'normalize': True,
        'normalize_method': 'safe_zscore',
        'base_fields': ['np', 'op']
    },
    # 综合成本与净利润关系
    {
        'name': 'TotalCostToNetProfit',
        'expression': '(toc1_norm + toc9_norm + toc10_norm + toc11_norm + toc12_norm) / np_norm',
        'category': 'ComprehensiveAnalysis',
        'normalize': True,
        'normalize_method': 'cut_mad_10',
        'base_fields': ['toc1', 'toc9', 'toc10', 'toc11', 'toc12', 'np']
    }
]

# ================== 核心函数 ==================
def calculate_factors(df, configs=FACTOR_CONFIGS):
    """
    因子计算与标准化主函数
    :param df: 包含原始字段的DataFrame
    :return: 包含所有因子及标准化结果的DataFrame
    """
    result_df = df.copy()

    # 对基础数据进行标准化
    for config in configs:
        for field in config['base_fields']:
            if field in result_df.columns:
                norm_col = f"{field}_norm"
                method = config['normalize_method']
                if method == 'guassian_rank':
                    result_df[norm_col] = guassian_rank(result_df[field].fillna(0))
                elif method == 'cut_mad_10':
                    result_df[norm_col] = cut_mad_10(result_df[field].fillna(0))
                elif method == 'winsorie':
                    result_df[norm_col] = winsorie(result_df[field].fillna(0))
                elif method == 'safe_zscore':
                    result_df[norm_col] = safe_zscore(result_df[field])

    for config in configs:
        # 行业特异性检查
        if 'industry_specific' in config:
            industry_mask = df['industry_code'].isin(config['industry_specific'])
            temp_df = df.loc[industry_mask].copy()
        else:
            temp_df = df.copy()

        try:
            # 计算原始因子
            result_df[config['name']] = temp_df.eval(config['expression'])

            # 处理分母为零的情况
            result_df[config['name']] = result_df[config['name']].replace([np.inf, -np.inf], np.nan)

            # 缩尾处理
            if 'winsorize' in config:
                lower, upper = config['winsorize']
                q_low = result_df[config['name']].quantile(lower)
                q_high = result_df[config['name']].quantile(upper)
                result_df[config['name']] = result_df[config['name']].clip(q_low, q_high)

        except Exception as e:
            print(f"计算因子 {config['name']} 失败: {str(e)}")
            result_df[config['name']] = np.nan

    return result_df

# ================== 使用示例 ==================
if __name__ == "__main__":
    # 模拟数据
    data = pd.DataFrame({
        'toc1': np.random.uniform(1e5, 1e6, 1000),
        'toc9': np.random.uniform(1e4, 1e5, 1000),
        'toc10': np.random.uniform(1e4, 1e5, 1000),
        'toc11': np.random.uniform(1e4, 1e5, 1000),
        'toc12': np.random.uniform(1e4, 1e5, 1000),
        'inve_income': np.random.uniform(-1e5, 1e5, 1000),
        'op': np.random.uniform(1e5, 1e6, 1000),
        'np': np.random.uniform(1e5, 1e6, 1000),
        'industry_code': np.random.choice(['Insurance', 'Banking', 'Manufacturing'], 1000)
    })

    # 计算因子
    result = calculate_factors(data)

    print("\n计算结果样例:")
    print(result[['CostRatio1']].head())
    print("\n部分结果描述:")
    print(result[['CostRatio1', 'CostRatio9', 'InvestmentProfitRatio']].describe())
    
