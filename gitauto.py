import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import openai
import threading

# Function to setup and run a chosen AI model
def run_ai_model(prompt, model_choice):
    openai.api_key = "your-openai-api-key"

    if model_choice == "GPT-3":
        model = "text-davinci-003"
    elif model_choice == "GPT-4":
        model = "gpt-4"
    else:
        model = "text-davinci-003"  # Default to GPT-3 if invalid

    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error with AI request: {e}")
        return "Error generating response."


# Function to execute Python code
def execute_python_code(code):
    try:
        exec(code)
        return "Python code executed successfully!"
    except Exception as e:
        return f"Error executing Python code: {e}"


# Function to handle AI interaction
def interact_with_ai():
    prompt = ai_input_text.get("1.0", tk.END).strip()
    model_choice = model_combobox.get()

    if not prompt:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)  # Clear previous result
    result_text.insert(tk.END, "Processing...\n")
    result_text.config(state=tk.DISABLED)

    # Run the AI model in a separate thread to avoid freezing the GUI
    def run_async():
        result = run_ai_model(prompt, model_choice)
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)

    threading.Thread(target=run_async).start()


# Function to handle Python code execution
def run_python_code():
    code = code_input_text.get("1.0", tk.END).strip()

    if not code:
        messagebox.showwarning("Input Error", "Please enter Python code.")
        return

    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Executing Python code...\n")
    result_text.config(state=tk.DISABLED)

    # Execute Python code in a separate thread to avoid freezing the GUI
    def execute_async():
        result = execute_python_code(code)
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, result)
        result_text.config(state=tk.DISABLED)

    threading.Thread(target=execute_async).start()


# GUI Setup
root = tk.Tk()
root.title("AI and Python Code Assistant")
root.geometry("800x600")

# AI interaction section
ai_section_frame = ttk.LabelFrame(root, text="AI Interaction", padding="10")
ai_section_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

ai_input_label = ttk.Label(ai_section_frame, text="Enter your AI prompt:")
ai_input_label.grid(row=0, column=0, sticky="w")

ai_input_text = tk.Text(ai_section_frame, height=5, width=50)
ai_input_text.grid(row=1, column=0, columnspan=2, pady=5)

model_combobox_label = ttk.Label(ai_section_frame, text="Choose AI Model:")
model_combobox_label.grid(row=2, column=0, sticky="w")

model_combobox = ttk.Combobox(ai_section_frame, values=["GPT-3", "GPT-4"], state="readonly")
model_combobox.set("GPT-3")  # Default to GPT-3
model_combobox.grid(row=2, column=1, pady=5)

ai_interact_button = ttk.Button(ai_section_frame, text="Get AI Response", command=interact_with_ai)
ai_interact_button.grid(row=3, column=0, columnspan=2, pady=10)

# Python code execution section
code_section_frame = ttk.LabelFrame(root, text="Python Code Execution", padding="10")
code_section_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

code_input_label = ttk.Label(code_section_frame, text="Enter Python Code:")
code_input_label.grid(row=0, column=0, sticky="w")

code_input_text = tk.Text(code_section_frame, height=10, width=50)
code_input_text.grid(row=1, column=0, columnspan=2, pady=5)

run_code_button = ttk.Button(code_section_frame, text="Run Python Code", command=run_python_code)
run_code_button.grid(row=2, column=0, columnspan=2, pady=10)

# Result display section
result_section_frame = ttk.LabelFrame(root, text="Results", padding="10")
result_section_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

result_text = tk.Text(result_section_frame, height=10, width=80, wrap="word", state=tk.DISABLED)
result_text.grid(row=0, column=0, pady=5)

# Start the GUI
root.mainloop()
