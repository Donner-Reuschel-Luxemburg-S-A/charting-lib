import numpy as np
from matplotlib import pyplot as plt
from source_engine.bloomberg_source import BloombergSource


def main():
    blp = BloombergSource()

    indices = ["UKX Index", "DAX Index", "FTSEMIB Index", "PSI20 Index", "CAC Index", "AEX Index",
               "SMI Index", "IBEX Index"]

    names = ["FTSE 100 Index", "DAX Index", "FTSE MIB Index", "PSI 20 Index", "CAC 40 Index", "AEX-Index",
             "Swiss Market Index", "IBEX 35 Index"]

    pe_ratio_dfs = [blp.get_series(series_id=idx, field="RR900", observation_start="20120101") for idx in indices]
    pe_ratios_backward = [df["y"].values for df, _ in pe_ratio_dfs]

    prices_df = [blp.get_series(series_id=idx, field="PX_LAST", observation_start="20120101") for idx in indices]
    prices = [df["y"].values for df, _ in prices_df]

    estimated_earnings_dfs = [blp.get_series(series_id=idx, field="INDX_WEIGHTED_EST_ERN", observation_start="20120101") for idx in indices]
    estimated_earnings = [df["y"].values for df, _ in estimated_earnings_dfs]

    pe_ratios_forward = [price/earnings for price, earnings in zip(prices, estimated_earnings)]

    latest_backward = [pe[-1] for pe in pe_ratios_backward]
    latest_forward = [pe[-1] for pe in pe_ratios_forward]

    num_indices = len(names)

    fig, ax = plt.subplots(figsize=(14, 8))

    positions_backward = np.arange(num_indices) * 2.0 - 0.4
    positions_forward = np.arange(num_indices) * 2.0 + 0.4

    ax.boxplot(pe_ratios_backward, positions=positions_backward, widths=0.8, patch_artist=True,
               boxprops=dict(facecolor='lightblue'), medianprops=dict(color='navy'))

    ax.boxplot(pe_ratios_forward, positions=positions_forward, widths=0.8, patch_artist=True,
               boxprops=dict(facecolor='lightgreen'), medianprops=dict(color='darkgreen'))

    ax.scatter(positions_backward, latest_backward, color='blue', marker='x', s=100, label='Latest Backward PE')
    ax.scatter(positions_forward, latest_forward, color='green', marker='x', s=100, label='Latest Forward PE')

    ax.set_xticks(np.arange(num_indices) * 2.0)
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.legend()

    ax.set_title('Backward and Forward P/E Ratios for European Indices')
    ax.set_ylabel('P/E Ratio')

    plt.savefig('test.png')


if __name__ == '__main__':
    main()
