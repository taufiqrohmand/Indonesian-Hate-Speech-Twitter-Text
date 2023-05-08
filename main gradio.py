import gradio as gr
import os
import pandas as pd

from Cleansing import cleansing


def process_text(text):
    # Text Processing
    processed_text = cleansing(text)
    return processed_text

def process_file(file):
    # File Processing
    if not file.name.endswith('.csv'):
        return "Error: Please upload a CSV file"
    try:
        df = pd.read_csv(file.name)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(file.name, encoding='latin1')
        except UnicodeDecodeError:
            return "Error: Could not decode file"
    
    def clean_file(val):
        if isinstance(val, str):
            return cleansing(val)
        else:
            return val
    
    processed_df = df.applymap(clean_file)
    
    
    processed_file_path = os.path.join(os.getcwd(), 'processed_file.csv')
    processed_df.to_csv(processed_file_path, index=False)
    return processed_file_path


def process(text=None, file=None):
    if text is not None:
        processed_text = process_text(text)
    else:
        processed_text = "No text input"
    
    if file is not None:
        processed_file = process_file(file)
    else:
        processed_file = None
    
    return processed_text, processed_file

inputs = [gr.inputs.Textbox(lines=5, label="Input Text", optional=True), gr.inputs.File(label="Input File", optional=True)]
outputs = [gr.outputs.Textbox(label="Processed Text"), gr.outputs.File(label="Processed File")]

gr.Interface(fn=process, inputs=inputs, outputs=outputs).launch()