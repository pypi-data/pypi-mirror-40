import pandas as pd
from pkg_resources import resource_filename

def oscars():
    csv = resource_filename('sample_python_package','/data/sample-data.csv')
    df = pd.read_csv(csv, skipinitialspace=True, quotechar='"', encoding='utf8').set_index('Index')
    janet = df.Name[1]
    return janet

