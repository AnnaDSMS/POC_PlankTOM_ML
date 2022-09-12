#data from PlankTOM12 to reconstruct POC_S and POC_L vertical profiles over the global ocean
import numpy as np
import xarray as xr
import pandas as pd
from collections import Counter

#PlankTOM12 mask
filename_mask = 'mesh_mask3_6.nc'
ds_mask = xr.open_dataset(filename_mask)
mask = ds_mask.tmask

mask = mask.where(mask > 0.)

#main loop
for year in np.arange(2009,2014,1):
    print(year)
    Temp_PlankTOM_to_file = []
    Temp_back_PlankTOM_to_file = []
    MLD_PlankTOM_to_file = []
    year_PlankTOM_to_file = []
    month_PlankTOM_to_file = []
    lat_PlankTOM_to_file = []
    lon_PlankTOM_to_file = []
    depth_PlankTOM_to_file = []
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
    filename_bottom = 'ORCA2_1m_20110101_20111231_diad_T.nc'
    ds_bottom = xr.open_dataset(filename_bottom)
    filename = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_grid_T.nc'
    ds = xr.open_dataset(filename)
    filename_ptrc = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_ptrc_T.nc'
    ds_ptrc = xr.open_dataset(filename_ptrc)
    filename_chl = 'ORCA2_1m_'+str(year)+'0101_'+str(year)+'1231_diad_T.nc'
    ds_chl = xr.open_dataset(filename_chl)
    print(filename)
    filename_back = 'ORCA2_1m_'+str(year-1)+'0101_'+str(year-1)+'1231_grid_T.nc'
    ds_back = xr.open_dataset(filename_back)
    filename_ptrc_back = 'ORCA2_1m_'+str(year-1)+'0101_'+str(year-1)+'1231_ptrc_T.nc'
    ds_ptrc_back = xr.open_dataset(filename_ptrc_back)
    filename_chl_back = 'ORCA2_1m_'+str(year-1)+'0101_'+str(year-1)+'1231_diad_T.nc'
    ds_chl_back = xr.open_dataset(filename_chl_back)
    lat_nan = ds.nav_lat.values * mask.values[0,0,:,:]
    lon_nan = ds.nav_lon.values * mask.values[0,0,:,:]
    for i in np.arange(0,len(lat_nan),1):
        for j in np.arange(0,len(lat_nan[1]),1):
            if (np.isnan(lat_nan[i,j]) == False) and (np.isnan(lon_nan[i,j]) == False):
               Temp = ds.votemper.values[:,:,i,j] 
               MLD  = ds.somxl030.values[:,i,j]
               O2   = ds_ptrc.O2.values[:,:,i,j]
               NO3  = ds_ptrc.NO3.values[:,:,i,j]
               Si   = ds_ptrc.Si.values[:,:,i,j]
               PO4  = ds_ptrc.PO4.values[:,:,i,j]
               POC  = ds_ptrc.POC.values[:,:,i,j]
               GOC  = ds_ptrc.GOC.values[:,:,i,j]
               BAC  = ds_ptrc.BAC.values[:,:,i,j]
               MES  = ds_ptrc.MES.values[:,:,i,j]
               PTE  = ds_ptrc.PTE.values[:,:,i,j]
               DIA  = ds_ptrc.DIA.values[:,:,i,j]
               COC  = ds_ptrc.COC.values[:,:,i,j]
               PIC  = ds_ptrc.PIC.values[:,:,i,j]
               PHA  = ds_ptrc.PHA.values[:,:,i,j]
               GEL  = ds_ptrc.GEL.values[:,:,i,j]
               PRO  = ds_ptrc.PRO.values[:,:,i,j]
               MAC  = ds_ptrc.MAC.values[:,:,i,j]
               MIX  = ds_ptrc.MIX.values[:,:,i,j]
               FIX  = ds_ptrc.FIX.values[:,:,i,j]
               CHL  = ds_chl.TChl.values[:,:,i,j]
               bottom = ds_bottom.bottom_depth.values[:,i,j]
               lat_PlankTOM = ds.nav_lat.values[i,j]
               lon_PlankTOM = ds.nav_lon.values[i,j]
               depth_PlankTOM = ds.deptht.values
               for month in np.arange(1,13,1):
                   for ind_T in np.arange(0,len(Temp[month-1,:]),1):
                       if depth_PlankTOM[ind_T] <= bottom[month-1]:
                          Temp_PlankTOM_to_file.append(Temp[month-1,ind_T])
                          if month == 1:
                             Temp_back = ds_back.votemper.values[11,:,i,j]
                          else:
                             Temp_back = ds.votemper.values[month-1,:,i,j]
                          Temp_back_PlankTOM_to_file.append(Temp_back[ind_T])
                          MLD_PlankTOM_to_file.append(MLD[month-1])
                          O2_PlankTOM_to_file.append(O2[month-1,ind_T])
                          if month == 1:
                             O2_back = ds_ptrc_back.O2.values[11,:,i,j]
                          else:
                             O2_back = ds_ptrc.O2.values[month-1,:,i,j]
                          O2_back_PlankTOM_to_file.append(O2_back[ind_T])
                          NO3_PlankTOM_to_file.append(NO3[month-1,ind_T])
                          if month == 1:
                             NO3_back = ds_ptrc_back.NO3.values[11,:,i,j]
                          else:
                             NO3_back = ds_ptrc.NO3.values[month-1,:,i,j]
                          NO3_back_PlankTOM_to_file.append(NO3_back[ind_T])
                          Si_PlankTOM_to_file.append(Si[month-1,ind_T])
                          if month == 1:
                             Si_back = ds_ptrc_back.Si.values[11,:,i,j]
                          else:
                             Si_back = ds_ptrc.Si.values[month-1,:,i,j]
                          Si_back_PlankTOM_to_file.append(Si_back[ind_T])
                          PO4_PlankTOM_to_file.append(PO4[month-1,ind_T])
                          if month == 1:
                             PO4_back = ds_ptrc_back.PO4.values[11,:,i,j]
                          else:
                             PO4_back = ds_ptrc.PO4.values[month-1,:,i,j]
                          PO4_back_PlankTOM_to_file.append(PO4_back[ind_T])
                          POC_PlankTOM_to_file.append(POC[month-1,ind_T])
                          GOC_PlankTOM_to_file.append(GOC[month-1,ind_T])
                          BAC_PlankTOM_to_file.append(BAC[month-1,ind_T])
                          if month == 1:
                             BAC_back = ds_ptrc_back.BAC.values[11,:,i,j]
                          else:
                             BAC_back = ds_ptrc.BAC.values[month-1,:,i,j]
                          BAC_back_PlankTOM_to_file.append(BAC_back[ind_T])
                          MES_PlankTOM_to_file.append(MES[month-1,ind_T])
                          if month == 1:
                             MES_back = ds_ptrc_back.MES.values[11,:,i,j]
                          else:
                             MES_back = ds_ptrc.MES.values[month-1,:,i,j]
                          MES_back_PlankTOM_to_file.append(MES_back[ind_T])
                          PTE_PlankTOM_to_file.append(PTE[month-1,ind_T])
                          if month == 1:
                             PTE_back = ds_ptrc_back.PTE.values[11,:,i,j]
                          else:
                             PTE_back = ds_ptrc.PTE.values[month-1,:,i,j]
                          PTE_back_PlankTOM_to_file.append(PTE_back[ind_T])
                          DIA_PlankTOM_to_file.append(DIA[month-1,ind_T])
                          if month == 1:
                             DIA_back = ds_ptrc_back.DIA.values[11,:,i,j]
                          else:
                             DIA_back = ds_ptrc.DIA.values[month-1,:,i,j]
                          DIA_back_PlankTOM_to_file.append(DIA_back[ind_T])
                          COC_PlankTOM_to_file.append(COC[month-1,ind_T])
                          if month == 1:
                             COC_back = ds_ptrc_back.COC.values[11,:,i,j]
                          else:
                             COC_back = ds_ptrc.COC.values[month-1,:,i,j]
                          COC_back_PlankTOM_to_file.append(COC_back[ind_T])
                          PIC_PlankTOM_to_file.append(PIC[month-1,ind_T])
                          if month == 1:
                             PIC_back = ds_ptrc_back.PIC.values[11,:,i,j]
                          else:
                             PIC_back = ds_ptrc.PIC.values[month-1,:,i,j]
                          PIC_back_PlankTOM_to_file.append(PIC_back[ind_T])
                          PHA_PlankTOM_to_file.append(PHA[month-1,ind_T])
                          if month == 1:
                             PHA_back = ds_ptrc_back.PHA.values[11,:,i,j]
                          else:
                             PHA_back = ds_ptrc.PHA.values[month-1,:,i,j]
                          PHA_back_PlankTOM_to_file.append(PHA_back[ind_T])
                          GEL_PlankTOM_to_file.append(GEL[month-1,ind_T])
                          if month == 1:
                             GEL_back = ds_ptrc_back.GEL.values[11,:,i,j]
                          else:
                             GEL_back = ds_ptrc.GEL.values[month-1,:,i,j]
                          GEL_back_PlankTOM_to_file.append(GEL_back[ind_T])
                          PRO_PlankTOM_to_file.append(PRO[month-1,ind_T])
                          if month == 1:
                             PRO_back = ds_ptrc_back.PRO.values[11,:,i,j]
                          else:
                             PRO_back = ds_ptrc.PRO.values[month-1,:,i,j]
                          PRO_back_PlankTOM_to_file.append(PRO_back[ind_T])
                          MAC_PlankTOM_to_file.append(MAC[month-1,ind_T])
                          if month == 1:
                             MAC_back = ds_ptrc_back.MAC.values[11,:,i,j]
                          else:
                             MAC_back = ds_ptrc.MAC.values[month-1,:,i,j]
                          MAC_back_PlankTOM_to_file.append(MAC_back[ind_T])
                          MIX_PlankTOM_to_file.append(MIX[month-1,ind_T])
                          if month == 1:
                             MIX_back = ds_ptrc_back.MIX.values[11,:,i,j]
                          else:
                             MIX_back = ds_ptrc.MIX.values[month-1,:,i,j]
                          MIX_back_PlankTOM_to_file.append(MIX_back[ind_T])
                          FIX_PlankTOM_to_file.append(FIX[month-1,ind_T])
                          if month == 1:
                             FIX_back = ds_ptrc_back.FIX.values[11,:,i,j]
                          else:
                             FIX_back = ds_ptrc.FIX.values[month-1,:,i,j]
                          FIX_back_PlankTOM_to_file.append(FIX_back[ind_T])
                          CHL_PlankTOM_to_file.append(CHL[month-1,ind_T])
                          if month == 1:
                             CHL_back = ds_chl_back.TChl.values[11,:,i,j]
                          else:
                             CHL_back = ds_chl.TChl.values[month-1,:,i,j]
                          CHL_back_PlankTOM_to_file.append(CHL_back[ind_T])
                          bottom_to_file.append(bottom[month-1])
                          year_PlankTOM_to_file.append(int(year))
                          month_PlankTOM_to_file.append(int(month))
                          lat_PlankTOM_to_file.append(lat_PlankTOM)
                          lon_PlankTOM_to_file.append(lon_PlankTOM)
                          depth_PlankTOM_to_file.append(depth_PlankTOM[ind_T])

    Data_all = pd.DataFrame({'year': year_PlankTOM_to_file, 'month': month_PlankTOM_to_file, 'lat_Pl': lat_PlankTOM_to_file, 'lon_Pl': lon_PlankTOM_to_file, 'depth': depth_PlankTOM_to_file, 'Temp': Temp_PlankTOM_to_file, 'Temp_back': Temp_back_PlankTOM_to_file, 'MLD': MLD_PlankTOM_to_file, 'POC': POC_PlankTOM_to_file, 'GOC': GOC_PlankTOM_to_file, 'O2': O2_PlankTOM_to_file, 'O2_back': O2_back_PlankTOM_to_file, 'NO3': NO3_PlankTOM_to_file, 'NO3_back': NO3_back_PlankTOM_to_file, 'PO4': PO4_PlankTOM_to_file, 'PO4_back': PO4_back_PlankTOM_to_file, 'Si': Si_PlankTOM_to_file, 'Si_back': Si_back_PlankTOM_to_file, 'CHL': CHL_PlankTOM_to_file, 'CHL_back': CHL_back_PlankTOM_to_file, 'BAC': BAC_PlankTOM_to_file, 'BAC_back': BAC_back_PlankTOM_to_file, 'MES': MES_PlankTOM_to_file, 'MES_back': MES_back_PlankTOM_to_file, 'PTE': PTE_PlankTOM_to_file, 'PTE_back': PTE_back_PlankTOM_to_file, 'DIA': DIA_PlankTOM_to_file, 'DIA_back': DIA_back_PlankTOM_to_file, 'COC': COC_PlankTOM_to_file, 'COC_back': COC_back_PlankTOM_to_file, 'PIC': PIC_PlankTOM_to_file, 'PIC_back': PIC_back_PlankTOM_to_file, 'PHA': PHA_PlankTOM_to_file, 'PHA_back': PHA_back_PlankTOM_to_file, 'GEL': GEL_PlankTOM_to_file, 'GEL_back': GEL_back_PlankTOM_to_file, 'PRO': PRO_PlankTOM_to_file, 'PRO_back': PRO_back_PlankTOM_to_file, 'MAC': MAC_PlankTOM_to_file, 'MAC_back': MAC_back_PlankTOM_to_file, 'MIX': MIX_PlankTOM_to_file, 'MIX_back': MIX_back_PlankTOM_to_file, 'FIX': FIX_PlankTOM_to_file, 'FIX_back': FIX_back_PlankTOM_to_file, 'bottom': bottom_to_file}, columns=['year','month','lat_Pl','lon_Pl','depth','Temp','Temp_back','MLD','POC','GOC','O2','O2_back','NO3','NO3_back','PO4','PO4_back','Si','Si_back','CHL','CHL_back','BAC','BAC_back','MES','MES_back','PTE','PTE_back','DIA','DIA_back','COC','COC_back','PIC','PIC_back','PHA','PHA_back','GEL','GEL_back','PRO','PRO_back','MAC','MAC_back','MIX','MIX_back','FIX','FIX_back','bottom'])

    Data_all.to_csv('Data_ML_PlankTOM_Reconstr_'+str(year)+'_04102021.csv')



