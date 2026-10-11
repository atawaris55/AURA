import sounddevice as sd 
from scipy.io.wavfile import write 
def record_audio(filename='input.wav',duration=5,fs=16000):
    print('Listening...')
    audio=sd.rec(int(duration*fs), samplerate=fs,channels=1,dtype='int16')
    sd.wait()
    write(filename,fs,audio)
    print("Recording saved:",filename)
    return filename 
if __name__=='__main__':
    record_audio()