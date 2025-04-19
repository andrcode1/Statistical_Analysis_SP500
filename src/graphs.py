import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.api import qqplot
from scipy import stats

COLS = ['Date','Open','High','Low','Close','Volume','Daily Return']

def load_data(filepath: str = "data/sp500_daily_returns.csv") -> pd.Series:
    data = pd.read_csv(filepath)
    daily_returns = data['Daily Return'].dropna()
    return daily_returns

def load_annual_means(filepath: str = "data/sp500_annual_data.csv") -> pd.Series:
    """Load full data and compute mean returns by quarter"""
    df = pd.read_csv(
        filepath,
        skiprows=3,
        header=None,
        names=COLS,
        parse_dates=['Date'],
        index_col='Date',
    )
    return df['Daily Return'].resample('YE').mean().dropna()

def plot_histogram_comparison(returns: pd.Series, save_path: str = None) -> None:
    """Plot a histogram of daily returns vs fitted normal distribution."""
    mu, sigma = returns.mean(), returns.std()
    normal_dist = np.random.normal(mu, sigma, 100000)
    
    plt.figure(figsize=(10, 6))
    sns.histplot(returns, bins=50, kde=True, color='steelblue', 
                stat='density', label='S&P 500 Returns')
    sns.histplot(normal_dist, bins=50, kde=True, color='red', 
                stat='density', alpha=0.3, label='Normal Dist')
    shapiro_p = stats.shapiro(returns)[1]
    plt.title(
        "S&P 500 Returns vs. Normal Distribution\n"
        f"Shapiro-Wilk p={shapiro_p:.3f}",
        pad=20
    )
    plt.legend()
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def plot_qq(returns: pd.Series, save_path: str = None) -> None:
    """Generate a QQ-plot of returns against a standard normal."""
    qqplot(returns, line='s')
    
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()

def demonstrate_clt_annual(quarter_means: pd.Series, save_path: str = None) -> None:
    """Illustrate the Central Limit Theorem on annual mean returns."""

    plt.figure(figsize=(10, 6))
    sns.histplot(quarter_means, kde=True, stat='density',
                 color='steelblue', label='Annual Means')
    
    mu, sigma = quarter_means.mean(), quarter_means.std()
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma), 'r--', linewidth=2,
             label=f'Normal Fit (μ={mu:.4f}, σ={sigma:.4f})')
    
    shapiro_p = stats.shapiro(quarter_means)[1]
    plt.title(
        f"CLT with Annual Means (n={len(quarter_means)})\n"
        f"Shapiro-Wilk p={shapiro_p:.3f}",
        pad=20
    )
    plt.xlabel("Annual Quarter Return")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300)
        plt.close()
    else:
        plt.show()

def run_normality_tests(returns: pd.Series) -> None:
    print("\nNormality Test Results:")
    print(f"Shapiro-Wilk p-value: {stats.shapiro(returns)[1]:.4f}")
    print(f"Mean: {returns.mean():.6f}")
    print(f"Standard Deviation: {returns.std():.6f}")

def main():
    try:
        returns = load_data("data/sp500_daily_returns.csv")
        plot_histogram_comparison(returns, 'data/returns_histogram.png')
        plot_qq(returns, 'data/qqplot_daily.png')
        run_normality_tests(returns)

        annual_means = load_annual_means("data/sp500_annual_data.csv")
        demonstrate_clt_annual(annual_means, save_path='data/clt_annual_means.png')
        plot_qq(annual_means, 'data/qqplot_annual.png')
        run_normality_tests(annual_means)

        print("\nAnalysis complete. Results saved to /data directory.")
    except Exception as e:
        print(f"\nError occurred during analysis: {str(e)}")

if __name__ == "__main__":
    main()