import os
import tempfile
from fastapi import UploadFile
from pydub import AudioSegment

def audio_reformat(audio_file):    
    # Extract file extension
    file_ext = os.path.splitext(audio_file)[-1][1:]  # Get the file extension without '.'
    #Log out the file ext
    print(f"THE FILE IS TYPE:{file_ext}")
    # Load the audio from the file path
    sound = AudioSegment.from_file(audio_file, format=file_ext)
    
    # Convert the audio to match Azure STT requirements
    sound = sound.set_channels(1)  # Set to mono
    sound = sound.set_sample_width(2)  # Set to 16 bits per sample (2 bytes = 16 bits)
    sound = sound.set_frame_rate(16000)  # Set to 16000 samples per second
    
    # Create a new WAV filename or save to another temporary file
    wav_filepath = os.path.splitext(audio_file)[0] + '.wav'
    
    # Export the audio to WAV format
    sound.export(wav_filepath, format='wav')
    
    return wav_filepath  # Return the path to the converted WAV file