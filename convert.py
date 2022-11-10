import pandas as pd

def csv_to_hdf5(csv):
    data = pd.read_csv(csv + ".csv")
    hdf = pd.HDFStore(csv + ".hdf5")
    hdf.put(csv, data, format = "table",data_columns=True)

csv_to_hdf5("players")
csv_to_hdf5("course_responses")