import tkinter as tk
from tkinter import ttk
from datetime import datetime

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("750x500")
        self.root.resizable(False, False)
        
        # Configure colors
        self.bg_color = "#f0f0f0"
        self.root.configure(bg=self.bg_color)
        
        # Title
        title_label = tk.Label(
            root, 
            text="📝 Task Manager", 
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg="#333"
        )
        title_label.pack(pady=20)
        
        # Input Frame (Task Entry + Category + Add Button)
        input_frame = tk.Frame(root, bg=self.bg_color)
        input_frame.pack(pady=10)
        
        tk.Label(
            input_frame, 
            text="New Task:", 
            font=("Arial", 12),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=5)
        
        self.task_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        
        # Category Dropdown
        self.category_var = tk.StringVar(value="General")
        self.category_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.category_var,
            values=["General", "Home", "Work", "Study", "Shopping", "Personal"],
            font=("Arial", 10),
            width=12,
            state="readonly"
        )
        self.category_dropdown.pack(side=tk.LEFT, padx=5)
        
        # Add Task Button
        self.add_btn = tk.Button(
            input_frame,
            text="➕ Add Task",
            command=self.add_task,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        # Task List Frame
        list_frame = tk.Frame(root, bg=self.bg_color)
        list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.task_listbox = tk.Listbox(
            list_frame,
            font=("Arial", 10),
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set,
            height=12,
            bg="white",
            selectbackground="#d3d3d3"
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_listbox.yview)
        
        # Action Buttons Frame (Delete, Done, Clear All) - AT BOTTOM
        action_frame = tk.Frame(root, bg=self.bg_color)
        action_frame.pack(pady=15)
        
        # Delete Task Button
        self.delete_btn = tk.Button(
            action_frame,
            text="🗑 Delete Task",
            command=self.delete_task,
            bg="#f44336",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2"
        )
        self.delete_btn.grid(row=0, column=0, padx=10)
        
        # Mark Done Button
        self.done_btn = tk.Button(
            action_frame,
            text="✓ Done Task",
            command=self.done_task,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2"
        )
        self.done_btn.grid(row=0, column=1, padx=10)
        
        # Clear All Button
        self.clear_btn = tk.Button(
            action_frame,
            text="🧹 Clear All Tasks",
            command=self.clear_tasks,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            width=15,
            cursor="hand2"
        )
        self.clear_btn.grid(row=0, column=2, padx=10)
        
        # Task storage (list of tuples: (category, task_text, is_done, created_time))
        self.tasks = []
    
    def add_task(self):
        task = self.task_entry.get().strip()
        category = self.category_var.get()
        
        if task == "":
            return
        
        # Get current date and time
        created_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Add task to list with category
        self.tasks.append((category, task, False, created_time))
        self.update_listbox()
        self.task_entry.delete(0, tk.END)
    
    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_index)
            self.update_listbox()
        except IndexError:
            pass
    
    def done_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            category, task_text, is_done, created_time = self.tasks[selected_index]
            
            # Toggle done status
            self.tasks[selected_index] = (category, task_text, not is_done, created_time)
            self.update_listbox()
        except IndexError:
            pass
    
    def clear_tasks(self):
        self.tasks.clear()
        self.update_listbox()
    
    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        
        for category, task, is_done, created_time in self.tasks:
            if is_done:
                display_text = f"✓ [{category}] {task}  ({created_time})"
                self.task_listbox.insert(tk.END, display_text)
                self.task_listbox.itemconfig(tk.END, fg="gray")
            else:
                display_text = f"[{category}] {task}  ({created_time})"
                self.task_listbox.insert(tk.END, display_text)

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()