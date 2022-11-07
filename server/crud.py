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