###############################################
## Voice Authentication Main Program
## (1) Record Voice (16KHz, 1 Ch, 16 bit, Mono, container=WAV)
## (2) Authenticate Voice
## Created by: Jixin Jia (09-Jan-2018)
###############################################

import urllib.parse, json, requests, config, pyaudio, wave


def authenticate_voice():
    ''' Record voice and convert to required audio format
    '''
    audioFormat = pyaudio.paInt16
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=audioFormat, channels=config.channels,
                    rate=config.sampleRate, input=True,
                    frames_per_buffer=config.chunk)
    print ("recording...")
    frames = []
    
    for i in range(0, int(config.sampleRate / config.chunk * config.record_sec)):
        data = stream.read(config.chunk)
        frames.append(data)
    print ("finished")
    
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(config.wav_output, 'wb')
    waveFile.setnchannels(config.channels)
    waveFile.setsampwidth(audio.get_sample_size(audioFormat))
    waveFile.setframerate(config.sampleRate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


    ''' Authenticate user with Speaker Recognition API
        against pre-registered voiceProfileId
    '''
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': config.voiceKey,
    }

    params = urllib.parse.urlencode({
        'verificationProfileId' : config.verificationProfileId
    })

    '''Passphrase 
    my voice is my passport. verify me
    '''

    audioFile = open(config.wav_output,'rb')
    body = audioFile.read()
    audioFile.close()

    r = requests.post(config.voiceAPI+'/verify?%s' %params, headers=headers, data=body)
    res = r.json()

    print("Response Status: ", r.status_code)
    print("Raw JSON response: ", res)

    if r.status_code == 200:
        statusCode = res['result']
    else:
        statusCode = 'rejected'
    
    return statusCode