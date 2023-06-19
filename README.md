<p align="center">
    <img src="https://www.donner-reuschel.lu/wp-content/uploads/2019/10/Donner-Reuschel-Logo-1-300x115.png">
</p>

The Charting Library is a Python library for generating customizable charts using Matplotlib. It provides a simple and intuitive way to create various types of charts, including line charts, bar charts, and scatter plots.

## Features

- Customizable axes, labels, and formatting options.
- Multiple y-axes support for displaying multiple series with different scales.
- Support for applying transformation functions to time series data.
- Save charts as PNG images.

## Available Transformers

- Invert 
- Average
- Lead
- Lag
- Resample

## Available Charts

- Time Series Chart
- Bar Chart

## Example

```python
# Data
df = pd.read_excel('nfib.xlsx', header=0, parse_dates=['Dates'], index_col='Dates')

# Create Chart
chart = TimeSeriesChart(title="NFIB Small Business Higher Prices & Nat'l Fed. of Ind. Business", num_y_axes=2)

# Configure y-axes
chart.configure_y_axis(axis_index=0, label="Last Price [€]", y_lim=(-35, 70), minor_locator=MultipleLocator(10))
chart.configure_y_axis(axis_index=1, label="Last Price [€]", minor_locator=MultipleLocator(0.5))

# Configure x-axis
major_locator = mdates.YearLocator(base=5)
minor_locator = mdates.YearLocator(base=1)
major_formatter = mdates.AutoDateFormatter(major_locator)
chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

chart.configure_x_ticks(which='minor', length=3, width=1)
chart.configure_x_ticks(which='major', length=20, width=1, pad=10)

# Add data to the chart
chart.add_data(df.index, df['SBOIPRIC Index'], label="NFIB Small Business Higher Prices", y_axis=0, color="black", fill=True,
               fill_color='skyblue', fill_threshold=-35, transformer=[Resample('M'), Lead(window=timedelta(weeks=40))])
chart.add_data(df.index, df['CLEVCPIA Index'], label="Federal Reserve Bank of Cleveland Median CPI YoY NSA",
               y_axis=1, color="skyblue", transformer=Resample('M'))

# Set legend
chart.legend(frameon=False, ncol=2)

# Save the plot
chart.plot(path="output/example.png")
```

Result:

![alt text](examples/output/example.png)

## Second example

```python
df = pd.read_csv('resources/DRTSCILM.csv', header=0, parse_dates=['DATE'], index_col='DATE')
pmi = pd.read_excel('resources/us-pmi.xlsx', header=5, parse_dates=['Dates'], index_col='Dates')
rec = pd.read_excel('resources/us-recession.xlsx', header=5, parse_dates=['Dates'], index_col='Dates')

chart = TimeSeriesChart(title="As industrial loan standards tighten, manufacturing contracts",
                        figsize=(14, 6), num_y_axes=2)

chart.configure_y_axis(axis_index=0, label="PMI Index", y_lim=(20, 65))
chart.configure_y_axis(axis_index=1, label="%", y_lim=(80, -40), invert_axis=True)

major_locator = mdates.YearLocator(base=2)
major_formatter = mdates.AutoDateFormatter(major_locator)
chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)

chart.add_data(pmi.index, pmi['PX_LAST'], label="US Manufacturing PMI", chart_type='bar',
               y_axis=0, bar_bottom=50, transformer=Center(val=50), alpha=0.7)
chart.add_data(df.index, df['DRTSCILM'], label="Tightening standards for C&I loans", y_axis=1)
chart.add_horizontal_line(y=0, axis_index=1)
chart.add_vertical_line(x=rec.index, y=rec["PX_LAST"], label="US Recession")

chart.legend(frameon=False, ncol=3)
chart.plot(path="output/loan.png")
```

Result:

![alt text](examples/output/loan.png)

