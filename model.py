#!/usr/bin/env python
# -*-coding:utf-8 -*-
import spacy
from log import new_logger
from asr.asr_for_custom_data import transcribe_audio_for_custom_data
from llm.llm import text_summarization, question_answer

logger = new_logger("model")


nlp = spacy.load('en_core_web_sm')


# fr_nlp = spacy.load('fr_core_news_sm')
# de_nlp = spacy.load('de_core_news_sm')
# ja_nlp = spacy.load('ja_core_news_sm')
# ru_nlp = spacy.load('ru_core_news_sm')
# es_nlp = spacy.load('es_core_news_sm')
#
# nlp_map = {
#     "english": en_nlp,
#     "french": fr_nlp,
#     "german": de_nlp,
#     "japanese": ja_nlp,
#     "russian": ru_nlp,
#     "spanish": es_nlp
# }


def audio_recognition(audio_filepath, language_name):
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
    return text_summarization(text)


def qa(input_text, question_text):
    return question_answer(input_text, question_text)
