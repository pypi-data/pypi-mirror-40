"""
Setup Google Sheet Connection
"""

import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
from gspread_dataframe import set_with_dataframe


def get_gs_con():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    return gspread.authorize(creds)


def get_ws_data(gs_conn, gs_key, ws_name):
    """
    Read data from worksheet and load into a pandas data frame
    """
    gs_obj = gs_conn.open_by_key(gs_key)
    ws_obj = gs_obj.worksheet(ws_name)
    return pd.DataFrame(ws_obj.get_all_records())


def update_ws(gs_conn, gs_key, ws_name, data_frame):
    """
    Drop a worksheet and loads in once again with values from data frame
    Google sheet is assumed to be already created
    """
    gs_obj = gs_conn.open_by_key(gs_key)
    ws_list = gs_obj.worksheets()
    if ws_name in [element.title for element in ws_list]:
        worksheet = gs_obj.worksheet(ws_name)
        gs_obj.del_worksheet(worksheet)
    worksheet = gs_obj.add_worksheet(title=ws_name,
                                     rows=data_frame.shape[0],
                                     cols=data_frame.shape[1])
    set_with_dataframe(worksheet, data_frame)
