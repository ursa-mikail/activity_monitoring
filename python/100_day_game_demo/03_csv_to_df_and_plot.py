def csv_to_df(csv_file='timeline_data.csv'):
    """Read CSV file into DataFrame"""
    return pd.read_csv(csv_file)

# Usage
df = csv_to_df('timeline_data.csv')
#create_mpld3_interactive_plots(df)

#!pip install mpld3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpld3
from mpld3 import plugins

def create_mpld3_interactive_plots(df):
    """Create truly interactive plots using mpld3 - THIS WILL WORK!"""
    categories = ['pneuma', 'psyche', 'soma', 'opus', 'kismet']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    for i, category in enumerate(categories):
        fig, ax = plt.subplots(figsize=(12, 6))
        
        dates = pd.to_datetime(df['timestamp'])
        scores = df[f'{category}.score']
        logs = df[f'{category}.log']
        
        # Create scatter plot
        scatter = ax.scatter(dates, scores, c=colors[i], s=100, alpha=0.7, 
                           label=f'{category.title()} Score')
        ax.plot(dates, scores, color=colors[i], alpha=0.5, linewidth=2)
        
        # Format the plot
        ax.set_title(f'{category.title()} Score Timeline', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        plt.xticks(rotation=45)
        
        # Create tooltips
        labels = []
        for j, (date, score, log) in enumerate(zip(dates, scores, logs)):
            labels.append(f"Date: {date.strftime('%Y-%m-%d')}<br>Score: {score}<br>Log: {log}")
        
        tooltip = plugins.PointHTMLTooltip(scatter, labels, css=".mpld3-tooltip {background: yellow;}")
        plugins.connect(fig, tooltip)
        
        plt.tight_layout()
        
        # Save as HTML (will open in browser)
        html_filename = f"{category}_interactive_plot.html"
        mpld3.save_html(fig, html_filename)
        print(f"Saved interactive plot to {html_filename}")
        
        # Also display inline if in Jupyter
        try:
            from IPython.display import display
            display(mpld3.display())
        except:
            pass
        
        plt.show()

# Run this first - it will create HTML files that you can open in your browser
create_mpld3_interactive_plots(df)

"""

"""