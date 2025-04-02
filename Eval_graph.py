import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
import concurrent.futures
import os
from typing import List, Dict, Tuple, Optional
import datetime

class GraphEvaluator:
    def __init__(self, graph_path: str, label_path: str, start_year: int = None, end_year: int = None):
        """
        Initialize the GraphEvaluator.
        
        Args:
            graph_path: Path to the directory containing graph adjacency matrices
            label_path: Path to the directory containing label adjacency matrices
            start_year: Starting year for evaluation (inclusive)
            end_year: Ending year for evaluation (inclusive)
        """
        self.graph_path = Path(graph_path)
        self.label_path = Path(label_path)
        self.start_year = start_year
        self.end_year = end_year
        self.dates = self._get_common_dates()
        
    def _get_common_dates(self) -> List[str]:
        """Get the list of dates that have both graph and label data within the specified year range."""
        # Get all available dates
        graph_files = set(f.stem for f in self.graph_path.glob("**/*.feather"))
        label_files = set(f.stem for f in self.label_path.glob("**/*.feather"))
        common_dates = sorted(list(graph_files.intersection(label_files)))
        
        # Filter by year range if specified
        if self.start_year is not None or self.end_year is not None:
            filtered_dates = []
            for date in common_dates:
                try:
                    year = int(date[:4])
                    if ((self.start_year is None or year >= self.start_year) and 
                        (self.end_year is None or year <= self.end_year)):
                        filtered_dates.append(date)
                except (ValueError, IndexError):
                    # Skip dates that don't have a valid year format
                    continue
            return filtered_dates
        
        return common_dates
    
    def _load_data_for_date(self, date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load graph and label adjacency matrices for a specific date.
        
        Args:
            date: Date in format 'yyyymmdd'
            
        Returns:
            Tuple of (graph_df, label_df)
        """
        year = date[:4]
        graph_file = self.graph_path / year / f"{date}.feather"
        label_file = self.label_path / year / f"{date}.feather"
        
        try:
            graph_df = pd.read_feather(graph_file)
            label_df = pd.read_feather(label_file)
            return graph_df, label_df
        except Exception as e:
            raise RuntimeError(f"Failed to load data for date {date}: {e}")
    
    def _find_common_stocks(self, graph_df: pd.DataFrame, label_df: pd.DataFrame) -> List[str]:
        """Find stocks that are present in both adjacency matrices."""
        graph_stocks = set(graph_df.index)
        label_stocks = set(label_df.index)
        return sorted(list(graph_stocks.intersection(label_stocks)))
    
    def _get_top_k_similar(self, df: pd.DataFrame, stock: str, k: int) -> List[str]:
        """
        Get the top k most similar stocks for a given stock.
        
        Args:
            df: Adjacency matrix
            stock: Stock code
            k: Number of similar stocks to retrieve
            
        Returns:
            List of top k similar stock codes
        """
        # Get the column for the stock and sort it in descending order
        similarities = df[stock].sort_values(ascending=False)
        
        # Exclude the stock itself (which will have highest similarity)
        if stock in similarities.index:
            similarities = similarities.drop(stock)
            
        # Return the top k
        return similarities.head(k).index.tolist()
    
    def _calculate_recall_at_k(self, 
                              predicted: List[str], 
                              actual: List[str], 
                              k: int) -> float:
        """
        Calculate recall@k.
        
        Args:
            predicted: List of predicted similar stocks
            actual: List of actual similar stocks
            k: k value for recall@k
            
        Returns:
            Recall@k value
        """
        # Take only the first k elements from each list
        predicted_k = predicted[:k]
        actual_k = actual[:k]
        
        # Count how many predicted stocks are in the actual list
        matches = len(set(predicted_k).intersection(set(actual_k)))
        
        # Calculate recall
        return matches / len(actual_k) if actual_k else 0.0
    
    def process_date(self, date: str) -> Tuple[str, Dict[int, float]]:
        """
        Process a single date to calculate recall@k for different k values.
        
        Args:
            date: Date in format 'yyyymmdd'
            
        Returns:
            Tuple of (date, Dictionary mapping k values to mean recall@k)
        """
        try:
            graph_df, label_df = self._load_data_for_date(date)
            common_stocks = self._find_common_stocks(graph_df, label_df)
            
            # Dictionary to store recall values for different k
            recalls = {1: [], 5: [], 10: [], 20: []}
            
            # Calculate recall for each stock
            for stock in common_stocks:
                # Get top 20 similar stocks from both matrices
                # (we'll use these for different recall@k calculations)
                pred_similar = self._get_top_k_similar(graph_df, stock, 20)
                actual_similar = self._get_top_k_similar(label_df, stock, 20)
                
                # Calculate recall@k for different k values
                for k in recalls.keys():
                    recall = self._calculate_recall_at_k(pred_similar, actual_similar, k)
                    recalls[k].append(recall)
            
            # Calculate mean recall for each k
            mean_recalls = {k: np.mean(vals) for k, vals in recalls.items()}
            
            print(f"Processed date: {date}")
            return date, mean_recalls
            
        except Exception as e:
            print(f"Error processing date {date}: {e}")
            return date, {}
    
    def evaluate_all_dates(self, max_workers: Optional[int] = None) -> Dict[str, Dict[int, float]]:
        """
        Process all dates in parallel and return recall metrics.
        
        Args:
            max_workers: Maximum number of worker threads/processes
            
        Returns:
            Dictionary mapping dates to recall metrics
        """
        results = {}
        
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            future_to_date = {executor.submit(self.process_date, date): date for date in self.dates}
            
            for future in concurrent.futures.as_completed(future_to_date):
                date = future_to_date[future]
                try:
                    date, recalls = future.result()
                    results[date] = recalls
                except Exception as e:
                    print(f"Error processing date {date}: {e}")
        
        return results
    
    def plot_results(self, results: Dict[str, Dict[int, float]], save_path: str) -> None:
        """
        Plot recall metrics over time and save the plot.
        
        Args:
            results: Dictionary mapping dates to recall metrics
            save_path: Path to save the plot
        """
        # Convert dates from string to datetime for better x-axis formatting
        dates = [datetime.datetime.strptime(date, '%Y%m%d') for date in sorted(results.keys())]
        
        # Extract recall values for each k
        recall_1 = [results[date.strftime('%Y%m%d')].get(1, np.nan) for date in dates]
        recall_5 = [results[date.strftime('%Y%m%d')].get(5, np.nan) for date in dates]
        recall_10 = [results[date.strftime('%Y%m%d')].get(10, np.nan) for date in dates]
        recall_20 = [results[date.strftime('%Y%m%d')].get(20, np.nan) for date in dates]
        
        # Create the plot
        plt.figure(figsize=(12, 8))
        plt.plot(dates, recall_1, label='Recall@1', marker='o', linestyle='-')
        plt.plot(dates, recall_5, label='Recall@5', marker='s', linestyle='-')
        plt.plot(dates, recall_10, label='Recall@10', marker='^', linestyle='-')
        plt.plot(dates, recall_20, label='Recall@20', marker='d', linestyle='-')
        
        # Set plot properties
        year_range = f"{self.start_year}-{self.end_year}" if self.start_year and self.end_year else "All Years"
        plt.title(f'Recall Performance Over Time ({year_range})')
        plt.xlabel('Date')
        plt.ylabel('Recall')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Format x-axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.gcf().autofmt_xdate()
        
        # Set y-axis limits
        plt.ylim(0, 1)
        
        # Save the plot
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Plot saved to {save_path}")

    def run_evaluation(self, save_path: str, max_workers: Optional[int] = None) -> None:
        """
        Run the full evaluation process and save the plot.
        
        Args:
            save_path: Path to save the plot
            max_workers: Maximum number of worker threads/processes
        """
        print(f"Starting evaluation with {len(self.dates)} dates from years {self.start_year} to {self.end_year}")
        results = self.evaluate_all_dates(max_workers)
        print(f"Evaluation complete, plotting results")
        self.plot_results(results, save_path)
        print(f"Evaluation finished!")
