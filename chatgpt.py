import openai
import os

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up the GPT-3 model
model_engine = "gpt-3.5-turbo"
prompt = "Hello, how can I assist you today?"

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
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello!" + prompt}
            # {"role": "user", content: "" }
        ]
    )

    print(completion.choices[0].message)
    # return completion.choices[0].message


# Get input from the user and generate a response
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    prompt += "\nUser: " + user_input
    response = generate_respone_v2(prompt)
    # print("ChatGPT: " + response)

