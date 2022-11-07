const dotenv = require("dotenv");
const aws = require("aws-sdk");

dotenv.config();

const region = "us-east-1"
const bucketName = "uservehicleimages"
const accessKeyId = process.env.AWS_ACCESS_KEY_ID
const secretAccessKey = process.env.AWS_SECRET_ACCESS_KEY

const s3 = new aws.S3({
    region, 
    accessKeyId,
    secretAccessKey,
    signatureVersion: 'v4'
})

module.exports = async function generateUploadURL(){
    const imageName = "UniqueImageName";
    const params = ({
        Bucket : bucketName,
        Key : imageName,
        Expires : 60
    }) 
    const uploadURL = await s3.getSignedUrlPromise('putObject',params)
    return uploadURL
};