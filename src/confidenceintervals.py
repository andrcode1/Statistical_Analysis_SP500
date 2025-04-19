import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats


def load_returns_data(filepath: str) ->pd.Series:
    return pd.read_csv(filepath)['Daily Return'].dropna()

def simulate_paths(returns: pd.Series, days: int, n_simulations: int) -> np.ndarray:
    """Run Monte Carlo simulation of cumulative returns"""
    mu, sigma = returns.mean(), returns.std()
    paths = np.zeros((days, n_simulations))
    
    for i in range(n_simulations):
        random_returns = np.random.normal(mu, sigma, days)
        paths[:, i] = (1 + random_returns).cumprod()
        
    return paths

def plot_fan_chart(paths: np.ndarray, days_to_project: int, confidence_level: float) -> None:
    """Plot and save a fan chart of Monte Carlo cumulative‐return simulations."""

    plt.figure(figsize=(12, 7))
    plt.plot(paths, color='gray', alpha=0.1, linewidth=0.8)
    
    median_path = np.median(paths, axis=1)
    lower_percentile = ((1 - confidence_level)/2) * 100
    upper_percentile = ((1 + confidence_level)/2) * 100

    lower_band = np.percentile(paths, lower_percentile, axis=1)
    upper_band = np.percentile(paths, upper_percentile, axis=1)
    
    plt.fill_between(
        range(days_to_project), 
        lower_band, 
        upper_band, 
        color='royalblue', 
        alpha=0.3,
        label=f'{int(confidence_level*100)}% Confidence Band'
    )
    
    # Median path
    plt.plot(
        median_path, 
        color='red', 
        linewidth=2.5, 
        linestyle='--',
        label='Median Path'
    )
    
    # Formatting
    plt.title(f"S&P 500 Cumulative Returns Projection\n({paths.shape[1]} Simulations, "
              f"{int(confidence_level*100)}% Confidence Band)", pad=20)
    plt.xlabel("Trading Days")
    plt.ylabel("Cumulative Return (Multiple of Investment)")
    plt.axhline(1, color='black', linestyle='-', linewidth=1)
    plt.legend(loc='upper left')
    plt.grid(alpha=0.2)
    
    # Annotations
    plt.annotate(
        f"Start: $1.00", 
        xy=(0, 1), 
        xytext=(10, 1.1),
        arrowprops=dict(arrowstyle="->"))
    plt.annotate(
        f"After {days_to_project} days:\n"
        f"Median: ${median_path[-1]:.2f}\n"
        f"{int(confidence_level*100)}% Range: ${lower_band[-1]:.2f}-${upper_band[-1]:.2f}", 
        xy=(days_to_project, median_path[-1]), 
        xytext=(days_to_project-50, median_path[-1]*0.7),
        arrowprops=dict(arrowstyle="->"))
    
    plt.tight_layout()
    plt.savefig('data/cumulative_returns_fan_chart.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    DATA_FILE = 'data/sp500_data.csv'
    DAYS_TO_PROJECT = 252  # 1 trading year
    N_SIMULATIONS = 1000
    CONFIDENCE_LEVEL = 0.95
    
    try:
        returns = load_returns_data(DATA_FILE)
        paths = simulate_paths(returns, DAYS_TO_PROJECT, N_SIMULATIONS)
        plot_fan_chart(paths, DAYS_TO_PROJECT, CONFIDENCE_LEVEL)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()