import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# File to store contacts
CONTACTS_FILE = 'contacts.json'

def load_contacts():
    """Load contacts from a JSON file."""
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_contacts(contacts):
    """Save contacts to a JSON file."""
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.contacts = load_contacts()
        self.selected_contact = None  # Track the selected contact

        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(4, weight=1)

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        """Create the GUI components."""
        # Name
        tk.Label(self.root, text="Name:").grid(row=0, column=0, padx=10, pady=10, sticky='ew')
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        # Phone
        tk.Label(self.root, text="Phone:").grid(row=1, column=0, padx=10, pady=10, sticky='ew')
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

        # Email
        tk.Label(self.root, text="Email:").grid(row=2, column=0, padx=10, pady=10, sticky='ew')
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        # Buttons
        tk.Button(self.root, text="Add Contact", command=self.add_contact).grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        tk.Button(self.root, text="View Contacts", command=self.view_contacts).grid(row=3, column=1, padx=10, pady=10, sticky='ew')

        # Contact list
        self.contact_listbox = tk.Listbox(self.root, width=50)
        self.contact_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.contact_listbox.bind('<<ListboxSelect>>', self.select_contact)

        # Edit and Delete buttons
        tk.Button(self.root, text="Edit Contact", command=self.edit_contact).grid(row=5, column=0, padx=10, pady=10, sticky='ew')
        tk.Button(self.root, text="Delete Contact", command=self.delete_contact).grid(row=5, column=1, padx=10, pady=10, sticky='ew')

    def add_contact(self):
        """Add a new contact."""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if name and phone and email:
            self.contacts[name] = {'phone': phone, 'email': email}
            save_contacts(self.contacts)
            messagebox.showinfo("Success", "Contact added successfully!")
            self.clear_entries()
            self.view_contacts()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def view_contacts(self):
        """Display the contact list."""
        self.contact_listbox.delete(0, tk.END)  # Clear the listbox
        for name in self.contacts:
            self.contact_listbox.insert(tk.END, name)

    def select_contact(self, event):
        """Select a contact from the list."""
        selected_contact = self.contact_listbox.curselection()
        if selected_contact:
            self.selected_contact = self.contact_listbox.get(selected_contact)  # Store the selected contact name
            contact_info = self.contacts[self.selected_contact]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.selected_contact)
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, contact_info['phone'])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, contact_info['email'])

    def edit_contact(self):
        """Edit the selected contact."""
        if self.selected_contact:
            new_name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            email = self.email_entry.get().strip()

            if new_name and phone and email:
                # Update the contact
                del self.contacts[self.selected_contact]  # Remove old contact
                self.contacts[new_name] = {'phone': phone, 'email': email}  # Add updated contact
                save_contacts(self.contacts)
                messagebox.showinfo("Success", "Contact updated successfully!")
                self.clear_entries()
                self.view_contacts()
                self.selected_contact = new_name  # Update the selected contact name
            else:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to edit.")

    def delete_contact(self):
        """Delete the selected contact."""
        if self.selected_contact:
            del self.contacts[self.selected_contact]
            save_contacts(self.contacts)
            messagebox.showinfo("Success", "Contact deleted successfully!")
            self.view_contacts()
            self.clear_entries()
            self.selected_contact = None  # Clear the selected contact
        else:
            messagebox.showwarning("Selection Error", "Please select a contact to delete.")

    def clear_entries(self):
        """Clear input fields."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManager(root)
    root.mainloop()
