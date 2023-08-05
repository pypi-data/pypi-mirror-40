import matplotlib.pyplot as plt
from .XPS_data_reader import XPSDataReader
from .XPS_functions import XPSFunctions
from plotly.offline import init_notebook_mode, iplot
import plotly.graph_objs as go
import numpy as np


class XPS:

    def __init__(self, filename_survey=None, filename_multi=None, gridfs_survey=None,gridfs_multi=None):
        self.filename_survey = filename_survey
        self.filename_multi = filename_multi
        self.survey_data = XPSDataReader.read_survey(filename=self.filename_survey, gridfs=gridfs_survey)
        self.multi_data = XPSDataReader.read_multi(filename=self.filename_multi,gridfs=gridfs_multi)
        self.is_survey_shifted = False
        self.is_multi_shifted = False

    def shift_survey(self, background_model='shirley',show_fit=False):
        if self.is_survey_shifted:
            return
        peak_position, error = XPSFunctions.find_carbon_peak(self.survey_data.energy,self.survey_data.counts,background_model,show_fit=show_fit)
        self.survey_data.energy = self.survey_data.energy-(peak_position-284.8)
        self.is_survey_shifted = True

    def shift_multi(self, background_model='shirley',show_fit=False):
        if self.is_multi_shifted:
            return
        peak_position, error = XPSFunctions.find_carbon_peak(self.multi_data.energy['C1s'], self.multi_data.counts['C1s'],background_model,show_fit=show_fit)
        for orbital in self.get_orbitals():
            self.multi_data.energy[orbital] = self.multi_data.energy[orbital] - (peak_position - 284.8)
        self.is_multi_shifted = True

    def get_orbitals(self):
        return list(self.multi_data.energy)

    def get_energy_multi(self,orbital):
        return self.multi_data.energy[orbital]

    def get_counts_multi(self,orbital):
        return self.multi_data.counts[orbital]

    def get_energy_survey(self,range=None):
        if range:
            start_index = self._find_index_of_nearest(array = self.survey_data.energy,value=max(range))
            end_index = self._find_index_of_nearest(array = self.survey_data.energy, value=min(range))
            return self.survey_data.energy[start_index:end_index]
        return self.survey_data.energy

    def get_counts_survey(self,range=None):
        if range:
            start_index = self._find_index_of_nearest(array=self.survey_data.energy, value=max(range))
            end_index = self._find_index_of_nearest(array=self.survey_data.energy, value=min(range))
            return self.survey_data.counts[start_index:end_index]
        return self.survey_data.counts

    def plot_orbital(self,orbital, ax=None, offset=0, label=None):
        counts = self.multi_data.counts[orbital]
        energy = self.multi_data.energy[orbital]
        if ax is not None:
            ax.plot(energy,counts+offset, label=label)
            ax.legend()
            return ax
        plt.plot(energy,counts+offset, label=label)
        plt.gca().set_xlabel('Energy [eV]')
        plt.gca().set_ylabel('Counts [a.u.]')
        plt.gca().invert_xaxis()
        plt.gca().legend()
        return plt.gca()

    def plotly_orbitals(self,title=''):
        init_notebook_mode(connected=True)
        data = []
        for orbital in self.get_orbitals():
            x = self.multi_data.energy[orbital]
            y = self.multi_data.counts[orbital]
            trace = XPS._create_x_y_trace(x, y, orbital)
            data.append(trace)
        layout = XPS._get_plotly_layout(title=title)
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig)

    def plotly_survey(self,title=''):
        init_notebook_mode(connected=True)
        x = self.survey_data.energy
        y = self.survey_data.counts
        trace = XPS._create_x_y_trace(x, y,'Survey')
        layout = XPS._get_plotly_layout(title=title)
        fig = go.Figure(data=[trace], layout=layout)
        return iplot(fig)

    def plotly_all(self,title=''):
        init_notebook_mode(connected=True)
        data = []
        x = self.survey_data.energy
        y = self.survey_data.counts
        trace = XPS._create_x_y_trace(x, y,'Survey')
        data.append(trace)
        for orbital in self.get_orbitals():
            x = self.multi_data.energy[orbital]
            y = self.multi_data.counts[orbital]
            trace = XPS._create_x_y_trace(x, y, orbital)
            data.append(trace)
        layout = XPS._get_plotly_layout(title=title)
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig)


    @staticmethod
    def _create_x_y_trace(x, y, name):
        return go.Scatter(x=x, y=y, name=name)

    @staticmethod
    def _get_plotly_layout(title=''):
        return go.Layout(
            title=title,
            xaxis=dict(
                autorange='reversed',
                title='Energy [eV]',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            ),
            yaxis=dict(
                title='Counts [a.u.]',
                titlefont=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                ),
                exponentformat='e',
                showexponent='all'
            )
        )

    @staticmethod
    def _find_index_of_nearest(array, value):
        return (np.abs(array - value)).argmin()

