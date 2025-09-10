import streamlit as st
import sys
import pandas as pd
import numpy as np
import string
import pymssql
import os
from conf import config

print('the working dir is: ', os.getcwd())
config_path = os.path.join(os.getcwd(),'conf')
output_path = os.path.join(os.getcwd(),'data')

server_prod = config.db_config['prod']['server']
database_prod = config.db_config['prod']['database']
username_prod = config.db_config['prod']['usr']
password_prod = config.db_config['prod']['psw']

def get_df_from_db(sql, server, database,username,password):
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database)
        cursor = conn.cursor()
        # cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        columnDes = cursor.description
        columnNames = [columnDes[i][0] for i in range(len(columnDes))]
        df = pd.DataFrame([list(i) for i in data],columns=columnNames)
        cursor.close()
        conn.close()
        return df
    except Exception as e:
        print("Database connection failed due to {}".format(e))

sql_picox = '''
select 
C.Name as Analyst_Name
,A.TaskDate as Date
,A.WorkHours as Hours
,B.BriefName as Brief_Name
,E.Name AS BU
,A.Memo as Remark
,CASE
WHEN A.Category = 1 then F.Name
WHEN A.Category = 2 then G.Name
WHEN A.Category = 3 then H.Name
WHEN A.Category = 4 then I.Name
WHEN A.Category = 5 then J.Name
WHEN A.Category = 6 then K.Name
END AS WorkingContent
,D.Name as Category
FROM  PICOX_DOS.TaskCalendarPicoX A
left join PICOX_DOS.BriefPicoX B
on A.BriefID = B.ID
AND b.ID>=17
left join PICOX_DOS.DesignPicoX C
on A.DesignID = C.ID
left join PICOX_DOS.SysParameterPicoX D
on A.Category = D.ParaID
and D.TypeID = 11
left join  PICOX_DOS.SysParameterPicoX E
on A.InternalClient =E.ParaID
and E.TypeID = 12
left join  PICOX_DOS.SysParameterPicoX F
on A.Content = F.ParaID
AND A.Category = 1
and F.TypeID = 14
left join  PICOX_DOS.SysParameterPicoX G
on A.Content = G.ParaID
AND A.Category = 2
and G.TypeID = 24
left join  PICOX_DOS.SysParameterPicoX H
on A.Content = H.ParaID
AND A.Category = 3
and H.TypeID = 25
left join  PICOX_DOS.SysParameterPicoX I
on A.Content = I.ParaID
AND A.Category = 4
and I.TypeID = 26
left join  PICOX_DOS.SysParameterPicoX J
on A.Content = J.ParaID
AND A.Category = 5
and J.TypeID = 27
left join  PICOX_DOS.SysParameterPicoX K
on A.Content = K.ParaID
AND A.Category = 6
and K.TypeID = 28
where A.BriefID >=17
order by C.Name, A.TaskDate
'''
df = get_df_from_db(sql_picox,server = server_prod, database = database_prod,username = username_prod,password = password_prod)
df = df.sort_values(by = ['Analyst_Name','Date'])
df = df.rename(columns = {'Analyst_Name':'Analyst Name', 'Brief_Name':'Brief Name'})
df.to_csv(os.path.join(output_path,'Pico_X_claim_data.csv'), encoding='utf-8', sep = "|", index=False)

st.sidebar.page_link("home.py", label="Home", icon="🏠")

