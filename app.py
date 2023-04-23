from flask import Flask, render_template, request
import requests


#VARIABLES FOR PROMPPTS
character_img_prompt_system = '''You are an image generation prompt maker, I will feed you some prompts so that you can see the structure of how a prompt should be written. PLease tell me what you understood at the end.
                                Before jumping into the prompts there are some VERY IMPORTANT things to keep in mind:
                                1.	He word order is very important in the prompts, the earlier a word appears the more impact it will have on the final image, so specify important details earlier on.
                                2.	Mostly use noun-adjective pairs, keep the verb usage at a absolute minimum.

                                !!VERY IMPORTANT!! You will only work on portraits, you will recive big descriptions of characters and you will create prompts based on them.
                                The model you will create the prompts for is called Stable Diffusion.
                                Lets look at an example  prompt:

                                “Hyperrealist portrait of female by david hockney and alphonse mucha,and giger, black hair, blue eyes black and white painting, fantasy art, photo realistic, dynamic lighting, artstation, poster, volumetric lighting, very detailed faces, 4 k, award winning”
                                Here are the most important things:
                                1. Begin the prompt with the type of artwork:  “Hyperrealist portrait of”, “close up photo of”, “portrait of”, etc
                                2. After the kind of the picture include the main subject, “woman”, “man”, etc. Make sure this is kept concise, don’t add unecesary details because this might throw off the model.
                                3. After that include relevant artist names, make sure the artists are relevant to the concept, you wouldn’t want an abstract art artist on a cyberpunk image.
                                4. After that add the features of your subject, for example : dark hair, blue eyes, smooth skin, scars, etc.
                                5. After that add style tags, these tags control the asthetic of the final image, for example : black and white painting, fantasy art, photo realistic, dynamic lighting, artstation, poster, volumetric lighting, very detailed faces, 4 k, award winning. These words are very important in shaping the final image, words like art station and award wining don’t mean that the artwork is literaly award wining or on art station, it just helps the model search thru the dataset for these kind of imaged because most of the time they are high quality.

                                Things to avoid:


                                1. The model dosnt know who the subject is, instead of saying its name you should include the characteristcs , instead of saying Nicolae "The Iron Hand" Alexandrescu, you shoudl describe him, for example : cyberpunk man. NEVER INCLUDE STORY SPECIFING ELEMENTS, DONT NAME CHARACTERS, PLACES, JUST DESCRIBE THEIR APPARANCE USING NORMAL NOUN ADJECTIVE PAIRS.
                                2. The description is too verbose. You should not tell a story , this is not how a prompt works, its not made from sentences, its made from diffrent elements.  You used too many verbs.
                                For example descriptions like:
                                "The gritty urban background and dynamic lighting give the image a sense of tension and danger." Is is a big error, you should specify individual elements separated by commas, it should sound more like this:
                                gritty urban backround, dynamic lighting, tension
                                4. You included too many details. for example this part:
                                "His weathered face and hardened exterior reflect his past as a soldier, but his strong sense of morality and justice shine through in his eyes, conveying his dedication to protecting the weak and fighting against corruption."
                                Should be completly non existant, when you mention a feature you just mention that feature, not how the subject aquierd that feature. This couyld all be summerized in: weatherd face, harden expresion.'''


character_img_prompt_user = '''give me a prompt for : In the underground world of Hollow Knight, there exists a beetle who goes by the name of Scarab. Scarab is a resident of the Kingdom of Hallownest, a once great kingdom that has fallen into ruins. Scarab is a skilled warrior who has dedicated his life to restoring Hallownest to its former glory. As a member of the Hallownest army, Scarab was tasked with protecting the kingdom from external threats. However, as the kingdom began to crumble from within, Scarab realized that his true duty lay in helping to rebuild it. He became a trusted advisor to the few remaining insects of the kingdom, using his knowledge of the land and his combat expertise to help them survive in the difficult conditions. Scarab is also known for being a fierce protector of the weak and vulnerable bugs in the kingdom, often putting himself in harm's way to ensure their safety. His bravery and selflessness have earned him many allies, despite his gruff exterior. As the player journeys through the underground world, they will encounter Scarab on many occasions, from battlefields to crumbling ruins. Scarab offers the player valuable advice and quests to aid in their journey, utilizing his extensive knowledge of the kingdom. Scarab is also a capable fighter, with his beetle exoskeleton providing ample protection in battles. He wields a formidable spear in combat, and his lightning-fast strikes can devastate foes if they're not careful. In the end, Scarab is not just a warrior, but a symbol of hope in a world that has lost much of its former glory. He reminds the player that even in the darkest of times, there is always the potential for light to shine through.'''

character_img_prompt_assistent = '''Portrait of beetle ,bug,  warrior, exoskeleton , strong, muscular, majestic,fantasy art,  photo realistic, dynamic lighting, artstation, poster, volumetric lighting, very detailed faces, 4 k, award winning'''
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


app = Flask(__name__)

# Set up API key and endpoint URL
API_KEY = "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"
ENDPOINT = "https://api.openai.com/v1/chat/completions"
IMG_API = "https://091a13f12aed3e5c05.gradio.live"

@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_response', methods=['POST'])
def get_response():
    user_question = request.form['question']

    # Compose input messages
    messages = [
        {"role": "system", "content": "You are an AI world builder, the user will input a concept for his world and you will expand on it, make it detailed."},
        {"role": "user", "content": user_question},
    ]

    # Set up headers with API key for authentication
    headers = { 
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Set up data with input messages and model parameter
    data = {
        "messages": messages,
        "model": "gpt-3.5-turbo"
    }

    # Send POST request to the ChatGPT API
    response = requests.post(ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        # Extract assistant's response from API response
        result = response.json()
        concept_extins = result["choices"][0]["message"]["content"]

        #locatia

        messages = [
            {"role": "system", "content": "You are an AI world builder, the user will input a concept for his world and you will create a location, a important place in that world, make it detailed., only describe its visual apearance"},
            {"role": "user", "content": concept_extins},
        ]

        # Set up headers with API key for authentication
        headers = { 
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # Set up data with input messages and model parameter
        data = {
            "messages": messages,
            "model": "gpt-3.5-turbo"
        }

        # Send POST request to the ChatGPT API
        response = requests.post(ENDPOINT, headers=headers, json=data)

        if response.status_code == 200:
            # Extract assistant's response from API response
            result = response.json()
            locatie1 = result["choices"][0]["message"]["content"]

            #location prompt

            messages = [
            {"role": "system", "content": '''You are an image generation prompt maker, I will feed you some prompts so that you can see the structure of how a prompt should be written. PLease tell me what you understood at the end.

            Prompts these are composed of more details about the asthetic, for example look at this prompt:
            It s very important to only include visual clues in the prompt, if you recive a long text concentrate on the visual aspect, I mostly interested in landscapes, landscapes are the most importsant.
            Before jumping into the prompts there are some VERY IMPORTANT things to keep in mind, the word order is very important in the prompts, the earlier a word appears the more impact it will have on the final image, so specify important details earlier on.

            Prompt:

            A forbidden castle high up in the mountains, (intricate details:1.12), hdr, (intricate details, hyperdetailed:1.15), (natural skin texture, hyperrealism, soft light, sharp:1.2), game art, key visual, surreal

            As you can see its focused more on certain keywords like: hyperrealism, soft light, sharp:1.2), game art, key visual, surreal
            This is the basic of prompt engeniring, The description of the scene should be pretty short and it should not contain many verbs, mainly use noun-adjective, always separate elements by a comma. Let's look at another prompt:

            8k portrait of beautiful cyborg with brown hair, intricate, elegant, highly detailed, majestic, digital photography, art by artgerm and ruan jia and greg rutkowski surreal painting gold butterfly filigree, broken glass, (masterpiece, sidelighting, finely detailed beautiful eyes: 1.2), hdr,


            Its recomanded to start the prompt with key words like: masterpiece, 8K.
            In this example you can also see that the description of the scene is quite short, most of the prompt is composed of key words, also use artist names that are relevant to the style.

            Lets see another prompt:

            (extremely detailed CG unity 8k wallpaper), full shot body photo of the most beautiful artwork in the world, beautiful women, sunset, professional majestic oil painting by Ed Blinkey, Atey Ghailan, Studio Ghibli, by Jeremy Mann, Greg Manchess, Antonio Moro, trending on ArtStation, trending on CGSociety, Intricate, High Detail, Sharp focus, dramatic, photorealistic painting art by midjourney and greg rutkowski

            Its important that when creating prompts to specify what type of image it is, for example:"full shot body photo ", "portrait of", "a painting of" , "b&w photo of", etc.
            Here are some other prompts:
            (masterpiece), (extremely intricate), fantasy, (((photorealistic photo of an evil hermit, male, villain, anti hero, evil face, masculine face, medium hair, Maroon hair, wicked, cruel, sinister, malicious, ruthless, masculine, athletic))), (((dark bloody clothing, intricate details on clothing))), (perfect composition:1.4), aspect ratio 1:1, beach, deviantart hd, artstation hd, concept art, detailed face and body, award-winning photography, margins, detailed face, professional oil painting by Ed Blinkey, Atey Ghailan, Jeremy Mann, Greg Manchess, Alex Gray, trending on ArtStation, trending on CGSociety, intricate, high detail, sharp focus, dramatic, award winning matte drawing cinematic lighting octane render unreal engine volumetrics dtx

            Here are some other prompts:
            "(masterpiece), (extremely intricate), fantasy, (((photorealistic photo of an evil hermit, male, villain, anti hero, evil face, masculine face, medium hair, Maroon hair, wicked, cruel, sinister, malicious, ruthless, masculine, athletic))), (((dark bloody clothing, intricate details on clothing))), (perfect composition:1.4), aspect ratio 1:1, beach, deviantart hd, artstation hd, concept art, detailed face and body, award-winning photography, margins, detailed face, professional oil painting by Ed Blinkey, Atey Ghailan, Jeremy Mann, Greg Manchess, Alex Gray, trending on ArtStation, trending on CGSociety, intricate, high detail, sharp focus, dramatic, award winning matte drawing cinematic lighting octane render unreal engine volumetrics dtx
            "

            "oil on matte canvas, sharp details, the expanse scifi spacescape ceres colony, intricate, highly detailed, digital painting, rich color, smooth, sharp focus, illustration, Unreal Engine 5, 8K, art by artgerm and greg rutkowski and alphonse mucha"
            "(8k, best quality, masterpiece:1.2),(best quality:1.0), (ultra highres:1.0), watercolor, a beautiful woman, shoulder, hair ribbons, by agnes cecile, half body portrait, extremely luminous bright design, pastel colors, (ink:1.3), autumn lights"


            Now I want to teach you about negative prompts, negative prompts are used to tell the model what to exclude in the image, for every prompt you generate I want you to also include a negative prompt, lets set some ground rules:
            1. Very IMPORTANT! Icluse in the negative prompt keywords that contradict your prompt. For example in a prompt that contains: watercolor,you will include words like:cartoon, 3d to help the model.
            2.When generating humans use these key words like this in your negative prompt: ((morbid)), ((mutilated)), [out of frame], extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck))), Photoshop, video game, ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, cross-eye, body out of frame, blurry, bad art, bad anatomy,.

            As an image generation prompt maker, I understand that a prompt should be composed of concise descriptions of the image, using noun-adjective and separating elements by a comma. It's important to include relevant keywords and artist names, and to specify what type of image it is, such as "full shot body photo" or "portrait of." Starting with key words like "masterpiece" or "8K" is also recommended.

            Negative prompts should include keywords that contradict the prompt, such as using words like "cartoon" or "3D" for a watercolor prompt. When generating humans, negative prompts should include words like "morbid," "mutilated," and "ugly," as well as mentioning poorly drawn or deformed body parts.'''},
            {"role": "user", "content": ''' Create a prompt for this location:

            The piece being described here is a captivating digital art that is truly a masterpiece in terms of its quality. The use of cinematic lighting in this artwork is particularly striking, with the colors being vivid and the contrast being very high. The mountain landscape is particularly eerie and unsettling, with twisted trees and lush grass that give it an almost mystical quality.

            This artwork has a horror theme, which is accentuated by the use of a menacing monster that seems to be lurking in the shadows. The atmosphere is dark and foreboding, with the use of blood rain pouring down from the sky, a blood-red river flowing through the scene, and a haunting blood moon in the sky. All of these elements come together to create a chilling and intense visual experience that is sure to stay with the viewer long after they have finished looking at the piece.

            In terms of the technical aspects of the artwork, the use of color is particularly effective. The colors are bright and bold, which helps to draw the viewer's eye to different parts of the scene. The contrast is also very high, which helps to create a sense of depth and texture that is particularly effective when it comes to the mountain landscape.

            Overall, this artwork is a stunning example of digital art that combines a captivating aesthetic with a horror theme. The use of cinematic lighting, colorful imagery, and high contrast all come together to create a truly immersive experience for the viewer. The addition of the menacing monster, blood rain, blood river, and blood moon all add to the dark and unsettling atmosphere of the scene, making this a piece of artwork that is sure to leave a lasting impression on anyone who views it.'''},
            {"role": "assistant", "content": ''' Ok, here is your prompt: 
            (masterpiece, best quality:1.4), cinematic light, colorful, high contrast, mountain, grass, tree, night, (horror (theme):1.2), (mon(masterpiece, best quality:1.4), (captivating digital art), cinematic lighting, colorful, high contrast, eerie mountain landscape, lush grass, twisted trees, night scene, (horror theme:1.2), (menacing monster:1.2) lurking in shadows, dark atmosphere, blood rain pouring down, blood-red river flowing, haunting blood moon in the sky, chilling and intense visual experiencester:1.2), dark, blood rain, blood river, blood moon'''},
            {"role": "user", "content":  concept_extins},
            ]

            # Set up headers with API key for authentication
            headers = { 
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            # Set up data with input messages and model parameter
            data = {
                "messages": messages,
                "model": "gpt-3.5-turbo"
            }

            # Send POST request to the ChatGPT API
            response = requests.post(ENDPOINT, headers=headers, json=data)

            if response.status_code == 200:
                # Extract assistant's response from API response
                result = response.json()
                locatie1_p = result["choices"][0]["message"]["content"]
                print(locatie1_p)
            
                import json
                import io
                import base64
                from PIL import Image, PngImagePlugin

                url = IMG_API

                payload = {
                    "prompt": locatie1_p,
                    "steps": 25,
                    "width": 1024,
                    "height": 512
                }

                response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

                r = response.json()
                for i in r['images']:
                    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

                    png_payload = {
                        "image": "data:image/png;base64," + i
                    }
                    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

                    pnginfo = PngImagePlugin.PngInfo()
                    pnginfo.add_text("parameters", response2.json().get("info"))
                    image.save('locimg1.png', pnginfo=pnginfo)
                    # Read the image file and convert to base64 encoding
                    with open('locimg1.png', 'rb') as image_file:
                        locimg1 = base64.b64encode(image_file.read()).decode('utf-8')
                    print(locimg1)
                
                #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

                messages = [
                {"role": "system", "content": "You are an AI world builder, the user will input a concept for his world and you will create a major event that happend at some point that changed the world"},
                {"role": "user", "content": concept_extins},
                ]

                # Set up headers with API key for authentication
                headers = { 
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }

                # Set up data with input messages and model parameter
                data = {
                    "messages": messages,
                    "model": "gpt-3.5-turbo"
                }

                # Send POST request to the ChatGPT API
                response = requests.post(ENDPOINT, headers=headers, json=data)

                if response.status_code == 200:
                    # Extract assistant's response from API response
                    result = response.json()
                    historie_1 = result["choices"][0]["message"]["content"]
                    
                    import json
                    import io
                    import base64
                    from PIL import Image, PngImagePlugin

                    url = IMG_API

                    payload = {
                        "prompt": historie_1,
                        "steps": 25
                    }

                    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

                    r = response.json()
                    for i in r['images']:
                        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

                        png_payload = {
                            "image": "data:image/png;base64," + i
                        }
                        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

                        pnginfo = PngImagePlugin.PngInfo()
                        pnginfo.add_text("parameters", response2.json().get("info"))
                        image.save('locimg2.png', pnginfo=pnginfo)
                        # Read the image file and convert to base64 encoding
                        with open('locimg2.png', 'rb') as image_file:
                            istimg1 = base64.b64encode(image_file.read()).decode('utf-8')
                        print(istimg1)
                        #jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj

                        messages = [
                        {"role": "system", "content": "You are an AI world builder, the user will input a concept for his world and you will create character that lives in that world and is important"},
                        {"role": "user", "content": concept_extins},
                        ]

                        # Set up headers with API key for authentication
                        headers = { 
                            "Authorization": f"Bearer {API_KEY}",
                            "Content-Type": "application/json"
                        }

                        # Set up data with input messages and model parameter
                        data = {
                            "messages": messages,
                            "model": "gpt-3.5-turbo"
                        }

                        # Send POST request to the ChatGPT API
                        response = requests.post(ENDPOINT, headers=headers, json=data)

                        if response.status_code == 200:
                            # Extract assistant's response from API response
                            result = response.json()
                            caracter_1 = result["choices"][0]["message"]["content"]

                            messages = [
                            {"role": "system", "content": character_img_prompt_system},
                            {"role": "user", "content": character_img_prompt_user},
                            {"role": "assistant", "content": character_img_prompt_assistent},
                            {"role": "user", "content": caracter_1},
                            ]

                            # Set up headers with API key for authentication
                            headers = { 
                                "Authorization": f"Bearer {API_KEY}",
                                "Content-Type": "application/json"
                            }

                            # Set up data with input messages and model parameter
                            data = {
                                "messages": messages,
                                "model": "gpt-3.5-turbo"
                            }
                            response = requests.post(ENDPOINT, headers=headers, json=data)
                            if response.status_code == 200:
                                # Extract assistant's response from API response
                                result = response.json()
                                caracter_1_prompt  = result["choices"][0]["message"]["content"]

                                url = IMG_API

                                payload = {
                                    "prompt": caracter_1_prompt,
                                    "steps": 25
                                }

                                response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
                                print(caracter_1_prompt)

                                r = response.json()
                                for i in r['images']:
                                    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

                                    png_payload = {
                                        "image": "data:image/png;base64," + i
                                    }
                                    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

                                    pnginfo = PngImagePlugin.PngInfo()
                                    pnginfo.add_text("parameters", response2.json().get("info"))
                                    image.save('locimg2.png', pnginfo=pnginfo)
                                    # Read the image file and convert to base64 encoding
                                    with open('locimg2.png', 'rb') as image_file:
                                        carimg1 = base64.b64encode(image_file.read()).decode('utf-8')
                                    print(istimg1)
                                    print(character_img_prompt_system,caracter_1, locatie1, locatie1_p, locimg1, concept_extins, historie_1, character_img_prompt_system)
                            
                                return render_template('index.html', concept_extins=concept_extins,locatie1= locatie1,historie1=historie_1, caracter1=caracter_1,locimg1 = locimg1, istimg1=istimg1, carimg1=carimg1)

            
