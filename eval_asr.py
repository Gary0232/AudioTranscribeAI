from datasets import load_dataset
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
from evaluate import load


def load_model_and_processor():
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small").to("cuda")
    return model, processor


def process_audio_samples(batch, model, processor):
    audio = batch["audio"]
    input_features = processor(audio["array"], sampling_rate=audio["sampling_rate"], return_tensors="pt").input_features
    batch["reference"] = processor.tokenizer._normalize(batch['text'])

    with torch.no_grad():
        predicted_ids = model.generate(input_features.to("cuda"))[0]
    transcription = processor.decode(predicted_ids)
    batch["prediction"] = processor.tokenizer._normalize(transcription)
    return batch


def main():
    librispeech_test_clean = load_dataset("librispeech_asr", "clean", split="test")
    model, processor = load_model_and_processor()
    result = librispeech_test_clean.map(lambda batch: process_audio_samples(batch, model, processor))
    wer_metric = load("wer")
    wer_score = 100 * wer_metric.compute(references=result["reference"], predictions=result["prediction"])
    print(wer_score)
