from flask import Flask, request
import json
import sys
from skimage.metrics import structural_similarity
import cv2
import matplotlib.pyplot as plt
import os
from skimage.transform import resize
from PIL import Image
import numpy as np
from skimage.util import img_as_bool
from boto3.session import Session

ACCESS_KEY_ID = 'AKIARXQBP2ZVBYLBIEWV'
SECRET_KEY = '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'

session = Session(aws_access_key_id = ACCESS_KEY_ID, aws_secret_access_key = SECRET_KEY)

s3 = session.resource('s3')

bucket = 'image-already-upload'

my_bucket = s3.Bucket(bucket)

print("Downloading from S3......")

my_bucket.download_file('imagefront','C:/Users/HarshGupta/Desktop/Image_user/Front_view/Front.jpg')
my_bucket.download_file('imageback','C:/Users/HarshGupta/Desktop/Image_user/Rear_view/Back.jpg')
my_bucket.download_file('imageleft','C:/Users/HarshGupta/Desktop/Image_user/LSide_view/Left.jpg')
my_bucket.download_file('imageright','C:/Users/HarshGupta/Desktop/Image_user/RSide_view/Right.jpg')

print("Downloaded successfully from s3....")

def orb_sim(img1, img2):
  orb = cv2.ORB_create()

  kp_a, desc_a = orb.detectAndCompute(img1, None)
  kp_b, desc_b = orb.detectAndCompute(img2, None)

  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
  matches = bf.match(desc_a, desc_b)
  similar_regions = [i for i in matches if i.distance < 60]  
  if len(matches) == 0:
    return 0
  return len(similar_regions) / len(matches)

def structural_sim(img1, img2):
  sim, diff = structural_similarity(img1, img2, full=True,  win_size=1, use_sample_covariance=False)
  return sim

"""### **Front_View**"""

data_f = []
data_of=[]
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/Front_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/Front_view"):
    img = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/Front_view/"+ filen)
    imga = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/Front_view/"+ filem)
    orb_similarity = orb_sim(img,imga)
    data_of.append(orb_similarity)
    data_f.append(filen)

data_sf = []
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/Front_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/Front_view"):
    imgb = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/Front_view/"+ filen)
    imgc = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/Front_view/"+ filem)
    imgb = resize(imgb, (imgc.shape[0], imgc.shape[1], imgc.shape[2]), anti_aliasing=True, preserve_range=True)
    img_b = np.squeeze(imgb)
    img_c = np.squeeze(imgc)
    ssim = structural_sim(img_b, img_c)
    data_sf.append(ssim)

maxi = data_of[0];    
c=0;
for i in range(0, len(data_of)):       
  if(data_of[i] > maxi):    
      maxi = data_of[i]; 
      c=i;

maxt = data_sf[0];    
d=0;
for i in range(0, len(data_sf)):       
  if(data_sf[i] > maxt):    
      maxt = data_sf[i]; 
      d=i;

avga = (maxt+maxi)/2;

"""## **Rear_View**"""

data_fb=[]
data_or=[]
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/Rear_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/Rear_view"):
    img = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/Rear_view/"+ filen)
    imga = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/Rear_view/"+ filem)
    orb_similarity = orb_sim(img,imga)
    data_or.append(orb_similarity)
    data_fb.append(filen)

data_sr = []
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/Rear_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/Rear_view"):
    imgb = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/Rear_view/"+ filen)
    imgc = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/Rear_view/"+ filem)
    imgb = resize(imgb, (imgc.shape[0], imgc.shape[1], imgc.shape[2]), anti_aliasing=True, preserve_range=True)
    img_b = np.squeeze(imgb)
    img_c = np.squeeze(imgc)
    ssim = structural_sim(img_b, img_c)
    data_sr.append(ssim)

maxi = data_or[0];    
c=0;
for i in range(0, len(data_or)):       
  if(data_or[i] > maxi):    
      maxi = data_or[i]; 
      c=i;

maxt = data_sr[0];    
d=0;
for i in range(0, len(data_sr)):       
  if(data_sr[i] > maxt):    
      maxt = data_sr[i]; 
      d=i;

avgb = (maxt+maxi)/2;

"""## **LSide_View**"""

data_fc=[]
data_ol=[]
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/LSide_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/LSide_view"):
    img = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/LSide_view/"+ filen)
    imga = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/LSide_view/"+ filem)
    orb_similarity = orb_sim(img,imga)
    data_ol.append(orb_similarity)
    data_fc.append(filen)

data_sl = []
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/LSide_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/LSide_view"):
    imgb = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/LSide_view/"+ filen)
    imgc = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/LSide_view/"+ filem)
    imgb = resize(imgb, (imgc.shape[0], imgc.shape[1], imgc.shape[2]), anti_aliasing=True, preserve_range=True)
    img_b = np.squeeze(imgb)
    img_c = np.squeeze(imgc)
    ssim = structural_sim(img_b, img_c)
    data_sl.append(ssim)

maxi = data_ol[0];    
c=0;
for i in range(0, len(data_ol)):       
  if(data_ol[i] > maxi):    
      maxi = data_ol[i]; 
      c=i;

maxt = data_sl[0];    
d=0;
for i in range(0, len(data_sl)):       
  if(data_sl[i] > maxt):    
      maxt = data_sl[i]; 
      d=i;

avgc = (maxt+maxi)/2;

"""## **RSide_View**"""

data_fd=[]
data_ors=[]
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/RSide_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/RSide_view"):
    img = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/RSide_view/"+ filen)
    imga = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/RSide_view/"+ filem)
    orb_similarity = orb_sim(img,imga)
    data_ors.append(orb_similarity)
    data_fd.append(filen)

data_srs = []
for filen in os.listdir("C:/Users/HarshGupta/Desktop/Images_org/RSide_view"):
  for filem in os.listdir("C:/Users/HarshGupta/Desktop/Image_user/RSide_view"):
    imgb = plt.imread("C:/Users/HarshGupta/Desktop/Images_org/RSide_view/"+ filen)
    imgc = plt.imread("C:/Users/HarshGupta/Desktop/Image_user/RSide_view/"+ filem)
    imgb = resize(imgb, (imgc.shape[0], imgc.shape[1], imgc.shape[2]), anti_aliasing=True, preserve_range=True)
    img_b = np.squeeze(imgb)
    img_c = np.squeeze(imgc)
    ssim = structural_sim(img_b, img_c)
    data_srs.append(ssim)

maxi = data_ors[0];    
c=0;
for i in range(0, len(data_ors)):       
  if(data_ors[i] > maxi):    
      maxi = data_ors[i]; 
      c=i;

maxt = data_srs[0];    
d=0;
for i in range(0, len(data_srs)):       
  if(data_srs[i] > maxt):    
      maxt = data_srs[i]; 
      d=i;

avgd = (maxt+maxi)/2;
total_score = (avga+avgb+avgc+avgd)/4;

with open('C:/Users/HarshGupta/Desktop/Images_output/out.txt', 'w') as f:
    print("Total Similarity Score : ", total_score, file=f)
