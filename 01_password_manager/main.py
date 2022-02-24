from tkinter import *
from tkinter import messagebox
from random import random, randint, shuffle, choice
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(numbers) for _ in range(randint(2, 4))]
    password_numbers = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    pyperclip.copy(password)
    entry_password.delete(0, END)
    entry_password.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = entry_website.get()
    email = entry_uname.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning!", message="Please don't leave any field empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"Do you want to save?\n"
                                                              f"Email: {email}\n"
                                                              f"Password: {password}")
        if is_ok:
            try:
                with open("data.json", mode='r') as data_file:
                    data = json.loads(data_file)
            except FileNotFoundError:
                with open("data.json", mode='w') as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", mode='w') as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                entry_website.delete(0, END)
                entry_password.delete(0, END)
                entry_website.focus()


# ---------------------------- SEARCH DATA ---------------------------- #
def search():
    website = entry_website.get()
    if len(website) == 0:
        messagebox.showwarning(title="Failed!", message="Please provide the website!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error!", message="No data file found!")
        else:
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Website: {website}\nEmail: {email}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error!", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #

win = Tk()
win.title("Password Manager")
win.config(padx=50, pady=50)

my_img = PhotoImage(file='logo.png')
canvas = Canvas(win, width=200, height=200)
canvas.create_image(100, 100, image=my_img)
canvas.grid(column=1, row=0)

# Labels
label_website = Label(text='Website:')
label_website.grid(column=0, row=1)
label_uname = Label(text='Email/Username:')
label_uname.grid(column=0, row=2)
label_password = Label(text='Password:')
label_password.grid(column=0, row=3)

# Entries
entry_website = Entry(width=33)
entry_website.grid(column=1, row=1)
entry_uname = Entry(width=53)
entry_uname.grid(column=1, row=2, columnspan=2)
entry_password = Entry(width=33)
entry_password.grid(column=1, row=3)

# Buttons
button_search = Button(text='Search', width=15, command=search)
button_search.grid(column=2, row=1)
button_generate = Button(text='Generate Password', width=15, command=generate_password)
button_generate.grid(column=2, row=3)
button_add = Button(text='Add', width=45, command=save)
button_add.grid(column=1, row=4, columnspan=2)

# functions
entry_website.focus()
entry_uname.insert(0, "example@email.com")

win.mainloop()
