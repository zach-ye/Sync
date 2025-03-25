import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
from util.TradingDate import TradingDate
from util import dir_range

class Evaluator_l1:
    def __init__(self, pool_name, feature_list, label_name):
        self.pool_name = pool_name
        self.label_name = label_name
        self.feature_list = feature_list

        current_file_path = Path(__file__).resolve()
        config_path = current_file_path.parent.parent / 'config' / 'config.json'
        config = json.load(open(config_path, 'r'))

        self.uni_path = Path(config['universe_path'])
        self.output_path = Path(config['output_path'])

    @staticmethod
    def calculate_ic_positive(group, feature):
        """Calculate IC for top half of sorted feature values"""
        sorted_group = group.sort_values(by=feature)
        half = sorted_group.iloc[len(sorted_group)//2:]
        return half['label'].corr(half[feature])

    @staticmethod
    def calculate_ic_negative(group, feature):
        """Calculate IC for bottom half of sorted feature values"""
        sorted_group = group.sort_values(by=feature)
        half = sorted_group.iloc[:len(sorted_group)//2]
        return half['label'].corr(half[feature])

    @staticmethod
    def process_feature(args):
        """Parallel processing function for a single feature"""
        feature, feature_df = args
        
        # Clean data for this feature
        df = feature_df.dropna(subset=[feature, 'label'])
        if df.empty:
            return feature, None, None, None, None

        # Calculate correlations
        try:
            ic = df.groupby('date').apply(lambda x: x['label'].corr(x[feature]))
            positive_ic = df.groupby('date').apply(
                lambda g: Evaluator_l1.calculate_ic_positive(g, feature)
            )
            negative_ic = df.groupby('date').apply(
                lambda g: Evaluator_l1.calculate_ic_negative(g, feature)
            )
        except Exception as e:
            print(f"Error processing {feature}: {str(e)}")
            return feature, None, None, None, None

        return feature, ic, positive_ic, negative_ic

    def backtest(self):
        """Main analysis pipeline with parallel processing"""
        td = TradingDate()
        dt_range = td.get_trading_date_range('2019-01-01', '2024-12-31')

        # Load and prepare data
        label_df = pd.read_feather(self.uni_path / 'all' / "universe.feather")
        label_df = label_df.query('20190101 <= DataDate <= 20241231')

        label_df = label_df[['STOCK_CODE', 'date', self.label_name]]

        # Load features and merge once
        pool = dir_range.read_date_range_feather(
            basedir=self.output_path / 'features' / self.pool_name,
            relpath=f'{self.pool_name}.feather',
            date_range=dt_range
        )

        pool['date'] = pd.to_datetime(pool['date'].astype(str), format='%Y%m%d')
        merged = pd.merge(pool, label_df, on=['date', 'STOCK_CODE'], how='inner')

        # Prepare feature-specific DataFrames
        feature_data = [
            (feature, merged[['date', feature, self.label_name]].copy())
            for feature in self.feature_list
        ]

        # Create output directory
        output_dir = self.output_path / self.pool_name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Parallel processing
        with Pool(processes=8) as pool:
            results = pool.map(self.process_feature, feature_data)

        # Process results and generate plots
        for result in results:
            feature, ic, pos_ic, neg_ic = result
            if ic is None:
                print(f"Skipping {feature} - no valid data")
                continue

            # Generate plot
            plt.figure(figsize=(12, 6))
            plt.title(f'Cumulative IC - {feature}')
            for series, label in zip(
                [ic, pos_ic, neg_ic],
                ['Full IC', 'Positive IC', 'Negative IC']
            ):
                plt.plot(series.index, series.cumsum(), label=label)
            
            plt.legend()
            plt.grid(True)
            plt.ylabel('Cumulative IC')
            fig_save_path = output_dir / self.pool_name / f'{feature}.png'
            plt.savefig(fig_save_path, bbox_inches='tight')
            plt.close()
