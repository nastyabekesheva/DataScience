
import pip
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])

#install('seaborn')

from spyre import server
import data
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
#for i in range(1,28):
 #   data._download_data(i)

server.include_df_index = True

class NOAA_web_page(server.App):
    title = "Web page for NOAA data"

    inputs = [{
        "type": 'dropdown',
        "label": 'NOAA data',
        "options": [
            {"label": "VCI", "value": "VCI"},
            {"label": "TCI", "value": "TCI"},
            {"label": "VHI", "value": "VHI"}],
        "key": 'index',
        "action_id": "update_data"
    },
    {
            "type": 'dropdown',
            "label": 'Region',
            "options": [
                {"label": "Vinnytsia r.", "value": "1"},
                {"label": "Volyn r.", "value": "2"},
                {"label": "Dnipro r.", "value": "3"},
                {"label": "Donetsk r.", "value": "4"},
                {"label": "Zhytomyr r.", "value": "5"},
                {"label": "Zakarpattia r.", "value": "6"},
                {"label": "Zaporizhzhia r.", "value": "7"},
                {"label": "Ivano-Frankivsk r.", "value": "8"},
                {"label": "Kyiv r.", "value": "9"},
                {"label": "Kirovohrad r.", "value": "10"},
                {"label": "Luhansk r.", "value": "11"},
                {"label": "Lviv r.", "value": "12"},
                {"label": "Mykolaiv r.", "value": "13"},
                {"label": "Odesa r.", "value": "14"},
                {"label": "Poltava r.", "value": "15"},
                {"label": "Rivne r.", "value": "16"},
                {"label": "Sumy r.", "value": "17"},
                {"label": "Ternopil r.", "value": "18"},
                {"label": "Kharkiv r.", "value": "19"},
                {"label": "Kherson r.", "value": "20"},
                {"label": "Khmelnytshyi r.", "value": "21"},
                {"label": "Cherkasy r.", "value": "22"},
                {"label": "Chernivtsi r.", "value": "23"},
                {"label": "Chernihiv r.", "value": "24"},
                {"label": "AR Crimea", "value": "25"},
                {"label": "Kyiv c.", "value": "26"},
                {"label": "Sevastopol c.", "value": "27"}],
            "value": 26,
            "key": 'region_index',
            "action_id": "update_data"
    },
    {
        "type": 'dropdown',
        "label": 'Plot by',
        "options": [
            {"label": "Weeks", "value": "Week"},
            {"label": "Years", "value": "Year"}],
        "key": 'column',
        "action_id": "update_data"
    },
    {
        "type": 'dropdown',
        "label": 'Type of plot',
        "options": [
            {"label": "Scatterplot", "value": "Scatterplot"},
            {"label": "Lineplot", "value": "Lineplot"},
            {"label": "Heatmap", "value": "Heatmap"},
            {"label": "Regplot", "value": "Regplot"},],
        "key": 'type_of_plot',
        "action_id": "update_data"
    },
    {
            "type": "text",
            "key": 'range_weeks',
            "label": "Range of weeks",
            "value": "1-52",
            "action_id": 'simple_html_output'
    },
    {
            "type": "text",
            "key": 'range_years',
            "label": "Range of years",
            "value": "1991-2022",
            "action_id": 'simple_html_output'
    }]

    controls = [
        {
            "type": "button",
            "id": "update_data",
            "label": "Show data"
        }]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "__get_plot__",
            "control_id": "update_data",
            "tab": "Plot"},
        {
            "type": "table",
            "id": "__get_data__",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]
    
    def __get_html__(self, params):
        return params["range"]
        
    def __parse_range__(self, r):
        temp = []
        r = [int(i) for i in r.split('-')]
        try:
            temp = range(r[0], r[1]+1)
        except IndexError:
            try:
                temp = range(r[0], r[0]+1)
            except IndexError:
                temp = []
        return temp
        
    def __get_all_data__(self, params):
        many_df = []
        for i in range(1, 28):
            many_df.append(data._load_data_to_df(i))
        df = data._merge_df(many_df)

        df = df.loc[df['Year'].isin(self.__parse_range__(params['range_years'])) & df['Week'].isin(self.__parse_range__(params['range_weeks'])) & (df['Region'] == params['region_index'])]
        df = df.sort_values('Year')
        df = df.reset_index()
        return df[['Year', 'Week', 'SMN', 'SMT', 'Region', 'VHI', 'VCI', 'TCI']]
        
    def __get_data__(self, params):
        df = self.__get_all_data__(params)
        return df[['Year', 'Week', 'SMN', 'SMT', 'Region', params['index']]]
        
        
    def __get_plot__(self, params):
        df = self.__get_data__(params)
        df_hm = self.__get_all_data__(params)
        df = df.sort_values(params['index'], ascending=False)
        pl = plt.figure(figsize = (18,12))
        if params['type_of_plot'] == "Scatterplot":
            ax = sns.scatterplot(x=params['column'], y=params['index'], data=df)
        elif params['type_of_plot'] == "Lineplot":
            ax = sns.lineplot(x=params['column'], y=params['index'], data=df)
        elif params['type_of_plot'] == "Heatmap":
            df_hm['VHI'] = [float(i) for i in df_hm['VHI']]
            df_hm['TCI'] = [float(i) for i in df_hm['TCI']]
            df_hm['VCI'] = [float(i) for i in df_hm['VCI']]
            df_hm['SMN'] = [float(i) for i in df_hm['SMN']]
            df_hm['SMT'] = [float(i) for i in df_hm['SMT']]
            ax = sns.heatmap(data=df_hm[['VHI', 'VCI', 'TCI', 'SMN', 'SMT']].corr(method='pearson'), annot=True)
        elif params['type_of_plot'] == "Regplot":
            df[params['index']] = [int(float(i)) for i in df[params['index']]]
            ax = sns.regplot(x=params['column'], y=params['index'], data=df)

        ax_base = 1
        n = len(self.__parse_range__(params['range_years']))
        if n > 1 and n < 5:
            ax_base = 3
        elif n >= 5 and n < 9:
            ax_base = 6
        elif n >= 9 and n < 14:
            ax_base = 9
        elif n >= 14 and n < 19:
            ax_base = 12
        elif n >= 19 and n < 23:
            ax_base = 15
        elif n >= 23 and n < 30:
            ax_base = 20
        elif n >= 30:
            ax_base = 25
            
        if params['type_of_plot'] != "Heatmap":
            ax.yaxis.set_major_locator(ticker.MultipleLocator(base=ax_base))
            if params['column'] != "Year":
                ax.xaxis.set_major_locator(ticker.MultipleLocator(base=1))
        return ax.get_figure()



app = NOAA_web_page()
app.launch(port=9093)

