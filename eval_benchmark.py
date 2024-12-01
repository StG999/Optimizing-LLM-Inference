import subprocess
import time

# Configuration
OLLAMA_EXECUTABLE = "./ollama"  # Path to your Ollama executable
MODEL_NAME = "qwen2.5:0.5b"  # Replace with the model you want to use
prompts = {
    "translation": [
        "Translate the following paragraph from English to French: 'The rapid advancement of artificial intelligence is reshaping industries globally.'",
        "Translate this German sentence to English: 'Die Bedeutung der erneuerbaren Energien nimmt im Kampf gegen den Klimawandel zu.'"
    ],
    "coding_problem": [
        "Write a Python function to calculate the factorial of a given number using recursion.",
        "Write a Python function to find all pairs of numbers whose sum is 50 given nums = [10, 20, 30, 40, 50]."
    ],
    "mathematics": [
        "Solve the equation: 3x + 5 = 20.",
        "What is the derivative of f(x) = x^3 - 2x^2 + 4x - 1?"
    ],
    "text_generation": [
        "Write a short story about a time traveler who arrives in 2050.",
        "Generate a formal email to a professor requesting a project extension."
    ],
    "text_summarization": [
        "Summarize this: 'AI has automated tasks, increasing productivity but raising ethical concerns.'",
        "Summarize in bullet points: 'The Great Wall of China was built to protect against invasions. It spans thousands of miles.'"
    ]
}

# Function to run Ollama command with a prompt
def run_ollama(prompt):
    try:
        # Build the command
        command = [OLLAMA_EXECUTABLE, "run", MODEL_NAME, "--verbose"]
        # Execute the command
        process = subprocess.run(
            command,
            input=prompt,  # Pass the prompt directly as input
            capture_output=True,
            text=True
        )
        # Capture and return the output
        return process.stdout.strip(), process.stderr.strip()
    except Exception as e:
        return None, f"Error: {e}"

# Iterate through prompts and log responses
results = {}
for category, category_prompts in prompts.items():
    print(f"--- {category.upper()} ---")
    results[category] = []
    for idx, prompt in enumerate(category_prompts, start=1):
        print(f"Running Prompt {idx}: {prompt}")
        stdout, stderr = run_ollama(prompt)
        print("--- Verbose Output ---")
        print(stdout)
        if stderr:
            print("--- Error/Additional Output ---")
            print(stderr)
        results[category].append({
            "prompt": prompt,
            "verbose_output": stdout,
            "error_output": stderr
        })
        time.sleep(1)  # Optional delay to avoid overwhelming the system

# Save results to a file
with open("ollama_results_verbose.txt", "w") as f:
    for category, logs in results.items():
        f.write(f"--- {category.upper()} ---\n")
        for log in logs:
            f.write(f"Prompt: {log['prompt']}\n")
            f.write(f"Verbose Output:\n{log['verbose_output']}\n")
            if log['error_output']:
                f.write(f"Error/Additional Output:\n{log['error_output']}\n")
            f.write("\n")