import numpy as np
from os.path import dirname, join
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Slider, TextInput, Button
from bokeh.plotting import figure

# Set up data
N = 200
x = np.linspace(0, 4*np.pi, N)
y = np.sin(x)
source = ColumnDataSource(data=dict(x=x, y=y))
output = ColumnDataSource(data=dict())

# Set up plot
plot = figure(plot_height=400, plot_width=400, title="my sine wave",
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_range=[0, 4*np.pi], y_range=[-2.5, 2.5])

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# Set up widgets
text = TextInput(title="title", value='my sine wave')
offset = Slider(title="offset", value=0.0, start=-5.0, end=5.0, step=0.1)
amplitude = Slider(title="amplitude", value=1.0, start=-5.0, end=5.0, step=0.1)
phase = Slider(title="phase", value=0.0, start=0.0, end=2*np.pi)
freq = Slider(title="frequency", value=1.0, start=0.1, end=5.1, step=0.1)

# Set up callbacks
# "Change the title"


def update_title(attrname, old, new):
    plot.title.text = text.value


text.on_change('value', update_title)


# "Run the model"
def update_data(attrname, old, new):

    # Get the current slider values
    a = amplitude.value
    b = offset.value
    w = phase.value
    k = freq.value

    # Generate the new curve
    x = np.linspace(0, 4*np.pi, N)
    y = a*np.sin(k*x + w) + b
    df = pd.DataFrame({'x': x, 'y': y})
    source.data = {
        'x': df['x'],
        'y': df['y']
    }


"Check to see if new data and update model if true"
for w in [offset, amplitude, phase, freq]:
    w.on_change('value', update_data)

"Download data"
button = Button(label="Download", button_type="success")
button.callback = CustomJS(args=dict(source=source),
                           code=open(join(dirname(__file__),
                           "download.js")).read())

# Set up layouts and add to document
inputs = widgetbox(text, offset, amplitude, phase, freq, button)


curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Sine wave"
