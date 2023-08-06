import pandas as pd

def oscars():
    df = pd.read_csv('sample-data.csv', skipinitialspace=True, quotechar='"', encoding='utf8').set_index('Index')
    janet = df.Name[1]
    return janet

