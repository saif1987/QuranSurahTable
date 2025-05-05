from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, LinearAxis
from bokeh.layouts import gridplot
import json

# Load data from data.json
with open('data.json', 'r') as f:
    periodic_table_data = json.load(f)

# Separate lanthanides and actinides
main_table_data = []
lanthanide_data = []
actinide_data = []

for element in periodic_table_data:
    if 58 <= element["number"] <= 71:  # Lanthanides
        lanthanide_data.append(element)
    elif 90 <= element["number"] <= 103:  # Actinides
        actinide_data.append(element)
    else:
        main_table_data.append(element)

def to_data_dict(data):
    data_dict = {}
    for element in data:
        for key, value in element.items():
            if key not in data_dict:
                data_dict[key] = []
            data_dict[key].append(value)
    return data_dict

main_source_data = to_data_dict(main_table_data)
lanthanide_source_data = to_data_dict(lanthanide_data)
actinide_source_data = to_data_dict(actinide_data)

print("Main Source Data:", main_source_data)
print("Lanthanide Source Data:", lanthanide_source_data)
print("Actinide Source Data:", actinide_source_data)

main_source = ColumnDataSource(main_source_data)
lanthanide_source = ColumnDataSource(lanthanide_source_data)
actinide_source = ColumnDataSource(actinide_source_data)

# ... (rest of your Bokeh code)


for element in periodic_table_data:
    if 57 <= element["number"] <= 71:  # Lanthanides
        lanthanide_data.append(element)
    elif 89 <= element["number"] <= 103:  # Actinides
        actinide_data.append(element)
    else:
        main_table_data.append(element)
        
# Add this dictionary at the beginning of your code, before creating p_main:
row_colors = {
    1: "lightcoral",
    2: "lightskyblue",
    3: "lightgreen",
    4: "khaki",
    5: "plum",
    6: "paleturquoise",
    7: "lightsalmon",
    8: "lightgray",
}

# Generate colors based on period values
periods = main_source.data['period']
max_period = max(periods)
colors = [f"#{int((period * 255) / max_period):02x}{150:02x}{200:02x}" for period in periods]

# Add colors to ColumnDataSource
main_source.data['colors'] = colors

# Main table figure
p_main = figure(
    x_range=(0, 19),
    y_range=(8, 0),
    width=900,
    height=500,
    title="Periodic Table",
    tools="hover,reset,pan,wheel_zoom",
)
p_main.rect(x="group", y="period", width=0.9, height=0.9, source=main_source,     fill_color="colors", line_color="black")
p_main.text(x="group", y="period", text="symbol", source=main_source, text_align="center", text_baseline="middle", text_font_size="12pt")


# Remove grid and axes for the main table
p_main.xgrid.visible = False
p_main.ygrid.visible = False
p_main.xaxis.visible = False
p_main.yaxis.visible = False



# Lanthanide figure
p_lanthanides = figure(
    x_range=(57, 72),  # Adjust x-range
    y_range=(0, 1),
    width=900,
    height=100,
    title="Lanthanides",
    tools="hover,reset,pan,wheel_zoom",
)

lanthanide_color = main_source.data['colors'][main_source.data['number'].index(57)]

p_lanthanides.rect(x="number", y=0.5, width=0.9, height=0.9, source=lanthanide_source, fill_color=lanthanide_color, line_color="black")
p_lanthanides.text(x="number", y=0.5, text="symbol", source=lanthanide_source, text_align="center", text_baseline="middle", text_font_size="12pt")

# Remove grid and axes for lanthanides
p_lanthanides.xgrid.visible = False
p_lanthanides.ygrid.visible = False
p_lanthanides.xaxis.visible = False
p_lanthanides.yaxis.visible = False

# Actinide figure
actinide_color = main_source.data['colors'][main_source.data['number'].index(89)]
p_actinides = figure(
    x_range=(89, 104),  # Adjust x-range
    y_range=(0, 1),
    width=900,
    height=100,
    title="Actinides",
    tools="hover,reset,pan,wheel_zoom",
)
p_actinides.rect(x="number", y=0.5, width=0.9, height=0.9, source=actinide_source, fill_color=actinide_color, line_color="black")
p_actinides.text(x="number", y=0.5, text="symbol", source=actinide_source, text_align="center", text_baseline="middle", text_font_size="12pt")

# Remove grid and axes for actinides
p_actinides.xgrid.visible = False
p_actinides.ygrid.visible = False
p_actinides.xaxis.visible = False
p_actinides.yaxis.visible = False
# Add hover tools
hover_main = p_main.select(dict(type=HoverTool))
hover_main.tooltips = [("Name", "@name"), ("Symbol", "@symbol"), ("Number", "@number"), ("Mass", "@mass"), ("Group", "@group"), ("Period", "@period")]
hover_lanthanides = p_lanthanides.select(dict(type=HoverTool))
hover_lanthanides.tooltips = [("Name", "@name"), ("Symbol", "@symbol"), ("Number", "@number"), ("Mass", "@mass")]
hover_actinides = p_actinides.select(dict(type=HoverTool))
hover_actinides.tooltips = [("Name", "@name"), ("Symbol", "@symbol"), ("Number", "@number"), ("Mass", "@mass")]

# Create grid layout
layout = gridplot([[p_main], [p_lanthanides], [p_actinides]])
show(layout)
