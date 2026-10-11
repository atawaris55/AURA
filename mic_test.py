
import sounddevice as sd
import soundfile as sf

duration = 5
sample_rate = 44100
device_id = 1

print("AURA: Speak now! Recording for 5 seconds...")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="float32",
    device=device_id
)

sd.wait()

sf.write("voice_test.wav", audio, sample_rate)

print("Recording saved as voice_test.wav")
