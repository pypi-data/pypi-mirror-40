###################################################### Daymark ############################################################# 

import requests
import time
import os,sys
from redis import Redis
import json

#import psutil

#Global instances

#Timestamp converter

global r
r = time.ctime(time.time())

#redis connection instance

global rmaster

class daymark():
	
	#Function to initialize basic configuration

	def init(redis_end_point):

		if redis_end_point:
			
			redisEndPoint = redis_end_point

			#Connects to redis master running inside the same kubernetes cluster in 'default' namespace
		
			rmaster = Redis(host = redisEndPoint, port=6379, db=0)
			pubsub = rmaster.pubsub()
			return rmaster

		else:

			sys.exit("No endpoint to connect")
	
	#function logs string to stdout in red & exits the code after publishing in redis

	def logError(errorMsg, envVar, instance):
		
		if errorMsg:

			print("\033[1;31;40m %s: %s \n " % (r, errorMsg) + "\n > Unfortunately Exiting the system!")
			
			rmaster = instance
			#The message that will be streamed in redis
			msg = {
				"id": envVar,
				"status": "FAILED"
			}
			streamMsg = json.dumps(msg)
			rmaster.publish('jobs', streamMsg)
			sys.exit(errorMsg)
		else:

			sys.exit(1)
	
	#function logs string to stdout in green & exits the code

	def logSuccessful(successMsg, envVar, instance):
		
		if successMsg:

			print("\033[1;32;40m %s: %s \n" % (r, successMsg) + "> Successfully Exiting the system!")

			rmaster = instance
			#The message that will be streamed in redis
			msg = {
				"id": envVar,
				"status": "COMPLETED"
			}
			streamMsg = json.dumps(msg)
			rmaster.publish('jobs', streamMsg)
			sys.exit(successMsg)
		else:

			sys.exit(0)
	
	#function logs string to stdout in yellow

	def logWarning(warningMsg):
		print("\033[1;33;40m %s time = %s \n" % (warningMsg, r))
	
	
	#function returns the progress percentage

	def getProgress(file_processed_count, total_file_count):
		
		processedCount = file_processed_count
		totalCount = total_file_count
		
		#Percentage
		per =  int(((processedCount/totalCount))*100)
		return per	

	
	#function shows the progress

	def showProgress(self, file_processed_count):
		
		processedCount = file_processed_count
		prog = '%d files (%.2f%%)' % (file_processed_count, self.percentDone())
		return prog

	
	#function to get environment variable

	def getEnvVar(name):
		
		#Function to get environment variable named jobId 
		envVar = name
		id = os.environ[envVar]
		return id

	
	#Set progress in redis-master

	def setProgress(key, value, instance):
		
		#Setting progress in redis-master
		rmaster = instance
		envVar = key
		percentage = value
		msg = {
				"id": envVar,
				"progress": percentage
			}
		streamMsg = json.dumps(msg)
		rmaster.publish('progress', streamMsg)

		
	#function to download a file from S3
	'''
	def downloadFromS3(inputBucket, key):

		BUCKET_NAME = inputBucket 

		KEY = key 

		s3 = boto3.resource('s3')

		try:

    		s3.Bucket(BUCKET_NAME).download_file(KEY, 'my_local_image.jpg')
			
		except botocore.exceptions.ClientError as e:
    			
			if e.response['Error']['Code'] == "404":
        			
				print("The object does not exist.")
    			
			else:
    			raise

	def uploadToS3(outputBucket, key):

		BUCKET_NAME = outputBucket

		KEY = key
			
		s3 = boto3.client('s3')
			
		s3.upload_file(Key, BUCKET_NAME, 'anything.anything')
	'''
	'''
	#Resource Monitor

	def showResourceUsage():
		#CPU frequency usage

		print(psutil.cpu_freq() + "-> current frequency usage")
		#CPU memory usage
		
		print(psutil.virtual_memory() + "-> current memory usage")
	'''
	
	
	#function to push data to s3 bucket

	'''def pushToS3():
		#Credentials of AWS
		AWS_ACCESS_KEY_ID = ''
		AWS_SECRET_ACCESS_KEY = ''
		
		bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
		
		filename = ''

		print('Uploading %s to Amazon S3 bucket %s' % (filename, bucket_name))

		def percent_cb(complete, total):
    		sys.stdout.write('')	
    		sys.stdout.flush()
		
		k = Key(bucket)
		k.key = 'my test file'
		k.set_contents_from_filename(testfile, cb=percent_cb, num_cb=10)
	'''

	#Function to download a file from a given url

	'''def downloader(self, Url):
		
		if Url:
			try:
				req = requests.get(url, allow_redirects=True)
        		size = int(req.headers['content-length'])
        		total = size/chunk_size
       	 		count = 0
        		filename = url.split('/')[-1]
        		with open(filename, 'wb') as f:
            		for data in tqdm( iterable = req.iter_content(chunk_size = chunk_size), total = size/chunk_size, unit = 'B'):
                		f.write(data)
                		count += 1
                		#id = self.getJobId()
                		#per = self.percentDone(count, total)
                		#self.createKey(id, per)
        		if(count == size):
            		self.logSuccessful("Download complete")
       			else:
            		raise Exception('The file could not be downloaded') 
    		except Exception as e:
        		self.logError(e)
		else:
    		self.logError("URL Unavailable")'''

	
	
	