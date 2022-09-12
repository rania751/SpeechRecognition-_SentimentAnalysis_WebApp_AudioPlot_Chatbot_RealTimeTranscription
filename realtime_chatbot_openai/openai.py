import openai
from api_secret import API_KEY_OPENAI

openai.api_key = API_KEY_OPENAI


#OpenAI’s API provides access to GPT-3, which performs a wide variety of natural language tasks, and Codex, #
#which translates natural language to code.
#The OpenAI API can be applied to virtually any task that involves understanding or generating natural language or code. 
#We offer a spectrum of models with different levels of power suitable for different tasks, as well as the ability to fine-tune your own custom models. 
#These models can be used for everything from content generation to semantic search and classification.


def ask_computer(prompt):
 
    res = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100
        )
    
    # print(res)
    return res["choices"][0]["text"]