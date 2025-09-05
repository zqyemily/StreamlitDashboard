import streamlit as st
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


Team_Mapping = {
    'ST':'Summer Xia'
    ,'Hi-Studio':'大海'
    ,'3D-B': 'Max Liu'
    ,'Planner':'Max Liu'
    , 'CAD-Porject':'Max Liu'
    , '3D-A':'Max Liu'
    , '2D-C':'Max Liu'    
}

sql = '''
select 
A.TaskDate
,A.WorkHours
,B.ProjectID
,B.ProjectName
,D.OfficeID
,D.TeamCode
,D.Name as GroupName
,E.DesignTypeName 
,C.Name as Designer
,C.Email as DesignerEmail
,G.Name as PayType
,F.ChargingValue 
from DOS.TaskCalendar A
left join  DOS.Brief B
on A.BriefID = B.ID
left join DOS.Design C
on A.DesignID = C.ID
left join DOS.[Group] D
on C.GroupID = D.ID
left join DOS.BriefDesigner E
on A.BriefID = E.BriefID 
and A.DesignID = E.DesignID 
left join DOS.DesignManHour F
on E.DesignManHourID = F.ID 
left join DOS.SysParameter G
on F.ChargingType = G.ParaID 
and G.TypeID = 23
where A.Content in (1,2) and G.TypeID = 23 and A.OfficeID in ('sem','she')
'''


df_claim = get_df_from_db(sql,server = server_prod, database = database_prod,username = username_prod,password = password_prod)
df_claim['Team_Leader'] = df_claim['TeamCode'].apply(lambda x: Team_Mapping[x])
df_claim.to_csv(os.path.join(output_path,'designer_claim_data.csv'), encoding='utf-8', sep = "|", index=False)

sql = '''
select 
A.ID as BriefID
,A.OfficeID
,A.ProjectTeamCode
,A.TeamCode
,A.ProjectID
,A.ProjectName
,A.SIC
,A.Customer
,A.BriefName
,A.CreationTime as BriefCreationTime
,A.ProjectNature
,B.ProjectType
,B.ShowCloseDate 
,B.ShowOpenDate 
,B.BidStatus 
,B.BidAmount
,B.BidCurrency 
,B.ProjectStatusCode 
from DOS.Brief A
left join DOS.Project B
on A.ProjectID  = B.ProjectCode 
where A.OfficeID in ('sem','she') and A.Status = 3 and A.IsDelete = 0
'''
df_brief = get_df_from_db(sql,server = server_prod, database = database_prod,username = username_prod,password = password_prod)
df_brief['Team_Leader'] = df_brief['TeamCode'].apply(lambda x: Team_Mapping[x])
df_brief['ProjectNature'] = df_brief['ProjectNature'].apply(lambda x: 'Special Design' if x == 'Special Design 特别设计' else x)
df_brief['BidStatus'] = df_brief['BidStatus'].apply(lambda x: 'unknown' if pd.isna(x)  else x)
df_brief.to_csv(os.path.join(output_path,'designer_brief_data.csv'), encoding='utf-8', sep = "|", index=False)