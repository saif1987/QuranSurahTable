from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.layouts import gridplot
import json
import pandas as pd
from bokeh.io import export_svg


# Load surah data from JSON file
with open("surah.json", "r") as f:
    surah_data = json.load(f)

df = pd.DataFrame(surah_data)

# Assign colors based on Makki/Madani
def assign_surah_color(row):
    if row['makki_madani'] == 'Makki':
        return '#90ee90'  # Light green
    elif row['makki_madani'] == 'Madani':
        return '#f08080'  # Light red
    else:
        return 'gray'  # Default color

df['colors'] = df.apply(assign_surah_color, axis=1)

# Limit surahs per row and create overflow groups
max_surahs_per_row = 17
overflow_data = []
main_data = []

for group in df['group'].unique():
    group_df = df[df['group'] == group]
    madani_surahs = group_df[group_df['makki_madani'] == 'Madani']
    makki_surahs = group_df[group_df['makki_madani'] == 'Makki']

    madani_count = len(madani_surahs)
    makki_count = len(makki_surahs)

    if madani_count <= max_surahs_per_row:
        if madani_count + makki_count <= max_surahs_per_row:
            main_data.extend(group_df.to_dict('records'))
        else:
            main_data.extend(madani_surahs.to_dict('records'))
            remaining_makki = max_surahs_per_row - madani_count
            main_data.extend(makki_surahs[:remaining_makki].to_dict('records'))
            overflow_data.extend(makki_surahs[remaining_makki:].to_dict('records'))

            for i in range(len(overflow_data)-1, -1, -1):
                if overflow_data[i]['group'] == group:
                    overflow_data[i]['group'] = f"{group}-overflow"
    else:
         main_data.extend(madani_surahs[:max_surahs_per_row].to_dict('records'))
         overflow_data.extend(madani_surahs[max_surahs_per_row:].to_dict('records'))
         overflow_data.extend(makki_surahs.to_dict('records'))
         for i in range(len(overflow_data)-1, -1, -1):
                if overflow_data[i]['group'] == group:
                    overflow_data[i]['group'] = f"{group}-overflow"

main_df = pd.DataFrame(main_data)
overflow_df = pd.DataFrame(overflow_data)

def calculate_positions(group_df):
    for group in group_df['group'].unique():
        group_data = group_df[group_df['group'] == group]
        madani_surahs = group_data[group_data['makki_madani'] == 'Madani']
        makki_surahs = group_data[group_data['makki_madani'] == 'Makki']

        madani_count = len(madani_surahs)
        makki_count = len(makki_surahs)

        madani_start = max_surahs_per_row + 1 - madani_count + 1

        for i, index in enumerate(makki_surahs.index):
            group_df.loc[index, 'position'] = i + 1

        for i, index in enumerate(madani_surahs.index):
            group_df.loc[index, 'position'] = madani_start + i

calculate_positions(main_df)
calculate_positions(overflow_df)

# Convert group to numerical values
groups_main = main_df['group'].unique()
group_mapping_main = {group: i + 1 for i, group in enumerate(groups_main)}
main_df['group'] = main_df['group'].map(group_mapping_main)

groups_overflow = overflow_df['group'].unique()
group_mapping_overflow = {group: i + 1 for i, group in enumerate(groups_overflow)}
overflow_df['group'] = overflow_df['group'].map(group_mapping_overflow)

# Adjust overflow positions for two rows
overflow_df['position'] = (overflow_df.groupby('group').cumcount() % 17) + 1
overflow_df['group'] = overflow_df.groupby('group').cumcount() // 17 + 1

source_main = ColumnDataSource(main_df)
source_overflow = ColumnDataSource(overflow_df)

# Create main figure
p_main = figure(
    x_range=(0, 19),
    y_range=(main_df['group'].max() + 1, 0),
    width=900,
    height=500,
    title="Quran Surah Periodic Table",
    tools="hover,reset,pan,wheel_zoom",
)


# Add rectangles (surahs) to main figure
p_main.rect(
    x="position",
    y="group",
    width=0.9,
    height=0.9,
    source=source_main,
    fill_color="colors",
    line_color="black",
)

# Add text (surah names) to main figure
p_main.text(
    x="position",
    y="group",
    text="order",
    source=source_main,
    text_align="center",
    text_baseline="middle",
    text_font_size="12pt",
    y_offset=-16,
)


# Add text (surah names) to main figure
p_main.text(
    x="position",
    y="group",
    text="Symbol",
    source=source_main,
    text_align="center",
    text_baseline="middle",
    text_font_size="14pt",
    y_offset=12,
)

# Remove grid and axes for actinides
p_main.xgrid.visible = False
p_main.ygrid.visible = False
p_main.xaxis.visible = False
p_main.yaxis.visible = False


# Add group names (Roman numerals) to the left
roman_numerals = ["I", "II", "III", "IV", "V", "VI", "VII"]
for i, group_num in enumerate(main_df['group'].unique()):
    p_main.text(
        x=0,
        y=group_num,
        text=[roman_numerals[i]],
        text_align="right",
        text_baseline="middle",
        text_font_size="14pt",
        x_offset=0, # Adjust horizontal position
    )

# Create overflow figure
p_overflow = figure(
    x_range=(0, 18),
    y_range=(overflow_df['group'].max() + 1, 0),
    width=900,
    height=200,
    title="Group VII (rest)",
    tools="hover,reset,pan,wheel_zoom",
)
p_overflow.title.align = "center"

# Add rectangles (surahs) to overflow figure
p_overflow.rect(
    x="position",
    y="group",
    width=0.9,
    height=0.9,
    source=source_overflow,
    fill_color="colors",
    line_color="black",
)

# Add text (surah names) to main figure
p_overflow.text(
    x="position",
    y="group",
    text="order",
    source=source_overflow,
    text_align="center",
    text_baseline="middle",
    text_font_size="12pt",
    y_offset=-16,
)
# Add text (surah names) to main figure
p_overflow.text(
    x="position",
    y="group",
    text="Symbol",
    source=source_overflow,
    text_align="center",
    text_baseline="middle",
    text_font_size="14pt",
    y_offset=12,
)

# Remove grid and axes for actinides
p_overflow.xgrid.visible = False
p_overflow.ygrid.visible = False
p_overflow.xaxis.visible = False
p_overflow.yaxis.visible = False

# Add hover tool
hover = HoverTool()
hover.tooltips = [
    ("Name", "@name"),
    ("Ayat Count", "@ayat_count"),
    ("Makki/Madani", "@makki_madani"),
    ("Group", "@group"),
    ("Order", "@order"),
]
p_main.add_tools(hover)
p_overflow.add_tools(hover)

# Create grid layout
grid = gridplot([[p_main], [p_overflow]])

# Show the grid layout
show(grid)

