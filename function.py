import json
import boto3

def lambda_handler(event, context):
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    client = boto3.client('textract')
    response1 = client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        FeatureTypes=['FORMS',]
        )
    
    client = boto3.client('translate')
    for i in range(1,len(response1['Blocks'])):
        if response1['Blocks'][i]['BlockType']=='LINE':
            line = response1['Blocks'][i]['Text']
            
            response2 = client.translate_text(
                Text=line,
                SourceLanguageCode='en',
                TargetLanguageCode='es'
                )
            print(response2['TranslatedText'])
            
    return