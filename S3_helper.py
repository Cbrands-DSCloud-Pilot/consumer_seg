#Helper functions for S3. Built by DataScience Cloud

import boto3
import os
import pandas as pd


class S3_helper(object):
    
    def __init__(self,access,secret,bucket):
        self.access = access
        self.secret = secret
        self.bucket = bucket
        self.s3 = boto3.client(service_name = 's3', 
                          aws_access_key_id = self.access, 
                          aws_secret_access_key = self.secret)


    def push_file_to_s3(self,path, key=None):
        """Take in a path and push to S3"""
        if key == None:
            print "Can't push to S3 without a key. Please specify a key."
            return
        key = key.replace(' ','-')  #replace spaces with '-'
    
        self.s3.upload_file(path, self.bucket, key)
        print "Sent file %s to S3 with key '%s'"%(path,key)


    def pull_file_from_s3(self,key, path):
    
        local_dir = '/'.join(path.split('/')[:-1])
        if not os.path.isdir(local_dir) and local_dir != '':
            print "Local directory %s doesn't exist"%(local_dir)
            return
    
        self.s3.download_file(self.bucket, key, path)
    
        print "Grabbed %s from S3. Local file %s is now available."%(key,path)


    def s3_CSVtoDF(self,file_name, **kwargs):
        """
        Stream a data file from S3 into a dataframe
    
        All **kwargs are passed to pandas.read_csv() and must
        therefore be valid keyword arguments of that function
        """
    
        obj = self.s3.get_object(Bucket=self.bucket, Key=file_name)
    
        return pd.read_csv(obj['Body'], **kwargs)
