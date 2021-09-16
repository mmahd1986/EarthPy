
# =============================================================
# === Description: ERA5_CDS_SL_Data_Download_Script.        ===
# === Version: 1.                                           ===      
# === Author: Mani Mahdinia                                 ===
# === Emails: mani.mahdinia@utoronto.ca,                    ===
# ===         mani.mahdinia@gmail.com                       ===    
# =============================================================


# Import needed modules
import sys                      # sys
import cdsapi                   # cds api module
import numpy as np              # numpy


# ====================================================
# == This code's used for individual data downloads == 
# ====================================================

def main():
    
    # Arguments
    download_area = [float(sys.argv[1]), float(sys.argv[2]), \
                     float(sys.argv[3]), float(sys.argv[4])]      # [N, W, S, E] (in degrees).
    hourly_freq = sys.argv[5]                                     # Data download hourly frequency.    
    input = sys.argv[6]                                           # Month data input.      

    # Single level dataset
    dataset_sl = 'reanalysis-era5-single-levels'     
    
    # Check if 24 hours is divisible by hourly_freq
    if ((24%int(hourly_freq))!=0):
        raise ValueError("mod(24,hourly_freq)!=0. "
            "24 hours should be divisible by hourly_freq.") 
        
    # Extract begin and end dates
    with open("input_list.txt", "r") as file:
        date1 = file.readline()
        for date2 in file:
            pass          
        
    # Show download process
    S = 'Dates: '+date1+'-'+date2+' / ''Downloading SL data for ' +input+ '.'
    S = S.replace("\n", "")
    print(S)    
    
    # Output file name
    output_file = './Data/ERA5-'+input[0:6]+'010000-'+input[0:8]+str(24-int(hourly_freq)).zfill(2)+'00-sl.grib'
    
    # Day range
    day_range_init = np.arange(1,int(input[6:8])+1)
    day_range = [str(item).zfill(2) for item in day_range_init]
    
    # Download parameters
    params = {
        'product_type':'reanalysis',
        'variable':[
            'surface_pressure','mean_sea_level_pressure',
            'skin_temperature','sea_surface_temperature',
            '2m_temperature','2m_dewpoint_temperature',
            '10m_u_component_of_wind','10m_v_component_of_wind',
            'land_sea_mask',        
            'soil_temperature_level_1','soil_temperature_level_2',
            'soil_temperature_level_3','soil_temperature_level_4',
            'volumetric_soil_water_layer_1','volumetric_soil_water_layer_2',
            'volumetric_soil_water_layer_3','volumetric_soil_water_layer_4',
            'snow_depth','sea_ice_cover'],        
        'area': download_area,          
        'year':input[0:4],
        'month':input[4:6],
        'day': day_range,
        'time':'00/to/23/by/'+hourly_freq,
        'format': 'grib'   
    }
    # NOTE: WRF needs "2m relative or specific humidity". Why do we get 
    # the "2m_dewpoint_temperature" (as mentioned by the guide)? ????? 
    # NOTE: WRF needs soil height. Why is this not specified in the above? ?????

    # Initialize cdsapi client
    cds = cdsapi.Client()

    # Retrieve data
    cds.retrieve(dataset_sl,params,output_file)
        
    
# main call    
if __name__ == "__main__":
   main()    
    



