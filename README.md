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

## Example 1

```python
df1, t1 = blp.get_series(series_id='SBOIPRIC Index', observation_start='19950131')
df2, t2 = blp.get_series(series_id='CLEVCPIA Index', observation_start='19950131')

chart = TimeSeriesChart(title="NFIB Small Business Higher Prices & Nat'l Fed. of Ind. Business", num_y_axes=2)

chart.configure_y_axis(axis_index=0, label="Last Price [€]", y_lim=(-35, 70), minor_locator=MultipleLocator(10))
chart.configure_y_axis(axis_index=1, label="Last Price [€]", minor_locator=MultipleLocator(0.5))

major_locator = mdates.YearLocator(base=5)
minor_locator = mdates.YearLocator(base=1)
major_formatter = mdates.AutoDateFormatter(major_locator)
chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

chart.configure_x_ticks(which='minor', length=3, width=1)
chart.configure_x_ticks(which='major', length=10, width=1, pad=5)

chart.add_data(x=df1.index, y=df1['y'], label=t1, y_axis=0, fill=True,
               fill_threshold=-35, transformer=[Resample('M'), Lead(offset=DateOffset(months=10))])
chart.add_data(x=df2.index, y=df2['y'], label=t2, y_axis=1,  transformer=Resample('M'))

chart.legend(frameon=False, ncol=1)
chart.plot(path="output/cpi.png")
```

Result:

![alt text](examples/charts/output/cpi.png)

## Example 2

```python
d1, t1 = fred.get_series(series_id='DRTSCILM')  # DRTSCILM
d2, t2 = fred.get_series(series_id='JHDUSRGDPBR')  # USRINDEX Index
d3, t3 = blp.get_series(series_id='NAPMPMI Index', observation_start=19900131)

chart = TimeSeriesChart(title="As industrial loan standards tighten, manufacturing contracts", num_y_axes=2)

chart.configure_y_axis(axis_index=0, label="PMI Index", y_lim=(20, 65))
chart.configure_y_axis(axis_index=1, label="%", y_lim=(80, -40), invert_axis=True)

minor_locator = mdates.YearLocator(base=1)
major_locator = mdates.YearLocator(base=4)
major_formatter = mdates.AutoDateFormatter(major_locator)
chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

chart.add_data(x=d1.index, y=d1['y'], label="Tightening standards for C&I loans", y_axis=1)
chart.add_data(x=d3.index, y=d3['y'], label=t3, chart_type='bar',
               y_axis=0, bar_bottom=50, transformer=Center(val=50), alpha=0.7)
chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")
chart.add_horizontal_line(y=0, axis_index=1)

chart.legend(frameon=False, ncol=2)
chart.plot(path="output/loan.png")
```

Result:

![alt text](examples/charts/output/loan.png)

## Example 3:

```python
d1, t1 = fred.get_series(series_id='RSAFS', observation_start="2020-01-01")

chart = TimeSeriesChart(title="US retail sales: YoY change",num_y_axes=1)

major_locator = mdates.MonthLocator(interval=2)
major_formatter = mdates.DateFormatter(fmt="%b %Y")
chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)
chart.configure_x_ticks(length=5, pad=5, rotation=90)

chart.configure_y_axis(axis_index=0, label="%", y_lim=(0, 35))

chart.add_data(x=d1.index, y=d1['y'], label=t1, chart_type='bar',
               y_axis=0, bar_bottom=0, transformer=[Pct(periods=12), Avg(offset=DateOffset(months=3))])

chart.legend(frameon=False, ncol=1, bbox_to_anchor=(0.5, -0.3))
chart.plot(path="output/retail.png")
```

![alt text](examples/charts/output/retail.png)

### Example 4:

```python
d1, t1 = blp.get_series(series_id='BNKRINDX Index', observation_start="20060101")
d2, t2 = fred.get_series(series_id='JHDUSRGDPBR', observation_start="2006-01-01")

chart = TimeSeriesChart(title="Bankruptcy filings moving up in recent weeks", num_y_axes=2)

chart.configure_y_axis(axis_index=0, label="Count")
chart.configure_y_axis(axis_index=1, label="Count")

minor_locator = mdates.YearLocator(base=1)
major_locator = mdates.YearLocator(base=2)
major_formatter = mdates.DateFormatter("%Y")
chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

chart.add_data(x=d1.index, y=d1['y'], label="Bankruptcy filings", y_axis=0,
               transformer=Avg(offset=DateOffset(months=1)))
chart.add_data(x=d1.index, y=d1['y'], label="Bankruptcy filings", y_axis=1,
               transformer=Avg(offset=DateOffset(months=3)))
chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")

chart.legend(frameon=False, ncol=2)
chart.plot(path="output/bankruptcy.png")
```

![alt text](examples/charts/output/bankruptcy.png)

### Example 5:

```python
headline_df, headline_title = fred.get_series(series_id='CPIAUCSL', observation_start='2016-01-01')
core_df, core_title = fred.get_series(series_id='CPILFESL', observation_start='2016-01-01')

food_df, _ = blp.get_series(series_id='CPSFFOOD Index', observation_start='20160101')
x, y = Pct(periods=12).transform(food_df.index, food_df['y'])
food_df = DataFrame({'y': y}, index=x)
food_weights_df, _ = blp.get_series(series_id='CPIVFOOD Index', observation_start='20160101')
food_df['weighted'] = food_df['y'] * food_weights_df['y'].shift(12) / 100
food_df.index = food_df.index.to_period('M').to_timestamp(how='start')

energy_df, _ = blp.get_series(series_id='CPUPENER Index', observation_start='20160101')
energy_weights_df, _ = blp.get_series(series_id='CPIVENER Index', observation_start='20160101')
x, y = Pct(periods=12).transform(energy_df.index, energy_df['y'])
energy_df = DataFrame({'y': y}, index=x)
energy_df['weighted'] = energy_df['y'] * energy_weights_df['y'].shift(12) / 100
energy_df.index = energy_df.index.to_period('M').to_timestamp(how='start')

goods_df, _ = blp.get_series(series_id='CPUPCXFE Index', observation_start='20160101')
goods_weights_df, _ = blp.get_series(series_id='CPIVCLFE Index', observation_start='20160101')
x, y = Pct(periods=12).transform(goods_df.index, goods_df['y'])
goods_df = DataFrame({'y': y}, index=x)
goods_df['weighted'] = goods_df['y'] * goods_weights_df['y'].shift(12) / 100
goods_df.index = goods_df.index.to_period('M').to_timestamp(how='start')

services_df, _ = blp.get_series(series_id='CPUPSXEN Index', observation_start='20160101')
services_weights_df, _ = blp.get_series(series_id='CPIVSLES Index', observation_start='20160101')
x, y = Pct(periods=12).transform(services_df.index, services_df['y'])
services_df = DataFrame({'y': y}, index=x)
services_df['weighted'] = services_df['y'] * services_weights_df['y'].shift(12) / 100
services_df.index = services_df.index.to_period('M').to_timestamp(how='start')

chart = TimeSeriesChart(title="U.S. CPI by Component", num_y_axes=1)

chart.configure_y_axis(axis_index=0, label="%", minor_locator=MultipleLocator(1), y_lim=(-2.5, 10))

major_locator = mdates.YearLocator(base=1)
minor_locator = mdates.MonthLocator(interval=2)
major_formatter = mdates.AutoDateFormatter(major_locator)
chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

chart.configure_x_ticks(which='minor', length=3, width=1)
chart.configure_x_ticks(which='major', length=10, width=1, pad=5)

chart.add_horizontal_line(axis_index=0)

chart.add_data(x=headline_df.index, y=headline_df['y'], label="Headline YoY", y_axis=0, transformer=Pct(periods=12), linewidth=2)
chart.add_data(x=core_df.index, y=core_df['y'], label="Core YoY", y_axis=0, transformer=Pct(periods=12), linewidth=2)

chart.add_data(x=services_df.index, y=services_df['weighted'], chart_type='bar', stacked=True,
               label="Services (Ex Food & Energy)", y_axis=0)

chart.add_data(x=goods_df.index, y=goods_df['weighted'], chart_type='bar', stacked=True,
               label="Goods (Ex Food & Energy)",
               y_axis=0)

chart.add_data(x=food_df.index, y=food_df['weighted'], chart_type='bar', stacked=True, label="Food", y_axis=0)

chart.add_data(x=energy_df.index, y=energy_df['weighted'], chart_type='bar', stacked=True, label="Energy",
               y_axis=0)

chart.legend(frameon=False, ncol=2)
chart.plot(path="output/inflation.png")
```

![alt text](examples/charts/output/inflation.png)