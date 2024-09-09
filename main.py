import time
import pyaudio
import wave
import os
from volume_adjustment import adjust_volume

def record_sample(duration=5, filename="original_sample.wav"):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print(f"Recording for {duration} seconds...")

    frames = []

    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(filename):
    CHUNK = 1024

    wf = wave.open(filename, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    print(f"Playing {filename}...")

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()

def main():
    # Record a sample
    record_sample(duration=5, filename="original_sample.wav")

    # Play the original sample
    play_audio("original_sample.wav")

    # Process the sample with volume reduction
    with wave.open("original_sample.wav", 'rb') as wf:
        audio_data = wf.readframes(wf.getnframes())

    reduced_audio = next(adjust_volume([audio_data], volume_reduction=0.8))

    # Save the reduced audio
    with wave.open("reduced_sample.wav", 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # Assuming 16-bit audio
        wf.setframerate(44100)
        wf.writeframes(reduced_audio)

    # Play the reduced sample
    play_audio("reduced_sample.wav")

    # Clean up
    os.remove("original_sample.wav")
    os.remove("reduced_sample.wav")

if __name__ == "__main__":
    main()
