###############################################
## API Main Application
## (1) Detect faces (primary only)
## (2) Identify PersonId of a face
## Created by: Jixin Jia (05-Jan-2018)
###############################################

import urllib.parse, json, requests, time, config, os
from twilio.rest import Client 
from colorama import init, Fore, Back, Style

init(convert=True) #For colorama

def sms(pin, destination):
    client = Client(config.account_sid, config.auth_token) 
    message = client.messages.create( 
                                from_='{YOUR_TWILLIO_PHONE_NUMBER}',  
                                body='Face identification PIN: '+str(pin),      
                                to=destination 
    )
    print(message.sid)


def identify(faceSession, fileName):

    faceId = None
    gender = None
    age = None
    glasses = None
    anger = None
    happiness = None
    neutral = None
    sadness = None
    fear = None
    surprise = None
    personId = None
    personName = None
    personPhone = None
    statusCode = None
    conf = None

    imageFile = open(config.directory+'/'+faceSession+'/'+fileName,'rb')
    body = imageFile.read()
    imageFile.close()

    #### (1) Extract facial attributes ####
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': config.APIKey,
    }
    params = urllib.parse.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,glasses,emotion'
    })
    r = requests.post(config.urlAPI+'/detect?%s' % params,headers=headers,  data=body)
    res = r.json()

    if r.status_code == 200:
        
        print(Fore.YELLOW + "[Info] {0} face(s) found:".format(len(res)))
        print(Style.RESET_ALL)

        # Only process first (major) face, ignore other faces
        if len(res) >0:
            faceId = res[0]['faceId']
            gender = res[0]['faceAttributes']['gender']
            age = res[0]['faceAttributes']['age']
            glasses = res[0]['faceAttributes']['glasses']
            anger = res[0]['faceAttributes']['emotion']['anger']
            happiness = res[0]['faceAttributes']['emotion']['happiness']
            neutral = res[0]['faceAttributes']['emotion']['neutral']
            sadness = res[0]['faceAttributes']['emotion']['sadness']
            fear = res[0]['faceAttributes']['emotion']['fear']
            surprise = res[0]['faceAttributes']['emotion']['surprise']

            print(Fore.YELLOW + "[Info] Gender={0}  Age={1} WearGlasses={2}".format(gender,age,glasses))
            print("[Info] Emotions: (Anger:{0}, Happiness:{1}, Neutral:{2}, Sadness:{3}, Fear:{4}, Surprise:{5})".format(anger,happiness,neutral,sadness,fear,surprise))
            print(Style.RESET_ALL)
            
            ####(2) Identify person's ID (name, phonenumber)
            headersIdentify = {
                'Content-Type' : 'application/json',
                'Ocp-Apim-Subscription-Key': config.APIKey
            }
            bodyIdentify = {
                "personGroupId": config.personGroupId,
                "faceIds": [faceId],
                "maxNumOfCandidatesReturned": 1,
                "confidenceThreshold": 0.5
            }
            bodyIdentify = json.dumps(bodyIdentify)

            r2 = requests.post(config.urlAPI+'/identify',headers=headersIdentify,  data=bodyIdentify)
            res2 = r2.json()

            if r2.status_code == 200:
                if len(res2[0]['candidates']) > 0:
                    personId = res2[0]['candidates'][0]['personId']
                    conf = res2[0]['candidates'][0]['confidence']
                    
                    r3 = requests.get(config.urlAPI+'/persongroups/'+config.personGroupId+'/persons/'+personId,headers=headersIdentify)
                    res3 = r3.json()
                    
                    # Fetch Person Name and User Data
                    if r3.status_code == 200:
                        personName = res3['name']
                        personPhone = res3['userData']
                        statusCode = 'OK'

                        print(Fore.GREEN + "[Info] personName:  {0} (personPhone: {1}) Confidence: {2}".format(personName, personPhone,conf))
                        print(Style.RESET_ALL)

                    else:
                        statusCode = '[INFO] Your identity cannot be determined'  
                        print(Fore.RED + "[Warning] No candidate found. Unknown face")
                        print(Style.RESET_ALL)              
                else:
                    statusCode = '[INFO] Your identity cannot be determined' 
            else:
                statusCode = '[INFO] Your identity cannot be determined' 
        else:
            statusCode = '[INFO] Low Image Quality. Adjust camera!'
            print(Fore.RED + "[ERROR] No face found !!")
            print(Style.RESET_ALL)
    else:
        statusCode = '[INFO] Low Image Quality. Adjust camera!'
        print(Fore.RED + "[ERROR] Failed to contact API")
        print(Style.RESET_ALL)

    return statusCode,gender,age,glasses,anger,happiness,neutral,sadness,fear,surprise,personId,personName,personPhone,conf