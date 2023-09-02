import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import hashlib
import pyperclip  # for clipboard functionality

# Supported hashing algorithms
hash_algorithms = sorted(hashlib.algorithms_guaranteed)

# Additional hashing algorithms
additional_algorithms = [
    'shake_128', 'shake_256', 'blake2s', 'blake2b', 'md5', 'sha1',
    'sha224', 'sha384', 'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
    'whirlpool', 'ripemd160'
]

hash_algorithms.extend(additional_algorithms)

def generate_hash():
    input_text = input_entry.get()
    selected_algorithm = algorithm_combobox.get()

    try:
        if selected_algorithm not in hash_algorithms:
            raise ValueError("Invalid hashing algorithm selected.")

        hash_obj = hashlib.new(selected_algorithm)
        hash_obj.update(input_text.encode('utf-8'))
        generated_hash = hash_obj.hexdigest()

        result_label.config(text=f'Generated Hash: {generated_hash}')
    except ValueError as e:
        messagebox.showerror("Error", str(e))

def save_to_file():
    generated_hash = result_label.cget("text")
    if generated_hash.startswith("Generated Hash: "):
        generated_hash = generated_hash[len("Generated Hash: "):]

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(generated_hash)
            messagebox.showinfo("Success", "Hash saved to file successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the hash: {str(e)}")

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                input_entry.delete(0, tk.END)  # Clear the current input
                input_entry.insert(0, file_contents)  # Load file contents into input field
                generate_hash()  # Calculate hash of loaded file contents
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file: {str(e)}")

def copy_to_clipboard():
    generated_hash = result_label.cget("text")
    if generated_hash.startswith("Generated Hash: "):
        generated_hash = generated_hash[len("Generated Hash: "):]
    
    pyperclip.copy(generated_hash)
    messagebox.showinfo("Success", "Hash copied to clipboard.")

# Create the main window
root = tk.Tk()
root.title("Hash Generator")

# Input label and entry
input_label = ttk.Label(root, text="Enter Text:")
input_label.pack(padx=10, pady=5, anchor='w')

input_entry = ttk.Entry(root, width=40)
input_entry.pack(padx=10, pady=5)

# Algorithm selection
algorithm_label = ttk.Label(root, text="Select Algorithm:")
algorithm_label.pack(padx=10, pady=5, anchor='w')

algorithm_combobox = ttk.Combobox(root, values=hash_algorithms)
algorithm_combobox.set(hash_algorithms[0])  # Set default algorithm
algorithm_combobox.pack(padx=10, pady=5)

# Generate button
generate_button = ttk.Button(root, text="Generate Hash", command=generate_hash)
generate_button.pack(padx=10, pady=5)

# Save to file button
save_button = ttk.Button(root, text="Save Hash to File", command=save_to_file)
save_button.pack(padx=10, pady=5)

# Load file button
load_button = ttk.Button(root, text="Load Text from File", command=load_file)
load_button.pack(padx=10, pady=5)

# Copy to clipboard button
copy_button = ttk.Button(root, text="Copy Hash to Clipboard", command=copy_to_clipboard)
copy_button.pack(padx=10, pady=5)

# Result label
result_label = ttk.Label(root, text="")
result_label.pack(padx=10, pady=5, anchor='w')

# Run the GUI
root.mainloop()
