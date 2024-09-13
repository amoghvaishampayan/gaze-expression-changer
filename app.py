import json
import os
import time
import random
import sys

import gradio as gr
import requests
import numpy as np

from PIL import Image

URL = "http://127.0.0.1:8188/prompt"
OUTPUT_DIR = "C:/Users/amogh/OneDrive/Documents/ComfyUI_windows_portable/ComfyUI/output/gradioapp"

def get_latest_image(folder):
   files = os.listdir(folder)
   image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))] #order the file according to the last file created
   image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
   latest_image = os.path.join(folder, image_files[-1]) if image_files else None
   return latest_image

def get_latest_reference_image(folder):
    files = os.listdir(folder)
    image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))] #order the file according to the last file created
    image_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)))
    latest_image = os.path.join(folder, image_files[-1]) if image_files else None
    return latest_image   

def start_queue (prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    requests.post(URL, data = data)

def genererate_random_seed():
    seed = random.randint(0, 2**32 - 1)  # Random integer between 0 and the maximum 32-bit value
    return seed

def generate_image(input_image, reference_image, rotate_pitch, rotate_yaw, rotate_roll, 
                  blink, eyebrow, wink, pupil_y, pupil_x, aaa, eee, woo, smile, src_ratio):
    # Define paths
    expressions_image_path = "C:/Users/amogh/OneDrive/Documents/ComfyUI_windows_portable/ComfyUI/input/gradioapp/expressions-image.png"
    reference_image_path = "C:/Users/amogh/OneDrive/Documents/ComfyUI_windows_portable/ComfyUI/input/gradioapp/reference-image.png"
    white_bg_image_path = "C:/Users/amogh/OneDrive/Documents/ComfyUI_windows_portable/ComfyUI/input/gradioapp/white-bg.png"
    
    # Initialize variables
    config_file = None
    
    # Determine which API config to use based on input conditions
    if input_image is not None and reference_image is not None:
        # Scenario 2: Both input and reference images are provided
        config_file = "expressions+face_api.json"
        # Save input image
        Image.fromarray(input_image).save(expressions_image_path)
        # Save reference image
        Image.fromarray(reference_image).save(reference_image_path)
    elif input_image is not None and reference_image is None:
        # Scenario 1: Only input image is provided
        config_file = "reference_bypassed_api.json"
        # Save input image
        Image.fromarray(input_image).save(expressions_image_path)
    elif input_image is None and reference_image is not None:
        # Scenario 3: Reference image is provided, input image is removed
        config_file = "expressions+face_api.json"
        # Use white background image as input
        Image.open(white_bg_image_path).save(expressions_image_path)
        # Save reference image
        Image.fromarray(reference_image).save(reference_image_path)
    else:
        # Scenario 4: Both input and reference images are removed
        config_file = "reference_bypassed_api.json"
        # Use white background image as input
        Image.open(white_bg_image_path).save(expressions_image_path)
    
    # Load the appropriate workflow config
    with open(config_file, "r") as file_json:
        prompt = json.load(file_json)
    
    # **Always** set the prompt's image input to "gradioapp/expressions-image.png"
    prompt["15"]["inputs"]["image"] = "gradioapp/expressions-image.png"
    
    prompt["110"]["inputs"]["rotate_pitch"] = rotate_pitch
    prompt["110"]["inputs"]["rotate_yaw"] = rotate_yaw
    prompt["110"]["inputs"]["rotate_roll"] = rotate_roll
    prompt["110"]["inputs"]["blink"] = blink
    prompt["110"]["inputs"]["eyebrow"] = eyebrow
    prompt["110"]["inputs"]["wink"] = wink
    prompt["110"]["inputs"]["pupil_y"] = pupil_y
    prompt["110"]["inputs"]["pupil_x"] = pupil_x
    prompt["110"]["inputs"]["aaa"] = aaa
    prompt["110"]["inputs"]["eee"] = eee
    prompt["110"]["inputs"]["woo"] = woo
    prompt["110"]["inputs"]["smile"] = smile
    prompt["110"]["inputs"]["src_ratio"] = src_ratio
     
    previous_image = get_latest_image(OUTPUT_DIR)

    start_queue(prompt)
    
    while True:
        latest_image = get_latest_image(OUTPUT_DIR)
        if latest_image !=previous_image:
            return latest_image

        time.sleep(1)


# def reset_all(input_image, reference_image, rotate_pitch, rotate_yaw, rotate_roll, blink, eyebrow, wink, pupil_y, pupil_x, aaa, eee, woo, smile, src_ratio):
#     """Reset all inputs and sliders to their default values."""
#     # Return None for images and default values for sliders
#     return None, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1

# def reset_sliders():
#     """Reset only the sliders to their default values."""
#     # Return default values in the order of the sliders
#     return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1

with gr.Blocks() as demo:
    # Header Row: Title and Restart Button
    with gr.Row():
        title = gr.Markdown("# Dash Actor", elem_id="title")  # Title on the left
        
    gr.Markdown("---")  # Separator

    with gr.Row():
        input_image = gr.Image(label="Input Image", type="numpy")
        reference_image = gr.Image(label = "Reference image (optional)", type = "numpy")

    with gr.Row():    
        with gr.Column():
            rotate_pitch = gr.Slider(minimum=-20, maximum=20, step=1, value=0, label="Rotate head up and down")
            rotate_yaw = gr.Slider(minimum=-20, maximum=20, step=1, value=0, label="Rotate head left and right")
            rotate_roll = gr.Slider(minimum=-20, maximum=20, step=1, value=0, label="Rotate head sideways")
            blink = gr.Slider(minimum=-20, maximum=5, step=1, value=0, label="Close eyes")
        with gr.Column():
            eyebrow = gr.Slider(minimum=-10, maximum=15, step=1, value=0, label="Move eyebrows")
            wink = gr.Slider(minimum=0, maximum=25, step=1, value=0, label="Wink eye")
            pupil_y = gr.Slider(minimum=-15, maximum=15, step=1, value=0, label="Move eyeballs up and down")
            pupil_x = gr.Slider(minimum=-15, maximum=15, step=1, value=0, label="Move eyeball left and right")
        with gr.Column():
            aaa = gr.Slider(minimum=-30, maximum=120, step=1, value=0, label="Open mouth")
            eee = gr.Slider(minimum=-20, maximum=15, step=1, value=0, label="Widen mouth")
            woo = gr.Slider(minimum=-20, maximum=15, step=1, value=0, label="Circular mouth")
            smile = gr.Slider(minimum=-0.3, maximum=1.3, step=0.1, value=0, label="Smile")
            src_ratio = gr.Slider(minimum=0, maximum=1, step=0.1, value=1, label="Src ratio")

    # with gr.Row():
    #     reset_all = gr.Button("Reset all")
    #     reset_sliders_button = gr.Button("Reset sliders")
    #     reset_sliders_button.click(fn=reset_sliders, 
    #                            inputs=None, 
    #                            outputs=[rotate_pitch, rotate_yaw, rotate_roll, 
    #                                     blink, eyebrow, wink, pupil_y, pupil_x, 
    #                                     aaa, eee, woo, smile, src_ratio])

    # Define the output image element
    output_image = gr.Image(label="Output Image")

    

    # Bind change events to all inputs (images and sliders) to trigger the live update
    input_elements = [input_image, reference_image, rotate_pitch, rotate_yaw, rotate_roll, 
                      blink, eyebrow, wink, pupil_y, pupil_x, aaa, eee, woo, smile, src_ratio]
    
    for element in input_elements:
        element.change(fn=generate_image, inputs=input_elements, outputs=[output_image])

# Launch the app
demo.launch()

    # demo = gr.Interface(fn= generate_image, inputs=[input_image, reference_image, 
    #                                                 rotate_pitch, 
    #                                                 rotate_yaw,
    #                                                 rotate_roll, 
    #                                                 blink, 
    #                                                 eyebrow, 
    #                                                 wink, 
    #                                                 pupil_y, 
    #                                                 pupil_x, 
    #                                                 aaa, 
    #                                                 eee, 
    #                                                 woo, 
    #                                                 smile, 
    #                                                 src_ratio], outputs=["image"], live=True)

#slider.change(fn=generate_image, inputs=["text", slider], outputs=["image"])


