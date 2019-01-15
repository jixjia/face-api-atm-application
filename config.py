global frameNum
global intervalRate
global capturedImages
global directory
global training
global urlAPI
global APIKey
global personGroupId 
global account_sid
global auth_token
global secret_key

# Application config
directory = "./captured"
voice = "./voice"
urlAPI = 'https://westus.api.cognitive.microsoft.com/face/v1.0'
voiceAPI = 'https://westus.api.cognitive.microsoft.com/spid/v1.0'
APIKey = '{YOUR_FACE_API_KEY}'
personGroupId = '{YOUR_PERSON_GROUP_ID}'
account_sid = '{YOUR_TWILLIO_ACCOUNT_SID}' 
auth_token = '{YOUR_TWILLIO_TOKEN}'
secret_key = '{FASK_RANDOM_SECRET_KEY_ANY}'
voiceKey = '{YOUR_SPEAKER_RECOGNITION_API_KEY}'
verificationProfileId = '{YOUR_TEST_USER_VOICE_PROFILE_ID}'

# Do not change these settings (Required by Azure Speaker Recognition API)
channels = 1
sampleRate = 16000
chunk = 1024
record_sec = 4
wav_output = voice+'/voice_recording.wav'


# Runtime parameters
humanPresence = False
frameNum = 0
intervalRate = 120
capturedImages = 0
runtime = 0
faceSession = None
filePath = None
currentUser = None
currentUserConf = None
currentUserPhone = None
currentFaceImage = None
sessionPIN = None
smsVerified = False
smsDisplay = False
identityVerified = False
verificationDisplay = False
humanPresenceDisplay = False