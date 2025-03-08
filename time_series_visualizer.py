import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import calendar

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
# df = pd.read_csv('fcc-forum-pageviews.csv')
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
df.columns = df.columns.str.strip()

print(len(df))
# Clean data
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]
print(len(df))

def draw_line_plot():
    # Draw line plot

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(df.index, df['value'], color='red', linewidth=1)

    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.grid(True)
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    
    # df_bar = df
    # df_bar['date'] = pd.to_datetime(df['date'])
    # df_bar['month'] = df_bar['date'].dt.month
    # df_bar['year'] = df_bar['date'].dt.year
    # # Draw bar plot
    # df_bar = df_bar.groupby(['year', 'month'], as_index=False)['value'].sum()
    # fig, ax = plt.subplots(figsize=(12,12))


    # years = df_bar['year'].unique()
    # width = 0.08
    # colors = {
    #     1: "blue",
    #     2: "green",
    #     3: "red",
    #     4: "purple",
    #     5: "orange",  # ✅ Replace 'pumpkin' with 'orange'
    #     6: "pink",
    #     7: "brown",
    #     8: "cyan",
    #     9: "lime",
    #     10: "magenta",
    #     11: "yellow",
    #     12: "black"
    # }

    # multiplier = 0
    # gap = 1
    # for i, month in enumerate(range(1,13)):
    #     # sorted(df_bar['year'].unique()):
    #     month_values = []
    #     # for month in range(1,13):
    #     for year in years:
    #         views = df_bar[(df_bar['year'] == year) & (df_bar['month'] == month)]
    #         value = views['value'].values[0] if not views.empty else 0
    #         print('value', value)
    #         month_values.append(value)

    #     month_name = calendar.month_name[month]

    #     x_positions = [y + (j * gap) + (i * width) for j,y  in enumerate(years)]
    #     # ax.bar()

    #     ax.bar(x_positions, month_values, width=width, label=month_name, color=colors[month])
            


    # ax.set_ylabel('Average Page Views')
    # ax.set_xlabel('Years')
    # # Calculate the center of each year group for x-ticks
    # year_positions = [y + ((12 * width) / 2) + (gap * i) for i, y in enumerate(years)]

    # # Set the adjusted x-ticks
    # ax.set_xticks(year_positions)
    # ax.set_xticklabels(years,rotation=90)
    
    # ax.legend(loc='upper left', title='Months', ncols=1,  )
    # ax.set_ylim(0, 4000000)

    # # Save image and return fig (don't change this part)
    # fig.savefig('bar_plot.png')
    # return fig

    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    df_bar.plot(kind='bar', ax=ax, colormap='tab10')

    # Labels and Formatting
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=[
        'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
    ], loc='upper left')

    # Save and Return
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy().reset_index()

    # ✅ Convert 'date' column to datetime (if not already)
    df_box['date'] = pd.to_datetime(df_box['date'])

    # ✅ Extract 'year' and 'month' features
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Short month names

    # ✅ Convert 'value' column to numeric type
    df_box['value'] = pd.to_numeric(df_box['value'], errors='coerce')

    # ✅ Define the correct month order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Create Subplots
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # ✅ Year-wise Box Plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # ✅ Month-wise Box Plot
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # ✅ Save and return the figure
    fig.savefig('box_plot.png')
    return fig
