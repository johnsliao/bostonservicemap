import sys
import pandas as pd

CASE_IGNORE = 5
YEAR = '2015'

def load_data(fname):
    df = pd.read_csv(fname)

    types = set()

    # find unique type in data set
    for row in range(len(df.index)):
        types.add(df['TYPE'][row])

    # write unique csv for each case title
    for type in types:
        print type

        # there are floats in the data (?)
        type = str(type)

        # forward slashes mess up directory paths
        type = type.replace('/', '_')

        # filter out cases based on unique case titles
        filter = df.loc[df['TYPE'].isin([type])]

        # filter out cases based on year
        filter = filter.loc[filter['OPEN_DT'].str.contains(YEAR)]

        # ignore for cases < 5
        if len(filter.index) > CASE_IGNORE:
            filter.to_csv('./cartoDB_data/' + type + '.csv')


def main(fname):
    load_data(fname)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print '''Usage: generate_csv.py <311_data.csv>'''
        exit(1)

    fname = sys.argv[1]
    main(fname)