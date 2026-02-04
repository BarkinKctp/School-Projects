import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd

root = tk.Tk()
AKTS = { "Physics" : 0.25, "Calculus" : 0.25, "Advanced Programming" : 0.30, "Chemistry": 0.20 }

class Mini_Project:
    def __init__(self, root):
        self.root = root
        self.root.title("Student GPA and Ranking")
        self.root.geometry("250x200")
        self.df = None

        P_X = 5 
        P_Y = 3 
        
        #GUI Elements (Browse Button)
        tk.Label(root, text="Open File:").grid(row=0, column=0, padx=P_X, pady=P_Y, sticky="w")
        tk.Button(root, text="Browse", command=self.browse_file,width=12).grid(row=0, column=1, padx=P_X, pady=P_Y, sticky="w")

        #GUI Elements (ID Entry)
        tk.Label(root, text="ID:").grid(row=1, column=0, padx=P_X, pady=P_Y, sticky="w")
        self.id_entry = tk.Entry(root, width=12)
        self.id_entry.grid(row=1, column=1, padx=P_X, pady=P_Y, sticky="w")

        #GUI Elements (Labels)
        tk.Label(root, text="Name Surname:").grid(row=2, column=0, padx=P_X, pady=P_Y, sticky="w")
        self.name_label = tk.Label(root, text="")
        self.name_label.grid(row=2, column=1, padx=P_X, pady=P_Y, sticky="w") 

        tk.Label(root, text="GPA:").grid(row=3, column=0, padx=P_X, pady=P_Y, sticky="w")
        self.gpa_label = tk.Label(root, text="")
        self.gpa_label.grid(row=3, column=1, padx=P_X, pady=P_Y, sticky="w")

        tk.Label(root, text="Rank:").grid(row=4, column=0, padx=P_X, pady=P_Y, sticky="w")
        self.rank_label = tk.Label(root, text="")
        self.rank_label.grid(row=4, column=1, padx=P_X, pady=P_Y, sticky="w")

        #GUI Elements (File Type)
        tk.Label(root, text="Please select file Type:").grid(row=5, column=0, padx=P_X, pady=P_Y, sticky="w")
        self.combo = ttk.Combobox(root, values=[".txt", ".xls"], width = 12, state="readonly") 
        self.combo.set(".txt")
        self.combo.grid(row=5, column=1, padx=P_X, pady=P_Y, sticky="w") # Default value txt

        #GUI Elements (Button)
        button_frame = tk.Frame(root)
        button_frame.grid(row=6, column=0, columnspan=2, pady=5) #Frame to center buttons
        
        tk.Button(button_frame, text="Display", command=self.display_info, width=8).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Export", command=self.export, width=8).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear, width=8).grid(row=0, column=2, padx=5)

    # Browse File Function
    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not file_path:
            return
        try:
            self.df = pd.read_excel(file_path)
            
            self.df["GPA"] = ( self.df["Physics"] * AKTS["Physics"] + self.df["Calculus"] * AKTS["Calculus"] +
            self.df["Advanced Programming"] * AKTS["Advanced Programming"] + self.df["Chemistry"] * AKTS["Chemistry"] ) #Calculating GPA

            self.df = self.df.sort_values("GPA", ascending=False).reset_index(drop=True) #Sorting by GPA
            self.df["Rank"] = self.df.index + 1     
            messagebox.showinfo("Success", f"File loaded and GPA calculated successfully.")
          
        except KeyError as e:
            messagebox.showerror("Error", f"Failed to calculate GPA. Column {e} is missing from the Excel file. Please ensure columns Name, Surname, ID, Physics, Calculus, Advanced Programming, and Chemistry are present.")
            self.df = None
        except Exception as e:
            messagebox.showerror("Error", f"Could not process file. Check structure of the file or the file path. Error: {e}")
            self.df = None

    # Display Info Function
    def display_info(self):
        if self.df is None:
            messagebox.showerror("Error", "Please load a valid file .")
            return
        try:
            student_id = int(self.id_entry.get())
        except:
            messagebox.showerror("Error", "Please enter a valid ID.")
            return
        row = self.df[self.df["ID"] == student_id]
        if row.empty:
            messagebox.showerror("Error", "ID not found.")
            return
        row = row.iloc[0]

        if pd.isna(row['GPA']):
            messagebox.showerror("Calculation Error", "GPA cannot be calculated for this student. One or more course grades are missing or invalid")
            
            self.name_label.config(text=f"{row['Name']} {row['Surname']}") 
            self.gpa_label.config(text="N/A")
            self.rank_label.config(text="N/A")
            return
        
        full_name = f"{row['Name']} {row['Surname']}"
        self.name_label.config(text=full_name)
        self.gpa_label.config(text=f"{row['GPA']:.2f}")
        self.rank_label.config(text=str(row['Rank']))

    # Export Function
    def export(self):
        
        student_name = self.name_label.cget("text")
        if not student_name:
            messagebox.showerror("Error", "No data to export. Display student info first.")
            return
        
        filetype = self.combo.get()
        student_id = self.id_entry.get().strip()
        filename = f"{student_id} {student_name}{filetype}"

        try:
            if filetype == ".txt":
                with open(filename, "w") as file:
                    file.write(f"ID: {student_id}\n")
                    file.write(f"Name: {self.name_label.cget('text')}\n")
                    file.write(f"GPA: {self.gpa_label.cget('text')}\n")
                    file.write(f"Rank: {self.rank_label.cget('text')}\n")

            elif filetype == ".xls":
                with open(filename, "w", newline='') as file: 
                    file.write("ID\tName\tGPA\tRank\n")
                    file.write(f"{student_id}\t{self.name_label.cget('text')}\t{self.gpa_label.cget('text')}\t{self.rank_label.cget('text')}\n")

            else: 
                raise ValueError(f"Unsupported file type selected: {filetype}. Only .txt and .xls are supported.")
            
            messagebox.showinfo("Success", f"File saved as {filename}.")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred during file export: {e}")

    #Clear Function
    def clear(self):
        self.name_label.config(text="")
        self.gpa_label.config(text="")  
        self.rank_label.config(text="")
        self.id_entry.delete(0, tk.END)

app = Mini_Project(root)
root.mainloop()
