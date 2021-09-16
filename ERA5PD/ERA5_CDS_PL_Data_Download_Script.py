
# =============================================================
# === Description: ERA5_CDS_PL_Data_Download_Script.        ===
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

    # Pressure level dataset
    dataset_pl = 'reanalysis-era5-pressure-levels'       
    
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
    S = 'Dates: '+date1+'-'+date2+' / ''Downloading PL data for ' +input+ '.'
    S = S.replace("\n", "")
    print(S)    
    
    # Output file name
    output_file = './Data/ERA5-'+input[0:6]+'010000-'+input[0:8]+str(24-int(hourly_freq)).zfill(2)+'00-pl.grib'
    
    # Day range
    day_range_init = np.arange(1,int(input[6:8])+1)
    day_range = [str(item).zfill(2) for item in day_range_init]
    
    # Download parameters
    params = {
        'product_type':'reanalysis',
        'variable':[
            'geopotential','relative_humidity','specific_humidity',
            'temperature','u_component_of_wind','v_component_of_wind'],        
        'area': download_area,   
        'pressure_level': [
            '1', '2', '3',
            '5', '7', '10',
            '20', '30', '50',
            '70', '100', '125',
            '150', '175', '200',
            '225', '250', '300',
            '350', '400', '450',
            '500', '550', '600',
            '650', '700', '750',
            '775', '800', '825',
            '850', '875', '900',
            '925', '950', '975',
            '1000'],     
        'year':input[0:4],
        'month':input[4:6],
        'day': day_range,
        'time':'00/to/23/by/'+hourly_freq,
        'format': 'grib'   
    }
    # NOTE: Some of the options are as follows:
    # 1) Area is in the format 'area':[North, West, South, East] (in degrees).
    #    For NA + Greenland + Alaska, it is: [88.0, -179.0, 6.0, -5.3].
    # 2) Format is either 'grib' or 'netcdf'. See the 1st and 2nd tables here:
    #    https://confluence.ecmwf.int/display/CKB/Climate+Data+Store+%28CDS%29+API+Keywords.
    # USEFUL REFERENCES:
    # 1-Climate Data Store (CDS) API Keywords:
    # https://confluence.ecmwf.int/display/CKB/Climate+Data+Store+%28CDS%29+API+Keywords.
    # 2-ERA5: data documentation:
    # https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation.
    
    # NOTE: Other possible options are as follows:
    # 1) 'class':'ea' is for ERA5 (https://apps.ecmwf.int/codes/grib/format/mars/class/).
    # 2) The 'type':'an' is for analysis. 
    #    For more information see: 
    #    https://apps.ecmwf.int/data-catalogues/era5/?class=ea&stream=oper&expver=1.
    # 3) For param: We get the parameter codes from here:
    #    https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation
    #    For "Table 12: model level parameters: instantaneous":
    #    For the parameters above: 
    #    129: Geopotential (z) (m^2/s^2), 
    #    130: Temperature (t) (K),
    #    131: U component of wind (u) (m/s), 
    #    132: V component of wind (v) (m/s),
    #    133: Specific humidity (q) (kg/kg),
    #    152: Logarithm of surface pressure (lnsp) (~).
    # 4) expver is for 'experiment version', which for ERA5, is 1.
    #    To see an example with a different expver, see this: 
    #    https://confluence.ecmwf.int/pages/viewpage.action?pageId=171414041.
    # 5) 'levtype':'ml' is for model levels. For more info about this see:
    #    https://apps.ecmwf.int/data-catalogues/era5/?class=ea&stream=mnth& ...
    #    expver=1&type=fc&year=2011.
    # 6) 'levelist':'1/to/137': For the picture and description of the 137 vertical levels 
    #    see this: https://confluence.ecmwf.int/display/CKB/ERA5%3A+compute+pressure+ ...
    #    and+geopotential+on+model+levels%2C+geopotential+height+and+geometric+height.
    # 7) For atmospheric model the stream is 'oper'. 
    #    For more info see: https://apps.ecmwf.int/data-catalogues/era5/?class=ea.
    # 8) 'grid': [0.25, 0.25] is for 0.25 degree resolution. See this:
    #    https://confluence.ecmwf.int/display/CKB/ERA5%3A+What+is+the+spatial+reference.

    # Initialize cdsapi client
    cds = cdsapi.Client()

    # Retrieve data
    cds.retrieve(dataset_pl,params,output_file)
        
    
# main call    
if __name__ == "__main__":
   main()    
    



