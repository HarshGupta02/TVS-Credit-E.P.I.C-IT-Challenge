import pandas as pd
fd=pd.read_csv('car_ad.csv')
fd.head()
import csv  
from csv import DictWriter
header = ['Vehicles', 'Model', 'Old_Price', 'Years_old', 'Prev_Owners', 'Location', 'Kms_Driven', 'Image_Score', 'Audio_Score', 'Final_Price']
data = {'Vehicles': 'bsjhdb', 'Model': 'Apache', 'Old_Price': 40000, 'Years_old': 3, 'Prev_Owners': 2, 'Location': 'Gujrat', 'Kms_Driven': 31000, 'Image_Score': 0.6, 'Audio_Score': 0.5, 'Final_Price':32000}
with open('car_ad.csv', 'a') as f_object:
    dictwriter_object = DictWriter(f_object, fieldnames=header)
    dictwriter_object.writerow(data)
    f_object.close()
fd=pd.read_csv('car_ad.csv')
fd.head()