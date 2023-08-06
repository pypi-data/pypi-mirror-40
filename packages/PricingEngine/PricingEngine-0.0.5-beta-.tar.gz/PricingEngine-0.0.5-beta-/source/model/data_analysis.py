import datetime

import matplotlib.mlab as m_lab
import matplotlib.pyplot as plt
import pandas as pd
from utilities.helper import Helper, Constants


class DataAnalysis:
    now = datetime.datetime.now()
    past = (datetime.datetime.now() - datetime.timedelta(days=15))
    need_to_remove_dir_name = Constants.GRAPH_DIRECTORY+'/'+past.strftime("%Y_%m_%d")
    Constants.GRAPH_DIRECTORY = Constants.GRAPH_DIRECTORY+'/'+now.strftime("%Y_%m_%d")
    Helper.remove_directory(need_to_remove_dir_name)
    Helper.crate_directory(Constants.GRAPH_DIRECTORY)
    # if we pass core than one column in array then we have to use kind=bar other wise it will give error

    def graph_plot(self, data_frame, column_array, target_column, title='Graph', kind='bar'):
        data_frame = pd.DataFrame(data_frame)
        data_frame.plot(x=target_column, y=column_array, kind=kind)
        self.show_graph(title)

    def plot_corr(self, df, size=11):
        df = df.drop([Constants.PREDICTION_TARGET], axis=1)
        corr = df.corr()
        fig, ax = plt.subplots(figsize=(size, size))
        ax.matshow(corr)
        plt.xticks(range(len(corr.columns)), corr.columns)
        plt.yticks(range(len(corr.columns)), corr.columns)

    @staticmethod
    def unique_value_count(data, column_name):
        count = data.groupby(column_name).size()
        key = list(count.keys())
        data = {column_name: key, 'Count': count}
        data = pd.DataFrame(data=data)
        data.to_csv(Constants.TEMP_DIRECTORY + '/' + column_name + '.csv', sep=',', encoding='utf-8')
        return data

    def simple_graph_plot(self, x, y, title='Graph', kind='scatter'):
        getattr(plt, kind)(x, y)
        self.show_graph(title)

    @staticmethod
    def show_graph(title):
        plt.title(title)
        now = datetime.datetime.now()
        plt.savefig(Constants.GRAPH_DIRECTORY + '/' + title + now.strftime("%H_%M_%S.png"), dpi=100)
        plt.show()

    @staticmethod
    def graph_for_variance(mu, sigma, x):
        title_name = (r'Histogram of IQ: $\mu=' + str("%.2f" % round(mu, 2)) +
                      '$, $\sigma=' + str("%.2f" % round(sigma, 2)) + '$')
        # mu  mean of distribution
        # sigma standard deviation of distribution
        num_bins = 20
        # the histogram of the data
        n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='blue', alpha=0.5)
        # add a 'best fit' line
        y = m_lab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('Smarts')
        plt.ylabel('Probability')
        plt.title = title_name

        plt.subplots_adjust(left=0.15)
        plt.show()

    def graph_for_all_numerical_data(self, data):
        data.hist(bins=30, figsize=(16, 16))
        title = 'Histogram for each numeric input variable'
        self.show_graph(title)

    @staticmethod
    def outlier_graph(pricing_data, title):
        d = DataAnalysis()
        # d.plot_corr(pricing_data.drop([Constants.ID], axis=1))
        d.graph_for_all_numerical_data(pricing_data)
        pricing_data.plot(kind="scatter", x="Mileage", y="SalesPrice", alpha=0.4
                          , s=pricing_data[["MakeName", "ModelName", "StyleName"]] / 100
                          , label="MMRAvgValue", c="MMRAvgValue", cmap=plt.get_cmap("jet"), colorbar=True,)
        plt.legend()
        plt.title(title)
        plt.show()
