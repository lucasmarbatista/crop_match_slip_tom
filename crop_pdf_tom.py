import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import fitz  # PyMuPDF

def crop_pdf(input_path, output_folder_path, crops):
    output_file_name = os.path.splitext(os.path.basename(input_path))[0] + "_cropped.pdf"
    output_path = os.path.join(output_folder_path, output_file_name)

    pdf_document = fitz.open(input_path)
    new_doc = fitz.open()  # Create a new blank PDF document.

    for (x1, y1, x2, y2) in crops:
        for page_num in range(len(pdf_document)):
            rect = fitz.Rect(x1, y1, x2, y2) # Define the crop rectangle.
            new_page = new_doc.new_page(width=rect.width, \
              height=rect.height) # Create a new page with the cropped size.
            new_page.show_pdf_page(new_page.rect, pdf_document, page_num, \
              clip=rect) # Add the cropped content to the new page.
            new_page.set_rotation(90) # Rotate the cropped page by 90 degrees.


    new_doc.save(output_path) # Save the new cropped PDF.
    new_doc.close()
    pdf_document.close()

def select_input_file():
    input_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if input_pdf_path:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, input_pdf_path)

def select_output_folder():
    output_folder_path = filedialog.askdirectory()
    if output_folder_path:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_folder_path)

def run_crop():
    input_path = input_entry.get()
    output_folder_path = output_entry.get()

    if not input_path:
        messagebox.showerror("Error", "Please select an input file.")
        return

    # Use the input directory if the output folder is not specified.
    if not output_folder_path:
        output_folder_path = os.path.dirname(input_path)

    # Get the checkbox state for including headers in the crop.
    header_state = header_var.get()

    # Define cropping areas based on the header state.
    if header_state:
        crops = [
          (1, 20, 590, 220),    # First area with header cropped.
          (1, 221, 590, 418),   # Second area cropped
          (1, 419, 590, 616),   # Third area cropped
          (1, 617, 590, 814)    # Fourth area cropped
      ]
    else:
        crops = [
          (1, 1, 590, 195),     # First area without header cropped.
          (1, 198, 590, 393),   # Second area cropped
          (1, 396, 590, 591),   # Third area cropped
          (1, 594, 590, 789)    # Fourth area cropped
      ]

    crop_pdf(input_path, output_folder_path, crops)
    messagebox.showinfo("Success", "The PDF was cropped and saved successfully. Check the output folder for the file.")

# GUI setup
root = tk.Tk()
root.title("PDF Cropper")
root.geometry("600x200")

# Configure the grid layout.
root.columnconfigure(1, weight=1)

input_button = tk.Button(root, text="Select Input PDF", command=select_input_file)
input_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

input_entry = tk.Entry(root)
input_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

output_button = tk.Button(root, text="Select Output Folder", command=select_output_folder)
output_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

output_entry = tk.Entry(root)
output_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

header_var = tk.BooleanVar(value=False) # Checkbox buttom for including page headers.
header_checkbox = tk.Checkbutton(root, text="Page with header", variable=header_var)
header_checkbox.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

crop_button = tk.Button(root, text="Crop PDF", command=run_crop)
crop_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

root.mainloop()
