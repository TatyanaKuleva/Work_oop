import pandas as pd
from pandas import DataFrame
import re


def sorted_data_by_set_number(get_data_list:list, data_for_sorted:str, n:int)->DataFrame:
    """сортирует данные по убыванию и выводит топ N-заданных данных"""
    df = pd.DataFrame(get_data_list).sort_values(data_for_sorted, ascending=False)
    df.columns = df.columns.map(lambda x: x.replace('_Vacancy__', ''))
    top_n_data = df.head(n).to_dict('records')

    return top_n_data


def filtr_data_by_set_word(get_data_list:list, data_for_filtr:str, word_for_filtr:list)->DataFrame:
    """фильтрует данные по заданному слову и выводит DF отфлльтрованных данных"""
    df = pd.DataFrame(get_data_list)
    df_filtr = df[df[data_for_filtr].str.contains('|'.join(word_for_filtr), na=False)]
    df_filtr.columns = df_filtr.columns.map(lambda x: x.replace('_Vacancy__', ''))
    result = df_filtr.to_dict('records')

    return result






if __name__ == "__main__":
   print(filtr_data_by_set_word())
