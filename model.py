#!/usr/bin/env python
# -*-coding:utf-8 -*-
import spacy
from log import new_logger
from asr.asr_for_custom_data import transcribe_audio_for_custom_data
from llm.llm import text_summarization, question_answer

logger = new_logger("model")

# load the spacy model
nlp = spacy.load('en_core_web_sm')


def audio_recognition(audio_filepath: str, language_name: str):
    """
    Recognize the audio and return the text and tokens
    :param audio_filepath:  The path of the audio file
    :param language_name: The language of the audio
    :return: dict of text, tokens, original_text, is_translation
    """
    result = transcribe_audio_for_custom_data(audio_filepath, language=language_name)
    if not result:
        raise Exception("Audio recognition failed")
    en_script = result["native_transcription"] if not result["is_translation"] else result["translation"]
    original_language = result.get("native_transcription", None)
    # nlp = nlp_map.get(language_name)
    # if not nlp:
    #     raise Exception("Unsupported language")
    doc = nlp(en_script)
    tokens = []
    for token in doc:
        if token.whitespace_:
            tokens.append({'text': token.text, 'pos': token.pos_})
            tokens.append({'text': ' ', 'pos': 'SPACE'})
        else:
            tokens.append({'text': token.text, 'pos': token.pos_})
    return {"text": en_script,
            "tokens": tokens,
            "original_text": original_language,
            "is_translation": result["is_translation"]}


def summarization(text):
    """
    Summarize the text
    :param text: The input text
    :return: The summarized text
    """
    return text_summarization(text)


def qa(input_text, question_text):
    """
    Answer the question based on the input text
    :param input_text: The input text
    :param question_text: The question text
    :return: The answer
    """
    return question_answer(input_text, question_text)
