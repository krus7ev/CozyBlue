import pandas as pd

def load_dataframe(
    data_path,
    header    = 0,
    separator = ','
):
    """
    Takes the path of a data file. Checks its type - 'csv', 'xlsx' or 'tsv'.
    Returns a DataFrame with the data from data_path.
    """
    if data_path.endswith('.xlsx'):
        df = pd.read_excel(data_path)
    elif data_path.endswith('.csv'):
        df = pd.read_csv(data_path, header=header, sep=separator, engine='python')
    elif data_path.endswith('.tsv'):
        df = pd.read_csv(data_path, sep=separator, header=header, engine='python')
    else:
        import os
        print(f'File with extension: {os.path.splitext(data_path)[-1].lower()}')

    print(f'Rows: {df.shape[0]}')

    return df
