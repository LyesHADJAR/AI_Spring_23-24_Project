import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import io
import sys
import csv  # Import the csv module
from DataLoader import DataLoader
from main import mycountry, search_for_year

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Project GUI")
        self.geometry("1000x1200")
        self.configure(bg='#013220')

        self.wilaya_file = None
        self.product_file = None

        self.upload_wilaya_button = tk.Button(self, text="Upload Wilaya CSV", command=self.upload_wilaya, bg='#013220', fg='white')
        self.upload_wilaya_button.pack(pady=10)

        self.upload_product_button = tk.Button(self, text="Upload Product CSV", command=self.upload_product, bg='#013220', fg='white')
        self.upload_product_button.pack(pady=10)

        self.search_method_var = tk.StringVar(self)
        self.search_method_var.set("Select Search Method")
        self.search_methods = ["IDA_Star", "IDS", "steepest", "UCS"]

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('TMenubutton', background='#013220', foreground='white', fieldbackground='#013220')

        self.search_menu = tk.OptionMenu(self, self.search_method_var, *self.search_methods)
        self.search_menu.config(bg='#013220', fg='white')
        self.search_menu.pack(pady=10)

        self.search_button = tk.Button(self, text="Search", command=self.perform_search, bg='#013220', fg='white')
        self.search_button.pack(pady=10)

        # Create a frame for the text field and scrollbar
        text_frame = tk.Frame(self, bg='#013220')
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.output_text = tk.Text(text_frame, wrap=tk.WORD, height=50, width=100, bg='#013220', fg='white', insertbackground='white')
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview, bg='#013220', troughcolor='#013220', activebackground='#004d00', highlightbackground='#013220', highlightcolor='#013220')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text.config(yscrollcommand=scrollbar.set)

        # Place the save button below the text_frame
        self.save_button = tk.Button(self, text="Save to CSV", command=self.save_output_to_csv, bg='#013220', fg='white')
        self.save_button.pack(side="bottom", pady=10)
        
    def upload_wilaya(self):
        self.wilaya_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.wilaya_file:
            self.upload_wilaya_button.config(text=self.wilaya_file.split("/")[-1])
        else:
            messagebox.showerror("Error", "Failed to upload Wilaya CSV file")

    def upload_product(self):
        self.product_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.product_file:
            self.upload_product_button.config(text=self.product_file.split("/")[-1])
        else:
            messagebox.showerror("Error", "Failed to upload Product CSV file")

    def perform_search(self):
        if not self.wilaya_file or not self.product_file:
            messagebox.showerror("Error", "Please upload both CSV files")
            return

        search_method = self.search_method_var.get()
        if search_method == "Select Search Method":
            messagebox.showerror("Error", "Please select a search method")
            return

        self.search_button.config(text="Searching...", state=tk.DISABLED)
        self.update_idletasks()

        try:
            cities_data, consumption, total_production, prices = DataLoader.load_country_data(self.wilaya_file, self.product_file)
            country = mycountry(cities_data, consumption, prices)

            old_stdout = sys.stdout
            redirected_output = sys.stdout = io.StringIO()

            search_for_year(country, search_method)

            sys.stdout = old_stdout

            output = redirected_output.getvalue()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)

            self.highlight_text("[ >>>>> SEARCH FOR SPRING SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR SUMMER SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR FALL SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR WINTER SEASON PLAN TOOK <<<<< ]: ", "#39FF14")
            self.highlight_text("[ >>>>> SEARCH FOR YEAR PLAN TOOK <<<<< ]", "#FFFF00")

            self.search_button.config(text="Done!", state=tk.NORMAL)

        except Exception as e:
            self.search_button.config(text="Search", state=tk.NORMAL)
            messagebox.showerror("Error", f"An error occurred: {e}")

        self.search_button.config(text="Done!", state=tk.NORMAL)

    def highlight_text(self, pattern, color):
        start_idx = self.output_text.search(pattern, "1.0", tk.END)
        while start_idx:
            end_idx = f"{start_idx} lineend"
            self.output_text.tag_add(pattern, start_idx, end_idx)
            self.output_text.tag_config(pattern, foreground=color)
            start_idx = self.output_text.search(pattern, end_idx, tk.END)

    def save_output_to_csv(self):
        output_text = self.output_text.get("1.0", tk.END).strip()
        lines = output_text.split("\n")

        with open("output.csv", "w", newline="") as file:
            writer = csv.writer(file)
            for line in lines:
                if line.strip():  # Check if the line is not empty
                    fields = [field.strip() for field in line.split('|')]  # Split using '|' and strip any extra spaces
                    writer.writerow(fields)

if __name__ == "__main__":
    app = App()
    app.mainloop()
