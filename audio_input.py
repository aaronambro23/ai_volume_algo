import pyaudio

def get_audio_stream(chunk_size=1024, rate=44100):
    """
    Initializes an audio stream from the microphone and yields audio chunks.
    
    Args:
        chunk_size (int): The size of each audio chunk (default 1024 bytes).
        rate (int): Sample rate for the audio stream (default 44100 Hz).
    
    Yields:
        Audio data chunks from the microphone.
    """
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open an input stream with the desired parameters
    stream = p.open(format=pyaudio.paInt16,  # 16-bit format
                    channels=1,             # Mono audio (1 channel)
                    rate=rate,              # Sample rate (44100 samples/sec)
                    input=True,             # It's an input stream (we're recording)
                    frames_per_buffer=chunk_size)  # Number of frames per buffer (size of each chunk)

    # Continuously yield audio chunks from the stream
    while True:
        audio_chunk = stream.read(chunk_size)  # Read the chunk from the input stream
        yield audio_chunk  # Yield it for further processing

    # This cleanup would be outside the loop, but it won't reach here in a continuous stream
    stream.stop_stream()
    stream.close()
    p.terminate()
