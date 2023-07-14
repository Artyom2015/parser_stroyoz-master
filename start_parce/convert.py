import os.path
import pandas as pd


path = r'../resul_parce'
files_exel = r'../Parce_xlsx'
try:
    for root, dirs, files in os.walk(path):
        for _file in files:
            print(_file)
            if _file == ".DS_Store":
                continue
            with open(f"{path}/{_file}", encoding='utf-8') as inputfile:
                df = pd.read_json(inputfile)
                _file1 = _file.replace('.json', '.xlsx')
            df.to_excel(f"{files_exel}/{_file1}")
            # print(_file)
except Exception as e: print(e)


# python convert.py