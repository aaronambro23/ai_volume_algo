import struct

def adjust_volume(audio_stream, volume_reduction=0.95, max_chunks=None):
    """
    Adjusts the volume of audio chunks from a stream.
    
    Args:
        audio_stream: A generator that yields audio chunks.
        volume_reduction (float): Factor to reduce volume by (default 0.95).
        max_chunks (int): Maximum number of chunks to process (default None).

    Yields:
        bytes: Adjusted audio chunks.
    """
    chunk_count = 0
    for audio_chunk in audio_stream:
        # Unpack audio data
        fmt = f"{len(audio_chunk)//2}h"
        samples = struct.unpack(fmt, audio_chunk)
        
        # Adjust volume
        adjusted = [int(sample * volume_reduction) for sample in samples]
        
        # Pack adjusted audio
        adjusted_chunk = struct.pack(fmt, *adjusted)
        
        print(f"Processed audio chunk {chunk_count + 1} of length: {len(audio_chunk)}")
        
        yield adjusted_chunk

        chunk_count += 1
        if max_chunks is not None and chunk_count >= max_chunks:
            print(f"Reached maximum number of chunks ({max_chunks}). Stopping.")
            break
    
    print("Finished processing audio chunks")

# Example usage:
# from your_audio_module import AudioStream
# 
# audio_stream = AudioStream("your_audio_file.wav")
# for adjusted_chunk in adjust_volume(audio_stream, max_chunks=100):  # Process up to 100 chunks
#     # Do something with the adjusted chunk, e.g., write to a file or play
#     pass
