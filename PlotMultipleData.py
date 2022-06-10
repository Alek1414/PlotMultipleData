import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from textwrap import wrap
from datetime import datetime
from datetime import timedelta
import numpy as np

PRIMARY = 0
SECONDARY = 1


class PlotMultipleData:
    def __init__(self):
        self.data_set = []
        self.graph = []

        self.plt_figure = None
        self.plt_axis = None

    def add_data_set(self, data, header, data_start, offset=timedelta(seconds=0, minutes=0, hours=0)):
        self.data_set.append(self.DataSet(self, data, header, data_start, offset))

    def add_graph(self,
                  interval_start=None,
                  interval_end=None,
                  primary_upper_limit=None,
                  primary_lower_limit=None,
                  secondary_upper_limit=None,
                  secondary_lower_limit=None):
        self.graph.append(self.GraphData(self,
                                         interval_start,
                                         interval_end,
                                         primary_upper_limit,
                                         primary_lower_limit,
                                         secondary_upper_limit,
                                         secondary_lower_limit))

    def plot(self):
        self.plt_figure, self.plt_axis = plt.subplots(len(self.graph), 1, figsize=(12, 5 * len(self.graph)))
        if len(self.graph) == 1:
            self.plt_axis = [self.plt_axis]

        for graph_id, graph_data in enumerate(self.graph):
            legend_prim = []
            legend_sec = []
            axis_prim = self.plt_axis[graph_id]
            axis_sec = None
            for axis_id, axis_data in enumerate(graph_data.axis):
                data_set_id, data_pos = self._find_data(axis_data.data_header)

                if graph_data.interval_start is None:
                    start = 0
                else:
                    start = self._get_data_pos(graph_data.interval_start,
                                               self.data_set[data_set_id].data,
                                               self.data_set[data_set_id].data_start,
                                               self.data_set[data_set_id].offset)

                if graph_data.interval_end is None:
                    end = -1
                else:
                    end = self._get_data_pos(graph_data.interval_end,
                                             self.data_set[data_set_id].data,
                                             self.data_set[data_set_id].data_start,
                                             self.data_set[data_set_id].offset)

                timestamp = self.data_set[data_set_id].data[0][start:end]
                data = self.data_set[data_set_id].data[data_pos[0][0]][start:end]

                if axis_data.y_axis == PRIMARY:
                    axis_prim.plot(timestamp, data, list(mcolors.TABLEAU_COLORS)[axis_id])
                    legend_prim.append('\n'.join(wrap(self.data_set[data_set_id].header[data_pos[0][0]], 25)))
                else:
                    axis_sec = self.plt_axis[graph_id].twinx()
                    axis_sec.plot(timestamp, data, list(mcolors.TABLEAU_COLORS)[axis_id])
                    legend_sec.append('\n'.join(wrap(self.data_set[data_set_id].header[data_pos[0][0]], 25)))

            axis_prim.legend(legend_prim, bbox_to_anchor=(1.05, 1), loc="upper left")
            axis_prim.set_ylim(graph_data.primary_upper_limit, graph_data.primary_lower_limit)
            if len(legend_sec) != 0:
                axis_sec.legend(legend_sec, bbox_to_anchor=(1.05, 0.5), loc="upper left")
                axis_sec.set_ylim(graph_data.secondary_upper_limit, graph_data.secondary_lower_limit)

        self.plt_axis[-1].set_xlabel("Timestamp [s]")
        self.plt_figure.subplots_adjust(left=0.038, right=0.862, bottom=0.062, top=0.98, hspace=0.088)
        mng = plt.get_current_fig_manager()
        mng.resize(1800, 900)
        plt.tight_layout()

        # self.plt_figure.suptitle("aaaaaa", fontsize=16, y=1.05)
        plt.show()

    def save_pdf(self, file_name, date_time="%y%m%d_%H%M"):
        # figurefilename = "" + "Plot_" + file_name + "_" + datetime.now().strftime("%y%m%d_%H%M") + ".pdf"
        # figure.savefig(figurefilename, bbox_inches="tight")
        pass

    def reset(self):
        pass

    def _find_data(self, data_header):
        data_set_id = None
        data_pos = None
        for data_set_id, data_set in enumerate(self.data_set):
            data_pos = np.where(self.data_set[data_set_id].header == data_header)
            if len(data_pos) != 0:
                break

        return data_set_id, data_pos

    def _get_data_pos(self, interval_point, data_set, data_start, offset):
        if type(data_start) == str:
            data_start = datetime.strptime(data_start, "%d.%m.%Y %H:%M:%S")
        if type(offset) != timedelta:
            offset = timedelta(seconds=offset).total_seconds()
        else:
            offset = offset.total_seconds()


        if type(interval_point) == str:
            print(datetime.strptime(interval_point, "%d.%m.%Y %H:%M:%S"))
            seconds = datetime.strptime(interval_point, "%d.%m.%Y %H:%M:%S") - data_start
            seconds = seconds.total_seconds() - offset
        else:
            seconds = interval_point - offset

        for timestamp_id, value in enumerate(data_set[0]):
            if seconds <= value:
                return timestamp_id

        return -1

    class DataSet:
        def __init__(self, parent, data, header, data_start, offset):
            self.data = data
            self.header = header
            self.data_start = data_start
            self.offset = offset

    class GraphData:
        def __init__(self,
                     parent,
                     interval_start,
                     interval_end,
                     primary_upper_limit,
                     primary_lower_limit,
                     secondary_upper_limit,
                     secondary_lower_limit):
            self.parent = parent
            self.axis = []
            self.interval_start = interval_start
            self.interval_end = interval_end
            self.primary_upper_limit = primary_upper_limit
            self.primary_lower_limit = primary_lower_limit
            self.secondary_upper_limit = secondary_upper_limit
            self.secondary_lower_limit = secondary_lower_limit
            # self.type = None
            # self.x_format = None
            pass

        def add_axis(self, data_header, y_axis=PRIMARY):
            self.axis.append(self.AxisData(data_header, y_axis))

        class AxisData:
            def __init__(self, data_header, y_axis):
                self.data_header = data_header
                self.y_axis = y_axis


if __name__ == "__main__":
    time = np.arange(0, 10, 0.1)
    sinus = np.vstack((time, np.sin(time), np.cos(time) * 5, np.tan(time)))

    headers = np.array(["Timestamp", "Sinus", "Cosines", "Tangent"])
    start_time = "07.06.2022 14:00:00"

    plot = PlotMultipleData()
    plot.add_data_set(sinus, headers, start_time)

    plot.add_graph(primary_upper_limit=0.5, primary_lower_limit=-0.5,
                   secondary_upper_limit=2, secondary_lower_limit=-2)
    plot.add_graph(interval_start=1.5, interval_end=5)
    #plot.add_graph()
    plot.graph[0].add_axis("Sinus")
    plot.graph[1].add_axis("Tangent")
    plot.graph[0].add_axis("Cosines", SECONDARY)

    plot.plot()
