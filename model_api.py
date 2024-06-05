import replicate
import os
import google.generativeai as genai
import config


def thin_plate_spline_motion(img, video_tag_switch):
    if video_tag_switch:
        video = "data/v1.mp4"
    else:
        video = "data/v2.mp4"
    os.environ["REPLICATE_API_TOKEN"] = "r8_4Fs17YBFe6lGopG0Z0BjsxDN2bg9acB2QJvzW"
    output = replicate.run(
        "yoyo-nb/thin-plate-spline-motion-model:382ceb8a9439737020bad407dec813e150388873760ad4a5a83a2ad01b039977",
        input={"source_image": open(img, "rb"), "driving_video": open(video, "rb")}
    )
    #dataset_name string
    # Choose a dataset.
    # Allowed values:vox, taichi, ted, mgif
    # Default value: vox

    # out is uri : example: https://replicate.delivery/pbxt/NHZcFRW1eyUpNS5TbhqUyAOHnoGC4b49YSecAEyeLu90M0eFB/output.mp4
    return output



class Assistant:
    def __init__(self):
        print(dir(genai))
        genai.configure(api_key=config.Gemini_api_key)

        # Set up the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        self.model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                           generation_config=generation_config,
                                           safety_settings=safety_settings)

        self.convo = self.model.start_chat(history=[])

    def ask_question(self, question):
        self.convo.send_message(question)
        return self.convo.last.text
