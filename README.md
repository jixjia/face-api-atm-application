# face-api-atm-application
Face API with container support applied to ATM use case. This is a PoC solution (Demo)


## How-to Install

Clone the git repository
Edit ``config.py`` and ``api.py`` with your favourite editor

#### 1. ``config.py``
| Variable | How-to |
|**YOUR_FACE_API_KEY**| Get Face API key from [Cognitive Service] (https://azure.microsoft.com/en-us/try/cognitive-services/?api=face-api)|



**YOUR_PERSON_GROUP_ID** : 
Go to [Face API testing console](https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236)
Type in any value to the personGroupId box.
This value is also the value for YOUR_PERSON_GROUP_ID.
copy and paste your face API key to the Ocp-Apim-Subscription-Key box.
click send at the bottom of the page.

YOUR_TWILIO_ACCOUNT_SID / YOUR_TWILIO_AUTH_TOKEN :
Register a trial Twilio account at www.twilio.com
Go to account page and find your ACCOUNT SID and AUTH TOKEN

(OPTIONAL)FLASK_RANDOM_SECRET_KEY_ANY :
leave this blank

YOUR_SPEAKER_RECOGNITION_API_KEY :
generate your speaker API key from https://projectoxfordkeysignup.azurewebsites.net/

YOUR_TEST_USER_VOICE_PROFILE_ID :
Option 1 : go to https://westus.dev.cognitive.microsoft.com/docs/services/563309b6778daf02acc0a508/operations/56406930e597ed20c8d8549d/console
Type in any value to the verificationProfileId box.
This value is also the value for YOUR_SPEAKER_RECOGNITION_API_KEY.
copy and paste your speaker API key to the Ocp-Apim-Subscription-Key box.
Record an audio file of your voice.
Convert the audio file to WAV file, 16K rate, 16bit sample format, Mono channel.
Conver the WAV file to binary data and paste into the "Request body" in the testing console.
Option 2 : go to https://rposbo.github.io/speaker-recognition-api/
paste your speaker API key and click go, follow the instruction on the screen to create your verificationProfileId

2. api.py
Go to your Twilio account page and find your Twilio phone number.
Copy and paste this number (including the '+' and country code) to #YOUR_TWILLIO_PHONE_NUMBER

3. running the application
Run main.py with python3.x using Anaconda prompt
Wait for a few seconds until the console shows "Running on http://localhost:5000/"
Open Chrome and go to localhost:5000

## Business Use Case
![Alt text](/screenshot/atm-use-case.png?raw=true "ATM Use Case")

## Solution Design
![Alt text](/screenshot/solution-arch.png?raw=true "Solution Architecture")

## Screenshots

### (1) Camera detects face and attempt to identify its ID
![Alt text](/screenshot/note1.jpg?raw=true)

### (2) Enter Authentication PIN received via SMS
![Alt text](/screenshot/note2.jpg?raw=true)

### (3) User perform Voice Authentication
![Alt text](/screenshot/note3.jpg?raw=true)

Authentication outcome:
![Alt text](/screenshot/voice_auth_outcome.png?raw=true)

### (4) Access Teller Screen upon security clearance
![Alt text](/screenshot/note4.jpg?raw=true)

### (5) Register new unknown user 
![Alt text](/screenshot/note5.jpg?raw=true)

### (6) Application "learns" about user's face on the spot
![Alt text](/screenshot/note6.jpg?raw=true)

### (7) User behaviour is recorded at backend for security purpose
![Alt text](/screenshot/face_recording.png?raw=true)
