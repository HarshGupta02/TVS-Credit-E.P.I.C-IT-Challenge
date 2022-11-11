list_of_lists = []

with open('C:/Users/HarshGupta/Desktop/outcomes/detail.txt') as f:
    for line in f:
        inner_list = [elt.strip() for elt in line.split(',')]
        list_of_lists.append(inner_list)

brand=(list_of_lists[0][0]) # br means brand

model=list_of_lists[0][1] # mo means model

old_price=int(list_of_lists[0][2]) # old_price to ptaa hi hai :)

yearold=int(list_of_lists[0][3]) #yo means years old
yearold_prev = yearold
yearold = yearold/10

ownership=int(list_of_lists[0][4]) #ow means ownership
ownership_prev = ownership
ownership = ownership/10

location=list_of_lists[0][5] #lo menas location
location_prev = location
if(location == 'Delhi'):
  location=0.2
elif(location == 'Gujrat'):
  location=0.1

km=int(list_of_lists[0][6]) #km means km driven
km_prev = km
if(km<10000):
  km = km/10000
elif(km>=10000 and km<100000):
  km = km/100000
elif(km>=100000 and km<1000000):
  km = km/1000000
  
image_score=float(list_of_lists[0][7]) # this is image socre
# print("the image score is : " , image_score)

# audio_sc=float(list_of_lists[8][0]) # this is one is audio... ;)

x1=4000 #years old
x2=3000 #owenership
x3=1000 #location
x4=4000 #kmdriven
x5=5000 #imagescore
# x6=5000 #audioscore

# Y=(old_price-((x1*yo)+(x2*ow)+(x3*lo)+(x4*km)+(x5*image_sc)+(x6*audio_sc)))
Y=(old_price-((x1*yearold)+(x2*ownership)+(x3*location)+(x4*km)+(x5*image_score)))

final_score = Y

with open('C:/Users/HarshGupta/Desktop/outcomes/Final_Price.txt', 'w') as f:
    print(final_score, file=f)

import pandas as pd
fd=pd.read_csv('car_ad.csv')
import csv  
from csv import DictWriter
header = ['Vehicles', 'Model', 'Old_Price', 'Years_old', 'Prev_Owners', 'Location', 'Kms_Driven', 'Image_Score', 'Audio_Score', 'Final_Price']
data = {'Vehicles': brand, 'Model': model, 'Old_Price': old_price, 'Years_old': yearold_prev, 'Prev_Owners': ownership_prev, 'Location': location_prev, 'Kms_Driven': km_prev, 'Image_Score': image_score, 'Audio_Score': 0.5, 'Final_Price':final_score}
with open('car_ad.csv', 'a', newline='') as f_object:
    dictwriter_object = DictWriter(f_object, fieldnames=header)
    dictwriter_object.writerow(data)
    f_object.close()
fd=pd.read_csv('car_ad.csv')
# print(final_score)

dataV={
    "Tvs":1,
    "Honda":2,
}
dataM={
    "CB_350":1,
    "Apache":2
}
dataL={
    "Delhi":1,
    "Gujrat":2
}

fd['Vehicles_num']=fd['Vehicles'].map(dataV)
fd=fd.drop(['Vehicles'], axis=1)
fd['Model_num']=fd['Model'].map(dataM)
fd=fd.drop(['Model'], axis=1)
fd['Location_num']=fd['Location'].map(dataL)
fd=fd.drop(['Location'], axis=1)

import numpy as np
from random import randrange, choice
from sklearn.neighbors import NearestNeighbors

def SMOTE(T, N, k):
    n_minority_samples, n_features = T.shape

    if N < 100:
        #create synthetic samples only for a subset of T.
        #TODO: select random minortiy samples
        N = 100
        pass

    if (N % 100) != 0:
        raise ValueError("N must be < 100 or multiple of 100")

    N = int(N/100)
    n_synthetic_samples = int(N * n_minority_samples)
    n_features = int(n_features)
    S = np.zeros(shape=(n_synthetic_samples, n_features))

    #Learn nearest neighbours
    neigh = NearestNeighbors(n_neighbors = k)
    neigh.fit(T)

    #Calculate synthetic samples
    for i in range(n_minority_samples):
        nn = neigh.kneighbors(T[i].reshape(1, -1), return_distance=False)
        for n in range(N):
            nn_index = choice(nn[0])
            #NOTE: nn includes T[i], we don't want to select it 
            while nn_index == i:
                nn_index = choice(nn[0])

            dif = T[nn_index] - T[i]
            gap = np.random.random()
            S[n + i * N, :] = T[i,:] + gap * dif[:]

    return S

fd = fd.to_numpy()
new_data = SMOTE(fd,10000,10)

df = pd.DataFrame(new_data)
df.to_csv("data1.csv")

file = pd.read_csv("data1.csv")
  
headerList = ['idx', 'Old_price', 'Years_old', 'Prev_Owners', 'Kms_Driven', 'Image_Score', 'Audio_Score', 'Final_Price', 'Vehicles_num', 'Model_num', 'Location_num']
  
# converting data frame to csv
file.to_csv("data2.csv", header=headerList, index=False)
  
# display modified csv file
file2 = pd.read_csv("data2.csv")

file2=file2.drop(['idx'], axis=1)

import math
import numpy

x=len(file2)

for column in file2[['Years_old', 'Prev_Owners', 'Vehicles_num', 'Model_num', 'Location_num']]:
    columnSeriesObj = file2[column]
    for i in range(0,x):
        columnSeriesObj.values[i] = numpy.round(columnSeriesObj.values[i])
        
file3=file2

dataoV={
    1:"Tvs",
    2:"Honda",
}

dataoM={
    1:"CB_350",
    2:"Apache"
}

dataoL={
    1:"Delhi",
    2:"Gujrat"
}

file2['Brand']=file2['Vehicles_num'].map(dataoV)
file2=file2.drop(['Vehicles_num'], axis=1)

file2['Model']=file2['Model_num'].map(dataoM)
file2=file2.drop(['Model_num'], axis=1)

file2['Location']=file2['Location_num'].map(dataoL)
file2=file2.drop(['Location_num'], axis=1)

file2 = file2[['Brand',	'Model','Location', 'Old_price'	,'Years_old','Prev_Owners',	'Kms_Driven', 'Image_Score', 'Audio_Score', 'Final_Price']]
dt = pd.DataFrame(file2)
dt.to_csv("final_data.csv")