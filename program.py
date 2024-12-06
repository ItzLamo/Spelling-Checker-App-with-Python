import tkinter as tk
from tkinter import messagebox, filedialog
from symspellpy import SymSpell, Verbosity


# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "D:\Hack Club\Project 5\en-80k.txt"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Function to check spelling and provide suggestions
def check_spelling():
    user_input = text_entry.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showinfo("Input Error", "Please enter some text to check spelling.")
        return

    corrected_text = []
    suggestions = []
    words = user_input.split()

    for word in words:
        correction = sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=2)
        if correction:
            # Add the best correction to corrected_text
            corrected_text.append(correction[0].term)
            # Store alternative suggestions if available
            suggestions.append(
                f"'{word}' -> {', '.join([c.term for c in correction[:3]])}"
            )
        else:
            # If no correction, keep the word as is
            corrected_text.append(word)

    result_label.config(text=f"Corrected Text:\n{' '.join(corrected_text)}", fg="green")
    suggestion_label.config(
        text="Suggestions:\n" + "\n".join(suggestions) if suggestions else "No suggestions found.",
        fg="blue",
    )

    word_count = len(words)
    char_count = len(user_input)
    stats_label.config(text=f"Word Count: {word_count}, Character Count: {char_count}")


# Function to save corrected text
def save_corrected_text():
    user_input = result_label.cget("text").replace("Corrected Text:\n", "")
    if not user_input.strip():
        messagebox.showinfo("Save Error", "No corrected text to save.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(user_input)
        messagebox.showinfo("Save Successful", f"Corrected text saved to {file_path}.")


# Function to clear text
def clear_text():
    text_entry.delete("1.0", tk.END)
    result_label.config(text="")
    suggestion_label.config(text="")
    stats_label.config(text="")


# Function to exit the application
def exit_app():
    root.destroy()


# GUI Setup
root = tk.Tk()
root.title("Spelling Checker with Suggestions")
root.geometry("700x600")
root.resizable(False, False)

# Title Label
title_label = tk.Label(
    root,
    text="Spelling Checker",
    font=("Helvetica", 16, "bold"),
)
title_label.pack(pady=10)

# Instruction Label
instruction_label = tk.Label(
    root,
    text="Enter text below to check spelling:",
    font=("Helvetica", 12),
)
instruction_label.pack(pady=5)

# Text Entry Box
text_entry = tk.Text(root, font=("Helvetica", 12), height=8, width=70)
text_entry.pack(pady=10)

# Button Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Check Spelling Button
check_button = tk.Button(
    button_frame,
    text="Check Spelling",
    font=("Helvetica", 12),
    bg="#4CAF50",
    fg="white",
    width=15,
    command=check_spelling,
)
check_button.grid(row=0, column=0, padx=10)

# Save Button
save_button = tk.Button(
    button_frame,
    text="Save Corrected Text",
    font=("Helvetica", 12),
    bg="#2196F3",
    fg="white",
    width=20,
    command=save_corrected_text,
)
save_button.grid(row=0, column=1, padx=10)

# Clear Button
clear_button = tk.Button(
    button_frame,
    text="Clear",
    font=("Helvetica", 12),
    bg="#FF9800",
    fg="white",
    width=10,
    command=clear_text,
)
clear_button.grid(row=0, column=2, padx=10)

# Exit Button
exit_button = tk.Button(
    button_frame,
    text="Exit",
    font=("Helvetica", 12),
    bg="#F44336",
    fg="white",
    width=10,
    command=exit_app,
)
exit_button.grid(row=0, column=3, padx=10)

# Result Label
result_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 16),
    wraplength=650,
    justify="center",
    fg="green",
)
result_label.pack(pady=10)

# Suggestion Label
suggestion_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 12),
    wraplength=650,
    justify="left",
    fg="blue",
)
suggestion_label.pack(pady=10)

# Stats Label
stats_label = tk.Label(
    root,
    text="",
    font=("Helvetica", 12),
    fg="#555",
)
stats_label.pack(pady=10)

# Start the GUI loop
root.mainloop()