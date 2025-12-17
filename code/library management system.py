import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# ------------------------------
# Database Class
# ------------------------------
class LibraryDatabase:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_title TEXT NOT NULL,
                author TEXT NOT NULL,
                date_borrowed TEXT,
                date_due TEXT,
                added_time TEXT
            )
        """)
        self.conn.commit()

    def insert_book(self, title, author, borrowed, due):
        added_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO books (book_title, author, date_borrowed, date_due, added_time)
            VALUES (?, ?, ?, ?, ?)
        """, (title, author, borrowed, due, added_time))
        self.conn.commit()

    def fetch_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# ------------------------------
# GUI Application
# ------------------------------
class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.db = LibraryDatabase()
        self.root.title("Library Management System")
        self.root.geometry("750x420")

        # Labels
        tk.Label(root, text="Book Title").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Author").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Date Borrowed").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(root, text="Date Due").grid(row=3, column=0, padx=10, pady=5)

        # Entry Fields
        self.title_entry = tk.Entry(root, width=30)
        self.author_entry = tk.Entry(root, width=30)
        self.borrowed_entry = tk.Entry(root, width=30)
        self.due_entry = tk.Entry(root, width=30)

        self.title_entry.grid(row=0, column=1)
        self.author_entry.grid(row=1, column=1)
        self.borrowed_entry.grid(row=2, column=1)
        self.due_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(root, text="Add Book", command=self.add_book).grid(row=4, column=0, pady=10)
        tk.Button(root, text="View Books", command=self.view_books).grid(row=4, column=1)
        tk.Button(root, text="Delete Book", command=self.delete_book).grid(row=4, column=2)

        # Listbox
        self.book_list = tk.Listbox(root, width=95)
        self.book_list.grid(row=5, column=0, columnspan=3, padx=10)
        self.book_list.bind("<<ListboxSelect>>", self.select_book)

        self.selected_book = None

    def add_book(self):
        if not self.title_entry.get() or not self.author_entry.get():
            messagebox.showwarning("Warning", "Title and Author are required")
            return

        self.db.insert_book(
            self.title_entry.get(),
            self.author_entry.get(),
            self.borrowed_entry.get(),
            self.due_entry.get()
        )
        messagebox.showinfo("Success", "Book added successfully")
        self.clear_entries()
        self.view_books()

    def view_books(self):
        self.book_list.delete(0, tk.END)
        for row in self.db.fetch_books():
            self.book_list.insert(tk.END, row)

    def select_book(self, event):
        try:
            index = self.book_list.curselection()[0]
            self.selected_book = self.book_list.get(index)
        except IndexError:
            self.selected_book = None

    def delete_book(self):
        if self.selected_book:
            self.db.delete_book(self.selected_book[0])
            messagebox.showinfo("Deleted", "Book deleted successfully")
            self.view_books()
        else:
            messagebox.showwarning("Warning", "Select a book to delete")

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.borrowed_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)

# ------------------------------
# Run Application
# ------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
