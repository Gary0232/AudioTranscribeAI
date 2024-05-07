#!/usr/bin/env python
# -*-coding:utf-8 -*-
import gradio as gr

def print_text(text):
    return "Hello World, " + text

interface = gr.Interface(fn=print_text, inputs="text", outputs="text")
interface.launch()