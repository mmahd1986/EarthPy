
# =============================================================
# === Description: ERA5_CDS_Data_Prepare_List_Script.       ===
# === Version: 1.                                           ===      
# === Author: Mani Mahdinia                                 ===
# === Emails: mani.mahdinia@utoronto.ca,                    ===
# ===         mani.mahdinia@gmail.com                       ===    
# =============================================================


# Import needed modules
import sys                   # sys
import pandas as pd          # pandas


# ==================================================
# == This code's used to prepare a file including ==
# == all months' data.                            == 
# ==================================================

def main():
    
    # Arguments
    start_year = sys.argv[1]     # Data download start year.
    end_year = sys.argv[2]       # Data download end year.
    end_month = sys.argv[3]      # Data download end month.
    end_day = sys.argv[4]        # Data download end day.
    
    # Create input date list
    datelist = pd.date_range(start='1/1/'+start_year, end=end_day+'/'+end_month+'/'+end_year)
    monthp = '00'; 
    input_list = []
    for item in datelist:
        d = str(item)
        year = d[0:4]
        month = d[5:7]
        day = d[8:10]
        if (int(day)==1):
            if (int(monthp)>0):            
                input_list.append(yearp+monthp+dayp)
        yearp = year
        monthp = month
        dayp = day
    input_list.append(end_year+end_month+end_day)

    # Write gnu-parallel input file
    f = open("input_list.txt", "w")
    for item in input_list:
        f.write(item+'\n')
    f.close()


# main call    
if __name__ == "__main__":
   main() 

