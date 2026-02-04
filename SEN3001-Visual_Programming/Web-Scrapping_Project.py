import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk # For using olympic rings image 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "olympic_rings.png")
medals = None
current_country = None
analytics = None

#Web scraping function

def scrape_medals(url: str) -> pd.DataFrame:

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.select("table tr")
    if not rows or len(rows) < 2:
        raise ValueError("Could not detect medal table on this page.")

    data = []

    for tr in rows[1:]:
        tds = tr.select("td")
        if len(tds) != 6:
            continue

        # Extract proper country name
        spans = tds[1].select("span")
        if len(spans) >= 2:
            country = spans[1].get_text(strip=True)
        else:
            country = tds[1].get_text(strip=True)

        # Extract medals
        try:
            gold = int(tds[2].get_text(strip=True))
            silver = int(tds[3].get_text(strip=True))
            bronze = int(tds[4].get_text(strip=True))
            total = int(tds[5].get_text(strip=True))
        except:
            continue

        data.append({
            "Country": country,
            "Gold": gold,
            "Silver": silver,
            "Bronze": bronze,
            "Total": total
        })

    if not data:
        raise ValueError("No medal rows found.")

    df = pd.DataFrame(data)

    # Compute ranking (doesnt affect alphabetical listbox)
    df = df.sort_values(
        by=["Gold", "Silver", "Bronze", "Total"],
        ascending=False
    ).reset_index(drop=True)
    df["Rank"] = range(1, len(df) + 1)

    return df



# GUI CALLBACKS

def show_list():
    global medals

    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    try:
        medals = scrape_medals(url)
    except Exception as e:
        messagebox.showerror("Scraping Error", f"{e}")
        return

    
    # SORT COUNTRIES ALPHABETICALLY

    sorted_countries = sorted(medals["Country"].tolist())

    country_list.delete(0, tk.END)
    for c in sorted_countries:
        country_list.insert(tk.END, c.upper())

    messagebox.showinfo("Success", "Countries loaded!")


def show_country_chart():
    global current_country

    if medals is None:
        messagebox.showwarning("Warning", "Load data first.")
        return

    sel = country_list.curselection()
    if not sel:
        messagebox.showwarning("Warning", "Select a country.")
        return

    selected_country = country_list.get(sel[0]).title()

    # find matching row
    row = medals[medals["Country"].str.upper() == selected_country.upper()].iloc[0]

    if current_country is not None:
        plt.close(current_country)

    labels = ["Gold", "Silver", "Bronze"]
    values = [row["Gold"], row["Silver"], row["Bronze"]]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=["gold", "silver", "sienna"])
    ax.set_title(f"Medal Count for {row['Country'].upper()}")
    ax.set_ylabel("Count")
    ax.set_xlabel("Medal Type")

    current_country = fig
    plt.show()


def show_analytics():
    global analytics

    if medals is None:
        messagebox.showwarning("Warning", "Load data first.")
        return

    df = medals.sort_values("Total", ascending=False).head(10)

    countries = df["Country"]
    golds = df["Gold"]
    silvers = df["Silver"]
    bronzes = df["Bronze"]
    totals = df["Total"]

    if analytics is not None:
        plt.close(analytics)

    fig, axes = plt.subplots(2, 2, figsize=(16, 8))

    gold_colors = ["gold", "goldenrod", "yellow", "orange", "khaki"] * 3
    silver_colors = ["silver", "lightgray", "gainsboro", "whitesmoke", "gray"] * 3
    bronze_colors = ["peru", "sienna", "chocolate", "brown", "tan"] * 3
    
    axes[0, 0].pie(golds, labels=countries, autopct="%1.1f%%", colors=gold_colors[:len(countries)])
    axes[0, 0].set_title("Gold Medals")

    axes[0, 1].pie(silvers, labels=countries, autopct="%1.1f%%", colors=silver_colors[:len(countries)])
    axes[0, 1].set_title("Silver Medals")

    axes[1, 0].pie(bronzes, labels=countries, autopct="%1.1f%%", colors=bronze_colors[:len(countries)])
    axes[1, 0].set_title("Bronze Medals")

    axes[1, 1].plot(countries, totals, marker="o")
    axes[1, 1].set_title("Total Medals")
    axes[1, 1].set_ylabel("Number of Medals")
    axes[1, 1].set_xlabel("Countries")

    fig.tight_layout()
    analytics = fig
    plt.show()



#TKINTER GUI (ROOT)

root = tk.Tk()
root.title("Olympics 2024")

try:
    img = Image.open(IMAGE_PATH)
    img = img.resize((160, 70))
    logo_img = ImageTk.PhotoImage(img)

    logo_label = tk.Label(root, image=logo_img)
    logo_label.image = logo_img  # keep reference
    logo_label.grid(row=1, column=0, pady=5)
except Exception as e:
    print("IMAGE LOAD ERROR:", e)
    print("IMAGE PATH USED:", IMAGE_PATH)  # If image fails print eror
    pass

title_label = tk.Label(root, text="Olympics 2024", font=("Arial", 12,))
title_label.grid(row=0, column=0, pady=5)


url_entry = tk.Entry(root, width=60)
url_entry.grid(row=2, column=0, padx=10, pady=5)

btn_load = tk.Button(root, width=10, text="Show List", command=show_list)
btn_load.grid(row=3, column=0, pady=5)

frame = tk.Frame(root)
frame.grid(row=4, column=0, pady=5)

country_list = tk.Listbox(frame, width=40, height=15)
country_list.grid(row=0, column=0)

scroll = tk.Scrollbar(frame, orient="vertical", command=country_list.yview)
scroll.grid(row=0, column=1, sticky="ns")
country_list.config(yscrollcommand=scroll.set)

label_info = tk.Label(root, text="Click on a country to see detailed medals:")
label_info.grid(row=5, column=0, pady=5)

btn_chart = tk.Button(root, text="Show Chart of Selected Country", command=show_country_chart)
btn_chart.grid(row=6   , column=0, pady=5)

btn_analytics = tk.Button(root, text="Show Top 10 Performing Countries Analytics", command=show_analytics)
btn_analytics.grid(row=7, column=0, pady=10)

root.mainloop()
