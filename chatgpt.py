import openai
import os
import re

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
    response = openai.ChatCompletion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message

def generate_respone_v2(prompt):
    import os
    import openai
    global history
    openai.api_key = os.getenv("OPENAI_API_KEY")
    pattern = "___code____"
    new_message = CONTENT_DICT
    new_message["content"] += prompt
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    re_pattern = fr"{pattern}\s*(.*?)\s*{pattern}"
    match = re.search(re_pattern, str(completion.choices[0].message), re.DOTALL)

    # Code to extract the command
    if match:
        code = match.group(1)
        print('code extracted')
        print("")
        print("this is the extracted code",code.strip())

    # Command to execute the command
    print(str(completion.choices[0].message.content))
    system_output_response = completion.choices[0].message.content
    output_dict = {"role":"assistant", "content":f"{system_output_response}"}
    history.append(output_dict)
    history = history + history[:2]


# Get input from the user and generate a response
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    prompt = "\nUser: " + user_input
    response = generate_respone_v2(prompt)
