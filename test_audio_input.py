from audio_input import get_audio_stream

def main():
    # Initialize audio stream
    audio_stream = get_audio_stream()

    print("Starting audio stream. Press Ctrl+C to stop.")
    
    try:
        # Read and print the first few audio chunks
        for _ in range(10):  # Adjust the number of chunks as needed
            audio_chunk = next(audio_stream)
            print(f"Received audio chunk of size: {len(audio_chunk)}")
    except KeyboardInterrupt:
        print("Stopping audio stream.")

if __name__ == "__main__":
    main()
