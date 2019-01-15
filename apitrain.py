###############################################
## API New Person Training
## (1) Add Person object (container)
## (2) Attach new faces
## (3) Retrain PersonGroup container
## Created by: Jixin Jia (05-Jan-2018)
##############################################

'''
API Interface
(1) Face API PersonGroup -AddPerson
     -input: config.personGroupId
     -output: personId
(2) Face API PersonGroup -Person -AddFace
     -input: config.personGroupId, personId
     -output: persistedFaceId
(3) Face API PersonGroup -Train
     -input: config.personGroupId
     -output: N/A
'''

import urllib.parse, json, requests, time , config, os
from random import randint

def registerface(userName, userPhone):
    
    personId = None
    faceCount = 0
    statusMsg = None
    statusCode = 0
    randId = str(randint(1000,9999))

    if not userName:
        userName = 'Guest '+str(randId)
    
    if not userPhone:
        userPhone = 'Not provided'

    #### (1) Create Person ####
    headersAddPerson = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config.APIKey,
    }
    bodyAddPerson = { 'name': userName, 'Userdata': userPhone }
    bodyAddPerson = json.dumps(bodyAddPerson)
    
    r = requests.post(config.urlAPI+"/persongroups/"+config.personGroupId+"/persons", headers=headersAddPerson, data=bodyAddPerson)
    res = r.json()
    
    if r.status_code == 200:
        personId = res['personId']
        
        #### (2) Add person & face(s) to PersonGroup ####
        headersAddFace = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': config.APIKey,
        }

        if len(os.listdir(config.filePath)) >0 :
            for filename in os.listdir(config.filePath):
                if filename.endswith(".jpg") or filename.endswith(".png"): 
                    imageFile = open(config.filePath+'/'+filename,'rb')
                    bodyAddFace = imageFile.read()
                    imageFile.close()

                    r2 = requests.post(config.urlAPI+"/persongroups/"+config.personGroupId+"/persons/"+personId+"/persistedFaces", headers=headersAddFace, data=bodyAddFace)
                    
                    if r2.status_code == 200:
                        faceCount += 1
                    continue
                else:
                    continue
        else:
            statusMsg = "No faces detected !" 

        #### (3) Train the PersonGroup with newly added Person & Face ####
        if faceCount >0 :
            headersTrain = {
                'Ocp-Apim-Subscription-Key': config.APIKey
            }
            
            r3 = requests.post(config.urlAPI+"/persongroups/"+config.personGroupId+"/train", headers=headersTrain)
            
            while True:
                r4 = requests.get(config.urlAPI+"/persongroups/"+config.personGroupId+"/training", headers=headersTrain)
                res4 = r4.json()
                
                if r4.status_code == 200 and res4['status'] == 'succeeded' :
                    statusMsg = "Successfully Registered " + userName + " !"
                    statusCode = 200
                    break
                
                elif r4.status_code == 200 and res4['status'] != 'succeeded':
                    time.sleep(5)
                    continue
                
                else:
                    statusMsg = "Registration Failed. Try Again Later"
                    break
        else:
            statusMsg = "No new faces available for registration"
    else:
        statusMsg = "Server Error ! Try Again"

    return statusCode, statusMsg
                



