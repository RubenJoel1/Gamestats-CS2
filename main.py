import sqlalchemy
import sqlalchemy as db
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
import sqlite3
from tkinter import PhotoImage
import PIL
from PIL import ImageTk, Image

#GUI Setup
root = tk.Tk()
image = tk.PhotoImage(file="Resources/logo.png")
root.title("Counter-Strike 2 Stats Tracker")
root.iconphoto(True, image)
root.geometry("800x600")
root.configure(bg="#1e1e1e")

#Database Setup
DB_PATH = "cs2_stats.db"
_maps = ["Dust2", "Mirage", "Inferno", "Train", "Overpass", "Ancient", "Vertigo"]

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                map TEXT NOT NULL,
                result TEXT NOT NULL CHECK(result IN ('Win', 'Loss'))
            )
    """)
    conn.commit()
    conn.close()

create_connection()

#Main Functions
def show_stats():
    show_stats_window = tk.Toplevel(root)
    show_stats_window.title("Player Stats")
    show_stats_window.geometry("420x360")
    show_stats_window.configure(bg="#1e1e1e")

    stats_info_frame = tk.LabelFrame(show_stats_window, text="Player Stats Per Map", bg="#1e1e1e", fg="#fb832b", font=("Comic Sans MS", 12))
    stats_info_frame.grid(row=0, column=0, padx=20, pady=20)

    tk.Label(stats_info_frame, text="Map", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=0, padx=10)
    tk.Label(stats_info_frame, text="Wins", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=1, padx=10)
    tk.Label(stats_info_frame, text="Losses", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10, "bold")).grid(row=0, column=2, padx=10)

    value_labels = {}
    for i, m in enumerate(_maps, start=1):
        tk.Label(stats_info_frame, text=m + ":", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10)).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        wins_lbl = tk.Label(stats_info_frame, text="0", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
        wins_lbl.grid(row=i, column=1)
        losses_lbl = tk.Label(stats_info_frame, text="0", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
        losses_lbl.grid(row=i, column=2)
        value_labels[m] = (wins_lbl, losses_lbl)

    tk.Label(stats_info_frame, text="Total Wins:", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10)).grid(row=len(_maps)+1, column=0, pady=(10,0))
    total_wins_value = tk.Label(stats_info_frame, text="0", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
    total_wins_value.grid(row=len(_maps)+1, column=1, pady=(10,0))

    tk.Label(stats_info_frame, text="Total Losses:", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10)).grid(row=len(_maps)+2, column=0)
    total_losses_value = tk.Label(stats_info_frame, text="0", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
    total_losses_value.grid(row=len(_maps)+2, column=1)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT map, result, COUNT(*) FROM matches GROUP BY map, result")
    rows = cur.fetchall()
    conn.close()

    totals = {"Win": 0, "Loss": 0}
    per_map_counts = {m: {"Win": 0, "Loss": 0} for m in _maps}
    for map_name, result, cnt in rows:
        if map_name in per_map_counts and result in ("Win", "Loss"):
            per_map_counts[map_name][result] = cnt
            totals[result] += cnt

    for m, (w_lbl, l_lbl) in value_labels.items():
        w_lbl.config(text=str(per_map_counts[m]["Win"]))
        l_lbl.config(text=str(per_map_counts[m]["Loss"]))

    total_wins_value.config(text=str(totals["Win"]))
    total_losses_value.config(text=str(totals["Loss"]))

    return

def enter_data():
    enter_data_window = tk.Toplevel(root)
    enter_data_window.title("Enter Match Data")
    enter_data_window.geometry("400x300")
    enter_data_window.configure(bg="#1e1e1e")


    stats_info_frame = tk.LabelFrame(enter_data_window, text="Map Info", bg="#1e1e1e", fg="#fb832b", font=("Comic Sans MS", 12))
    stats_info_frame.grid(row=0, column=0, padx=90, pady=90)

    map_info_label = tk.Label(stats_info_frame, text="Choose Map:", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
    map_info_label.grid(row=0, column=0)

    map_info_label_combobox = ttk.Combobox(stats_info_frame, values=["Dust II", "Mirage", "Inferno", "Train", "Overpass", "Ancient", "Vertigo"], font=("Comic Sans MS", 10))
    map_info_label_combobox.grid(row=0, column=1)

    map_win_or_loss_label = tk.Label(stats_info_frame, text="Win or Loss:", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
    map_win_or_loss_label.grid(row=1, column=0)

    map_win_or_loss_combobox = ttk.Combobox(stats_info_frame, values=["", "Win", "Loss"], font=("Comic Sans MS", 10))
    map_win_or_loss_combobox.grid(row=1, column=1)

    def on_submit():
        selected_map = map_info_label_combobox.get()
        selected_result = map_win_or_loss_combobox.get()
        if not selected_map or not selected_result:
            messagebox.showerror("Input Error", "Please select both map and result.")
            return
    
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("INSERT INTO matches (map, result) VALUES (?, ?)", (selected_map, selected_result))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", f"{selected_result} on {selected_map} saved.")
        enter_data_window.destroy()

    btn_submit = tk.Button(enter_data_window, text="Submit", bg="#fb832b", fg="#1e1e1e", font=("Comic Sans MS", 12), command=on_submit)
    btn_submit.place(x=160, y=220)

    return

def delete_data():
    delete_data_window = tk.Toplevel(root)
    delete_data_window.title("Delete Match Data")
    delete_data_window.geometry("400x300")
    delete_data_window.configure(bg="#1e1e1e")

    stats_info_frame = tk.LabelFrame(delete_data_window, text="Map Info", bg="#1e1e1e", fg="#fb832b", font=("Comic Sans MS", 12))
    stats_info_frame.grid(row=0, column=0, padx=90, pady=90)

    map_info_label = tk.Label(stats_info_frame, text="Choose Map:", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
    map_info_label.grid(row=0, column=0)

    map_info_label_combobox = ttk.Combobox(stats_info_frame, values=["Dust II", "Mirage", "Inferno", "Train", "Overpass", "Ancient", "Vertigo"], font=("Comic Sans MS", 10))
    map_info_label_combobox.grid(row=0, column=1)

    map_win_or_loss_label = tk.Label(stats_info_frame, text="Win or Loss:", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 10))
    map_win_or_loss_label.grid(row=1, column=0)

    map_win_or_loss_combobox = ttk.Combobox(stats_info_frame, values=["", "Win", "Loss"], font=("Comic Sans MS", 10))
    map_win_or_loss_combobox.grid(row=1, column=1)
    map_win_or_loss_combobox.current(0)

    def on_delete():
        selected_map = map_info_label_combobox.get()
        selected_result = map_win_or_loss_combobox.get()
        if not selected_map or not selected_result:
            messagebox.showerror("Error", "Please select both map and result.")
            return
    
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
                    DELETE FROM matches
                    WHERE id = (
                        SELECT id FROM matches
                        WHERE map = ? AND result = ?
                        ORDER BY id DESC
                        LIMIT 1
                    )
                """, (selected_map, selected_result))
        deleted = cur.rowcount
        conn.commit()
        conn.close()
        if deleted:
            messagebox.showinfo("Deleted", f"Last {selected_result} on {selected_map} has been deleted.")
        else:
            messagebox.showinfo("Not Found", f"No matching record found for {selected_result} on {selected_map}.")

    btn_delete = tk.Button(delete_data_window, text="Delete", bg="#fb832b", fg="#1e1e1e", font=("Comic Sans MS", 12), command=on_delete)
    btn_delete.place(x=160, y=220)

    return    

#Labels and Buttons
lbl = tk.Label(root, text="Counter-Strike 2 Stats Tracker", bg="#1e1e1e", fg="#fb832b", font=("Comic Sans MS", 30))
lbl.pack()

lbl2 = tk.Label(root, text="Developed by RubenJoel1", bg="#1e1e1e", fg="#fb832b", font=("Comic Sans MS", 10))
lbl2.pack()

lbl3 = tk.Label(root, text=" Dust II       Mirage       Inferno       Train       Overpass      Ancient      Vertigo  ", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 16))
lbl3.place(x=10, y=130)

image_dust2 = Image.open("Resources/Dust 2.png").resize((80, 80))
image_dust2 = ImageTk.PhotoImage(image_dust2)
lbl_dust2 = tk.Label(root, image=image_dust2, bg="#1e1e1e")
lbl_dust2.place(x=20, y=170)

image_mirage = Image.open("Resources/Mirage.png").resize((80, 80))
image_mirage = ImageTk.PhotoImage(image_mirage)
lbl_mirage = tk.Label(root, image=image_mirage, bg="#1e1e1e")
lbl_mirage.place(x=130, y=170)

image_inferno = Image.open("Resources/Inferno.png").resize((80, 80))
image_inferno = ImageTk.PhotoImage(image_inferno)
lbl_inferno = tk.Label(root, image=image_inferno, bg="#1e1e1e")
lbl_inferno.place(x=240, y=170)

image_train = Image.open("Resources/Train.png").resize((80, 80))
image_train = ImageTk.PhotoImage(image_train)
lbl_train = tk.Label(root, image=image_train, bg="#1e1e1e")
lbl_train.place(x=350, y=170)

image_overpass = Image.open("Resources/Overpass.png").resize((80, 80))
image_overpass = ImageTk.PhotoImage(image_overpass)
lbl_overpass = tk.Label(root, image=image_overpass, bg="#1e1e1e")
lbl_overpass.place(x=465, y=170)

image_ancient = Image.open("Resources/Ancient.png").resize((80, 80))
image_ancient = ImageTk.PhotoImage(image_ancient)
lbl_ancient = tk.Label(root, image=image_ancient, bg="#1e1e1e")
lbl_ancient.place(x=580, y=170)

image_vertigo = Image.open("Resources/Vertigo.png").resize((80, 80))
image_vertigo = ImageTk.PhotoImage(image_vertigo)
lbl_vertigo = tk.Label(root, image=image_vertigo, bg="#1e1e1e")
lbl_vertigo.place(x=690, y=170)

lbl4 = tk.Label(root, text="Maps:", bg="#1e1e1e", fg="#fdfdfd", font=("Comic Sans MS", 20))
lbl4.pack()

btn = tk.Button(root, text="View Stats", bg="#fb832b", fg="#1e1e1e", font=("Comic Sans MS", 15), command=show_stats)
btn.place(x=650, y=530)

btn = tk.Button(root, text="Enter Data", bg="#fb832b", fg="#1e1e1e", font=("Comic Sans MS", 15), command=enter_data)
btn.place(x=30, y=535)

btn = tk.Button(root, text="Delete Data", bg="#fb832b", fg="#1e1e1e", font=("Comic Sans MS", 15), command=delete_data)
btn.place(x=340, y=535)
root.mainloop()                                                                                                    