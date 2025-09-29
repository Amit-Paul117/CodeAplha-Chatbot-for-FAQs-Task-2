from google import genai
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext, messagebox

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not found!")
    print("Please set your API key using: export GOOGLE_API_KEY='your_api_key_here'")
    exit(1)

client = genai.Client(api_key=API_KEY)

def generate_response(input_from_user):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{input_from_user}"
        )
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def main():
    print("=== Google Gemini Chat Interface ===")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ['quit', 'exit', 'bye', '']:
            print("Goodbye!")
            break
        print("\nGemini: ", end="")
        response = generate_response(user_input)
        print(response)

# GUI Code 
def start_gui():
    def send_message():
        user_input = entry.get().strip()
        if user_input == "":
            messagebox.showwarning("Empty Input", "Please type something!")
            return
        
        chat_box.insert(tk.END, f"You: {user_input}\n", "user")
        entry.delete(0, tk.END)
        
        response = generate_response(user_input)
        chat_box.insert(tk.END, f"Gemini: {response}\n\n", "bot")
        chat_box.see(tk.END)

    root = tk.Tk()
    root.title("Gemini FAQ Chatbot")
    root.geometry("600x500")

    chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="normal", font=("Arial", 12))
    chat_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    chat_box.tag_config("user", foreground="blue")
    chat_box.tag_config("bot", foreground="green")

    entry_frame = tk.Frame(root)
    entry_frame.pack(fill=tk.X, padx=10, pady=5)

    entry = tk.Entry(entry_frame, font=("Arial", 12))
    entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    send_btn = tk.Button(entry_frame, text="Send", command=send_message, font=("Arial", 12), bg="lightblue")
    send_btn.pack(side=tk.RIGHT)

    root.mainloop()

# Choose CLI or GUI
if __name__ == "__main__":
    print("Choose mode:")
    print("1. CLI (terminal)")
    print("2. GUI (window)")
    mode = input("Enter choice (1/2): ").strip()

    if mode == "1":
        main()
    else:
        start_gui()