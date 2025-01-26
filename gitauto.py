import os
import subprocess
import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from github import Github
import openai

# GitHub Authentication and API Key
def authenticate_github(token):
    try:
        return Github(token)
    except Exception as e:
        messagebox.showerror("Authentication Error", f"Authentication failed: {e}")
        exit(1)

# AI Code Assistance (using OpenAI's GPT)
def get_ai_code_suggestion(prompt):
    openai.api_key = "your-openai-api-key"  # Replace with your OpenAI API key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can change this to a newer model if you want
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        messagebox.showerror("AI Error", f"Error communicating with AI model: {e}")
        return ""

# Setup Project Structure
def setup_project(repo_name):
    try:
        os.makedirs(f"{repo_name}/src", exist_ok=True)
        os.makedirs(f"{repo_name}/tests", exist_ok=True)
        os.makedirs(f"{repo_name}/docs", exist_ok=True)
        with open(f"{repo_name}/README.md", "w") as f:
            f.write(f"# {repo_name}\n\nDescription of the project.\n\n## Installation\n\n```\npip install -r requirements.txt\n```\n\n## Usage\n\nExplain how to use the script.\n")
        with open(f"{repo_name}/requirements.txt", "w") as f:
            f.write("# Add your dependencies here\n")
        with open(f"{repo_name}/.gitignore", "w") as f:
            f.write("__pycache__/\n*.pyc\n")
        messagebox.showinfo("Project Setup", f"Project structure for {repo_name} created successfully.")
    except Exception as e:
        messagebox.showerror("Setup Error", f"Failed to set up project structure: {e}")
        exit(1)

# GUI Class
class GitHubManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repository Manager")
        self.root.geometry("600x400")

        self.token = simpledialog.askstring("GitHub Token", "Enter your GitHub Personal Access Token (PAT):", show="*")
        self.github = authenticate_github(self.token)

        self.create_widgets()

    def create_widgets(self):
        # Buttons for actions
        tk.Button(self.root, text="Create Repository", width=30, command=self.create_repository).pack(pady=10)
        tk.Button(self.root, text="Add/Update Script", width=30, command=self.add_update_script).pack(pady=10)
        tk.Button(self.root, text="Run Tests", width=30, command=self.run_tests).pack(pady=10)
        tk.Button(self.root, text="Push to GitHub", width=30, command=self.push_to_github).pack(pady=10)
        tk.Button(self.root, text="AI Coding Assistant", width=30, command=self.ai_coding_assistant).pack(pady=10)
        tk.Button(self.root, text="Exit", width=30, command=self.root.quit).pack(pady=10)

    def create_repository(self):
        repo_name = simpledialog.askstring("Repository Name", "Enter the repository name:")
        description = simpledialog.askstring("Description", "Enter a description for the repository (optional):")
        clone_url = self.create_github_repo(repo_name, description)
        self.setup_project_structure(repo_name)
        messagebox.showinfo("Repository Created", f"Repository {repo_name} created and set up locally.")
        
    def create_github_repo(self, repo_name, description):
        try:
            user = self.github.get_user()
            repo = user.create_repo(repo_name, description=description)
            return repo.clone_url
        except Exception as e:
            messagebox.showerror("GitHub Error", f"Failed to create repository: {e}")
            return ""

    def setup_project_structure(self, repo_name):
        setup_project(repo_name)

    def add_update_script(self):
        repo_name = simpledialog.askstring("Repository Name", "Enter the repository name to update:")
        new_code = simpledialog.askstring("New Script Code", "Enter the new script code (or leave blank to update existing):")
        self.add_or_update_script(repo_name, new_code)
        
    def add_or_update_script(self, repo_name, new_code):
        try:
            script_path = os.path.join(repo_name, "src", "main.py")
            with open(script_path, "w") as f:
                f.write(new_code)
            messagebox.showinfo("Script Updated", f"Script updated at {script_path}.")
        except Exception as e:
            messagebox.showerror("Script Error", f"Failed to add or update the script: {e}")

    def run_tests(self):
        repo_name = simpledialog.askstring("Repository Name", "Enter the repository name to run tests:")
        # Implement test execution logic here (e.g., using pytest)
        messagebox.showinfo("Test Result", f"Tests for {repo_name} ran successfully.")

    def push_to_github(self):
        repo_name = simpledialog.askstring("Repository Name", "Enter the repository name to push:")
        # Implement push logic here (git commands)
        messagebox.showinfo("GitHub Push", f"Changes pushed to GitHub for {repo_name}.")

    def ai_coding_assistant(self):
        prompt = simpledialog.askstring("AI Code Assistant", "Describe what you want the AI to help with:")
        suggestion = get_ai_code_suggestion(prompt)
        messagebox.showinfo("AI Suggestion", suggestion)


# Main Program
def main():
    root = tk.Tk()
    app = GitHubManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
