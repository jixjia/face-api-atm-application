# face-api-atm-application
Face API with container support applied to ATM use case. This is a PoC solution (Demo)


## How-to Install

Clone the git repository. Edit ``config.py`` and ``api.py`` with your favourite editor

#### ``config.py``
| Property        | Description |How TO  |
| ------------- |:-------------:| -----:|
| YOUR_FACE_API_KEY| Face API key | Get Face API key from [Cognitive Service] (https://azure.microsoft.com/en-us/try/cognitive-services/?api=face-api)|
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |


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
