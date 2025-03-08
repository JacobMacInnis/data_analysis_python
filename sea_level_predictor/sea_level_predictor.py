import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

def draw_plot():
    """
    Generates a **scatter plot with two best-fit regression lines** to analyze 
    global sea level changes from historical data.

    - Uses **Matplotlib** to create the scatter plot and trend lines.
    - Uses **SciPy's linregress()** to calculate linear regression.
    - The x-axis represents **Year** (1880-2050).
    - The y-axis represents **CSIRO Adjusted Sea Level (inches)**.
    - Saves the output as **sea_level_plot.png**.

    Key Features:
    - **Scatter Plot** → Visualizes historical sea level data points.
    - **First Regression Line (Red)** → Covers **full dataset (1880-2050)**.
    - **Second Regression Line (Green)** → Covers **recent data (2000-2050)** for modern trend analysis.
    """

    # **1️⃣ Load Data**
    df = pd.read_csv("epa-sea-level.csv")

    # **2️⃣ Create Figure and Scatter Plot**
    fig, ax = plt.subplots(figsize=(10, 6))  # Create figure (10x6 inches)

    # 🔹 Scatter Plot: Visualizes the raw data points
    ax.scatter(
        df["Year"], df["CSIRO Adjusted Sea Level"], 
        label="Data", color='blue', alpha=0.6  # Alpha makes it slightly transparent
    )

    # **3️⃣ Function to Fit and Plot Regression Line**
    def plot_best_fit(df_subset, start_year, color, label):
        """
        Fits a regression line using `scipy.stats.linregress()` and plots it.
        
        - `df_subset`: The subset of the data to fit the regression.
        - `start_year`: The first year in the range (1880 or 2000).
        - `color`: Color of the regression line.
        - `label`: Legend label.
        """
        # 🔹 Compute the regression line (y = mx + b)
        slope, intercept, _, _, _ = linregress(df_subset["Year"], df_subset["CSIRO Adjusted Sea Level"])

        # 🔹 Generate predicted values for the range (extrapolating to 2050)
        years = np.arange(start_year, 2051)  # Years from `start_year` to 2050
        sea_levels = slope * years + intercept  # Compute corresponding sea levels

        # 🔹 Plot the regression line
        ax.plot(years, sea_levels, color=color, label=label, linewidth=2)

    # **4️⃣ Plot Two Best Fit Lines**
    plot_best_fit(df, 1880, 'r', "Best Fit (1880-2050)")  # 🔴 Full dataset regression (Historical Trend)
    plot_best_fit(df[df["Year"] >= 2000], 2000, 'g', "Best Fit (2000-2050)")  # 🟢 Recent trend regression

    # **5️⃣ Labels & Formatting**
    ax.set_xlabel("Year")  # Set x-axis label
    ax.set_ylabel("Sea Level (inches)")  # Set y-axis label
    ax.set_title("Rise in Sea Level")  # Set title
    ax.legend()  # Enable legend to differentiate trend lines
    ax.grid(True)  # Enable grid for better readability

    # **6️⃣ Save & Return the Plot**
    plt.savefig("sea_level_plot.png")  # Save the figure
    return plt.gca()  # Return the axis object

# Run the function to generate the plot
draw_plot()
