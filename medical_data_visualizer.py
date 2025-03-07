import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from rich.console import Console
from rich.table import Table

pd.set_option("display.max_columns", None)  # Show all columns
pd.set_option("display.width", 100)        # Prevent line breaks
pd.set_option("display.colheader_justify", "center")  # Center-align headers

console = Console()

def print_rich_table(df, rows=20):
    table = Table(show_header=True, header_style="bold magenta")
    
    # Add columns
    for col in df.columns:
        table.add_column(col, justify="center")
    
    # Add rows
    for _, row in df.head(rows).iterrows():
        table.add_row(*map(str, row.values))
    
    console.print(table)

# 1
df = pd.read_csv('medical_examination.csv')

df.columns = df.columns.str.strip()
# 2
df['overweight'] = np.where(df['weight'] / ((df['height'] /100) ** 2) > 25,1,0).astype(int)

# 3
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# 4
def draw_cat_plot():
    # 5 
    # Melt variables
    sorted_columns = sorted(
        ["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )
    df_cat = pd.melt(df, id_vars=["cardio"], value_vars=sorted_columns)

    # Step 6: Group by 'cardio', 'variable', and 'value', then count occurrences
    df_cat = df_cat.groupby(["cardio", "variable", "value"]).size().reset_index()

    df_cat.rename(columns={0: "total"}, inplace=True)

    fig = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar',
        order=sorted_columns
    )

    fig.set_ylabels('total')
    fig.set_xlabels('variable')
    fig = fig.fig


    # print_rich_table(df_cat, 10)
    


    # 9
    fig.savefig('catplot.png')
    return fig

# 10
def draw_heat_map():
    # 11
    '''
    Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
        diastolic pressure is higher than systolic (Keep the correct data with (df['ap_lo'] <= df['ap_hi']))
        height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
        height is more than the 97.5th percentile
        weight is less than the 2.5th percentile
        weight is more than the 97.5th percentile
    '''

    df_heat = df[
        # Remove incorrect blood pressure data (diastolic should not be higher than systolic)
        (df['ap_lo'] <= df['ap_hi']) &
        # Remove heights below the 2.5th percentile
        (df['height'] >= df['height'].quantile(0.025)) &
        # Remove heights above the 97.5th percentile
        (df['height'] <= df['height'].quantile(0.975)) &
        # Remove weights below the 2.5th percentile
        (df['weight'] >= df['weight'].quantile(0.025)) & 
        # Remove weights above the 97.5th percentile
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12
    corr = df_heat.corr()
    
    
    # Step 13: Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize=(10,8))

    # 15
    sns.heatmap(
        corr,                   # Correlation matrix
        mask=mask,              # Apply the mask to hide upper triangle
        annot=True,             # Display correlation values
        fmt=".1f",              # Format float numbers
        linewidths=0.5,         # Line width between squares
        cmap="coolwarm",        # Color map for visualization
        ax=ax                   # Use the Matplotlib subplot
    )


    # 16
    fig.savefig('heatmap.png')
    return fig
draw_heat_map()
