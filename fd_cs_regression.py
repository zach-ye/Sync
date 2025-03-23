import pandas as pd
import numpy as np
from factor.pool_base import _PoolBaseDaily
from util.TradingDate import TradingDate
from scipy.stats import norm
import statsmodels.api as sm

class fd_cs_regression(_PoolBaseDaily):


    def load_daily_data(self, date):
        td = TradingDate()
        year = int(date[:4])
        data_path = self.zyyx_path / 'fin_main_ratio.feather'
        data = pd.read_feather(data_path)

        data = data[(data['REPORT_TYPE'] == 1081) | (data['REPORT_TYPE'] == 1083)]

        data["ENTRYDATE"] = data["ENTRYTIME"].dt.date
        data = data[(data['ENTRYDATE'].astype(str) < date) & (data['ENTRYDATE'].astype(str) >= td.prev_tradingday(date, 2*252))]

        data = data[(data['DECLARE_DATE'].astype(str) < date) & (data['DECLARE_DATE'].astype(str) >= td.prev_tradingday(date, 2*252))]

        data = data[data['REPORT_YEAR'] >= year - 3]
        data = data.sort_values(by=['REPORT_YEAR', 'REPORT_QUARTER', 'REPORT_TYPE', 'UPDATETIME'])

        data = data.drop_duplicates(subset=['STOCK_CODE', 'REPORT_YEAR', 'REPORT_QUARTER'], keep='last')

        data = data[data.groupby('STOCK_CODE')['STOCK_CODE'].transform('size') >= 4]

        reverse_rank = data.groupby('STOCK_CODE').cumcount(ascending=False)

        filtered_df = data[reverse_rank < 4]
        columns_to_process = [
            "GP_RATIO", "ROE", "ROA", "NF_MARGIN", "MAN_RATIO", "FE_RATIO", "MAR_RATIO", "TP_CE_RATIO", "EXP_RATIO",
            "AR_TURNOVER", "INV_TURNOVER", "WC_TURNOVER", "TA_TURNOVER", "FA_TURNOVER", "CA_TURNOVER", "NA_TURNOVER",
            "CA_RATIO", "MP_RATIO", "TMA_TATIO", "INV_RATIO", "FA_RATIO", "DS_RATIO", "DEBT_EQ_RATIO", "EQ_AS_RATIO",
            "DEBT_AS_RATIO", "EQ_MULTIPLIER", "CUR_RATIO", "QUICK_RATIO", "CASH_RATIO", "INT_MULTIPLIER", "CD_RATIO",
            "OR_GRATE_YOY", "OR_GRATE_OQ", "NP_GRATE_YOY", "NP_GRATE_OQ", "NA_GRATE_YOY", "NA_GRATE_OQ",
            "FA_GRATE_YOY", "FA_GRATE_OQ", "OP_GRATE_YOY", "OP_GRATE_OQ", "NCFOA_CL_RATIO", "NCFOA_TL_RATIO",
            "ICFOA_OR_RATIO", "ICFOA_OR_RATIO_TTM", "NCF_TA_RATIO", "NCF_TA_RATIO_TTM", "NCFOA_OR_RATIO",
            "NCFOA_OR_RATIO_TTM", "NCFOA_NP_RATIO", "NCFOA_NP_RATIO_TTM"
        ]
        std_last4_df = filtered_df.groupby('STOCK_CODE')[columns_to_process].std().add_suffix('_last4q_std').reset_index()
        std_last4_df['date'] = date


    @property
    def reg_config(self):
        REG_CONFIGS = [
            {
                "name": "hetero_roa",
                "y": "ROA",
                "x": ["DEBT_AS_RATIO", "log_listing_age", "sw1_dummy"],
                "normalize": {
                    "ROA": "mad_10",
                    "DEBT_AS_RATIO": "mad_10"
                }
            },
            {
                "name": "core_gp",
                "y": "GP_RATIO",
                "x": ["MAR_RATIO", "LOG_TA", "sw1_summy"],
                "normalize": {
                    "GP_RATIO": "mad_10",
                    "MAR_RATIO": "mad_10"
                }
            },
            {
                "name": "efficient_turnover",
                "y": "TA_TURNOVER",
                "x": ["FA_RATIO", "OR_GRATE_YOY", "sw1_dummy"],
                "normalize": {
                    "TA_TURNOVER": "mad_10",
                    "FA_RATIO": "mad_10"
                }
            },
            {
                "name": "cash_quality",
                "y": "NCFOA_NP_RATIO",
                "x": ["NF_MARGIN", "AR_TURNOVER", "sw1_dummy"],
                "normalize": {
                    "NCFOA_NP_RATIO": "mad_10",
                    "NF_MARGIN": "mad_10"
                }
            }
        ]
        return REG_CONFIGS

    
    def normalize_column(self, s, method, **kwargs):
        """Generic normalization dispatcher"""
        if method == 'mad_10':
            return self.cut_mad_10(s)
        elif method == 'winsorize':
            return self.winsorize(s, **kwargs)
        elif method == 'gaussian_rank':
            return self.gaussian_rank(s, **kwargs)
        else:
            raise ValueError(f"Unknown normalization method: {method}")

    def cut_mad_10(self, s):
        median = s.median()
        mad = s.mad()
        return s.clip(median - 10 * mad, median + 10 * mad)

    def winsorize(self, s, lower=0.01, upper=0.99):
        q = s.quantile([lower, upper])
        return s.clip(q.iloc[0], q.iloc[1])

    def gaussian_rank(self, s, clip_lower=0.05, clip_upper=0.95):
        """Gaussian rank normalization with optional clipping"""
        ranked = s.rank(pct=True)
        clipped = ranked.clip(clip_lower, clip_upper)
        return clipped.apply(norm.ppf)
    
   
    def calculate_cross_section_factors(self, date):
        curr_df = self.load_daily_data(date)
        
        # Add transformed columns
        curr_df['log_listing_age'] = np.log1p(curr_df['listing_age'])
        curr_df['LOG_TA'] = np.log(curr_df['total_assets'])
        
       
        curr_df, ind_cols = self.create_industry_dummies(curr_df)
        
        factor_results = curr_df[['stock_code']].copy()
        
        for config in self.reg_config:
            y_col = config['y']
            X_cols = config['x']
            normalize_config = config.get('normalize', {})
            
            
            X_cols_expanded = []
            for col in X_cols:
                if col == 'industry_dummy':
                    X_cols_expanded.extend(ind_cols)
                else:
                    X_cols_expanded.append(col)
            
            # Prepare regression data
            all_cols = [y_col] + X_cols_expanded
            data = curr_df[all_cols].dropna()
            
            if len(data) < 10:
                factor_results[config['name']] = np.nan
                continue
                
            # Apply column-wise normalization
            for col, method in normalize_config.items():
                if col not in data.columns:
                    continue  # Skip missing columns
                
                # Handle method parameters
                kwargs = {}
                if method == 'winsorize':
                    kwargs = {'lower': 0.05, 'upper': 0.95}  # Defaults can be changed
                
                data[col] = self.normalize_column(data[col], method, **kwargs)
            
            # Prepare matrices
            y = data[y_col]
            X = sm.add_constant(data[X_cols_expanded])
            
            # Run regression
            try:
                model = sm.OLS(y, X).fit()
                residuals = y - model.predict(X)
                
                # Map residuals to original index
                factor_values = curr_df.index.map(
                    pd.Series(residuals, index=data.index).to_dict()
                ).fillna(np.nan)
                factor_results[config['name']] = factor_values
            except Exception as e:
                print(f"Regression failed for {config['name']}: {str(e)}")
                factor_results[config['name']] = np.nan
        
        return factor_results

    
    def create_industry_dummies(self, df, industry_col='industry_code'):
        """Create industry dummy variables with prefix"""
        dummies = pd.get_dummies(
            df[industry_col], 
            prefix='ind',
            drop_first=True
        )
        return pd.concat([df, dummies], axis=1), list(dummies.columns)
