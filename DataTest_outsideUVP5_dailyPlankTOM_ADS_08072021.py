#creation of data outside of the regions coverd by observations, based on daily PlankTOM12 outputs
import numpy as np
import xarray as xr
import pandas as pd
from collections import Counter
import random as rd

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


year_list = np.arange(2009,2014,1)

#PalnkTOM12 bathymetry
filename_bottom = 'ORCA2_1m_20110101_20111231_diad_T.nc'
ds_bottom = xr.open_dataset(filename_bottom)

#mask of PlankTOM12
filename_mask = 'mesh_mask3_6.nc'
ds_mask = xr.open_dataset(filename_mask)
mask = ds_mask.tmask

mask = mask.where(mask > 0.)

#main loop
for year in year_list:
    print(year)
    day_list = rd.sample(range(1, 365), 10)
    filename = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_grid_T.nc'
    ds = xr.open_dataset(filename)
    filename_ptrc = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_ptrc_T.nc'
    ds_ptrc = xr.open_dataset(filename_ptrc)
    filename_chl = 'ORCA2_1d_'+str(year)+'0101_'+str(year)+'1231_diad_T.nc'
    ds_chl = xr.open_dataset(filename_chl)
    filename_back = 'ORCA2_1d_'+str(year-1)+'0101_'+str(year-1)+'1231_grid_T.nc'
    ds_back = xr.open_dataset(filename_back)
    filename_ptrc_back = 'ORCA2_1d_'+str(year-1)+'0101_'+str(year-1)+'1231_ptrc_T.nc'
    ds_ptrc_back = xr.open_dataset(filename_ptrc_back)
    filename_chl_back = 'ORCA2_1d_'+str(year-1)+'0101_'+str(year-1)+'1231_diad_T.nc'
    ds_chl_back = xr.open_dataset(filename_chl_back)
    print(filename)
    for day in day_list:
        zone = 0
        time_index = int(day) - 1
        for zone in np.arange(0,4,1):
            if zone == 0:
               lat_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(0., 20.), 2)
                   lat_array.append(x)
               lon_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(-50., -10.), 2)     
                   lon_array.append(x)
            if zone == 1:
               lat_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(-60., -20.), 2)
                   lat_array.append(x)
               lon_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(70., 110.), 2)
                   lon_array.append(x)
            if zone == 2:
               lat_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(0., 40.), 2)
                   lat_array.append(x)
               lon_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(130., 170.), 2)
                   lon_array.append(x)
            if zone == 3:
               lat_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(-60., -20.), 2)
                   lat_array.append(x)
               lon_array = []
               for i in range(0, 6):
                   x = round(rd.uniform(-170., -150.), 2)
                   lon_array.append(x)
            for ij in np.arange(0,6,1):
                lat_test = lat_array[ij]
                lon_test = lon_array[ij]
                lat_nan = ds.nav_lat.values
                lon_nan = ds.nav_lon.values
                lat_nan = ds.nav_lat.values * mask.values[0,0,:,:]
                lon_nan = ds.nav_lon.values * mask.values[0,0,:,:]
                abslat = np.abs(lat_nan-lat_test)
                abslon = np.abs(lon_nan-lon_test)
                c = np.sqrt(abslon**2+abslat**2)
                xt = np.where(c == np.nanmin(c))
                if len(xt[0]) == 1:
                   ([yloc], [xloc]) = np.where(c == np.nanmin(c))
                else:
                   ([yloc], [xloc]) = (np.array([xt[0][0]]),np.array([xt[1][0]]))
                Temp = ds.votemper[time_index,:,yloc,xloc].values 
                MLD  = ds.somxl030[time_index,yloc,xloc].values
                O2   = ds_ptrc.O2[time_index,:,yloc,xloc].values
                NO3  = ds_ptrc.NO3[time_index,:,yloc,xloc].values
                Si   = ds_ptrc.Si[time_index,:,yloc,xloc].values
                PO4  = ds_ptrc.PO4[time_index,:,yloc,xloc].values
                BAC  = ds_ptrc.BAC[time_index,:,yloc,xloc].values
                MES  = ds_ptrc.MES[time_index,:,yloc,xloc].values
                PTE  = ds_ptrc.PTE[time_index,:,yloc,xloc].values
                DIA  = ds_ptrc.DIA[time_index,:,yloc,xloc].values
                COC  = ds_ptrc.COC[time_index,:,yloc,xloc].values
                PIC  = ds_ptrc.PIC[time_index,:,yloc,xloc].values
                PHA  = ds_ptrc.PHA[time_index,:,yloc,xloc].values
                GEL  = ds_ptrc.GEL[time_index,:,yloc,xloc].values
                PRO  = ds_ptrc.PRO[time_index,:,yloc,xloc].values
                MAC  = ds_ptrc.MAC[time_index,:,yloc,xloc].values
                MIX  = ds_ptrc.MIX[time_index,:,yloc,xloc].values
                FIX  = ds_ptrc.FIX[time_index,:,yloc,xloc].values
                CHL  = ds_chl.TChl[time_index,:,yloc,xloc].values
                if time_index > 0:
                   Temp_back = ds.votemper[time_index-1,:,yloc,xloc].values
                   O2_back = ds_ptrc.O2[time_index-1,:,yloc,xloc].values
                   NO3_back = ds_ptrc.NO3[time_index-1,:,yloc,xloc].values
                   Si_back = ds_ptrc.Si[time_index-1,:,yloc,xloc].values
                   PO4_back = ds_ptrc.PO4[time_index-1,:,yloc,xloc].values
                   BAC_back = ds_ptrc.BAC[time_index-1,:,yloc,xloc].values
                   MES_back = ds_ptrc.MES[time_index-1,:,yloc,xloc].values
                   PTE_back = ds_ptrc.PTE[time_index-1,:,yloc,xloc].values
                   DIA_back = ds_ptrc.DIA[time_index-1,:,yloc,xloc].values
                   COC_back = ds_ptrc.COC[time_index-1,:,yloc,xloc].values
                   PIC_back = ds_ptrc.PIC[time_index-1,:,yloc,xloc].values
                   PHA_back = ds_ptrc.PHA[time_index-1,:,yloc,xloc].values
                   GEL_back = ds_ptrc.GEL[time_index-1,:,yloc,xloc].values
                   PRO_back = ds_ptrc.PRO[time_index-1,:,yloc,xloc].values
                   MAC_back = ds_ptrc.MAC[time_index-1,:,yloc,xloc].values
                   MIX_back = ds_ptrc.MIX[time_index-1,:,yloc,xloc].values
                   FIX_back = ds_ptrc.FIX[time_index-1,:,yloc,xloc].values
                   CHL_back  = ds_chl_back.TChl[time_index-1,:,yloc,xloc].values
                if time_index == 0:
                   Temp_back = ds_back.votemper[len(ds_back.votemper.values)-1,:,yloc,xloc].values
                   O2_back = ds_ptrc_back.O2[len(ds_ptrc_back.O2.values)-1,:,yloc,xloc].values
                   NO3_back = ds_ptrc_back.NO3[len(ds_ptrc_back.NO3.values)-1,:,yloc,xloc].values
                   Si_back = ds_ptrc_back.Si[len(ds_ptrc_back.Si.values),:,yloc,xloc].values
                   PO4_back = ds_ptrc_back.PO4[len(ds_ptrc_back.PO4.values),:,yloc,xloc].values
                   BAC_back = ds_ptrc_back.BAC[len(ds_ptrc_back.BAC.values),:,yloc,xloc].values
                   MES_back = ds_ptrc_back.MES[len(ds_ptrc_back.MES.values),:,yloc,xloc].values
                   PTE_back = ds_ptrc_back.PTE[len(ds_ptrc_back.PTE.values),:,yloc,xloc].values
                   DIA_back = ds_ptrc_back.DIA[len(ds_ptrc_back.DIA.values),:,yloc,xloc].values
                   COC_back = ds_ptrc_back.COC[len(ds_ptrc_back.COC.values),:,yloc,xloc].values
                   PIC_back = ds_ptrc_back.PIC[len(ds_ptrc_back.PIC.values),:,yloc,xloc].values
                   PHA_back = ds_ptrc_back.PHA[len(ds_ptrc_back.PHA.values),:,yloc,xloc].values
                   GEL_back = ds_ptrc_back.GEL[len(ds_ptrc_back.GEL.values),:,yloc,xloc].values
                   PRO_back = ds_ptrc_back.PRO[len(ds_ptrc_back.PRO.values),:,yloc,xloc].values
                   MAC_back = ds_ptrc_back.MAC[len(ds_ptrc_back.MAC.values),:,yloc,xloc].values
                   MIX_back = ds_ptrc_back.MIX[len(ds_ptrc_back.MIX.values),:,yloc,xloc].values
                   FIX_back = ds_ptrc_back.FIX[len(ds_ptrc_back.FIX.values),:,yloc,xloc].values
                   CHL_back = ds_chl_back.TChl[len(ds_chl_back.TChl.values),:,yloc,xloc].values
                POC  = ds_ptrc.POC[time_index,:,yloc,xloc].values
                GOC  = ds_ptrc.GOC[time_index,:,yloc,xloc].values
                lat_PlankTOM = ds.nav_lat[yloc,xloc].values
                lon_PlankTOM = ds.nav_lon[yloc,xloc].values
                depth_PlankTOM = ds.deptht.values
                time_year = year
                if time_index < 31:
                   month = 1
                if (time_index >= 31) & (time_index < 59):
                   month = 2
                if (time_index >= 59) & (time_index < 90):
                   month = 3
                if (time_index >= 90) & (time_index < 120):
                   month = 4
                if (time_index >= 120) & (time_index < 151):
                   month = 5
                if (time_index >= 151) & (time_index < 181):
                   month = 6
                if (time_index >= 181) & (time_index < 212):
                   month = 7
                if (time_index >= 212) & (time_index < 243):
                   month = 8
                if (time_index >= 243) & (time_index < 273):
                   month = 9
                if (time_index >= 273) & (time_index < 304):
                   month = 10
                if (time_index >= 304) & (time_index < 334):
                   month = 11
                if (time_index >= 334) & (time_index < 365):
                   month = 12
                time_month = month
                time_day = day
                bottom = ds_bottom.bottom_depth[month-1,yloc,xloc].values
                for ind_T in np.arange(0,len(Temp),1):
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
                    year_PlankTOM_to_file.append(int(year))
                    month_PlankTOM_to_file.append(int(month))
                    day_PlankTOM_to_file.append(int(day))
                    lat_PlankTOM_to_file.append(lat_PlankTOM)
                    lon_PlankTOM_to_file.append(lon_PlankTOM)
                    depth_PlankTOM_to_file.append(depth_PlankTOM[ind_T])
                    lat_Tara_to_file.append(lat_test)
                    lon_Tara_to_file.append(lon_test)
                    bottom_to_file.append(bottom)

#data into dataframe
Data_all = pd.DataFrame({'year': year_PlankTOM_to_file, 'month': month_PlankTOM_to_file,'day': day_PlankTOM_to_file, 'lat': lat_Tara_to_file, 'lon': lon_Tara_to_file, 'lat_Pl': lat_PlankTOM_to_file, 'lon_Pl': lon_PlankTOM_to_file, 'depth': depth_PlankTOM_to_file, 'Temp': Temp_PlankTOM_to_file, 'Temp_back': Temp_back_PlankTOM_to_file, 'MLD': MLD_PlankTOM_to_file, 'POC': POC_PlankTOM_to_file, 'GOC': GOC_PlankTOM_to_file, 'O2': O2_PlankTOM_to_file, 'NO3': NO3_PlankTOM_to_file, 'PO4': PO4_PlankTOM_to_file, 'Si': Si_PlankTOM_to_file, 'CHL': CHL_PlankTOM_to_file, 'BAC': BAC_PlankTOM_to_file, 'MES': MES_PlankTOM_to_file, 'PTE': PTE_PlankTOM_to_file, 'DIA': DIA_PlankTOM_to_file, 'COC': COC_PlankTOM_to_file, 'PIC': PIC_PlankTOM_to_file, 'PHA': PHA_PlankTOM_to_file, 'GEL': GEL_PlankTOM_to_file, 'PRO': PRO_PlankTOM_to_file, 'MAC': MAC_PlankTOM_to_file, 'MIX': MIX_PlankTOM_to_file, 'FIX': FIX_PlankTOM_to_file, 'O2_back': O2_back_PlankTOM_to_file, 'NO3_back': NO3_back_PlankTOM_to_file, 'PO4_back': PO4_back_PlankTOM_to_file, 'Si_back': Si_back_PlankTOM_to_file, 'CHL_back': CHL_back_PlankTOM_to_file, 'BAC_back': BAC_back_PlankTOM_to_file, 'MES_back': MES_back_PlankTOM_to_file, 'PTE_back': PTE_back_PlankTOM_to_file, 'DIA_back': DIA_back_PlankTOM_to_file, 'COC_back': COC_back_PlankTOM_to_file, 'PIC_back': PIC_back_PlankTOM_to_file, 'PHA_back': PHA_back_PlankTOM_to_file, 'GEL_back': GEL_back_PlankTOM_to_file, 'PRO_back': PRO_back_PlankTOM_to_file, 'MAC_back': MAC_back_PlankTOM_to_file, 'MIX_back': MIX_back_PlankTOM_to_file, 'FIX_back': FIX_back_PlankTOM_to_file, 'bottom': bottom_to_file}, columns=['year','month','day','lat','lon','lat_Pl','lon_Pl','depth','Temp','Temp_back','MLD','POC','GOC','O2','NO3','PO4','Si','CHL','BAC','MES','PTE','DIA','COC','PIC','PHA','GEL','PRO','MAC','MIX','FIX','O2_back','NO3_back','PO4_back','Si_back','CHL_back','BAC_back','MES_back','PTE_back','DIA_back','COC_back','PIC_back','PHA_back','GEL_back','PRO_back','MAC_back','MIX_back','FIX_back','bottom'])

#save dataframe
Data_all.to_csv('Data_ML_PlankTOM_All_Daily_Validation_03112021.csv')




