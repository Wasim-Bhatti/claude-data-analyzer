# data_visualizer.py

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

class DataVisualizer:
    def __init__(self, df):
        self.df = df

    def create_matplotlib_plot(self, x, y, kind='scatter', title=''):
        plt.figure(figsize=(10, 6))
        if kind == 'scatter':
            plt.scatter(self.df[x], self.df[y])
        elif kind == 'bar':
            plt.bar(self.df[x], self.df[y])
        elif kind == 'line':
            plt.plot(self.df[x], self.df[y])
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()

    def create_seaborn_plot(self, x, y, kind='scatter', title=''):
        plt.figure(figsize=(10, 6))
        if kind == 'scatter':
            sns.scatterplot(data=self.df, x=x, y=y)
        elif kind == 'bar':
            sns.barplot(data=self.df, x=x, y=y)
        elif kind == 'line':
            sns.lineplot(data=self.df, x=x, y=y)
        plt.xlabel(x)
        plt.ylabel(y)
        plt.title(title)
        plt.xticks(rotation=45)
        plt.tight_layout()

    def create_plotly_plot(self, x, y, kind='scatter', title=''):
        if kind == 'scatter':
            fig = px.scatter(self.df, x=x, y=y, title=title)
        elif kind == 'bar':
            fig = px.bar(self.df, x=x, y=y, title=title)
        elif kind == 'line':
            fig = px.line(self.df, x=x, y=y, title=title)
        fig.show()