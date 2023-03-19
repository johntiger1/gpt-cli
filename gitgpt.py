

import openai
import os
import subprocess
import git

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Set up the GPT-3 model
model_engine = "gpt-3.5-turbo"

CONTENT_DICT = {"role": "user", "content": f"Produce ONLY an executable shell command for the following prompt. "
                                    f"Do not include any explanation or natural language. "
                                           f"If the shell command is deemed 'dangerous', i.e. it will delete resources "
                                           f"then please echo the command and inform the user. Otherwise, please give the "
                                           f"executable command directly. "
                                           f"The prompt will begin now. "
                                    }

# can we auto summarize the changes.
# need to git add;
# then git commit
# then git push

history = [
    {"role": "system", "content": "You are shellGPT. You return runnable shell commands only. Produce"
                                      "an error message if appropriate.}"},
        CONTENT_DICT]
# Define a function to generate a response
def generate_response(prompt):
    global history
    new_message = CONTENT_DICT

    # we keep passing the full user history
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

def execute_response(response):
    '''in the future, we can do zero-shot toxicity detection '''
    print("The generated command that will be run is:\n")
    print(response)
    user_input = input("Execute Command?(Y/n) ")
    if user_input.lower() == "Y":
        code = os.system(response)
        print("Command returned {} exit code\n".format(code))

print('Welcome to gitGPT.')

def add_step():
    pass

def commit_step():
    pass

def push_step():
    pass


# can make these config varaibles or inputtable later
# Set up Git repository path and branch name
repo_path = "./"
branch_name = "master"

# Connect to the Git repository
repo = git.Repo(repo_path)

# simply do git gpt execute
# i.e.
# os.system('git add .')

status_output = subprocess.check_output(["git", "status"], cwd=repo_path).decode("utf-8")
diff_output = subprocess.check_output(["git", "diff", "--no-color"], cwd=repo_path).decode("utf-8")

total_payload = f'''
git status: {status_output}
git diff: {diff_output}
'''


summary = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Summarize the following Git information about this repo. For now, we will provide the output of "
           f" both `git status` as "
           f"well as `git diff`. This will enable you to pick up new files, as well as changes to existing files.  "
           f"creating a message that describes the current changes in the repo, and which is directly "
           f"usable for git commit -m `message`. "
           f""
           f":\n\n{total_payload}",
    max_tokens=180,
    n=1,
    stop=None,
    temperature=0.5,
)["choices"][0]["text"].strip()

print(summary)