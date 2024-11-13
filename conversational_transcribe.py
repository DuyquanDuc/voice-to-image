from dotenv import load_dotenv
#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
"""
Conversation transcription samples for the Microsoft Cognitive Services Speech SDK
"""

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)
import os
from audio_file_converter import audio_reformat


# Load env variables
load_dotenv('local.env')
#Retrieve Secrets
speech_key=os.getenv("ACS_SUBSCRIPTION_KEY")
service_region = os.getenv("ACS_SUBSCRIPTION_REGION")

def conversation_transcription(convo):
    """Transcribes a conversation from a WAV file."""
    #Turn the input to a WAV 16000 hz file
    convo = audio_reformat(convo)

    # Create speech configuration with subscription info
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region, speech_recognition_language="ja-JP")

    # Create audio configuration from the input WAV file
    audio_config = speechsdk.audio.AudioConfig(filename=convo)

    # Initialize the conversation transcriber
    transcriber = speechsdk.transcription.ConversationTranscriber(speech_config, audio_config)

    transcribed_text = ""  # Variable to store concatenated transcription
    done = False  # Flag to control the transcription process

    # Callback to stop transcription
    def stop_cb(evt: speechsdk.SessionEventArgs):
        #print('CLOSING {}'.format(evt))
        nonlocal done
        done = True

    # Callback to handle transcriptions as they come in
    def transcribed_cb(evt: speechsdk.SpeechRecognitionEventArgs):
        nonlocal transcribed_text
        transcribed_text += f"""Text: {evt.result.text}\n
                                Speaker: {evt.result.speaker_id}"""
        print(f"TRANSCRIBED: Speaker: {evt.result.speaker_id}, Text: {evt.result.text}")

    # Subscribe to events
    transcriber.transcribed.connect(transcribed_cb)
    transcriber.session_stopped.connect(stop_cb)
    transcriber.canceled.connect(stop_cb)

    # Start continuous transcription
    transcriber.start_transcribing_async()
    #print("Transcribing...")
    # Keep the program running until transcription is complete
    while not done:
        pass  # Simple loop to keep the transcription active until completion

    # Stop the transcriber after transcription is done
    transcriber.stop_transcribing_async()
    
    # Return the final transcribed text
    return transcribed_text