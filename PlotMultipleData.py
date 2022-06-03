import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from textwrap import wrap
import datetime as datetime


class PlotMultipleData:
    def __init__(self, data_sets, headers):
        self.data_sets = data_sets
        self.headers = headers

        self.primary_axis_layout = None
        self.secondary_axis_layout = None
        self.primary_axis_scale = None
        self.secondary_axis_scale = None

        self.interval_start = None
        self.interval_end = None

        self.figure = None
        self.axis = None

        #self.data_sets_shape = []
        #for data in self.data_sets:
        #    self.data_sets_shape.append(data.shape)

        #for idx, shape in enumerate(self.data_sets_shape):
        #    if shape[0] != self.headers[idx].shape[0]:
        #        print("ERROR: Headers and data_sets shape are not the same")

    def str_config_to_list(self, config):
        config = config.split(" ")
        str_config = [[]]
        group_count = 0
        for x in config:
            if x == ";":
                group_count += 1
                str_config.append([])
            else:
                str_config[group_count].append(int(x))
                
        return str_config

    def show_data_order(self):
        index = 0
        for data_headers in self.headers:
            for data_name in data_headers[1:]:
                index += 1
                print("Arduino DUE data id " + str(index) + ": " + data_name)

    def set_primary_axis_layout(self, config):
        if type(config) == str:
            self.primary_axis_layout = self.str_config_to_list(config)
        else:
            self.primary_axis_layout = config
    
    def set_secondary_axis_layout(self, config):
        if type(config) == str:
            self.secondary_axis_layout = self.str_config_to_list(config)
        else:
            self.secondary_axis_layout = config

    def set_primary_axis_scale(self, config):
        if type(config) == str:
            self.primary_axis_scale = self.str_config_to_list(config)
        else:
            self.primary_axis_scale = config

    def set_secondary_axis_scale(self, config):
        if type(config) == str:
            self.secondary_axis_scale = self.str_config_to_list(config)
        else:
            self.secondary_axis_scale = config

    def set_interval(self, start, end):


    def plot(self):
        self.figure, self.axis = plt.subplots(len(layout)+len(hist_layout), 1, figsize =(12, 5*len(layout)))

        for ax_id, axis_layout in enumerate(layout):
            for plot_id, data_id in enumerate(axis_layout):
                # DUE
                if data_id < len(due_data):
                    plt_timestamp = due_data[0][sid_interval_due:eid_interval_due]
                    plt_data = due_data[data_id][sid_interval_due:eid_interval_due]
                    plt_legend = '\n'.join(wrap(due_header[data_id], 25))
                # Inoson level detector
                elif data_id >= len(due_data) and data_id < len(due_data) + len(ild_data) - 1:
                    plt_timestamp = ild_data[0][sid_interval_ild:eid_interval_ild]
                    plt_data = ild_data[data_id-len(due_data)+1][sid_interval_ild:eid_interval_ild]
                    plt_legend = '\n'.join(wrap(ild_header[data_id-len(due_data)+1], 25))
                # Bubble count
                elif data_id >= len(due_data) + len(ild_data) - 1 and data_id < len(due_data) + len(ild_data) + len(bc_data) - 2:
                    plt_timestamp = bc_data[0][sid_interval_bc:eid_interval_bc]
                    plt_data = bc_data[data_id-len(due_data)-len(ild_data)+2][sid_interval_bc:eid_interval_bc]
                    plt_legend = '\n'.join(wrap(bc_header[data_id-len(due_data)-len(ild_data)+2], 25))
                # Inoson Flow Sensor
                else:
                    plt_timestamp = ifs_data[0][sid_interval_ifs:eid_interval_ifs]
                    plt_data = ifs_data[data_id-len(due_data)-len(ild_data)-len(bc_data)+3][sid_interval_ifs:eid_interval_ifs]
                    plt_legend = '\n'.join(wrap(ifs_header[data_id-len(due_data)-len(ild_data)-len(bc_data)+3], 25))
                    
                
                if len(layout) == 1:
                    if scale[ax_id][plot_id] == 1:
                        axis.plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                        axis.legend(bbox_to_anchor=(1.05,1), loc="upper left")
                        if len(y1_range[ax_id]) == 2:
                            axis.set_ylim(y1_range[ax_id][0], y1_range[ax_id][1])
                    elif scale[ax_id][plot_id] == 2:
                        axis2 = axis.twinx()
                        axis2.plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                        axis2.legend(bbox_to_anchor=(1.05,0.5), loc="lower left")
                        if len(y2_range[ax_id]) == 2:
                            axis2.set_ylim(y2_range[ax_id][0], y2_range[ax_id][1])
                else:
                    if scale[ax_id][plot_id] == 1:
                        axis[ax_id].plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                        axis[ax_id].legend(bbox_to_anchor=(1.05,1), loc="upper left")
                        if len(y1_range[ax_id]) == 2:
                            axis[ax_id].set_ylim(y1_range[ax_id][0], y1_range[ax_id][1])
                    elif scale[ax_id][plot_id] == 2:
                        axis2 = axis[ax_id].twinx()
                        axis2.plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                        axis2.legend(bbox_to_anchor=(1.05,0.5), loc="lower left")
                        if len(y2_range[ax_id]) == 2:
                            axis2.set_ylim(y2_range[ax_id][0], y2_range[ax_id][1])

        if len(layout) == 1:
            axis.set_xlabel("Timestamp [s]")    
        else:
            axis[len(layout)-1].set_xlabel("Timestamp [s]")

        figure.subplots_adjust(left=0.038, right=0.862, bottom=0.062, top=0.98, hspace=0.088)
        mng = plt.get_current_fig_manager()
        mng.resize(1800, 900)
        plt.tight_layout()

        figure.suptitle(infostring, fontsize=16, y=1.05)
        plt.show()   

    def save_pdf(self, fiel_name):
        figurefilename=""+"Plot_"+fiel_name+"_"+datetime.now().strftime("%y%m%d_%H%M")+".pdf"
        figure.savefig(figurefilename,bbox_inches="tight")


# Defines the layout of the plotted data
# the column indexes separeted with a space to show in one graph and each graph separeted with a semicolon 
# EXAMPLE: 2 4 ; 7 8
#graph_layout = "3 5 ; 18 ; 19"
#graph_layout = "3 5 ; 19 ; 38 ; 32 ; 33 ; 34 ; 35 ; 36"
#graph_layout = "3 5 ; 18 ; 19"
#graph_layout = "40 ; 23 ; 24 ; 25 ; 26 ; 27 ; 28 ; 29 ; 30 ; 31 ; 32 ; 33 ; 34 ; 35 ; 36"
#graph_layout = "27 ; 28 ; 29 ; 30"
graph_layout = "38 30 ; 40 ; 31 ; 32 ; 46 ; 47 ; 73"
scale_select = "1 2 ; 1 ; 1 ; 1 ; 1 ; 1 ; 1"

# Defines the range of all the y axis
# The vlues separeted with a space correspond to the start and end of the range
# The ranges for each graph is separeted with a semicolon
# Automatic range is set by leving just one value between semicolons instead of two
y1_range = "0 ; 0 ; 0 ; 0 ; 0 ; 0 ; 0"
y2_range = "0 ; 0 ; 0 ; 0 ; 0 ; 0 ; 0"

additional_histograms = ""

normed=True
amount_of_bins= 31 #240

layout = str_config_to_list(graph_layout)
scale = str_config_to_list(scale_select)
y1_range = str_config_to_list(y1_range)
y1_range = str_config_to_list(y2_range)

if additional_histograms != "":
    hist_layout = additional_histograms.split(" ")
else:
    hist_layout = []

figure, axis = plt.subplots(len(layout)+len(hist_layout), 1, figsize =(12, 5*len(layout)))

for ax_id, axis_layout in enumerate(layout):
    for plot_id, data_id in enumerate(axis_layout):
        # DUE
        if data_id < len(due_data):
            plt_timestamp = due_data[0][sid_interval_due:eid_interval_due]
            plt_data = due_data[data_id][sid_interval_due:eid_interval_due]
            plt_legend = '\n'.join(wrap(due_header[data_id], 25))
        # Inoson level detector
        elif data_id >= len(due_data) and data_id < len(due_data) + len(ild_data) - 1:
            plt_timestamp = ild_data[0][sid_interval_ild:eid_interval_ild]
            plt_data = ild_data[data_id-len(due_data)+1][sid_interval_ild:eid_interval_ild]
            plt_legend = '\n'.join(wrap(ild_header[data_id-len(due_data)+1], 25))
        # Bubble count
        elif data_id >= len(due_data) + len(ild_data) - 1 and data_id < len(due_data) + len(ild_data) + len(bc_data) - 2:
            plt_timestamp = bc_data[0][sid_interval_bc:eid_interval_bc]
            plt_data = bc_data[data_id-len(due_data)-len(ild_data)+2][sid_interval_bc:eid_interval_bc]
            plt_legend = '\n'.join(wrap(bc_header[data_id-len(due_data)-len(ild_data)+2], 25))
        # Inoson Flow Sensor
        else:
            plt_timestamp = ifs_data[0][sid_interval_ifs:eid_interval_ifs]
            plt_data = ifs_data[data_id-len(due_data)-len(ild_data)-len(bc_data)+3][sid_interval_ifs:eid_interval_ifs]
            plt_legend = '\n'.join(wrap(ifs_header[data_id-len(due_data)-len(ild_data)-len(bc_data)+3], 25))
            
        
        if len(layout) == 1:
            if scale[ax_id][plot_id] == 1:
                axis.plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                axis.legend(bbox_to_anchor=(1.05,1), loc="upper left")
                if len(y1_range[ax_id]) == 2:
                    axis.set_ylim(y1_range[ax_id][0], y1_range[ax_id][1])
            elif scale[ax_id][plot_id] == 2:
                axis2 = axis.twinx()
                axis2.plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                axis2.legend(bbox_to_anchor=(1.05,0.5), loc="lower left")
                if len(y2_range[ax_id]) == 2:
                    axis2.set_ylim(y2_range[ax_id][0], y2_range[ax_id][1])
        else:
            if scale[ax_id][plot_id] == 1:
                axis[ax_id].plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                axis[ax_id].legend(bbox_to_anchor=(1.05,1), loc="upper left")
                if len(y1_range[ax_id]) == 2:
                    axis[ax_id].set_ylim(y1_range[ax_id][0], y1_range[ax_id][1])
            elif scale[ax_id][plot_id] == 2:
                axis2 = axis[ax_id].twinx()
                axis2.plot(plt_timestamp, plt_data, list(mcolors.TABLEAU_COLORS)[plot_id], label=plt_legend)
                axis2.legend(bbox_to_anchor=(1.05,0.5), loc="lower left")
                if len(y2_range[ax_id]) == 2:
                    axis2.set_ylim(y2_range[ax_id][0], y2_range[ax_id][1])
            
# plot histograms
for ax_id, axis_layout in enumerate(hist_layout, len(layout)):
    if axis_layout == "5":
        axis[ax_id].hist(due_data[int(axis_layout)], amount_of_bins, density=normed, label='\n'.join(wrap("Histogram ABD Serial_2", 25)))
        axis[ax_id].legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0)
    if axis_layout == "3":
        axis[ax_id].hist(due_data[int(axis_layout)], amount_of_bins, density=normed, label='\n'.join(wrap("Histogram ABD Serial_1", 25)))
        axis[ax_id].legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0)

if len(layout) == 1:
    axis.set_xlabel("Timestamp [s]")    
else:
    axis[len(layout)-1].set_xlabel("Timestamp [s]")       
#left  = 0.125  # the left side of the subplots of the figure
#right = 0.9    # the right side of the subplots of the figure
#bottom = 0.1   # the bottom of the subplots of the figure
#top = 0.9      # the top of the subplots of the figure
#wspace = 0.2   # the amount of width reserved for blank space between subplots
#hspace = 0.2   # the amount of height reserved for white space between subplots
figure.subplots_adjust(left=0.038, right=0.862, bottom=0.062, top=0.98, hspace=0.088)
mng = plt.get_current_fig_manager()
mng.resize(1800, 900)
plt.tight_layout()

figure.suptitle(infostring, fontsize=16, y=1.05)
plt.show()



