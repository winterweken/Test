from pyrevit.output import charts
from pyrevit import script

output = script.get_output()
output.set_width(600)
chart = output.make_radar_chart()

chart.data.labels = ['North', 'East', 'South', 'West']

set_a = chart.data.new_dataset('Wall Total')
set_a.data = [100, 100, 100, 100]

set_b = chart.data.new_dataset('South')
set_b.data = [0, 0, 63, 0]



chart.randomize_colors()

# Finally let's draw the chart
chart.draw()