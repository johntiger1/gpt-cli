import openai
import os
import re
import subprocess

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up the GPT-3 model
model_engine = "gpt-3.5-turbo"

CONTENT_DICT = {"role": "user", "content": f"Produce ONLY an executable shell command for the following prompt. "
                                    f"Do not include any explanation or natural language. The prompt will begin now."
                                    }

history = [
    {"role": "system", "content": "You are shellGPT. You return runnable shell commands only. Produce"
                                      "an error message if appropriate.}"},
        CONTENT_DICT]
# Define a function to generate a response
def generate_response(prompt):
    global history
    pattern = "___code____"
    new_message = CONTENT_DICT
    new_message["content"] += prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    # Command to execute the command
    system_output_response = completion.choices[0].message.content
    output_dict = {"role":"assistant", "content":f"{system_output_response}"}
    history.append(output_dict)
    history = history + history[:2]
    return system_output_response


# Get input from the user and generate a response
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    prompt = "\nUser: " + user_input
    print("\n")
    response = str(generate_response(prompt))
    print("The generated command that will be run is:\n")
    print(response)
    user_input = input("Execute Command?(Y/N) ")

    if user_input.lower() == "y":
         os.system(response)
    print("\n")