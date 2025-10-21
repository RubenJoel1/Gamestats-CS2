import sqlalchemy
import sqlalchemy as db
import tkinter as tk
from tkinter import messagebox
import sqlite3

#GUI Setup
root = tk.Tk()
image = tk.PhotoImage(file="logo.png")
root.title("Counter-Strike 2 Stats Tracker")
root.iconphoto(True, image)
root.geometry("800x600")
root.configure(bg="#1e1e1e")

#Functions
def show_stats():
    root = tk.Tk()
    root.title("Player Stats")
    root.geometry("400x300")
    root.configure(bg="#1e1e1e")
    root.mainloop()

def enter_data():
    root = tk.Tk()
    root.title("Enter Match Data")
    root.geometry("400x300")
    root.configure(bg="#1e1e1e")
    root.mainloop()

#Labels
lbl = tk.Label(root, text="Counter-Strike 2 Stats Tracker", bg="#1e1e1e", fg="#fb832b", font=("Times New Roman", 30))
lbl.pack()

lbl2 = tk.Label(root, text="Developed by RubenJoel1", bg="#1e1e1e", fg="#fb832b", font=("Times New Roman", 10))
lbl2.pack()

lbl3 = tk.Label(root, text="Dust II           Mirage           Inferno           Train           Overpass           Ancient           Vertigo", bg="#1e1e1e", fg="#fdfdfd", font=("Times New Roman", 16))
lbl3.place(x=10, y=130)

lbl4 = tk.Label(root, text="Maps:", bg="#1e1e1e", fg="#fdfdfd", font=("Times New Roman", 20))
lbl4.pack()

#Buttons
btn = tk.Button(root, text="View Stats", bg="#fb832b", fg="#1e1e1e", font=("Times New Roman", 15), command=show_stats)
btn.place(x=650, y=530)

btn = tk.Button(root, text="Enter Data", bg="#fb832b", fg="#1e1e1e", font=("Times New Roman", 15), command=enter_data)
btn.place(x=30, y=535)

root.mainloop()