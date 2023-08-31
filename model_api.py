# from gradio_client import Client
#
# client = Client("https://hysts-controlnet-v1-1.hf.space/")
# result = client.predict(
# 				"https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image) in 'parameter_8' Image component
# 				"Howdy!",	# str in 'Prompt' Textbox component
# 				"Howdy!",	# str in 'Additional prompt' Textbox component
# 				"Howdy!",	# str in 'Negative prompt' Textbox component
# 				1,	# int | float (numeric value between 1 and 1) in 'Number of images' Slider component
# 				256,	# int | float (numeric value between 256 and 768) in 'Image resolution' Slider component
# 				1,	# int | float (numeric value between 1 and 100) in 'Number of steps' Slider component
# 				0.1,	# int | float (numeric value between 0.1 and 30.0) in 'Guidance scale' Slider component
# 				0,	# int | float (numeric value between 0 and 2147483647) in 'Seed' Slider component
# 				1,	# int | float (numeric value between 1 and 255) in 'Canny low threshold' Slider component
# 				1,	# int | float (numeric value between 1 and 255) in 'Canny high threshold' Slider component
# 				api_name="/canny"
# )
#
# print(result)


import replicate
import os

def thin_plate_spline_motion(img):
    os.environ["REPLICATE_API_TOKEN"] = "r8_4Fs17YBFe6lGopG0Z0BjsxDN2bg9acB2QJvzW"
    output = replicate.run(
        "yoyo-nb/thin-plate-spline-motion-model:382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977",
        input={"source_image": open(img, "rb"), "driving_video": open("data/v1.mp4", "rb")}
    )
    #dataset_name string
    # Choose a dataset.
    # Allowed values:vox, taichi, ted, mgif
    # Default value: vox

    # out is uri : example: https://replicate.delivery/pbxt/NHZcFRW1eyUpNS5TbhqUyAOHnoGC4b49YSecAEyeLu90M0eFB/output.mp4
    return output

