list_of_lists = []

with open('C:/Users/HarshGupta/Desktop/outcomes/detail.txt') as f:
    for line in f:
        inner_list = [elt.strip() for elt in line.split(',')]
        list_of_lists.append(inner_list)

br=(list_of_lists[0][0]) # br means brand

mo=list_of_lists[0][1] # mo means model

old_price=int(list_of_lists[0][2]) # old_price to ptaa hi hai :)

yo=int(list_of_lists[0][3]) #yo means years old
yo = yo/10

ow=int(list_of_lists[0][4]) #ow means ownership
ow = ow/10

lo=list_of_lists[0][5] #lo menas location
if(lo == 'Delhi'):
  lo=0.2
elif(lo == 'Gujrat'):
  lo=0.1

km=int(list_of_lists[0][6]) #km means km driven
if(km<10000):
  km = km/10000
elif(km>=10000 and km<100000):
  km = km/100000
elif(km>=100000 and km<1000000):
  km = km/1000000
  
image_sc=float(list_of_lists[0][7]) # this is image socre

# audio_sc=float(list_of_lists[8][0]) # this is one is audio... ;)

x1=4000 #years old
x2=3000 #owenership
x3=1000 #location
x4=4000 #kmdriven
x5=5000 #imagescore
# x6=5000 #audioscore

# Y=(old_price-((x1*yo)+(x2*ow)+(x3*lo)+(x4*km)+(x5*image_sc)+(x6*audio_sc)))
Y=(old_price-((x1*yo)+(x2*ow)+(x3*lo)+(x4*km)+(x5*image_sc)))

final_score = Y

with open('C:/Users/HarshGupta/Desktop/outcomes/Final_Price.txt', 'w') as f:
    print(final_score, file=f)