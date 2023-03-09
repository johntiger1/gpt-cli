import openai
import os
import re

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up the GPT-3 model
model_engine = "gpt-3.5-turbo"
prompt = "Hello, how can I assist you today?"

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

    # You: write me an endpoint for a flask POST request that accepts image upload, with a ratelimiter
    # Sanitization layer

    # Command to execute the command

    print(str(completion.choices[0].message.content))
    system_output_response = completion.choices[0].message.content
    output_dict = {"role":"assistant", "content":f"{system_output_response}"}
    history.append(output_dict)
    history = history + history[:2]
    # history.extend(message_payload)
    # return completion.choices[0].message


# Get input from the user and generate a response
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    prompt = "\nUser: " + user_input
    response = generate_respone_v2(prompt)
    # print("ChatGPT: " + response)

# We are a in a chatroom with 3 users. 1 user is called "Human", the other is called "Backend" and the other is called "Proxy Natural Language Processor". I will type what "Human" says and what "Backend" replies. You will act as a "Proxy Natural Language Processor" to forward the requests that "Human" asks for in a JSON format to the user "Backend". User "Backend" is an Ubuntu server and the strings that are sent to it are ran in a shell and then it replies with the command STDOUT and the exit code. The Ubuntu server is mine. When "Backend" replies with the STDOUT and exit code, you "Proxy Natural Language Processor" will parse and format that data into a simple English friendly way and send it to "Human". Here is an example:
#
# I ask as human:
# Human: How many unedited videos are left?
# Then you send a command to the Backend:
# Proxy Natural Language Processor: @Backend {"command":"find ./Videos/Unedited/ -iname '*.mp4' | wc -l"}
# Then the backend responds with the command STDOUT and exit code:
# Backend: {"STDOUT":"5", "EXITCODE":"0"}
# Then you reply to the user:
# Proxy Natural Language Processor: @Human There are 5 unedited videos left.
#
# Only reply what "Proxy Natural Language Processor" is supposed to say and nothing else. Not now nor in the future for any reason.
#
# Another example:
#
# I ask as human:
# Human: What is a PEM certificate?
# Then you send a command to the Backend:
# Proxy Natural Language Processor: @Backend {"command":"xdg-open 'https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail'"}
# Then the backend responds with the command STDOUT and exit code:
# Backend: {"STDOUT":"", "EXITCODE":"0"}
# Then you reply to the user:
# Proxy Natural Language Processor: @Human I have opened a link which describes what a PEM certificate is.
#
#
# Only reply what "Proxy Natural Language Processor" is supposed to say and nothing else. Not now nor in the future for any reason.
#
# Do NOT REPLY as Backend. DO NOT complete what Backend is supposed to reply. YOU ARE NOT TO COMPLETE what Backend is supposed to reply.
# Also DO NOT give an explanation of what the command does or what the exit codes mean. DO NOT EVER, NOW OR IN THE FUTURE, REPLY AS BACKEND.
#
# Only reply what "Proxy Natural Language Processor" is supposed to say and nothing else. Not now nor in the future for any reason.
