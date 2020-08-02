#!/usr/bin/python
# -*- coding: utf-8 -*-
import glob
import re
import datetime as dt
from itertools import chain

import pdfplumber
import pandas as pd


table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines"
}


def get_date_from_pdf_path_func():
    date_pattern = re.compile("\d+年\d+月\d+日")
    date_fmt = "%Y年%m月%d日"
    
    def get_date_from_pdf_path(pdf_path):
        date_string = re.search(date_pattern, pdf_path).group(0)
        return dt.datetime.strptime(date_string, date_fmt)
    
    return get_date_from_pdf_path


dtfpath = get_date_from_pdf_path_func()


def is_target_table(plumber_table):
    # plumber_table is presented as a list of list(line of a table)
    return len(plumber_table[0]) > 7
    
    
def extract_table_from_pdf(pdf):
    target_tables = []
    for page in pdf.pages:
        tables = page.extract_tables(table_settings)
        target_tables.extend([table for table in tables if is_target_table(table)])
    
    table_lines = list(chain(*target_tables))
    df = pd.DataFrame(data=table_lines).fillna('')
    df = df.applymap(lambda x: x.replace('\n', ''))
    df.columns = list(df.iloc[0, :].values.tolist())
    return df.iloc[1:, :]
    

if __name__ == '__main__':
    pdf_paths = list(glob.iglob('../downloads/环境卫星/日报/*.pdf'))[0:10]
    for pdf_path in pdf_paths:
        with pdfplumber.open(pdf_path) as pdf:
            df = extract_table_from_pdf(pdf)
            df['日期'] = dtfpath(pdf_path)
        print(df)
