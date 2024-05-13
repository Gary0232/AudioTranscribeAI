import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf
from log import new_logger
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

logger = new_logger("ASR")

# Initialize the processor and model globally
processor = WhisperProcessor.from_pretrained("openai/whisper-small")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")

def split_audio(audio_path, chunk_length_s=30):
    """
    Split audio into chunks of specified length.
    Args:
        audio_path: Path to the audio file
        chunk_length_s: Length of each chunk in seconds
    Returns:
        List of audio chunks
    """
    audio = AudioSegment.from_file(audio_path)
    chunk_length_ms = chunk_length_s * 1000
    return [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

def transcribe_audio_chunk(audio_chunk, sr=16000, language="english"):
    """
    Transcribe or translate a single audio chunk using Whisper.
    Args:
        audio_chunk: An audio segment chunk
        sr: Sampling rate (default is 16000 Hz)
        language: Language for transcription or translation
    Returns:
        Dictionary containing transcribed text and optionally translated text
    """
    # Set up for transcription
    chunk_path = "temp_chunk.wav"
    audio_chunk.export(chunk_path, format="wav")
    sample, sr = librosa.load(chunk_path, sr=sr)
    input_features = processor(sample, sampling_rate=sr, return_tensors="pt").input_features

    # Transcribe in native language
    native_transcription_ids = model.generate(input_features)
    native_transcription = processor.batch_decode(native_transcription_ids, skip_special_tokens=True)[0]

    results = {"native_transcription": native_transcription}

    # Translate to English if necessary
    if language != "english":
        forced_decoder_ids = processor.get_decoder_prompt_ids(language="english", task="translate")
        translation_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
        translation = processor.batch_decode(translation_ids, skip_special_tokens=True)[0]
        results["translation"] = translation
        results["is_translation"] = True
    else:
        results["is_translation"] = False

    return results

def transcribe_long_audio(audio_path, chunk_length_s=30, language="english", max_workers=8):
    """
    Transcribe and optionally translate long audio files.
    Args:
        audio_path: Path to the audio file
        chunk_length_s: Length of each chunk in seconds
        language: Language for transcription or translation
        max_workers: Number of threads to use for parallel processing
    Returns:
        Combined transcription and optional translation
    """
    chunks = split_audio(audio_path, chunk_length_s)
    transcriptions = [""] * len(chunks)
    translations = [""] * len(chunks) if language != "english" else None

    print(f"Processing audio in {chunk_length_s}-second chunks using {max_workers} threads...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, chunk in enumerate(chunks):
            futures.append(executor.submit(transcribe_audio_chunk, chunk, sr=16000, language=language))

        with tqdm(total=len(futures), desc="Transcribing Chunks", unit="chunk") as pbar:
            for future in as_completed(futures):
                index = futures.index(future)
                result = future.result()
                transcriptions[index] = result["native_transcription"]
                if translations is not None:
                    translations[index] = result["translation"]
                pbar.update(1)

    if translations is not None:
        return " ".join(transcriptions), " ".join(translations)
    else:
        return " ".join(transcriptions), None

def transcribe_audio_for_custom_data(file_path, language="english"):
    logger.info("Loading audio file...")
    total_duration_s = librosa.get_duration(filename=file_path)
    if total_duration_s > 2 * 60 * 60:
        logger.error("Audio duration exceeds the maximum allowed limit of 2 hours.")
        return {"error": "Audio duration exceeds the maximum allowed limit of 2 hours."}

    transcriptions, translations = transcribe_long_audio(file_path, language=language)
    if translations is not None:
        response = {
            "native_transcription": transcriptions,
            "is_translation": True,
            "translation": translations
        }
    elif translations is None:
        response = {
            "native_transcription": transcriptions,
            "is_translation": False
        }
    print(117, repr(response))
    return response

def main():
    languages = {
        "ja": "japanese",
        "fr": "french",
        "de": "german",
        "es": "spanish",
        "ru": "russian"
    }

    file_path = '../audio_data/en/wk11clips.mp3'
    result = transcribe_audio_for_custom_data(file_path, language="english")
    logger.info(result)

if __name__ == "__main__":
    main()
