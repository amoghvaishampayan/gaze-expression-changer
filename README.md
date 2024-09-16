# gaze-expression-changer
A gradio app that uses live portrait running on a comfy ui backend to change the gaze and expression of a portrait in real time

## Installation
1. Install ComfyUI
2. Download the ComfyUI custom node [Advanced Live Portrait](https://github.com/PowerHouseMan/ComfyUI-AdvancedLivePortrait).
3. Get the [live portrait models from here](https://huggingface.co/Kijai/LivePortrait_safetensors/tree/main)
4. Put the white-bg.png file in the relative path of ComfyUI installation .../ComfyUI/input/gradioapp/white-bg.png . This file serves as placeholder input when the user removes the previous input and is going to upload a new one. Since the workflow triggers on every change, this prevents the comfy backend api from receiving a None input for the image and throwing an error.

## Input image*
Upload an image containing a person's face whose gaze or expression you want to change. This is a mandatory field.

## Reference iamge
Upload an image containing a reference image of another person's face. The gaze and expression will be extracted and applied to the input image. Optional input

## Sliders
Change these for the respective change to be reflected in the output.
1. Rotate head up and down
2. Rotate head left and right
3. Rotate head sideways
4. Close eyes
5. Move eyebrows
6. Wink eye
7. Move eyeballs up and down
8. Move eyeball left and right
9. Open mouth
10. Widen mouth
11. Circular mouth
12. Smile
13. Src ratio

Refresh the page to reset to defaults.
