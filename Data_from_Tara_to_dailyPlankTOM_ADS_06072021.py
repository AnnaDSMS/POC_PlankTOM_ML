#colocalization of Tara data with daily PlankTOM12
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

data_all_Tara_date = Data_position.groupby(['year','month','day'])
data_all_Tara_coord = Data_position.groupby(['coordinates'])

#empty arrays for variables that will be written into file
year_PlankTOM_to_file = []
month_PlankTOM_to_file = []
day_PlankTOM_to_file = []
lat_PlankTOM_to_file = []
lon_PlankTOM_to_file = []
depth_PlankTOM_to_file = []
lat_Tara_to_file = []
lon_Tara_to_file = []

Temp_PlankTOM_to_file = []
Temp_back_PlankTOM_to_file = []
MLD_PlankTOM_to_file = []
O2_PlankTOM_to_file = []
O2_back_PlankTOM_to_file = []
NO3_PlankTOM_to_file = []
NO3_back_PlankTOM_to_file = []
Si_PlankTOM_to_file = []
Si_back_PlankTOM_to_file = []
PO4_PlankTOM_to_file = []
PO4_back_PlankTOM_to_file = []
BAC_PlankTOM_to_file = []
MES_PlankTOM_to_file = []
PTE_PlankTOM_to_file = []
DIA_PlankTOM_to_file = []
COC_PlankTOM_to_file = []
PHA_PlankTOM_to_file = []
PIC_PlankTOM_to_file = []
GEL_PlankTOM_to_file = []
PRO_PlankTOM_to_file = []
MAC_PlankTOM_to_file = []
MIX_PlankTOM_to_file = []
FIX_PlankTOM_to_file = []
BAC_back_PlankTOM_to_file = []
MES_back_PlankTOM_to_file = []
PTE_back_PlankTOM_to_file = []
DIA_back_PlankTOM_to_file = []
COC_back_PlankTOM_to_file = []
PHA_back_PlankTOM_to_file = []
PIC_back_PlankTOM_to_file = []
GEL_back_PlankTOM_to_file = []
PRO_back_PlankTOM_to_file = []
MAC_back_PlankTOM_to_file = []
MIX_back_PlankTOM_to_file = []
FIX_back_PlankTOM_to_file = []
CHL_PlankTOM_to_file = []
CHL_back_PlankTOM_to_file = []
POC_PlankTOM_to_file = []
GOC_PlankTOM_to_file = []
bottom_to_file = []

#mask of PlankTOM12
filename_mask = 'mesh_mask3_6.nc'
ds_mask = xr.open_dataset(filename_mask)
mask = ds_mask.tmask

mask = mask.where(mask > 0.)

#PlankTOM12 bathymetry 
filename_bottom = 'ORCA2_1m_20110101_20111231_diad_T.nc'
ds_bottom = xr.open_dataset(filename_bottom)

#main loop
t = 0
for key, item in data_all_Tara_date:
    print('Time: ',key)
    year = int(key[0])
    month = int(key[1])
    day = item['day_numb'].values[0]
    if t == 0: 
       filename = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_grid_T.nc'
       ds = xr.open_dataset(filename)
       filename_ptrc = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_ptrc_T.nc'
       ds_ptrc = xr.open_dataset(filename_ptrc)
       filename_chl = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_diad_T.nc'
       ds_chl = xr.open_dataset(filename_chl)
       t = 1
       year_before = year
       print(filename_ptrc)
    if year_before != year:
       filename = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_grid_T.nc'
       ds = xr.open_dataset(filename)
       filename_ptrc = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_ptrc_T.nc'
       ds_ptrc = xr.open_dataset(filename_ptrc)
       filename_chl = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_diad_T.nc'
       ds_chl = xr.open_dataset(filename_chl)
       year_before = year
       print(filename_ptrc)
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
        lat_nan = ds_ptrc.nav_lat.values * mask.values[0,0,:,:]
        lon_nan = ds_ptrc.nav_lon.values * mask.values[0,0,:,:]
        abslat = np.abs(lat_nan-lat_Tara[0])
        abslon = np.abs(lon_nan-lon_Tara[0])
        c = np.sqrt(abslon**2+abslat**2)
        xt = np.where(c == np.nanmin(c))
        print('check:', xt)
        if len(xt[0]) == 1:
           ([yloc], [xloc]) = np.where(c == np.nanmin(c))
        else:
           ([yloc], [xloc]) = (np.array([xt[0][0]]),np.array([xt[1][0]]))
        print('PlankTOM: ',ds_ptrc.nav_lat.values[yloc,xloc],ds_ptrc.nav_lon.values[yloc,xloc])
        Temp = ds.votemper[int(day)-1,:,yloc,xloc].values
        MLD  = ds.somxl030[int(day)-1,yloc,xloc].values
        O2   = ds_ptrc.O2[int(day)-1,:,yloc,xloc].values
        NO3  = ds_ptrc.NO3[int(day)-1,:,yloc,xloc].values
        Si   = ds_ptrc.Si[int(day)-1,:,yloc,xloc].values
        PO4  = ds_ptrc.PO4[int(day)-1,:,yloc,xloc].values
        BAC  = ds_ptrc.BAC[int(day)-1,:,yloc,xloc].values
        MES  = ds_ptrc.MES[int(day)-1,:,yloc,xloc].values
        PTE  = ds_ptrc.PTE[int(day)-1,:,yloc,xloc].values
        DIA  = ds_ptrc.DIA[int(day)-1,:,yloc,xloc].values
        COC  = ds_ptrc.COC[int(day)-1,:,yloc,xloc].values
        PIC  = ds_ptrc.PIC[int(day)-1,:,yloc,xloc].values
        PHA  = ds_ptrc.PHA[int(day)-1,:,yloc,xloc].values
        GEL  = ds_ptrc.GEL[int(day)-1,:,yloc,xloc].values
        PRO  = ds_ptrc.PRO[int(day)-1,:,yloc,xloc].values
        MAC  = ds_ptrc.MAC[int(day)-1,:,yloc,xloc].values
        MIX  = ds_ptrc.MIX[int(day)-1,:,yloc,xloc].values
        FIX  = ds_ptrc.FIX[int(day)-1,:,yloc,xloc].values
        CHL  = ds_chl.TChl[int(day)-1,:,yloc,xloc].values
        Temp_back = ds.votemper[int(day)-2,:,yloc,xloc].values
        O2_back   = ds_ptrc.O2[int(day)-2,:,yloc,xloc].values
        NO3_back  = ds_ptrc.NO3[int(day)-2,:,yloc,xloc].values
        Si_back   = ds_ptrc.Si[int(day)-2,:,yloc,xloc].values
        PO4_back  = ds_ptrc.PO4[int(day)-2,:,yloc,xloc].values
        BAC_back  = ds_ptrc.BAC[int(day)-2,:,yloc,xloc].values
        MES_back  = ds_ptrc.MES[int(day)-2,:,yloc,xloc].values
        PTE_back  = ds_ptrc.PTE[int(day)-2,:,yloc,xloc].values
        DIA_back  = ds_ptrc.DIA[int(day)-2,:,yloc,xloc].values
        COC_back  = ds_ptrc.COC[int(day)-2,:,yloc,xloc].values
        PIC_back  = ds_ptrc.PIC[int(day)-2,:,yloc,xloc].values
        PHA_back  = ds_ptrc.PHA[int(day)-2,:,yloc,xloc].values
        GEL_back  = ds_ptrc.GEL[int(day)-2,:,yloc,xloc].values
        PRO_back  = ds_ptrc.PRO[int(day)-2,:,yloc,xloc].values
        MAC_back  = ds_ptrc.MAC[int(day)-2,:,yloc,xloc].values
        MIX_back  = ds_ptrc.MIX[int(day)-2,:,yloc,xloc].values
        FIX_back  = ds_ptrc.FIX[int(day)-2,:,yloc,xloc].values
        CHL_back  = ds_chl.TChl[int(day)-2,:,yloc,xloc].values
        POC  = ds_ptrc.POC[int(day)-1,:,yloc,xloc].values
        GOC  = ds_ptrc.GOC[int(day)-1,:,yloc,xloc].values
        bottom = ds_bottom.bottom_depth.values[int(month)-1,yloc,xloc]
        lat_PlankTOM = ds_ptrc.nav_lat.values[yloc,xloc]
        lon_PlankTOM = ds_ptrc.nav_lon.values[yloc,xloc]
        depth_PlankTOM = ds_ptrc.deptht.values
        time_year = year
        time_month = month
        time_day = day
        item1_values = item1['depth'].values.astype(np.float)
        for ind_T in np.arange(0,len(POC),1):
            if depth_PlankTOM[ind_T] <= np.max(item1_values):
               Temp_PlankTOM_to_file.append(Temp[ind_T])
               MLD_PlankTOM_to_file.append(MLD)
               O2_PlankTOM_to_file.append(O2[ind_T])
               NO3_PlankTOM_to_file.append(NO3[ind_T])
               Si_PlankTOM_to_file.append(Si[ind_T])
               PO4_PlankTOM_to_file.append(PO4[ind_T])
               BAC_PlankTOM_to_file.append(BAC[ind_T])
               MES_PlankTOM_to_file.append(MES[ind_T])
               PTE_PlankTOM_to_file.append(PTE[ind_T])
               DIA_PlankTOM_to_file.append(DIA[ind_T])
               COC_PlankTOM_to_file.append(COC[ind_T])
               PIC_PlankTOM_to_file.append(PIC[ind_T])
               PHA_PlankTOM_to_file.append(PHA[ind_T])
               GEL_PlankTOM_to_file.append(GEL[ind_T])
               PRO_PlankTOM_to_file.append(PRO[ind_T])
               MAC_PlankTOM_to_file.append(MAC[ind_T])
               MIX_PlankTOM_to_file.append(MIX[ind_T])
               FIX_PlankTOM_to_file.append(FIX[ind_T])
               CHL_PlankTOM_to_file.append(CHL[ind_T])
               Temp_back_PlankTOM_to_file.append(Temp_back[ind_T])
               O2_back_PlankTOM_to_file.append(O2_back[ind_T])
               NO3_back_PlankTOM_to_file.append(NO3_back[ind_T])
               Si_back_PlankTOM_to_file.append(Si_back[ind_T])
               PO4_back_PlankTOM_to_file.append(PO4_back[ind_T])
               BAC_back_PlankTOM_to_file.append(BAC_back[ind_T])
               MES_back_PlankTOM_to_file.append(MES_back[ind_T])
               PTE_back_PlankTOM_to_file.append(PTE_back[ind_T])
               DIA_back_PlankTOM_to_file.append(DIA_back[ind_T])
               COC_back_PlankTOM_to_file.append(COC_back[ind_T])
               PIC_back_PlankTOM_to_file.append(PIC_back[ind_T])
               PHA_back_PlankTOM_to_file.append(PHA_back[ind_T])
               GEL_back_PlankTOM_to_file.append(GEL_back[ind_T])
               PRO_back_PlankTOM_to_file.append(PRO_back[ind_T])
               MAC_back_PlankTOM_to_file.append(MAC_back[ind_T])
               MIX_back_PlankTOM_to_file.append(MIX_back[ind_T])
               FIX_back_PlankTOM_to_file.append(FIX_back[ind_T])
               CHL_back_PlankTOM_to_file.append(CHL_back[ind_T])
               POC_PlankTOM_to_file.append(POC[ind_T])
               GOC_PlankTOM_to_file.append(GOC[ind_T])
               bottom_to_file.append(bottom)
               year_PlankTOM_to_file.append(int(year))
               month_PlankTOM_to_file.append(int(month))
               day_PlankTOM_to_file.append(int(day))
               lat_PlankTOM_to_file.append(lat_PlankTOM)
               lon_PlankTOM_to_file.append(lon_PlankTOM)
               depth_PlankTOM_to_file.append(depth_PlankTOM[ind_T])
               lat_Tara_to_file.append(lat_Tara[0])
               lon_Tara_to_file.append(lon_Tara[0])

#data into dataframe
Data_all = pd.DataFrame({'year': year_PlankTOM_to_file, 'month': month_PlankTOM_to_file,'day': day_PlankTOM_to_file, 'lat': lat_Tara_to_file, 'lon': lon_Tara_to_file, 'lat_Pl': lat_PlankTOM_to_file, 'lon_Pl': lon_PlankTOM_to_file, 'depth': depth_PlankTOM_to_file, 'Temp': Temp_PlankTOM_to_file, 'Temp_back': Temp_back_PlankTOM_to_file, 'MLD': MLD_PlankTOM_to_file, 'POC': POC_PlankTOM_to_file, 'GOC': GOC_PlankTOM_to_file, 'O2': O2_PlankTOM_to_file, 'NO3': NO3_PlankTOM_to_file, 'PO4': PO4_PlankTOM_to_file, 'Si': Si_PlankTOM_to_file, 'CHL': CHL_PlankTOM_to_file, 'BAC': BAC_PlankTOM_to_file, 'MES': MES_PlankTOM_to_file, 'PTE': PTE_PlankTOM_to_file, 'DIA': DIA_PlankTOM_to_file, 'COC': COC_PlankTOM_to_file, 'PIC': PIC_PlankTOM_to_file, 'PHA': PHA_PlankTOM_to_file, 'GEL': GEL_PlankTOM_to_file, 'PRO': PRO_PlankTOM_to_file, 'MAC': MAC_PlankTOM_to_file, 'MIX': MIX_PlankTOM_to_file, 'FIX': FIX_PlankTOM_to_file, 'O2_back': O2_back_PlankTOM_to_file, 'NO3_back': NO3_back_PlankTOM_to_file, 'PO4_back': PO4_back_PlankTOM_to_file, 'Si_back': Si_back_PlankTOM_to_file, 'CHL_back': CHL_back_PlankTOM_to_file, 'BAC_back': BAC_back_PlankTOM_to_file, 'MES_back': MES_back_PlankTOM_to_file, 'PTE_back': PTE_back_PlankTOM_to_file, 'DIA_back': DIA_back_PlankTOM_to_file, 'COC_back': COC_back_PlankTOM_to_file, 'PIC_back': PIC_back_PlankTOM_to_file, 'PHA_back': PHA_back_PlankTOM_to_file, 'GEL_back': GEL_back_PlankTOM_to_file, 'PRO_back': PRO_back_PlankTOM_to_file, 'MAC_back': MAC_back_PlankTOM_to_file, 'MIX_back': MIX_back_PlankTOM_to_file, 'FIX_back': FIX_back_PlankTOM_to_file, 'bottom': bottom_to_file}, columns=['year','month','day','lat','lon','lat_Pl','lon_Pl','depth','Temp','Temp_back','MLD','POC','GOC','O2','NO3','PO4','Si','CHL','BAC','MES','PTE','DIA','COC','PIC','PHA','GEL','PRO','MAC','MIX','FIX','O2_back','NO3_back','PO4_back','Si_back','CHL_back','BAC_back','MES_back','PTE_back','DIA_back','COC_back','PIC_back','PHA_back','GEL_back','PRO_back','MAC_back','MIX_back','FIX_back','bottom'])

#save dataframe
Data_all.to_csv('Data_Tara_Back_PlankTOMDaily_bottom_21102021.csv')
