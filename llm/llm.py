import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, pipeline
import pandas as pd

import sacrebleu
from tqdm import tqdm
import os
import pdb
import re

# expected input text from audio stage
# expected output: QA / Sumamrization

# used https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
model_name = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'
# model_name = 'meta-llama/Llama-2-7b-chat-hf'

pipe = pipeline("text-generation", model=model_name, torch_dtype=torch.float16, device_map="auto")


def question_answer(input_text, question_text, prompt_template="background text: {}, question: {}"):
    messages = [
        {
            "role": "system",
            "content": "You are a expert question answer chat bot who always responds in the style of professional, you will be givin a background text, and a question, you need to answerthe question based on the background text",
        },
        {"role": "user", "content": prompt_template.format(input_text, question_text)},
    ]

    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    outputs = outputs[0]["generated_text"]

    if model_name == "TinyLlama/TinyLlama-1.1B-Chat-v1.0":
        outputs = outputs.split("<|assistant|>")[1].strip()
    elif model_name == "meta-llama/Llama-2-7b-chat-hf":
        outputs = outputs.split("[/INST]")[-1].strip()

    return outputs


def text_summarization(input_text, prompt_template="please summarize the text: {}"):
    messages = [
        {
            "role": "system",
            "content": "You are a expert text summarization who always responds in the style of professional, please direct output the summarization, without other unnecessary sentences.",
        },
        {"role": "user", "content": prompt_template.format(input_text)},
    ]

    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    outputs = outputs[0]["generated_text"]

    # get <|assistant|>
    if model_name == "TinyLlama/TinyLlama-1.1B-Chat-v1.0":
        outputs = outputs.split("<|assistant|>")[1].strip()
    elif model_name == "meta-llama/Llama-2-7b-chat-hf":
        outputs = outputs.split("[/INST]")[-1].strip()

    return outputs


def cal_bleu(reference, hypothesis):
    bleu = sacrebleu.corpus_bleu([hypothesis], [[reference]])
    return bleu.score


def evaluation(test_df, prompt_template):
    # make test_df a datasets
    pred_df = pd.DataFrame(columns=["Input", "Ground Truth", "Prediction", "BLEU Score"])

    all_bleu = 0
    counter = 0

    pbar = tqdm(total=len(test_df), desc="Evaluating")

    for i in range(len(test_df)):
        input = test_df.iloc[i]["ctext"]
        model_output = text_summarization(input, prompt_template)
        gt = test_df.iloc[i]["text"]
        bleu_score = cal_bleu(gt, model_output)
        all_bleu += bleu_score
        counter += 1
        running_avg = all_bleu / counter

        pred_df = pd.concat([pred_df, pd.DataFrame([[input, gt, model_output, bleu_score]],
                                                   columns=["Input", "Ground Truth", "Prediction", "BLEU Score"])])

        pbar.set_postfix({"BLEU": running_avg})
        pbar.update(1)

    return running_avg, pred_df


if __name__ == "__main__":
    # dataset from https://www.kaggle.com/datasets/sunnysai12345/news-summary
    data_df = pd.read_csv("../data/news_summary/news_summary_sampled.csv")
    # drop the row containing NaN
    data_df = data_df.dropna()

    prompt_template = ["summarize: {}", "summarize the text: {}", "please summarize the text: {}"]

    eval_performance_df = pd.DataFrame(columns=["Prompt", "BLEU Score"])

    for prompt in prompt_template:
        print(f"Prompt: {prompt}")
        bleu_score, pred_df = evaluation(data_df, prompt)

        # save pred_df
        if not os.path.exists("../llm_eval_results"):
            os.makedirs("../llm_eval_results")

        save_path = os.path.join("../llm_eval_results", model_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        pred_df.to_csv(os.path.join(save_path, f"{prompt}_pred_df.csv"), index=False)

        eval_performance_df = pd.concat(
            [eval_performance_df, pd.DataFrame([[prompt, bleu_score]], columns=["Prompt", "BLEU Score"])])
        print(f"BLEU Score: {bleu_score}")
        print("\n")

    # save
    eval_performance_df.to_csv(os.path.join(save_path, "eval_performance_df.csv"), index=False)


# if __name__ == '__main__':
#     ori_text = "So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So we first talk about the background and the significance of recommended systems. And then we'll move on to talk about some of the details about the recommendation algorithms, including collaborative filtering, content-based and learning-based and context-aware recommendation. And then finally, we'll talk about how to evaluate recommended systems. So recommendation is everywhere. So here we just provide a list of the benefits of recommendation systems. So we see that the first one is that you can use the recommendation systems to provide a list of the benefits of recommendation systems. So here we have a list of the benefits of recommendation systems. So we see that the first one is that you can use the recommendation systems to provide a list of the benefits of recommendation systems. Um"
    
#     # res = text_summarization(ori_text)
#     res = question_answer(ori_text, "what is the significance of recommended systems?")
#     pdb.set_trace()