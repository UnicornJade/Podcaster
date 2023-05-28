import os
import streamlit
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def translate(file_path,destlang):
    def openai_translate(text,lang):
        en2zh = """I've been working on my podcasts recently, and I have a lot of podcasts that have a lot of people talking to each other before, and my podcasts are just my monologues, so I need to translate those into my monologue podcasts, where I'm telling the story. Here's what I need you to do with my transcript: 1. Delete other people's speeches: Please delete other people's speeches from the audio and keep only my podcast monologue transcript 2. Incorporate the conversation: Please incorporate the responses and questions from the conversation into my presentation, in the style of a podcast monologue. 3. Remove filler words and catchphrases: Please remove or reduce filler words, catchphrases, and unnecessary pauses in your podcast monologue. Correct grammar and sentence patterns: Please correct grammar and sentence patterns to make it more fluid, concise, and easy to understand. 5. Delete noise and non-verbal sounds: Please delete noise, noise and non-verbal sounds in the audio, such as background music and coughing. 6. Cohesion and transition: Add cohesion and transition sentences to make the podcast monologue flow more smoothly between the storylines.As a solo podcast host, here are some tips and considerations to guide you in improving your storytelling, engaging your audience, and delivering impactful content:
Speaking Style and Format:
Clarity: Use concise and clear language to express your ideas, avoiding excessive details and complex sentence structures.
Logical Flow: Organize your thoughts and present them in a logical sequence to ensure coherence and coherence in the information you share.
Engaging Narrative: Make your storytelling more engaging by incorporating vivid language, personal anecdotes, humor, and relatable experiences.
Style and Tone:
Authenticity: Stay true to your own style and voice, avoiding excessive imitation or artificiality.
Approachability: Establish a connection with your audience by using a friendly and approachable tone that makes them feel understood and valued.
Encouraging Interaction: Foster audience participation and engagement by encouraging discussions, questions, and feedback through comments, emails, or other interactive platforms.
Emotion and Expression:
Emotional Connection: When appropriate, express emotions and sentiments to foster a deeper connection with your audience.
Respectful Language: Avoid offensive, demeaning, or discriminatory language, and show respect for your audience's backgrounds, perspectives, and experiences.
Smooth Delivery and Language:
Practice Delivery: Prepare your scripts in advance and practice delivering them to ensure smoothness and naturalness in your presentation.
Use Concise Language: Avoid overly complex vocabulary and long sentences, and instead, use concise language that enhances understandability.
Avoid Rambling: Eliminate unnecessary or tangential information, maintaining concise and focused content.
Storylines and Plot Development:
Structured Narratives: If your content involves stories or narratives, ensure they have engaging beginnings, well-developed plots, and satisfying resolutions to captivate your audience.
Use Examples and Case Studies: Provide specific examples and real-life case studies to enhance understanding and allow listeners to connect with your content.
Above all, maintain a genuine passion and enthusiasm for your subject matter. Approach your podcast with sincerity and dedication, and share your knowledge and experiences with authenticity. Continuously reflect on your delivery, listen to feedback from your audience, and make adjustments as needed. Practice and accumulate experience to develop your unique podcasting style that suits your personality and resonates with your listeners.
        
        Here is the original version of my podcast:{text} Note: The output should not contain your response to my previous request, only the subject of the podcast.The podcast
         that translated to Fluent and vivid Chinese language:"""
        zh2en = """I've been working on my podcasts recently, and I have a lot of podcasts that have a lot of people talking to each other before, and my podcasts are just my monologues, so I need to translate those into my monologue podcasts, where I'm telling the story. Here's what I need you to do with my transcript: 1. Delete other people's speeches: Please delete other people's speeches from the audio and keep only my podcast monologue transcript 2. Incorporate the conversation: Please incorporate the responses and questions from the conversation into my presentation, in the style of a podcast monologue. 3. Remove filler words and catchphrases: Please remove or reduce filler words, catchphrases, and unnecessary pauses in your podcast monologue. Correct grammar and sentence patterns: Please correct grammar and sentence patterns to make it more fluid, concise, and easy to understand. 5. Delete noise and non-verbal sounds: Please delete noise, noise and non-verbal sounds in the audio, such as background music and coughing. 6. Cohesion and transition: Add cohesion and transition sentences to make the podcast monologue flow more smoothly between the storylines.As a solo podcast host, here are some tips and considerations to guide you in improving your storytelling, engaging your audience, and delivering impactful content:
Speaking Style and Format:
Clarity: Use concise and clear language to express your ideas, avoiding excessive details and complex sentence structures.
Logical Flow: Organize your thoughts and present them in a logical sequence to ensure coherence and coherence in the information you share.
Engaging Narrative: Make your storytelling more engaging by incorporating vivid language, personal anecdotes, humor, and relatable experiences.
Style and Tone:
Authenticity: Stay true to your own style and voice, avoiding excessive imitation or artificiality.
Approachability: Establish a connection with your audience by using a friendly and approachable tone that makes them feel understood and valued.
Encouraging Interaction: Foster audience participation and engagement by encouraging discussions, questions, and feedback through comments, emails, or other interactive platforms.
Emotion and Expression:
Emotional Connection: When appropriate, express emotions and sentiments to foster a deeper connection with your audience.
Respectful Language: Avoid offensive, demeaning, or discriminatory language, and show respect for your audience's backgrounds, perspectives, and experiences.
Smooth Delivery and Language:
Practice Delivery: Prepare your scripts in advance and practice delivering them to ensure smoothness and naturalness in your presentation.
Use Concise Language: Avoid overly complex vocabulary and long sentences, and instead, use concise language that enhances understandability.
Avoid Rambling: Eliminate unnecessary or tangential information, maintaining concise and focused content.
Storylines and Plot Development:
Structured Narratives: If your content involves stories or narratives, ensure they have engaging beginnings, well-developed plots, and satisfying resolutions to captivate your audience.
Use Examples and Case Studies: Provide specific examples and real-life case studies to enhance understanding and allow listeners to connect with your content.
Above all, maintain a genuine passion and enthusiasm for your subject matter. Approach your podcast with sincerity and dedication, and share your knowledge and experiences with authenticity. Continuously reflect on your delivery, listen to feedback from your audience, and make adjustments as needed. Practice and accumulate experience to develop your unique podcasting style that suits your personality and resonates with your listeners.
Here is the original version of my podcast:{text} Note: The output should not contain your response to my previous request, only the subject of the podcast. The podcast that make sure the subject language is English:"""
        if lang == 'en':
            template = zh2en
        elif lang == 'zh':
            template = en2zh
        else:
            template = en2zh
    
        llm = ChatOpenAI(temperature=0)
        prompt = PromptTemplate(
            input_variables=["text"],  # 提示词·可控变量
            template=template,
        )
        chain = LLMChain(llm=llm, prompt=prompt)
        translated = chain.run(text).strip()
        return translated

    with open(file_path,"r") as file:
        content = file.read()
    # print(content)
    translated = openai_translate(content,destlang)
    # print(translated)
    translated_name = file_path.split('/')[-1]
    with open(f"./results/audio2txt/translated/{translated_name}","w") as file:
        file.write(translated)
    print("[ * ] Translate finished💡. ")