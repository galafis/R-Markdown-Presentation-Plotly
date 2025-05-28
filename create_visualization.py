import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# Create a figure with 3 subplots
fig = make_subplots(
    rows=2, cols=2,
    specs=[[{}, {}], [{"colspan": 2}, None]],
    subplot_titles=("Distribution of Cars by Cylinders and Gears", 
                    "Horsepower vs. MPG",
                    "Weight vs. Quarter Mile Time"),
    column_widths=[0.5, 0.5],
    row_heights=[0.5, 0.5],
    vertical_spacing=0.12,
    horizontal_spacing=0.08
)

# Read the data
cars = pd.read_csv('data/mtcars.csv')

# Add model name as index
cars.index = cars['model']

# 1. Stacked bar chart for cylinders and gears
cyl_gear_counts = cars.groupby(['cyl', 'gear']).size().reset_index(name='count')

# Get unique values for cylinders and gears
cylinders = sorted(cars['cyl'].unique())
gears = sorted(cars['gear'].unique())

# Create a color map for gears
colors = ['#3366CC', '#33CC99', '#FF6666']

# Add traces for each gear
for i, gear in enumerate(gears):
    gear_data = cyl_gear_counts[cyl_gear_counts['gear'] == gear]
    fig.add_trace(
        go.Bar(
            x=gear_data['cyl'],
            y=gear_data['count'],
            name=f'{gear} Gears',
            marker_color=colors[i]
        ),
        row=1, col=1
    )

# 2. Scatter plot for horsepower vs mpg
for cyl in cylinders:
    cyl_data = cars[cars['cyl'] == cyl]
    fig.add_trace(
        go.Scatter(
            x=cyl_data['hp'],
            y=cyl_data['mpg'],
            mode='markers',
            name=f'{cyl} Cylinders',
            marker=dict(
                size=cyl_data['wt'] * 5,
                sizemode='area',
                sizeref=0.1
            ),
            text=[f"Car: {model}<br>MPG: {mpg}<br>HP: {hp}<br>Weight: {wt}" 
                  for model, mpg, hp, wt in zip(cyl_data.index, cyl_data['mpg'], cyl_data['hp'], cyl_data['wt'])],
            hoverinfo='text'
        ),
        row=1, col=2
    )

# 3. Scatter plot for weight vs quarter mile time with trend line
# Create separate traces for automatic and manual transmission
automatic = cars[cars['am'] == 0]
manual = cars[cars['am'] == 1]

fig.add_trace(
    go.Scatter(
        x=automatic['wt'],
        y=automatic['qsec'],
        mode='markers',
        name='Automatic',
        marker=dict(
            color='#FF5733',
            size=automatic['hp'] / 5,
            symbol='circle'
        ),
        text=[f"Car: {model}<br>Weight: {wt} tons<br>Quarter Mile: {qsec} sec<br>Transmission: Automatic" 
              for model, wt, qsec in zip(automatic.index, automatic['wt'], automatic['qsec'])],
        hoverinfo='text'
    ),
    row=2, col=1
)

fig.add_trace(
    go.Scatter(
        x=manual['wt'],
        y=manual['qsec'],
        mode='markers',
        name='Manual',
        marker=dict(
            color='#33A2FF',
            size=manual['hp'] / 5,
            symbol='diamond'
        ),
        text=[f"Car: {model}<br>Weight: {wt} tons<br>Quarter Mile: {qsec} sec<br>Transmission: Manual" 
              for model, wt, qsec in zip(manual.index, manual['wt'], manual['qsec'])],
        hoverinfo='text'
    ),
    row=2, col=1
)

# Add trend line
x = cars['wt']
y = cars['qsec']
z = np.polyfit(x, y, 1)
p = np.poly1d(z)

x_trend = np.linspace(min(x), max(x), 100)
y_trend = p(x_trend)

fig.add_trace(
    go.Scatter(
        x=x_trend,
        y=y_trend,
        mode='lines',
        name='Trend Line',
        line=dict(color='rgba(0, 0, 0, 0.5)', width=2)
    ),
    row=2, col=1
)

# Update layout
fig.update_layout(
    title={
        'text': 'Interactive Data Visualization',
        'y':0.98,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24, color='white')
    },
    barmode='stack',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    height=800,
    width=1200,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=60, r=30, t=100, b=60),
    showlegend=True
)

# Update axes
fig.update_xaxes(title_text="Number of Cylinders", row=1, col=1)
fig.update_yaxes(title_text="Count", row=1, col=1)

fig.update_xaxes(title_text="Horsepower", row=1, col=2)
fig.update_yaxes(title_text="Miles Per Gallon", row=1, col=2)

fig.update_xaxes(title_text="Weight (tons)", row=2, col=1)
fig.update_yaxes(title_text="Quarter Mile Time (sec)", row=2, col=1)

# Add a dark blue header background
fig.add_shape(
    type="rect",
    x0=0, y0=0.95, x1=1, y1=1,
    fillcolor="#2c3e50",
    line_width=0,
    layer="below"
)

# Save the figure
fig.write_image("images/plotly_visualization.png", scale=2)
print("Visualization image created successfully!")
