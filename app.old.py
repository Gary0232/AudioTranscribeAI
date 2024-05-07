import gradio as gr
import moviepy.editor as mp
import os


# interface for uploading audio or video files
def audio_recognition(filepath):
    if filepath.endswith('.mp4'):
        # convert video to audio
        video = mp.VideoFileClip(filepath)
        audio = video.audio
        audio_f = filepath.replace('.mp4', '.mp3')
        audio.write_audiofile(audio_f)
        video.close()
        audio.close()
        os.remove(filepath)
        return f"audio file saved as: {audio_f}", f"audio file saved as: {audio_f}"
    elif filepath.endswith('.mp3'):
        # 处理音频文件
        os.remove(filepath)
        return f"AUDIO FILE RECEIVED: {os.path.basename(filepath)}", f"AUDIO FILE RECEIVED: {os.path.basename(filepath)}"
    else:
        os.remove(filepath)
        return "No support file type, please upload MP4 or MP3 file", "No support file type, please upload MP4 or MP3 file"


def text_summarization(text):
    # text summarization
    return f"summarized text: {text}", f"summarized text: {text}"


with gr.Blocks() as demo:
    gr.Markdown("## AudioTranscribeAI: Efficient Speech Recognition and Language Model "
                "Integration for Enhanced Textual Interaction")
    with gr.Tab("Fully Process"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Task 1: Automatic Speech Recognition")
                audio_file = gr.File(type="filepath", label="Upload Audio or Video", file_types=["mp3", "mp4"])
                audio_recognition_button = gr.Button("Submit File")
                audio_recognition_result = gr.Label(label="Output")
            with gr.Column():
                gr.Markdown("## Task 2: Text Summarization")
                text_input = gr.Textbox(lines=9, label="Enter Text", interactive=True)
                text_summarization_button = gr.Button("Summarize Text")
                summarization_output = gr.Label(label="Output")
        gr.Markdown("---")
        gr.Markdown("## Task 3: Keyword Wiki Retrieval")

        with gr.Row():
            with gr.Column():
                source_text = gr.Textbox(lines=20, label="Enter Text", interactive=True)
            with gr.Column():
                pass
        audio_recognition_button.click(audio_recognition,
                                       inputs=audio_file,
                                       outputs=[audio_recognition_result, text_input])
        text_summarization_button.click(text_summarization, inputs=audio_recognition_result,
                                        outputs=[summarization_output, source_text])
    with gr.Tab("Single Task"):
        with gr.Tab("Automatic Speech Recognition"):
            gr.Markdown("## Upload File")

demo.launch(share=False)
