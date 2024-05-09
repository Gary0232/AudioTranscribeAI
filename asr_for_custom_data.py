import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import Audio, load_dataset
import soundfile as sf


def translate_audio_samples(dataset, num_samples, language="japanese"):
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    forced_decoder_ids = processor.get_decoder_prompt_ids(language=language, task="translate")
    dataset = dataset.cast_column("audio", Audio(sampling_rate=16_000))
    transcriptions = []

    for sample in dataset.take(num_samples):
        input_speech = sample["audio"]
        input_features = processor(input_speech["array"], sampling_rate=input_speech["sampling_rate"],
                                   return_tensors="pt").input_features
        predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        transcriptions.append(transcription)

    return transcriptions


def transcribe_audio(sample, processor, model):
    input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"],
                               return_tensors="pt").input_features
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

    return transcription


def transcribe_audio_samples(dataset, num_samples):
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    model.config.forced_decoder_ids = None

    transcriptions = []

    for sample in dataset.take(num_samples):
        input_features = processor(sample["audio"]["array"], sampling_rate=sample["audio"]["sampling_rate"],
                                   return_tensors="pt").input_features

        predicted_ids = model.generate(input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        transcriptions.append(transcription[0])

    return transcriptions


def transcribe_foreign_audio(dataset, num_samples, language="japanese"):
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

    forced_decoder_ids = processor.get_decoder_prompt_ids(language=language, task="transcribe")

    dataset = dataset.cast_column("audio", Audio(sampling_rate=16_000))

    transcriptions = []

    for sample in dataset.take(num_samples):
        input_features = processor(sample["audio"]["array"], sampling_rate=sample["audio"]["sampling_rate"],
                                   return_tensors="pt").input_features

        predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)

        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        transcriptions.append(transcription[0])

    return transcriptions


def process_language(language_code, language_name, num_samples=10):
    ds = load_dataset("mozilla-foundation/common_voice_11_0", language_code, split="test", streaming=True,
                      trust_remote_code=True)

    translate_result = translate_audio_samples(ds, num_samples, language=language_name)
    transcribe_result = transcribe_foreign_audio(ds, num_samples, language=language_name)
    return translate_result, transcribe_result

def transcribe_audio_for_custom_data(file_path, language="english"):
    print("Loading audio file...")

    audio, sr = sf.read(file_path)
    if sr != 16000:
        print(f"Resampling from {sr} Hz to 16000 Hz...")
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        sr = 16000

    print("Loading model and processor...")
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

    task_type = 'translate' if language != 'english' else 'transcribe'
    print(f"Preparing to {task_type}...")

    if language != "english":
        forced_decoder_ids = processor.get_decoder_prompt_ids(language=language, task="translate")
    else:
        forced_decoder_ids = None

    print("Processing audio...")
    input_features = processor(audio, sampling_rate=sr, return_tensors="pt").input_features

    print("Generating native transcription...")
    native_transcription_ids = model.generate(input_features)
    native_transcription = processor.batch_decode(native_transcription_ids, skip_special_tokens=True)

    if language != "english":
        print("Generating translation...")
        translation_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
        translation = processor.batch_decode(translation_ids, skip_special_tokens=True)
        print("Native Transcription: ", native_transcription[0])
        print("Translation: ", translation[0])
        return native_transcription[0], translation[0]
    else:
        print("Native Transcription: ", native_transcription[0])
        return native_transcription[0]
def main():
    languages = {
        "ja": "japanese",
        "fr": "french",
        "de": "german",
        "es": "spanish",
        "ru": "russian"
    }
    file_path = 'audio_data/fr/common_voice_fr_33153455.mp3'
    transcribe_audio_for_custom_data(file_path, language="french")

if __name__ == "__main__":
    main()
