#!/usr/bin/env python3

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Google Cloud Speech API sample that demonstrates how to request word
level confidence information.

Example usage:
    python transcribe_word_level_confidence.py \
        resources/Google_Gnome.wav
    python transcribe_word_level_confidence.py \
        gs://cloud-samples-tests/speech/Google_Gnome.wav
"""

import argparse


# [START speech_transcribe_word_level_confidence]
def speech_transcribe_word_level_conf(speech_file):
    """Transcribe the given audio file synchronously with
      word level confidence."""
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    with open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_confidence=True)

    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
        print(u'First Word and Confidence:{} {}'.format(
            alternative.words[0].word, alternative.words[0].confidence))
# [END speech_transcribe_word_level_confidence]


# [START speech_transcribe_word_level_confidence_gcs]
def speech_transcribe_word_level_conf_gcs(gcs_uri):
    """Transcribe the given audio file asynchronously with
      word level confidence."""
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()

    audio = speech.types.RecognitionAudio(uri=gcs_uri)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_confidence=True)

    print('Waiting for operation to complete...')
    response = client.recognize(config, audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print('-' * 20)
        print('First alternative of result {}'.format(i))
        print(u'Transcript: {}'.format(alternative.transcript))
        print(u'First Word and Confidence:{} {}'.format(
            alternative.words[0].word, alternative.words[0].confidence))
# [END speech_transcribe_word_level_confidence_gcs]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')

    args = parser.parse_args()

    if args.path.startswith('gs://'):
        speech_transcribe_word_level_conf_gcs(args.path)
    else:
        speech_transcribe_word_level_conf(args.path)
