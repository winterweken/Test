from pyrevit.output import charts
from pyrevit import script

output = script.get_output()
output.set_width(600)
chart = output.make_bar_chart()

chart.data.labels = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']


chart.options.title = {'display': True,
                       'text':'Chart Title',
                       'fontSize': 18,
                       'fontColor': '#000',
                       'fontStyle': 'bold'
					   }



set_b = chart.data.new_dataset('South')
set_b.data = [10, 37, 63, 21]



chart.randomize_colors()

# Finally let's draw the chart
chart.draw()

print(dir(chart.options.title))