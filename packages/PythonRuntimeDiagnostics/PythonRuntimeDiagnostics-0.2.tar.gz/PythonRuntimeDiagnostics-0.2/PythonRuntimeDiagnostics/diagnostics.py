import time
import logging
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure, output_notebook, output_file, reset_output, show
from bokeh.palettes import Set1

class DiagnosticsUtility: 
    def __init__(self, column_names):
        # set up logging to file - see previous section for more details
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename='myapp.log',
                            filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        self.logger = logging.getLogger('DiagLogger')
        self.data = {'timestamp': []}
        for col in column_names:
            self.data[col] = []
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        keys = list(self.data.keys())
        return "Diagnostics Utility with keys: {0}".format(keys)
    
    def log(self, data):
        self.data['timestamp'].append(time.time())
        for new_data_key in data.keys():
            if self.check_key(new_data_key):
                self.data[new_data_key].append(data[new_data_key])
                self.logger.debug("appending to key: {0}".format(new_data_key))
        
    def check_key(self, key):
        if key not in self.data:
            self.logger.warning("Key not found : {0}".format(key))
            return False
        return True
    
    def to_csv(self, file):
        pd.DataFrame(self.data).set_index('timestamp').to_csv(file)
        
    def clear(self):
        for key in self.data.keys():
            self.data[key] = []
    
    def generate_timeseries_plot(self ,y_labels, x_label = 'timestamp', file = 'timeseries.html', save_only = False):
        src = ColumnDataSource(self.data)
        fig = figure(x_axis_type="datetime")
        index = 0
        for label, color in zip(y_labels, Set1[9]):
            fig.line(source = src, x = x_label, y = label,
                     legend = " "+label+" ", color = color)
            index += 1
        reset_output()
        output_file(file)
        fig.legend.click_policy = 'hide'
        if save_only:
            save(fig)
        else:
            show(fig)
        
    def generate_xy_plot(self, x_labels, y_labels, file = 'xyplot.html'):
        src = ColumnDataSource(self.data)
        fig = figure()
        index = 0
        for x_label, y_label, color in zip(x_labels, y_labels, Set1[9]):
            fig.line(source = src, x = x_label, y = y_label, legend = "{0}|{1}".format(x_label,y_label),
                    color = color)
            index+=1
            
        reset_output()
        output_file(file)
        fig.legend.click_policy = 'hide'
        if save_only:
            save(fig)
        else:
            show(fig)