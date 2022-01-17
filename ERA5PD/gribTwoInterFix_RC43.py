
# Imported modules
import os
import pygrib
import numpy as np
import pywinter.winter as pyw


# Input parameters
in_grib_path = '/project/p/peltier/mahdinia/MY_DATA/ERA5_NA_DATA/Data/Split_Data_Files/Compressed/'  # grib files' path.
inter_path = '/scratch/p/peltier/mahdinia/WRF4.3_Verification_Runs/ERA5_RC43/'                       # Intermediate files' path.
in_pl_int_prefix = 'ATM'                                                                             # Input PL intermediate file prefix.      
out_pl_int_prefix = 'ATM-F'                                                                          # Output PL intermediate file prefix.  
in_sl_int_prefix = 'SUR'                                                                             # Input SL intermediate file prefix.      
out_sl_int_prefix = 'SUR-F'                                                                          # Output SL intermediate file prefix. 
fill_missing = -1E30                                                                                 # Value to put for SEAICE missing vals. 
inter_times = ['1979-01-25_00',
               '1979-01-25_03',
               '1979-01-25_06',
               '1979-01-25_09',
               '1979-01-25_12',
               '1979-01-25_15',
               '1979-01-25_18',
               '1979-01-25_21',
               '1979-01-26_00',
               '1979-01-26_03',
               '1979-01-26_06',
               '1979-01-26_09',
               '1979-01-26_12',
               '1979-01-26_15',
               '1979-01-26_18',
               '1979-01-26_21',
               '1979-01-27_00',
               '1979-01-27_03',
               '1979-01-27_06',
               '1979-01-27_09',
               '1979-01-27_12',
               '1979-01-27_15',
               '1979-01-27_18',
               '1979-01-27_21',
               '1979-01-28_00',
               '1979-01-28_03',
               '1979-01-28_06',
               '1979-01-28_09',
               '1979-01-28_12',
               '1979-01-28_15',
               '1979-01-28_18',
               '1979-01-28_21',
               '1979-01-29_00',
               '1979-01-29_03',
               '1979-01-29_06',
               '1979-01-29_09',
               '1979-01-29_12',
               '1979-01-29_15',
               '1979-01-29_18',
               '1979-01-29_21',
               '1979-01-30_00',
               '1979-01-30_03',
               '1979-01-30_06',
               '1979-01-30_09',
               '1979-01-30_12',
               '1979-01-30_15',
               '1979-01-30_18',
               '1979-01-30_21',
               '1979-01-31_00',
               '1979-01-31_03',
               '1979-01-31_06',
               '1979-01-31_09',
               '1979-01-31_12',
               '1979-01-31_15',
               '1979-01-31_18',
               '1979-01-31_21',
               '1979-02-01_00',
               '1979-02-01_03',
               '1979-02-01_06',
               '1979-02-01_09',
               '1979-02-01_12',
               '1979-02-01_15',
               '1979-02-01_18',
               '1979-02-01_21',
               '1979-02-02_00',
               '1979-02-02_03',
               '1979-02-02_06',
               '1979-02-02_09',
               '1979-02-02_12',
               '1979-02-02_15',
               '1979-02-02_18',
               '1979-02-02_21',
               '1979-02-03_00',
               '1979-02-03_03',
               '1979-02-03_06',
               '1979-02-03_09',
               '1979-02-03_12',
               '1979-02-03_15',
               '1979-02-03_18',
               '1979-02-03_21',
               '1979-02-04_00',
               '1979-02-04_03',
               '1979-02-04_06',
               '1979-02-04_09',
               '1979-02-04_12',
               '1979-02-04_15',
               '1979-02-04_18',
               '1979-02-04_21',
               '1979-02-05_00',
               '1979-02-05_03',
               '1979-02-05_06',
               '1979-02-05_09',
               '1979-02-05_12',
               '1979-02-05_15',
               '1979-02-05_18',
               '1979-02-05_21',
               '1979-02-06_00',
               '1979-02-06_03',
               '1979-02-06_06',
               '1979-02-06_09',
               '1979-02-06_12',
               '1979-02-06_15',
               '1979-02-06_18',
               '1979-02-06_21',
               '1979-02-07_00',
               '1979-02-07_03',
               '1979-02-07_06',
               '1979-02-07_09',
               '1979-02-07_12',
               '1979-02-07_15',
               '1979-02-07_18',
               '1979-02-07_21',
               ]                                                # Intermediate files' times. 
in_pl_grib_files = ['ERA5-197901250000-pl.grib',
                    'ERA5-197901250300-pl.grib',
                    'ERA5-197901250600-pl.grib',
                    'ERA5-197901250900-pl.grib',
                    'ERA5-197901251200-pl.grib',
                    'ERA5-197901251500-pl.grib',
                    'ERA5-197901251800-pl.grib',
                    'ERA5-197901252100-pl.grib',
                    'ERA5-197901260000-pl.grib',
                    'ERA5-197901260300-pl.grib',
                    'ERA5-197901260600-pl.grib',
                    'ERA5-197901260900-pl.grib',
                    'ERA5-197901261200-pl.grib',
                    'ERA5-197901261500-pl.grib',
                    'ERA5-197901261800-pl.grib',
                    'ERA5-197901262100-pl.grib',
                    'ERA5-197901270000-pl.grib',
                    'ERA5-197901270300-pl.grib',
                    'ERA5-197901270600-pl.grib',
                    'ERA5-197901270900-pl.grib',
                    'ERA5-197901271200-pl.grib',
                    'ERA5-197901271500-pl.grib',
                    'ERA5-197901271800-pl.grib',
                    'ERA5-197901272100-pl.grib',
                    'ERA5-197901280000-pl.grib',
                    'ERA5-197901280300-pl.grib',
                    'ERA5-197901280600-pl.grib',
                    'ERA5-197901280900-pl.grib',
                    'ERA5-197901281200-pl.grib',
                    'ERA5-197901281500-pl.grib',
                    'ERA5-197901281800-pl.grib',
                    'ERA5-197901282100-pl.grib',
                    'ERA5-197901290000-pl.grib',
                    'ERA5-197901290300-pl.grib',
                    'ERA5-197901290600-pl.grib',
                    'ERA5-197901290900-pl.grib',
                    'ERA5-197901291200-pl.grib',
                    'ERA5-197901291500-pl.grib',
                    'ERA5-197901291800-pl.grib',
                    'ERA5-197901292100-pl.grib',
                    'ERA5-197901300000-pl.grib',
                    'ERA5-197901300300-pl.grib',
                    'ERA5-197901300600-pl.grib',
                    'ERA5-197901300900-pl.grib',
                    'ERA5-197901301200-pl.grib',
                    'ERA5-197901301500-pl.grib',
                    'ERA5-197901301800-pl.grib',
                    'ERA5-197901302100-pl.grib',
                    'ERA5-197901310000-pl.grib',
                    'ERA5-197901310300-pl.grib',
                    'ERA5-197901310600-pl.grib',
                    'ERA5-197901310900-pl.grib',
                    'ERA5-197901311200-pl.grib',
                    'ERA5-197901311500-pl.grib',
                    'ERA5-197901311800-pl.grib',
                    'ERA5-197901312100-pl.grib',
                    'ERA5-197902010000-pl.grib',
                    'ERA5-197902010300-pl.grib',
                    'ERA5-197902010600-pl.grib',
                    'ERA5-197902010900-pl.grib',
                    'ERA5-197902011200-pl.grib',
                    'ERA5-197902011500-pl.grib',
                    'ERA5-197902011800-pl.grib',
                    'ERA5-197902012100-pl.grib',
                    'ERA5-197902020000-pl.grib',
                    'ERA5-197902020300-pl.grib',
                    'ERA5-197902020600-pl.grib',
                    'ERA5-197902020900-pl.grib',
                    'ERA5-197902021200-pl.grib',
                    'ERA5-197902021500-pl.grib',
                    'ERA5-197902021800-pl.grib',
                    'ERA5-197902022100-pl.grib',
                    'ERA5-197902030000-pl.grib',
                    'ERA5-197902030300-pl.grib',
                    'ERA5-197902030600-pl.grib',
                    'ERA5-197902030900-pl.grib',
                    'ERA5-197902031200-pl.grib',
                    'ERA5-197902031500-pl.grib',
                    'ERA5-197902031800-pl.grib',
                    'ERA5-197902032100-pl.grib',
                    'ERA5-197902040000-pl.grib',
                    'ERA5-197902040300-pl.grib',
                    'ERA5-197902040600-pl.grib',
                    'ERA5-197902040900-pl.grib',
                    'ERA5-197902041200-pl.grib',
                    'ERA5-197902041500-pl.grib',
                    'ERA5-197902041800-pl.grib',
                    'ERA5-197902042100-pl.grib',
                    'ERA5-197902050000-pl.grib',
                    'ERA5-197902050300-pl.grib',
                    'ERA5-197902050600-pl.grib',
                    'ERA5-197902050900-pl.grib',
                    'ERA5-197902051200-pl.grib',
                    'ERA5-197902051500-pl.grib',
                    'ERA5-197902051800-pl.grib',
                    'ERA5-197902052100-pl.grib',
                    'ERA5-197902060000-pl.grib',
                    'ERA5-197902060300-pl.grib',
                    'ERA5-197902060600-pl.grib',
                    'ERA5-197902060900-pl.grib',
                    'ERA5-197902061200-pl.grib',
                    'ERA5-197902061500-pl.grib',
                    'ERA5-197902061800-pl.grib',
                    'ERA5-197902062100-pl.grib',
                    'ERA5-197902070000-pl.grib',
                    'ERA5-197902070300-pl.grib',
                    'ERA5-197902070600-pl.grib',
                    'ERA5-197902070900-pl.grib',
                    'ERA5-197902071200-pl.grib',
                    'ERA5-197902071500-pl.grib',
                    'ERA5-197902071800-pl.grib',
                    'ERA5-197902072100-pl.grib']                        # PL grib2 files' names.
in_sl_grib_files = ['ERA5-197901250000-sl.grib',
                    'ERA5-197901250300-sl.grib',
                    'ERA5-197901250600-sl.grib',
                    'ERA5-197901250900-sl.grib',
                    'ERA5-197901251200-sl.grib',
                    'ERA5-197901251500-sl.grib',
                    'ERA5-197901251800-sl.grib',
                    'ERA5-197901252100-sl.grib',
                    'ERA5-197901260000-sl.grib',
                    'ERA5-197901260300-sl.grib',
                    'ERA5-197901260600-sl.grib',
                    'ERA5-197901260900-sl.grib',
                    'ERA5-197901261200-sl.grib',
                    'ERA5-197901261500-sl.grib',
                    'ERA5-197901261800-sl.grib',
                    'ERA5-197901262100-sl.grib',
                    'ERA5-197901270000-sl.grib',
                    'ERA5-197901270300-sl.grib',
                    'ERA5-197901270600-sl.grib',
                    'ERA5-197901270900-sl.grib',
                    'ERA5-197901271200-sl.grib',
                    'ERA5-197901271500-sl.grib',
                    'ERA5-197901271800-sl.grib',
                    'ERA5-197901272100-sl.grib',
                    'ERA5-197901280000-sl.grib',
                    'ERA5-197901280300-sl.grib',
                    'ERA5-197901280600-sl.grib',
                    'ERA5-197901280900-sl.grib',
                    'ERA5-197901281200-sl.grib',
                    'ERA5-197901281500-sl.grib',
                    'ERA5-197901281800-sl.grib',
                    'ERA5-197901282100-sl.grib',
                    'ERA5-197901290000-sl.grib',
                    'ERA5-197901290300-sl.grib',
                    'ERA5-197901290600-sl.grib',
                    'ERA5-197901290900-sl.grib',
                    'ERA5-197901291200-sl.grib',
                    'ERA5-197901291500-sl.grib',
                    'ERA5-197901291800-sl.grib',
                    'ERA5-197901292100-sl.grib',
                    'ERA5-197901300000-sl.grib',
                    'ERA5-197901300300-sl.grib',
                    'ERA5-197901300600-sl.grib',
                    'ERA5-197901300900-sl.grib',
                    'ERA5-197901301200-sl.grib',
                    'ERA5-197901301500-sl.grib',
                    'ERA5-197901301800-sl.grib',
                    'ERA5-197901302100-sl.grib',
                    'ERA5-197901310000-sl.grib',
                    'ERA5-197901310300-sl.grib',
                    'ERA5-197901310600-sl.grib',
                    'ERA5-197901310900-sl.grib',
                    'ERA5-197901311200-sl.grib',
                    'ERA5-197901311500-sl.grib',
                    'ERA5-197901311800-sl.grib',
                    'ERA5-197901312100-sl.grib',
                    'ERA5-197902010000-sl.grib',
                    'ERA5-197902010300-sl.grib',
                    'ERA5-197902010600-sl.grib',
                    'ERA5-197902010900-sl.grib',
                    'ERA5-197902011200-sl.grib',
                    'ERA5-197902011500-sl.grib',
                    'ERA5-197902011800-sl.grib',
                    'ERA5-197902012100-sl.grib',
                    'ERA5-197902020000-sl.grib',
                    'ERA5-197902020300-sl.grib',
                    'ERA5-197902020600-sl.grib',
                    'ERA5-197902020900-sl.grib',
                    'ERA5-197902021200-sl.grib',
                    'ERA5-197902021500-sl.grib',
                    'ERA5-197902021800-sl.grib',
                    'ERA5-197902022100-sl.grib',
                    'ERA5-197902030000-sl.grib',
                    'ERA5-197902030300-sl.grib',
                    'ERA5-197902030600-sl.grib',
                    'ERA5-197902030900-sl.grib',
                    'ERA5-197902031200-sl.grib',
                    'ERA5-197902031500-sl.grib',
                    'ERA5-197902031800-sl.grib',
                    'ERA5-197902032100-sl.grib',
                    'ERA5-197902040000-sl.grib',
                    'ERA5-197902040300-sl.grib',
                    'ERA5-197902040600-sl.grib',
                    'ERA5-197902040900-sl.grib',
                    'ERA5-197902041200-sl.grib',
                    'ERA5-197902041500-sl.grib',
                    'ERA5-197902041800-sl.grib',
                    'ERA5-197902042100-sl.grib',
                    'ERA5-197902050000-sl.grib',
                    'ERA5-197902050300-sl.grib',
                    'ERA5-197902050600-sl.grib',
                    'ERA5-197902050900-sl.grib',
                    'ERA5-197902051200-sl.grib',
                    'ERA5-197902051500-sl.grib',
                    'ERA5-197902051800-sl.grib',
                    'ERA5-197902052100-sl.grib',
                    'ERA5-197902060000-sl.grib',
                    'ERA5-197902060300-sl.grib',
                    'ERA5-197902060600-sl.grib',
                    'ERA5-197902060900-sl.grib',
                    'ERA5-197902061200-sl.grib',
                    'ERA5-197902061500-sl.grib',
                    'ERA5-197902061800-sl.grib',
                    'ERA5-197902062100-sl.grib',
                    'ERA5-197902070000-sl.grib',
                    'ERA5-197902070300-sl.grib',
                    'ERA5-197902070600-sl.grib',
                    'ERA5-197902070900-sl.grib',
                    'ERA5-197902071200-sl.grib',
                    'ERA5-197902071500-sl.grib',
                    'ERA5-197902071800-sl.grib',
                    'ERA5-197902072100-sl.grib']                        # SL grib2 files' names. 
pressure_levels = np.array([100000.,  97500.,  95000.,  92500.,  90000.,  \
    87500.,  85000.,  82500.,  80000., 77500.,  75000.,  70000.,  65000., \
    60000.,  55000.,  50000.,  45000.,  40000.,  35000.,  30000., 25000., \
    22500.,  20000.,  17500.,  15000.,  12500.,  10000.,  7000.,   5000., \
    3000.,   2000.,   1000.,    700.,    500.,  300.,    200.,  100.])         # Grib pressure levels.                               
sl_layers = ['000007', '007028', '028100', '100289']                           # 3D soil layers.
FIX_IM_LATLONS = True                                                          # To fix IM lats and lons or not.
[stlat_a, stlon_a] = [86.95000457763672, -199.20001220703125]                  # Correct (grib1) IM stlat and stlon.   

# NOTE: How do we get FIX_IM_LATLONS_VALS? ?????
                       
                        
# Clear screen
os.system('clear')


# Check if the number of grib2 PL and SL files and intermediate files is the same
if (len(in_pl_grib_files)!=len(in_sl_grib_files)):
    raise ValueError("len(in_pl_grib_files)~=len(in_sl_grib_files). "
            "There should be same number of grib2 PL and SL files.") 
if (len(in_pl_grib_files)!=len(inter_times)):
    raise ValueError("len(in_pl_grib_files)~=len(inter_times). "
            "There should be same number of PL grib2 and intermediate files.") 

                      
# Number of files    
N = len(in_pl_grib_files)


# Form input intermediate files' names
in_pl_inter_files = []
for t in inter_times:
    in_pl_inter_files.append(in_pl_int_prefix+":"+t)
in_sl_inter_files = []
for t in inter_times:
    in_sl_inter_files.append(in_sl_int_prefix+":"+t)


# Form complete in_grib and in_inter file path+names
in_pl_grib_files_c = []
for file in in_pl_grib_files:
    in_pl_grib_files_c.append(in_grib_path+file)    
in_sl_grib_files_c = []
for file in in_sl_grib_files:
    in_sl_grib_files_c.append(in_grib_path+file)        
in_pl_inter_files_c = []
for file in in_pl_inter_files:
    in_pl_inter_files_c.append(inter_path+file) 
in_sl_inter_files_c = []
for file in in_sl_inter_files:
    in_sl_inter_files_c.append(inter_path+file) 
    
 
# Fixing PL data, if needed
if (FIX_IM_LATLONS==True):

    # Prompting on screen
    print('\n******************************************************************') 
    print('******************************************************************')
    print('********************** Processing PL data ************************')
    print('******************************************************************')
    print('******************************************************************\n')
 
    # Process all files
    for i in np.arange(N):

        # Open grib2 IM file
        interf = pyw.rinter(in_pl_inter_files_c[i])         

        # Print all IM file keys and some other info (only i=0)
        if (i==0):
            print('==================================================================')
            print('=============== Some info from first grib2 IM file ===============')
            print('==================================================================')
            print('Keys =',interf.keys())
            print(interf['RH'].general)
            print(interf['TT'].general)
            print(interf['UU'].general)
            print(interf['GHT'].general)
            print(interf['VV'].general,'\n')
    
        # stlat, stlon, dlat and dlon (only i=0)
        if (i==0):
            stlat = interf['UU'].geoinfo['STARTLAT']
            stlon = interf['UU'].geoinfo['STARTLON']
            dlat = interf['UU'].geoinfo['DELTALAT']
            dlon = interf['UU'].geoinfo['DELTALON']  
        
        # Prompting on screen (only i=0):
        if (i==0):    
            print('==================================================================')
            print('======================== Fixing PL data ==========================')
            print('==================================================================')    
    
        # Fix stlat and stlon values, if needed 
        if ((stlat!=stlat_a) or (stlon!=stlon_a)):
            stlat = stlat_a
            stlon = stlon_a
            print('stlat,stlon != stlat_a.stlon_a, so fixed the values!')   
        
        # Setup geo
        geo = pyw.Geo0(stlat,stlon,dlat,dlon)
    
        # Gather non-soil variables
        tt = pyw.V3dp('TT',interf['TT'].val,pressure_levels)
        uu = pyw.V3dp('UU',interf['UU'].val,pressure_levels)
        ght = pyw.V3dp('GHT',interf['GHT'].val,pressure_levels)
        vv = pyw.V3dp('VV',interf['VV'].val,pressure_levels)
        rh = pyw.V3dp('RH',interf['RH'].val,pressure_levels)

        # Listing fields
        total_fields = [tt,uu,ght,vv,rh]

        # Writing output intermediate file
        pyw.cinter(out_pl_int_prefix,inter_times[i],geo,total_fields,inter_path)

    # Move on to next line 
    print('') 

  
# Prompting on screen
print('\n******************************************************************') 
print('******************************************************************')
print('********************** Processing SL data ************************')
print('******************************************************************')
print('******************************************************************\n') 
     
# Process all files
for i in np.arange(N):

    # Open grib2 SL IM file & read seaice values
    interf = pyw.rinter(in_sl_inter_files_c[i])
    interV = interf['SEAICE'].val    

    # Open grib2 SL file & read seaice values
    grbs = pygrib.open(in_sl_grib_files_c[i])
    grb = grbs.select(name='Sea ice area fraction')[0]
    grbV = grb.values
    
    # Check if arrays are the same shape
    if (interV.shape!=grbV.shape):
        raise ValueError("interV.shape!=grbV.shape. "
            "grib2 and intermediate SL arrays should be the same size.")         

    # Print all IM file keys and some other info (only i=0)
    if (i==0):
        print('==================================================================')
        print('============== Some info from first grib2 & IM files =============')
        print('==================================================================')
        print('interV.shape = ',interV.shape)
        print('grbV.shape = ',grbV.shape)
        print('Keys =',interf.keys())
        print(interf['PSFC'].general)
        print(interf['PMSL'].general)
        print(interf['SKINTEMP'].general)
        print(interf['SST'].general)
        print(interf['TT2M'].general)
        print(interf['DEWPT'].general)
        print(interf['UU10M'].general)
        print(interf['VV10M'].general)
        print(interf['LANDSEA'].general)
        print(interf['SNOWH'].general)
        print(interf['SEAICE'].general)
        print(interf['SNOW'].general)
        print(interf['RH2M'].general)
        print(interf['ST'].general)
        print(interf['SM'].general)
        print('ST levels =',interf['ST'].level)
        print('SM levels =',interf['SM'].level,'\n')

    # stlat, stlon, dlat and dlon (only i=0)
    if (i==0):
        stlat = interf['PSFC'].geoinfo['STARTLAT']
        stlon = interf['PSFC'].geoinfo['STARTLON']
        dlat = interf['PSFC'].geoinfo['DELTALAT']
        dlon = interf['PSFC'].geoinfo['DELTALON']

    # Prompting on screen (only i=0):
    if (i==0):    
        print('==================================================================')
        print('======================== Fixing SL data ==========================')
        print('==================================================================')

    # Fix stlat and stlon values, if needed 
    if ((FIX_IM_LATLONS==True) and ((stlat!=stlat_a) or (stlon!=stlon_a))):
        stlat = stlat_a
        stlon = stlon_a
        print('stlat,stlon != stlat_a.stlon_a, so fixed the values!') 

    # Setup geo
    geo = pyw.Geo0(stlat,stlon,dlat,dlon)

    # Fix SEAICE values
    CICE = np.array(interf['SEAICE'].val, copy=True) 
    CICE[grbV.mask==True] = fill_missing

    # Gather non-soil variables
    psfc = pyw.V2d('PSFC',interf['PSFC'].val,'Surface Pressure','Pa','200100')
    pmsl = pyw.V2d('PMSL',interf['PMSL'].val,'Sea-level Pressure','Pa','201300')
    skintemp = pyw.V2d('SKINTEMP',interf['SKINTEMP'].val,'Sea-Surface Temperature','K','200100')
    sst = pyw.V2d('SST',interf['SST'].val,'Sea-Surface Temperature','K','200100')
    tt2m = pyw.V2d('TT',interf['TT2M'].val,'Temperature','K','200100')
    dewpt = pyw.V2d('DEWPT',interf['DEWPT'].val,'At 2 m','K','200100')
    uu10m = pyw.V2d('UU',interf['UU10M'].val,'U','m s-1','200100')
    vv10m = pyw.V2d('VV',interf['VV10M'].val,'V','m s-1','200100')
    landsea = pyw.V2d('LANDSEA',interf['LANDSEA'].val,'Land/Sea flag','0/1 Flag','200100')
    snowh = pyw.V2d('SNOWH',interf['SNOWH'].val,'Physical Snow Depth','m','200100')
    seaice = pyw.V2d('SEAICE',CICE,'Sea-Ice Fraction','fraction','200100')
    snow = pyw.V2d('SNOW',interf['SNOW'].val,'Water Equivalent of Accumulated Snow Depth','kg m-2','200100')
    rh2m = pyw.V2d('RH',interf['RH2M'].val,'Relative Humidity','%','200100')
   
    # Gather 3D soil variables
    st = pyw.Vsl('ST',interf['ST'].val,sl_layers)
    sm = pyw.Vsl('SM',interf['SM'].val,sl_layers)

    # Listing fields
    total_fields = [seaice,snow,skintemp,sm,sst,dewpt,landsea,psfc,st,pmsl,snowh,tt2m,rh2m,uu10m,vv10m]

    # Writing output intermediate file
    pyw.cinter(out_sl_int_prefix,inter_times[i],geo,total_fields,inter_path)
    
    
# Move on to next line
print('\n')    





