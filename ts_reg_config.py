import pandas as pd
import numpy as np
from sklearn.utils import check_array

# ================== 回归配置 ==================
REGRESSION_CONFIGS = [
    {
        'y': 'np',                # 因变量：净利润
        'x': ['roa', 'roe'],      # 自变量：总资产净利率、净资产收益率
        'groupby': ['stock_code'],  # 分组键（支持多列分组）
        'window_size': 8,         # 时间窗口大小
        'prefix': 'np_roa_roe'    # 结果列前缀
    },
    {
        'y': 'op',                # 因变量：营业利润
        'x': ['gp_ratio', 'nf_margin'],  # 自变量：营业利润率、净利润率
        'groupby': ['stock_code'],
        'window_size': 12,
        'prefix': 'op_gp_nf'
    }
]


# ================== 核心函数 ==================
def calculate_time_series_regressions(df, configs=REGRESSION_CONFIGS):
    """
    时间序列回归主函数（支持多列分组和灵活窗口）
    
    :param df: 包含基础字段的DataFrame（需包含groupby列和时间字段）
    :param configs: 回归配置列表
    :return: 包含回归系数、残差和R²的DataFrame
    """
    df = df.copy().sort_values(by=['declare_date'])  # 先按时间排序
    
    for config in configs:
        y = config['y']
        x = config['x']
        groupby = config['groupby']
        window = config['window_size']
        prefix = config['prefix']
        
        # 生成结果列名
        cols = {
            'intercept': f'intercept_{prefix}',
            'residual': f'residual_{prefix}',
            'r2': f'r2_{prefix}'
        }
        slope_cols = {f'slope_{var}_{prefix}': var for var in x}  # 斜率列
        
        # 初始化结果列
        df[cols.values() + list(slope_cols.keys())] = np.nan
        
        # 分组处理（支持多列分组，如['stock_code', 'industry']）
        for key, group in df.groupby(groupby):
            # 数据清洗与排序
            valid_group = group.dropna(subset=[y] + x)\
                               .sort_values(by='declare_date')
            
            if len(valid_group) < 2:  # 至少需要2个点拟合
                continue
            
            # 截取最近N个数据
            window_data = valid_group.tail(window)
            if len(window_data) < 2:
                continue
            
            # 构造回归矩阵
            X = window_data[x].values
            y_values = window_data[y].values.reshape(-1, 1)
            
            # 带截距项的回归矩阵
            X_with_intercept = np.hstack([np.ones((len(X), 1)), X])
            
            # 最小二乘回归
            try:
                coeffs, residuals, rank, _ = np.linalg.lstsq(
                    X_with_intercept, y_values, rcond=None
                )
            except np.LinAlgError:
                continue  # 处理奇异矩阵
            
            # 提取结果
            intercept = coeffs[0, 0]
            slopes = coeffs[1:, 0] if len(coeffs) > 1 else []
            residual = y_values - X_with_intercept @ coeffs
            ss_res = np.sum(residual**2)
            ss_tot = np.sum((y_values - y_values.mean())**2)
            r2 = 1 - ss_res/ss_tot if ss_tot != 0 else 0
            
            # 赋值结果
            window_data[cols['intercept']] = intercept
            window_data[cols['residual']] = residual.flatten()
            window_data[cols['r2']] = r2
            
            # 赋值斜率
            for i, var in enumerate(x):
                window_data[list(slope_cols.keys())[i]] = slopes[i]
            
            # 更新原DataFrame
            df.update(window_data[cols.values() + list(slope_cols.keys())])
    
    return df


# ================== 使用示例 ==================
if __name__ == "__main__":
    # 模拟数据（包含2只股票，每只15个时间点）
    data = pd.DataFrame({
        'stock_code': ['A']*15 + ['B']*15,
        'declare_date': pd.date_range('2020-01-01', periods=30, freq='Q'),
        'np': np.random.randn(30)*100,       # 净利润
        'roa': np.random.randn(30)*0.1 + 0.05, # 总资产净利率
        'roe': np.random.randn(30)*0.2 + 0.1,  # 净资产收益率
        'gp_ratio': np.random.randn(30)*0.15, # 营业利润率
        'nf_margin': np.random.randn(30)*0.1  # 净利润率
    })
    
    # 执行回归
    result = calculate_time_series_regressions(data)
    
    # 查看结果（股票A最后8行）
    print("回归结果示例（股票A最后8行）:")
    print(result[result['stock_code']=='A'].tail(8)[
        ['stock_code', 'declare_date', 'intercept_np_roa_roe', 
         'slope_roa_np_roa_roe', 'slope_roe_np_roa_roe', 'residual_np_roa_roe', 'r2_np_roa_roe']
    ])
