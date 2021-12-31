
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def number_of_trips_per_year():
    plt.figure(figsize=(12, 6), tight_layout=True)
    data = pd.DataFrame({
        '2019 (sep-dec)': 4340136,
        '2020 (all year)': 3466690,
        '2021 (jan-nov)': 2193056
   }.items(), columns=['date', 'n_trips'])
    print(data.head())
    ax = sns.barplot(x=data['date'], y=data['n_trips'], palette='pastel')
    ax.set(title='Number of trips per year', xlabel='years', ylabel='Number of trips')
    ax.set(ylim=(0, 5000000))
    plt.xlabel('years')
    plt.ylabel('Number of trips')
    plt.title('Number of trips per year')
    plt.savefig(f'./viz/overall_data')

def compare_query_time(q):
    plt.figure(figsize=(12, 6), tight_layout=True)
    data = [
        {'database': 'Postgresql', 'query': 12 , 'query_time': [25986.038, 24493.246,23768.349,23309.691,21791.345], 'cache': 'yes'},
        {'database': 'Postgresql', 'query': 12 , 'query_time': [28185.207, 28363.405, 30100.143, 25368.974,25486.098], 'cache': 'no'},
        {'database': 'MonetDB', 'query': 12 , 'query_time': [1248.792,1038.961,671.854,751.839,793.257], 'cache': 'yes'},
        {'database': 'MonetDB', 'query': 12 , 'query_time': [1260.339,1265.989,1288.428,1534.348,1283.357], 'cache': 'no'},

        {'database': 'Postgresql', 'query': 11 , 'query_time': [369351.815,382000.304,360894.306,306283.596,301352.682], 'cache': 'yes'},
        {'database': 'Postgresql', 'query': 11 , 'query_time': [282231.622, 282917.659, 290730.634, 275964.505,280381.437], 'cache': 'no'},
        {'database': 'MonetDB', 'query': 11 , 'query_time': [8803.854,6393.352,6595.567,7719.279,7975.699], 'cache': 'yes'},
        {'database': 'MonetDB', 'query': 11 , 'query_time': [8039.317, 8093.544, 8539.98, 7960.76, 7839.176], 'cache': 'no'},

        {'database': 'Postgresql', 'query': 9, 'query_time': [22637.111, 15179.696, 15373.803, 14913.231, 14400.02], 'cache': 'yes'},
        {'database': 'Postgresql', 'query': 9, 'query_time': [18597.637, 19592.120, 19435.459, 20484.262, 20475.098], 'cache': 'no'},
        {'database': 'MonetDB', 'query': 9, 'query_time': [674.161, 185.393,284.994,182.698,167.036], 'cache': 'yes'},
        {'database': 'MonetDB', 'query': 9, 'query_time': [349.95, 340.137, 339.133, 348.573, 331.452], 'cache': 'no'},

        {'database': 'Postgresql (w/aggregation)', 'query': 3, 'query_time': [1.256, 1.991, 1.190, 1.147, 1.085], 'cache': 'yes'},
        {'database': 'Postgresql (w/aggregation)', 'query': 3, 'query_time': [6.524, 6.443, 5.384, 3.735, 3.298], 'cache': 'no'},
        {'database': 'Postgresql (no aggregation)', 'query': 3, 'query_time': [16264.065, 17585.592, 17079.588, 18460.145, 16593.414], 'cache': 'yes'},
        {'database': 'Postgresql (no aggregation)', 'query': 3, 'query_time': [18457.982, 17581.291, 16814.816, 18319.746, 17123.725], 'cache': 'no'},

        {'database': 'Postgresql', 'query': 1, 'query_time': [238410.431, 241433.862, 235787.261, 228391.943, 229032.360],'cache': 'yes'},
        {'database': 'Postgresql', 'query': 1, 'query_time': [236995.265, 236170.807, 236684.965, 249191.875, 276765.701],'cache': 'no'},
        {'database': 'MonetDB', 'query': 1,'query_time': [2902141.289], 'cache': 'yes'},
        {'database': 'MonetDB', 'query': 1,'query_time': [2922656.184], 'cache': 'no'},
    ]
    data = pd.DataFrame(data)
    print(data.head())
    filtered_data = data.loc[data['query'] == q]
    filtered_data['query_time'] = filtered_data['query_time'].apply(lambda l: (sum(l)/1000)/len(l))
    #print(filtered_data['query_time'].values.mean())
    print(np.array(filtered_data['query_time']))
    ax = sns.barplot(x='database', y='query_time', hue='cache', data=filtered_data,
        palette='pastel',
        order=['Postgresql', 'MonetDB'],
        capsize=0.05,
        saturation=8,
        errcolor='gray', errwidth=2,
        ci='sd'
    )
    for container in ax.containers:
        ax.bar_label(container)
    plt.xlabel('Database (w/n cache)')
    plt.ylabel('Query execution time (s)')
    plt.title(f'Postgresql VS MonetDB Query time (w/n cache) [Query {q}]')
    plt.savefig(f'./viz/query_{q}')
def main():
    #number_of_trips_per_year()
    #compare_query_time(12)
    #compare_query_time(11)
    #compare_query_time(9)
    compare_query_time(1)

if __name__ == '__main__':
    main()