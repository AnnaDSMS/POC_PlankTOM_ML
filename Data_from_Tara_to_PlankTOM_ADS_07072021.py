#colocalization of Tara data with PlankTOM12
import numpy as np
import xarray as xr
import pandas as pd
from datetime import date
from collections import Counter

#read original UVP5 measurements 
r_filenameTSV = 'Target_Only_Biovol.csv'
data_all_1 = pd.read_csv(r_filenameTSV)

#creation of columns for year, month and day
data_all_1[['date','time']] = data_all_1.date_time_utc.str.split(" ",expand=True,)
data_all_1 = data_all_1.drop(columns=['Unnamed: 0'])
data_all_1[['year','month','day']] = data_all_1.date.str.split("/",expand=True,)
data_all_1['year'] = data_all_1['year'].astype(int)
data_all_1['month'] = data_all_1['month'].astype(int)
data_all_1['day'] = data_all_1['day'].astype(int)

Data_position = data_all_1[['station_name','lat','lon','year','month','day','depth']]
Data_position['coordinates'] = list(zip(Data_position.lat, Data_position.lon))

Data_position['day_numb'] = Data_position['day']

for i in Data_position.index.to_numpy():
    delta = date(Data_position['year'][i],Data_position['month'][i],Data_position['day'][i]) - date(Data_position['year'][i],1,1)
    Data_position.loc[Data_position.index == i,'day_numb'] = delta.days + 1

data_all_Tara_date = Data_position.groupby(['year','month'])
data_all_Tara_coord = Data_position.groupby(['coordinates'])

#empty arrays for variables that will be written into file
Temp_PlankTOM_to_file = []
Temp_back_PlankTOM_to_file = []
MLD_PlankTOM_to_file = []
year_PlankTOM_to_file = []
month_PlankTOM_to_file = []
lat_PlankTOM_to_file = []
lon_PlankTOM_to_file = []
depth_PlankTOM_to_file = []
lat_Tara_to_file = []
lon_Tara_to_file = []

O2_PlankTOM_to_file = []
O2_back_PlankTOM_to_file = []
NO3_PlankTOM_to_file = []
NO3_back_PlankTOM_to_file = []
Si_PlankTOM_to_file = []
Si_back_PlankTOM_to_file = []
PO4_PlankTOM_to_file = []
PO4_back_PlankTOM_to_file = []
POC_PlankTOM_to_file = []
GOC_PlankTOM_to_file = []
BAC_PlankTOM_to_file = []
BAC_back_PlankTOM_to_file = []
MES_PlankTOM_to_file = []
MES_back_PlankTOM_to_file = []
PTE_PlankTOM_to_file = []
PTE_back_PlankTOM_to_file = []
DIA_PlankTOM_to_file = []
DIA_back_PlankTOM_to_file = []
COC_PlankTOM_to_file = []
COC_back_PlankTOM_to_file = []
PHA_PlankTOM_to_file = []
PHA_back_PlankTOM_to_file = []
PIC_PlankTOM_to_file = []
PIC_back_PlankTOM_to_file = []
GEL_PlankTOM_to_file = []
GEL_back_PlankTOM_to_file = []
PRO_PlankTOM_to_file = []
PRO_back_PlankTOM_to_file = []
MAC_PlankTOM_to_file = []
MAC_back_PlankTOM_to_file = []
MIX_PlankTOM_to_file = []
MIX_back_PlankTOM_to_file = []
FIX_PlankTOM_to_file = []
FIX_back_PlankTOM_to_file = []
CHL_PlankTOM_to_file = []
CHL_back_PlankTOM_to_file = []
bottom_to_file = []

#mask of PlankTOM12
filename_mask = 'mesh_mask3_6.nc'
ds_mask = xr.open_dataset(filename_mask)
mask = ds_mask.tmask

mask = mask.where(mask > 0.)

#main loop
t = 0
for key, item in data_all_Tara_date:
    print('Time: ',key)
    year = int(key[0])
    month = int(key[1])
    filename_bottom = 'ORCA2_1m_20110101_20111231_diad_T.nc'
    ds_bottom = xr.open_dataset(filename_bottom)
    if t == 0: 
       filename = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_grid_T.nc'
       ds = xr.open_dataset(filename)
       filename_ptrc = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_ptrc_T.nc'
       ds_ptrc = xr.open_dataset(filename_ptrc)
       filename_chl = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_diad_T.nc'
       ds_chl = xr.open_dataset(filename_chl)
       t = 1
       year_before = year
       print(filename)
    if year_before != year:
       filename = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_grid_T.nc'
       ds = xr.open_dataset(filename)
       filename_ptrc = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_ptrc_T.nc'
       ds_ptrc = xr.open_dataset(filename_ptrc)
       filename_chl = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_diad_T.nc'
       ds_chl = xr.open_dataset(filename_chl)
       year_before = year
       print(filename)
    if int(month) == 1:
       filename_back = 'ORCA2_1m_'+str(year-1)+'0101_'+str(year-1)+'1231_grid_T.nc'
       ds_back = xr.open_dataset(filename_back)
       filename_ptrc_back = 'ORCA2_1m_'+str(year-1)+'0101_'+str(year-1)+'1231_ptrc_T.nc'
       ds_ptrc_back = xr.open_dataset(filename_ptrc_back)
       filename_chl_back = 'ORCA2_1m_'+str(year-1)+'0101_'+str(year-1)+'1231_diad_T.nc'
       ds_chl_back = xr.open_dataset(filename_chl_back)
    time_index = int(month) - 1
    test = data_all_Tara_date.get_group(key)
    data_all_Tara_date_coord = test.groupby(['coordinates'])
    for key1, item1 in data_all_Tara_date_coord:
        print('Coordinates: ',key1)
        lat_array = data_all_Tara_date_coord.get_group(key1)['lat'].values
        lon_array = data_all_Tara_date_coord.get_group(key1)['lon'].values
        if lat_array.size > 1:
           lat_Tara = [item for item, count in Counter(lat_array).items() if count > 1]
           lon_Tara = [item for item, count in Counter(lon_array).items() if count > 1]
        else:
           lat_Tara = lat_array
           lon_Tara = lon_array
        lat_nan = ds.nav_lat.values * mask.values[0,0,:,:]
        lon_nan = ds.nav_lon.values * mask.values[0,0,:,:]
        abslat = np.abs(lat_nan-lat_Tara[0])
        abslon = np.abs(lon_nan-lon_Tara[0])
        c = np.sqrt(abslon**2+abslat**2)
        xt = np.where(c == np.nanmin(c))
        if len(xt[0]) == 1:
           ([yloc], [xloc]) = np.where(c == np.nanmin(c))
        else:
           ([yloc], [xloc]) = (np.array([xt[0][0]]),np.array([xt[1][0]]))
        print('PlankTOM: ',ds.nav_lat.values[yloc,xloc],ds.nav_lon.values[yloc,xloc])
        Temp = ds.votemper.values[time_index,:,yloc,xloc] 
        if time_index == 0:
           Temp_back = ds_back.votemper.values[11,:,yloc,xloc]
        else:
           Temp_back = ds.votemper.values[time_index-1,:,yloc,xloc]
        MLD  = ds.somxl030.values[time_index,yloc,xloc]
        O2   = ds_ptrc.O2.values[time_index,:,yloc,xloc]
        if time_index == 0:
           O2_back = ds_ptrc_back.O2.values[11,:,yloc,xloc]
        else:
           O2_back = ds_ptrc.O2.values[time_index-1,:,yloc,xloc]
        NO3  = ds_ptrc.NO3.values[time_index,:,yloc,xloc]
        if time_index == 0:
           NO3_back = ds_ptrc_back.NO3.values[11,:,yloc,xloc]
        else:
           NO3_back = ds_ptrc.NO3.values[time_index-1,:,yloc,xloc]
        Si   = ds_ptrc.Si.values[time_index,:,yloc,xloc]
        if time_index == 0:
           Si_back = ds_ptrc_back.Si.values[11,:,yloc,xloc]
        else:
           Si_back = ds_ptrc.Si.values[time_index-1,:,yloc,xloc]
        PO4  = ds_ptrc.PO4.values[time_index,:,yloc,xloc]
        if time_index == 0:
           PO4_back = ds_ptrc_back.PO4.values[11,:,yloc,xloc]
        else:
           PO4_back = ds_ptrc.PO4.values[time_index-1,:,yloc,xloc]
        POC  = ds_ptrc.POC.values[time_index,:,yloc,xloc]
        GOC  = ds_ptrc.GOC.values[time_index,:,yloc,xloc]
        BAC  = ds_ptrc.BAC.values[time_index,:,yloc,xloc]
        if time_index == 0:
           BAC_back = ds_ptrc_back.BAC.values[11,:,yloc,xloc]
        else:
           BAC_back = ds_ptrc.BAC.values[time_index-1,:,yloc,xloc]
        MES  = ds_ptrc.MES.values[time_index,:,yloc,xloc]
        if time_index == 0:
           MES_back = ds_ptrc_back.MES.values[11,:,yloc,xloc]
        else:
           MES_back = ds_ptrc.MES.values[time_index-1,:,yloc,xloc]
        PTE  = ds_ptrc.PTE.values[time_index,:,yloc,xloc]
        if time_index == 0:
           PTE_back = ds_ptrc_back.PTE.values[11,:,yloc,xloc]
        else:
           PTE_back = ds_ptrc.PTE.values[time_index-1,:,yloc,xloc]
        DIA  = ds_ptrc.DIA.values[time_index,:,yloc,xloc]
        if time_index == 0:
           DIA_back = ds_ptrc_back.DIA.values[11,:,yloc,xloc]
        else:
           DIA_back = ds_ptrc.DIA.values[time_index-1,:,yloc,xloc]
        COC  = ds_ptrc.COC.values[time_index,:,yloc,xloc]
        if time_index == 0:
           COC_back = ds_ptrc_back.COC.values[11,:,yloc,xloc]
        else:
           COC_back = ds_ptrc.COC.values[time_index-1,:,yloc,xloc]
        PIC  = ds_ptrc.PIC.values[time_index,:,yloc,xloc]
        if time_index == 0:
           PIC_back = ds_ptrc_back.PIC.values[11,:,yloc,xloc]
        else:
           PIC_back = ds_ptrc.PIC.values[time_index-1,:,yloc,xloc]
        PHA  = ds_ptrc.PHA.values[time_index,:,yloc,xloc]
        if time_index == 0:
           PHA_back = ds_ptrc_back.PHA.values[11,:,yloc,xloc]
        else:
           PHA_back = ds_ptrc.PHA.values[time_index-1,:,yloc,xloc]
        GEL  = ds_ptrc.GEL.values[time_index,:,yloc,xloc]
        if time_index == 0:
           GEL_back = ds_ptrc_back.GEL.values[11,:,yloc,xloc]
        else:
           GEL_back = ds_ptrc.GEL.values[time_index-1,:,yloc,xloc]
        PRO  = ds_ptrc.PRO.values[time_index,:,yloc,xloc]
        if time_index == 0:
           PRO_back = ds_ptrc_back.PRO.values[11,:,yloc,xloc]
        else:
           PRO_back = ds_ptrc.PRO.values[time_index-1,:,yloc,xloc]
        MAC  = ds_ptrc.MAC.values[time_index,:,yloc,xloc]
        if time_index == 0:
           MAC_back = ds_ptrc_back.MAC.values[11,:,yloc,xloc]
        else:
           MAC_back = ds_ptrc.MAC.values[time_index-1,:,yloc,xloc]
        MIX  = ds_ptrc.MIX.values[time_index,:,yloc,xloc]
        if time_index == 0:
           MIX_back = ds_ptrc_back.MIX.values[11,:,yloc,xloc]
        else:
           MIX_back = ds_ptrc.MIX.values[time_index-1,:,yloc,xloc]
        FIX  = ds_ptrc.FIX.values[time_index,:,yloc,xloc]
        if time_index == 0:
           FIX_back = ds_ptrc_back.FIX.values[11,:,yloc,xloc]
        else:
           FIX_back = ds_ptrc.FIX.values[time_index-1,:,yloc,xloc]
        CHL  = ds_chl.TChl.values[time_index,:,yloc,xloc]
        if time_index == 0:
           CHL_back = ds_chl_back.TChl.values[11,:,yloc,xloc]
        else:
           CHL_back = ds_chl.TChl.values[time_index-1,:,yloc,xloc]
        bottom = ds_bottom.bottom_depth.values[time_index,yloc,xloc]
        lat_PlankTOM = ds.nav_lat.values[yloc,xloc]
        lon_PlankTOM = ds.nav_lon.values[yloc,xloc]
        depth_PlankTOM = ds.deptht.values
        time_year = year
        time_month = month
        item1_values = item1['depth'].values.astype(np.float)
        for ind_T in np.arange(0,len(Temp),1):
            if depth_PlankTOM[ind_T] <= np.max(item1_values):
               Temp_PlankTOM_to_file.append(Temp[ind_T])
               Temp_back_PlankTOM_to_file.append(Temp_back[ind_T]) 
               MLD_PlankTOM_to_file.append(MLD)
               O2_PlankTOM_to_file.append(O2[ind_T])
               O2_back_PlankTOM_to_file.append(O2_back[ind_T])
               NO3_PlankTOM_to_file.append(NO3[ind_T])
               NO3_back_PlankTOM_to_file.append(NO3_back[ind_T])
               Si_PlankTOM_to_file.append(Si[ind_T])
               Si_back_PlankTOM_to_file.append(Si_back[ind_T])
               PO4_PlankTOM_to_file.append(PO4[ind_T])
               PO4_back_PlankTOM_to_file.append(PO4_back[ind_T])
               POC_PlankTOM_to_file.append(POC[ind_T])
               GOC_PlankTOM_to_file.append(GOC[ind_T])
               BAC_PlankTOM_to_file.append(BAC[ind_T])
               BAC_back_PlankTOM_to_file.append(BAC_back[ind_T])
               MES_PlankTOM_to_file.append(MES[ind_T])
               MES_back_PlankTOM_to_file.append(MES_back[ind_T])
               PTE_PlankTOM_to_file.append(PTE[ind_T])
               PTE_back_PlankTOM_to_file.append(PTE_back[ind_T])
               DIA_PlankTOM_to_file.append(DIA[ind_T])
               DIA_back_PlankTOM_to_file.append(DIA_back[ind_T])
               COC_PlankTOM_to_file.append(COC[ind_T])
               COC_back_PlankTOM_to_file.append(COC_back[ind_T])
               PIC_PlankTOM_to_file.append(PIC[ind_T])
               PIC_back_PlankTOM_to_file.append(PIC_back[ind_T])
               PHA_PlankTOM_to_file.append(PHA[ind_T])
               PHA_back_PlankTOM_to_file.append(PHA_back[ind_T])
               GEL_PlankTOM_to_file.append(GEL[ind_T])
               GEL_back_PlankTOM_to_file.append(GEL_back[ind_T])
               PRO_PlankTOM_to_file.append(PRO[ind_T])
               PRO_back_PlankTOM_to_file.append(PRO_back[ind_T])
               MAC_PlankTOM_to_file.append(MAC[ind_T])
               MAC_back_PlankTOM_to_file.append(MAC_back[ind_T])
               MIX_PlankTOM_to_file.append(MIX[ind_T])
               MIX_back_PlankTOM_to_file.append(MIX_back[ind_T])
               FIX_PlankTOM_to_file.append(FIX[ind_T])
               FIX_back_PlankTOM_to_file.append(FIX_back[ind_T])
               CHL_PlankTOM_to_file.append(CHL[ind_T])
               CHL_back_PlankTOM_to_file.append(CHL_back[ind_T])
               bottom_to_file.append(bottom)
               year_PlankTOM_to_file.append(int(year))
               month_PlankTOM_to_file.append(int(month))
               lat_PlankTOM_to_file.append(lat_PlankTOM)
               lon_PlankTOM_to_file.append(lon_PlankTOM)
               depth_PlankTOM_to_file.append(depth_PlankTOM[ind_T])
               lat_Tara_to_file.append(lat_Tara[0])
               lon_Tara_to_file.append(lon_Tara[0])

#data into dataframe
Data_all = pd.DataFrame({'year': year_PlankTOM_to_file, 'month': month_PlankTOM_to_file, 'lat_Pl': lat_PlankTOM_to_file, 'lon_Pl': lon_PlankTOM_to_file, 'depth': depth_PlankTOM_to_file, 'Temp': Temp_PlankTOM_to_file, 'Temp_back': Temp_back_PlankTOM_to_file, 'MLD': MLD_PlankTOM_to_file, 'POC': POC_PlankTOM_to_file, 'GOC': GOC_PlankTOM_to_file, 'O2': O2_PlankTOM_to_file, 'O2_back': O2_back_PlankTOM_to_file, 'NO3': NO3_PlankTOM_to_file, 'NO3_back': NO3_back_PlankTOM_to_file, 'PO4': PO4_PlankTOM_to_file, 'PO4_back': PO4_back_PlankTOM_to_file, 'Si': Si_PlankTOM_to_file, 'Si_back': Si_back_PlankTOM_to_file, 'CHL': CHL_PlankTOM_to_file, 'CHL_back': CHL_back_PlankTOM_to_file, 'BAC': BAC_PlankTOM_to_file, 'BAC_back': BAC_back_PlankTOM_to_file, 'MES': MES_PlankTOM_to_file, 'MES_back': MES_back_PlankTOM_to_file, 'PTE': PTE_PlankTOM_to_file, 'PTE_back': PTE_back_PlankTOM_to_file, 'DIA': DIA_PlankTOM_to_file, 'DIA_back': DIA_back_PlankTOM_to_file, 'COC': COC_PlankTOM_to_file, 'COC_back': COC_back_PlankTOM_to_file, 'PIC': PIC_PlankTOM_to_file, 'PIC_back': PIC_back_PlankTOM_to_file, 'PHA': PHA_PlankTOM_to_file, 'PHA_back': PHA_back_PlankTOM_to_file, 'GEL': GEL_PlankTOM_to_file, 'GEL_back': GEL_back_PlankTOM_to_file, 'PRO': PRO_PlankTOM_to_file, 'PRO_back': PRO_back_PlankTOM_to_file, 'MAC': MAC_PlankTOM_to_file, 'MAC_back': MAC_back_PlankTOM_to_file, 'MIX': MIX_PlankTOM_to_file, 'MIX_back': MIX_back_PlankTOM_to_file, 'FIX': FIX_PlankTOM_to_file, 'FIX_back': FIX_back_PlankTOM_to_file, 'bottom': bottom_to_file}, columns=['year','month','lat_Pl','lon_Pl','depth','Temp','Temp_back','MLD','POC','GOC','O2','O2_back','NO3','NO3_back','PO4','PO4_back','Si','Si_back','CHL','CHL_back','BAC','BAC_back','MES','MES_back','PTE','PTE_back','DIA','DIA_back','COC','COC_back','PIC','PIC_back','PHA','PHA_back','GEL','GEL_back','PRO','PRO_back','MAC','MAC_back','MIX','MIX_back','FIX','FIX_back','bottom'])

#save dataframe
Data_all.to_csv('Data_ML_PlankTOM_All_PFTCHL_bottom_13122021.csv')

