import pandas as pd
import numpy as np
from sklearn.utils import check_array

# ================== 回归配置 ==================
REGRESSION_CONFIGS = [
    {
        'y': 'np',                # 因变量：净利润
        'x': ['roa', 'roe'],      # 自变量：总资产净利率、净资产收益率
        'window_size': 8,         # 时间窗口大小
        'factors': [             # 输出因子定义
            {'name': 'residual_np_roa_roe', 'type': 'last_residual'},
            {'name': 'r2_np_roa_roe', 'type': 'r2'},
            {'name': 'intercept_np_roa_roe', 'type': 'intercept'},
            {'name': 'slope_roa_np_roa_roe', 'type': 'slope', 'var': 'roa'},
            {'name': 'slope_roe_np_roa_roe', 'type': 'slope', 'var': 'roe'}
        ]
    },
    {
        'y': 'op',                # 因变量：营业利润
        'x': ['gp_ratio', 'nf_margin'],
        'window_size': 12,
        'factors': [
            {'name': 'residual_op_gp_nf', 'type': 'last_residual'},
            {'name': 'r2_op_gp_nf', 'type': 'r2'},
            {'name': 'intercept_op_gp_nf', 'type': 'intercept'},
            {'name': 'slope_gp_ratio_op_gp_nf', 'type': 'slope', 'var': 'gp_ratio'},
            {'name': 'slope_nf_margin_op_gp_nf', 'type': 'slope', 'var': 'nf_margin'}
        ]
    }
]


# ================== 核心函数 ==================
def calculate_time_series_factors(df, configs=REGRESSION_CONFIGS):
    """
    时间序列回归因子计算（每个股票仅保留最新结果）
    
    :param df: 包含基础字段的DataFrame
    :param configs: 回归配置列表
    :return: 因子数据框（每个股票一行，包含最新回归结果）
    """
    # 数据预处理
    df = df.sort_values(by=['stock_code', 'declare_date']).reset_index(drop=True)
    factors = []

    for config in configs:
        y = config['y']
        x = config['x']
        window = config['window_size']
        factor_defs = config['factors']

        # 提取每个股票的最新回归结果
        def process_group(group):
            valid_group = group.dropna(subset=[y] + x).sort_values(by='declare_date')
            if len(valid_group) < 2:
                return None
            
            window_data = valid_group.tail(window)
            if len(window_data) < 2:
                return None
            
            X = window_data[x].values
            y_values = window_data[y].values.reshape(-1, 1)
            X_with_intercept = np.hstack([np.ones((len(X), 1)), X])
            
            try:
                coeffs, residuals, rank, _ = np.linalg.lstsq(X_with_intercept, y_values, rcond=None)
            except np.LinAlgError:
                return None
            
            result = {'stock_code': group['stock_code'].iloc[0]}
            
            # 计算R²
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y_values - y_values.mean())**2)
            result['r2'] = 1 - ss_res/ss_tot if ss_tot != 0 else 0
            
            # 截距
            result['intercept'] = coeffs[0, 0]
            
            # 斜率
            for i, var in enumerate(x):
                result[f'slope_{var}'] = coeffs[i+1, 0] if len(coeffs) > 1 else np.nan
            
            # 最后一个残差
            result['last_residual'] = residuals[-1, 0] if len(residuals) > 0 else np.nan
            
            return result
        
        # 按股票分组处理
        group_results = df.groupby('stock_code').apply(process_group).dropna()
        
        # 转换为因子格式
        if not group_results.empty:
            factor_df = pd.DataFrame(group_results.tolist())
            
            # 映射因子定义
            for factor in factor_defs:
                factor_name = factor['name']
                factor_type = factor['type']
                
                if factor_type == 'r2':
                    factor_df[factor_name] = factor_df['r2']
                elif factor_type == 'intercept':
                    factor_df[factor_name] = factor_df['intercept']
                elif factor_type == 'last_residual':
                    factor_df[factor_name] = factor_df['last_residual']
                elif factor_type == 'slope':
                    var = factor['var']
                    factor_df[factor_name] = factor_df[f'slope_{var}']
            
            factors.append(factor_df[['stock_code'] + [f['name'] for f in factor_defs]])

    # 合并所有因子
    if factors:
        return pd.concat(factors, axis=1).drop_duplicates('stock_code')
    else:
        return pd.DataFrame(columns=['stock_code'] + [f['name'] for cfg in configs for f in cfg['factors']])


# ================== 使用示例 ==================
if __name__ == "__main__":
    # 模拟数据（包含2只股票，每只15个时间点）
    data = pd.DataFrame({
        'stock_code': ['A']*15 + ['B']*15,
        'declare_date': pd.date_range('2020-01-01', periods=30, freq='Q'),
        'np': np.random.randn(30)*100,       # 净利润
        'roa': np.random.randn(30)*0.1 + 0.05, # 总资产净利率
        'roe': np.random.randn(30)*0.2 + 0.1,  # 净资产收益率
        'op': np.random.randn(30)*50,        # 营业利润
        'gp_ratio': np.random.randn(30)*0.15, # 营业利润率
        'nf_margin': np.random.randn(30)*0.1  # 净利润率
    })
    
    # 计算因子
    factors = calculate_time_series_factors(data)
    
    # 查看结果
    print("最终因子结果（每个股票一行）:")
    print(factors.set_index('stock_code'))
