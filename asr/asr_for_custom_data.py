import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import Audio, load_dataset
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
    chunk_length_ms = chunk_length_s * 1000  # Convert to milliseconds
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks
def transcribe_audio_chunk(audio_chunk, sr=16000, language="english"):
    """
    Transcribe a single audio chunk using Whisper.
    Args:
        audio_chunk: An audio segment chunk
        sr: Sampling rate (default is 16000 Hz)
        language: Language for transcription or translation
    Returns:
        Transcribed or translated text
    """
    task_type = 'translate' if language != 'english' else 'transcribe'
    if language != "english":
        forced_decoder_ids = processor.get_decoder_prompt_ids(language=language, task=task_type)
    else:
        forced_decoder_ids = None
    # Export audio chunk to temporary file
    chunk_path = "temp_chunk.wav"
    audio_chunk.export(chunk_path, format="wav")
    # Load the chunk into memory
    sample, sr = librosa.load(chunk_path, sr=sr)
    # Process the audio sample
    input_features = processor(sample, sampling_rate=sr, return_tensors="pt").input_features
    # Generate transcription or translation
    predicted_ids = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
    return transcription[0]


def transcribe_long_audio(audio_path, chunk_length_s=30, language="english", max_workers=8):
    """
    Transcribe long audio files by splitting them into smaller chunks.
    Args:
        audio_path: Path to the audio file
        chunk_length_s: Length of each chunk in seconds (default 30s = 30 seconds)
        language: Language for transcription or translation
        max_workers: Number of threads to use for parallel processing
    Returns:
        Full transcribed text
    """
    chunks = split_audio(audio_path, chunk_length_s)
    full_transcription = [""] * len(chunks)

    print(f"Transcribing audio in {chunk_length_s}-second chunks using {max_workers} threads...")

    def transcribe_chunk_wrapper(index, chunk):
        return index, transcribe_audio_chunk(chunk, language=language)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(transcribe_chunk_wrapper, i, chunk): i for i, chunk in enumerate(chunks)}

        with tqdm(total=len(futures), desc="Transcribing Chunks", unit="chunk") as pbar:
            for future in as_completed(futures):
                index, transcribed_text = future.result()
                full_transcription[index] = transcribed_text
                pbar.update(1)

    return " ".join(full_transcription)

def transcribe_audio_for_custom_data(file_path, language="english"):
    logger.info("Loading audio file...")

    chunk_length_s = 30  # 30-second chunks
    total_duration_s = librosa.get_duration(filename=file_path)

    if total_duration_s > 2 * 60 * 60:
        logger.error("Audio duration exceeds the maximum allowed limit of 2 hours.")
        return {"error": "Audio duration exceeds the maximum allowed limit of 2 hours."}

    transcribed_text = transcribe_long_audio(file_path, chunk_length_s=chunk_length_s, language=language)
    audio, sr = sf.read(file_path)
    if sr != 16000:
        print(f"Resampling from {sr} Hz to 16000 Hz...")
        audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        sr = 16000

    if language != "english":
        input_features = processor(audio, sampling_rate=sr, return_tensors="pt").input_features
        native_transcription_ids = model.generate(input_features)
        native_transcription = processor.batch_decode(native_transcription_ids, skip_special_tokens=True)
        return {
            "native_transcription": transcribed_text,
            "is_translation": True,
            "translation": native_transcription[0]
        }
    else:
        return {
            "native_transcription": transcribed_text,
            "is_translation": False
        }


def main():
    languages = {
        "ja": "japanese",
        "fr": "french",
        "de": "german",
        "es": "spanish",
        "ru": "russian"
    }

    file_path = '../audio_data/fr/common_voice_fr_33153455.mp3'
    result = transcribe_audio_for_custom_data(file_path, language="french")
    logger.info(result)


if __name__ == "__main__":
    main()
