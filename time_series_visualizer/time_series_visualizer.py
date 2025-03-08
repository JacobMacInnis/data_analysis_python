import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()  # Enables time-series plotting support

# 📌 Import data and ensure 'date' is parsed as a datetime index
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
df.columns = df.columns.str.strip()  # Remove unnecessary whitespace in column names

# 🔹 Filter out the top 2.5% and bottom 2.5% of page views to remove extreme outliers
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]


def draw_line_plot():
    """
    Generates a **line plot** of daily page views over time.

    - Uses **Matplotlib** to create the line chart.
    - The x-axis represents **Date** and the y-axis represents **Page Views**.
    - Includes a **grid** for better readability.
    - Saves the output as **line_plot.png**.
    """

    # ✅ Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 5))

    # ✅ Plot the line graph (red line, thin width)
    ax.plot(df.index, df['value'], color='red', linewidth=1)

    # ✅ Formatting
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.grid(True)  # Enable grid

    # ✅ Save and return figure
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    """
    Generates a **bar chart** of monthly average page views, grouped by year.

    - Uses **Matplotlib** to create the grouped bar chart.
    - The x-axis represents **Years**, and bars within each group represent **Months**.
    - The y-axis represents **Average Page Views** per month.
    - Saves the output as **bar_plot.png**.
    """

    # ✅ Create a copy of the DataFrame and extract year and month
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # ✅ Group by year & month, calculating the mean page views for each
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # ✅ Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # ✅ Plot grouped bar chart with **colormap='tab10'** for distinct colors
    df_bar.plot(kind='bar', ax=ax, colormap='tab10')

    # ✅ Formatting
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(
        title="Months",
        labels=[
            'January', 'February', 'March', 'April', 'May', 'June', 'July', 
            'August', 'September', 'October', 'November', 'December'
        ],
        loc='upper left'
    )

    # ✅ Save and return figure
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    """
    Generates two **box plots**:
    
    1. **Year-wise Box Plot (Trend)** → Visualizes distribution of page views per year.
    2. **Month-wise Box Plot (Seasonality)** → Shows how page views fluctuate across months.

    - Uses **Seaborn** to create the box plots.
    - Saves the output as **box_plot.png**.
    """

    # ✅ Create a copy of the DataFrame and reset index
    df_box = df.copy().reset_index()

    # ✅ Ensure 'date' is in datetime format (should already be)
    df_box['date'] = pd.to_datetime(df_box['date'])

    # ✅ Extract year and month (use short names for months)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')  # Short month names

    # ✅ Convert 'value' column to numeric
    df_box['value'] = pd.to_numeric(df_box['value'], errors='coerce')

    # ✅ Define correct month order for consistent display
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # ✅ Create side-by-side box plots
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    # 🔹 **Year-wise Box Plot** (Trend over time)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # 🔹 **Month-wise Box Plot** (Seasonality trends)
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # ✅ Save and return figure
    fig.savefig('box_plot.png')
    return fig
