#!/usr/bin/env python

from flask import Flask, request, render_template, redirect, url_for,Response, session, jsonify
from camera import SecurityCam
from api import identify, sms
from apitrain import registerface
from voice import authenticate_voice
from random import randint
import time, subprocess, config, os
from colorama import init, Fore, Back, Style

init(convert=True) #For colorama

app = Flask(__name__, static_folder='static')
app.config["SECRET_KEY"] = config.secret_key

@app.route('/', methods=["GET", "POST"])
def index():

    ''' Initiate app runtime parameters '''
    
    # reset runtime status
    config.runtime = 0
    config.capturedImages = 0
    config.frameNum = 0
    config.currentUser = None
    config.currentUserPhone = None
    config.smsVerified = False
    config.smsDisplay = False
    config.identityVerified = False
    config.verificationDisplay = False
    config.currentFaceImage = None
    config.humanPresence = False
    config.humanPresenceDisplay = False

    # initiate a new session based on current unix timestamp
    config.faceSession = str(time.time())[0:10] 
    config.filePath = config.directory+'/'+config.faceSession
    if not os.path.exists(config.filePath):
        os.makedirs(config.filePath)

    return render_template('index.html')


def livestream(source):
    while True:
        frame = source.input()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(livestream(SecurityCam()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/verify_pin')
def verify_pin():
    pin = request.args.get('pin', 0, type=int)
    if pin == config.sessionPIN:
        pin_result = "PIN Correct !"
        config.smsVerified = True
        config.smsDisplay = False
    else:
        pin_result = "PIN Invalid !"
    return jsonify(pin_result=pin_result)


@app.route('/auth_voice')
def auth_voice():
    statusCode = authenticate_voice()
    if statusCode == 'Accept':
        voice_result = "Voice Authentication Successful !"
        config.identityVerified = True
        config.verificationDisplay = False
    else:
        voice_result = "Voice Authentication Failed !"
    return jsonify(voice_result=voice_result)



@app.route('/register_face')
def register_face():
    username = request.args.get('username', 'Not provided', type=str)
    userphone = request.args.get('userphone', 'Not provided', type=str)
    
    ''' Program logic to train newly captured face(s)
        User supplied information will be stored in FaceAPI - PersonGroup Person container
    '''
    
    statusCode, statusMsg = registerface(username, userphone)
    return jsonify(train_result=statusMsg, status_code=statusCode)


@app.route("/verified",  methods=["GET", "POST"])
def verified(): 
    return render_template('verified.html', userName=config.currentUser)


@app.route('/consoleStreaming')
def consoleStreaming():
    def generate2():

        '''  Begin Main Console Processing Logic  '''

        if config.runtime == 0:
            msg = "Camera Activated"
            yield "data:"+str(msg)+"\n\n"      
            config.runtime += 1

        elif config.runtime == 1:
            if config.humanPresence == True and config.humanPresenceDisplay == False:
                msg = "Face detected. Start analyzing..."
                yield "data:"+str(msg)+"\n\n"
                config.humanPresenceDisplay = True
            else:
                pass
        
            ''' Begin processing latest face image captured by camera 
                This process repeats until Id of a face is identified 
            '''

            if config.smsVerified == True and config.smsDisplay == False:
                 yield "data: SMS Verified ! Complete Voice Authentication...\n\n\n"
                 config.smsDisplay = True
            
            if config.identityVerified == True and config.verificationDisplay == False:
                 yield "data: Identity Verified ! Granting you access...\n\n\n"
                 config.verificationDisplay = True

            allFiles = os.listdir(config.filePath)
            if len(allFiles) >0:
                # Fetch most recent face image in a Session
                latestFile = max([os.path.join(config.filePath, fileName) for fileName in allFiles], key=os.path.getctime)
                _, latestFileName = os.path.split(latestFile)

                if latestFileName.endswith(".jpg") or latestFileName.endswith(".png"): 

                    if config.currentFaceImage is None or latestFileName != config.currentFaceImage:
                        
                        print(Fore.YELLOW + "[INFO] Processing image: {0}".format(latestFileName))
                        print(Style.RESET_ALL)
                    
                        # Execute Program API (Container)
                        config.currentFaceImage = latestFileName
                        statusCode,gender,age,glasses,anger,happiness,neutral,sadness,fear,surprise,personId,personName,personPhone,conf = identify(config.faceSession, latestFileName)

                        if personName is None:
                            config.currentUser = 'Unknown'
                            yield "data:"+str(statusCode)+"\n\n\n"

                        elif personName == config.currentUser:
                            pass #Skip
                        
                        elif personName != config.currentUser and conf > 0.5:
                            if statusCode == 'OK':
                                
                                # (1) Register person as the new currentUser
                                config.currentUser = personName
                                config.currentUserConf = str(int(conf * 100))+'%'
                                config.currentUserPhone = personPhone

                                # (2) Stream console outputs
                                msg = "Welcome  " + config.currentUser
                                yield "data:"+str(msg)+"\n\n\n"

                                msg = "PersonId: "+ personId
                                yield "data:"+str(msg)+"\n\n\n"
                                
                                msg = "Confidence: " + config.currentUserConf
                                yield "data:"+str(msg)+"\n\n\n"
                                
                                if glasses is not None:
                                    msg = "Attributes (Gender: " + str(gender) +", Age: "+str(age)+", Wearing Glass: Yes)"
                                else:
                                    msg = "Attributes (Gender: " + str(gender) +", Age: "+str(age)+")"
                                yield "data:"+str(msg)+"\n\n\n"
                                
                                msg = "Emtion (Anger: "+str(anger)+", Happy: "+str(happiness)+", Neutral: "+str(neutral)+", Fear: "+str(fear)+")"+", Sadness: "+str(sadness)+")"+", Surprise: "+str(surprise)+")"
                                yield "data:"+str(msg)+"\n\n\n"

                                # (3) Send PIN to registered user phone (SMS)
                                config.sessionPIN = randint(1000,9999)
                                config.smsVerified = False
                                try:
                                    yield "data: Verify PIN just sent to you (Phone: "+str(config.currentUserPhone)+")\n\n\n"
                                    # yield "data: [DEBUG] PIN: "+str(config.sessionPIN) +"\n\n\n"
                                    sms(config.sessionPIN, config.currentUserPhone)
                                except:
                                    yield "data: [ERROR] SMS delivery failed ! \n\n\n"
                            else:
                                yield "data:"+str(statusCode)+"\n\n\n"
                        else:
                            pass #Skip
                    else:
                        pass #Skip
                else:
                    pass #Skip
            else:
                pass #Skip      
        else :
            pass #Skip

    return Response(generate2(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host="localhost", debug=False)
