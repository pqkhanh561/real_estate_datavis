import pandas as pd
import numpy as np

NAN_LIST = ['Trống', 'Không xác định', 'Để trống', 'Khác', '']

if __name__=='__main__':
    data_path = "./data/raw_propzy.csv"

    data = pd.read_csv(data_path)
    property_set = set()
    for i in range(len(data['details_property'])):
        property_value = data['details_property'][i].split('\\n')[2::2]
        property_att = data['details_property'][i].split('\\n')[1::2]
        for j, att in enumerate(property_att):
            try:
                data[f"property_{att}"]
            except KeyError:
                data[f"property_{att}"] = np.nan
            while not property_value[j][-1].isalnum():
                property_value[j] = property_value[j][:-1]
            if not property_value[j] in NAN_LIST:
                data.at[i, f"property_{att}"] = property_value[j]
    data = data.drop("details_property", axis=1)

    utility_set = set()
    for i in range(len(data['utility'])):
        utility_att = data['utility'][i].split('\n')
        for j, att in enumerate(utility_att):
            try:
                data[f"utility_{att}"]
            except KeyError:
                data[f"utility_{att}"] = np.nan
            data.at[i, f"utility_{att}"] = True
    data = data.drop("utility", axis=1)
    # More process
    data = data.drop("Unnamed: 0", axis=1)
    data = data.replace("Na", np.nan)
    data = data.replace("Không xác định", np.nan)
    data = data.set_index("item_code")


    data.to_csv("./post_propzy.csv")