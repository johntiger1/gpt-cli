

import openai
import os
import subprocess
import git

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]


print('Welcome to gitGPT.')



# can make these config varaibles or inputtable later
# Set up Git repository path and branch name
repo_path = "./"
branch_name = "master"

# Connect to the Git repository
repo = git.Repo(repo_path)

diff_output = subprocess.check_output(["git", "diff", "--no-color"], cwd=repo_path).decode("utf-8")
print(diff_output)
modified_files = [item.a_path for item in repo.index.diff(None) if item.change_type != 'D']

# print(diff_output)
total_payload = f'''{diff_output}'''


example_git_messages = '''
git commit -m "Fix typo in header of README.md"

git commit -m "Add new feature to user profile page"

git commit -m "Refactor file handling logic for improved performance"

git commit -m "Update dependencies to fix security vulnerability"

git commit -m "Remove unused code and files"

git commit -m "Improve error handling for invalid input"
'''

summary = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"Summarize the following Git diff output, creating a `git commit` message. Describe the changes in each file, "
           f"creating one sentence per file change. "
           f"Prepend `generated with GitGPT` to "
           f"start of your git commit message. Here is the git diff:"
           f"{total_payload}"
           f" ",
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
)["choices"][0]["text"].strip()

print(summary)



index = repo.index
for file in modified_files:
    index.add([file])

index.commit(summary)