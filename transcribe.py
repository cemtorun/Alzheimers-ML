from __future__ import print_function
import time
import boto3
import json
transcribe = boto3.client('transcribe')

job_name = "AlexaTest3"
job_uri = "https://s3.us-east-2.amazonaws.com/princetonhackbob/alexa.mp3"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    OutputBucketName= "princetonhackbob",
    MediaFormat='mp3',
    LanguageCode='en-US'
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(1)
print(status)
# parsed_json = json.dumps(status)
# print(parsed_json['TranscriptionJob'])
