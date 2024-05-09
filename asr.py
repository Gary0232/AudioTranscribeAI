from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import Audio, load_dataset



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


def main():
    ds_en = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation",
                         trust_remote_code=True)
    transcription_result = transcribe_audio_samples(ds_en, 10)
    print("English transcription: ", transcription_result)

    languages = {
        "ja": "japanese",
        "fr": "french",
        "de": "german",
        "es": "spanish",
        "ru": "russian"
    }

    for code, name in languages.items():
        translated_samples, transcribed_samples = process_language(code, name, num_samples=10)
        print(f"{name.capitalize()} translated samples: ", translated_samples)
        print(f"{name.capitalize()} transcribe samples: ", transcribed_samples)


if __name__ == "__main__":
    main()