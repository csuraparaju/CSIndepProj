import time
import boto3
import requests
import json

"""
This method produces a text transcript of the given audio file (specified by the URI of the object in an aws S3 bucket).The audio format must be a .wav file. 
A string representing the name of the job must also be given in order to identify the correct JSON information.  
:param elements: string(job_name), string(media_uri)
:return: string(textTranscript)
"""

def getResult(job_name, media_uri):
    
    jobDone = False
    transcribeclient = boto3.client('transcribe')
    
    transcribeclient.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_uri},
        MediaFormat='wav',
        LanguageCode='en-US'
    )
    
    while not jobDone:
        status = transcribeclient.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            jobDone = True
        print("Job in progress...")
        time.sleep(10)
    
    transcriptUrl = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    response = requests.get(url = transcriptUrl)
    transcriptJsonResp = json.loads(response.text)
    
    textTranscript = (transcriptJsonResp["results"]["transcripts"][0]["transcript"])
    
    return textTranscript
    
    

    
    
