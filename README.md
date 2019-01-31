# face-api-atm-application
Face API with container support applied to ATM use case. This is a PoC solution (Demo)


## How-to Install

Clone the git repository.   
Edit file ``config.py`` and ``api.py`` with your favourite editor as following:

### config.py
Create and put following keys in to this configuration file:  

| Property        | Description |How To|
|:------------- |:-------------|:-----|
|YOUR_FACE_API_KEY| Face API key |Get Face API key from [Cognitive Service Face API](https://azure.microsoft.com/en-us/try/cognitive-services/?api=face-api)|
|YOUR_PERSON_GROUP_ID      | Face API's person group container Id      |Go to [Face API test console](https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395244/console) and create a new personGroupId (any name will do) using your Face API key |
|YOUR_TWILIO_ACCOUNT_SID YOUR_TWILIO_AUTH_TOKEN | Twilio account's SID and authorization token | Register a trial Twilio account at [Twilio](http://www.twilio.com). Go to account page and find your ACCOUNT SID and AUTH TOKEN |
|YOUR_SPEAKER_RECOGNITION_API_KEY| Speaker Recognition API key | Get Speaker API key from [Cognitive Service Speaker Recognition API](https://azure.microsoft.com/en-us/services/cognitive-services/speaker-recognition/) |
|YOUR_TEST_USER_VOICE_PROFILE_ID| Speaker's voice profile Id | Go to [Speaker Recognition test console](https://westus.dev.cognitive.microsoft.com/docs/services/563309b6778daf02acc0a508/operations/56406930e597ed20c8d8549d/console) and create a new verificationProfileId (any name will do) using your Speaker Recognition API key|

Record an audio file of your voice:
Go to [here](https://rposbo.github.io/speaker-recognition-api/)
Paste your speaker API key and click go, follow the instruction on the screen to create your verificationProfileId

### api.py
Go to your Twilio account page and find your Twilio phone number.  
Copy and paste this number (including the '+' and country code) to #YOUR_TWILLIO_PHONE_NUMBER

### Running the application
Run ``main.py`` with python3.x to start the program.   
Wait for a few seconds until the console shows "Running on http://localhost:5000/"  
Open Chrome/Firefox (note IE and Edge is not officially supported)  


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
