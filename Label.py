import tkinter as tk
import csv

# Create the root window
root = tk.Tk()

# Create a Canvas widget
canvas = tk.Canvas(root)
canvas.pack()

# Set the row height
row_height = 60

# Set the column widths
col_widths = [100, 100, 200]

# Set the initial x and y coordinates
x, y = 0, 0

# Draw the column headers
headers = ['Jogo', 'Data', 'BetHouses']
for i, header in enumerate(headers):
    canvas.create_text(x + col_widths[i] / 2, y + row_height / 2, text=header)
    x += col_widths[i]
x, y = 0, row_height

# Create a list to store the row IDs
row_ids = []

# Open the CSV file
with open("Apostas.csv", "r", newline="") as csvfile:
    reader = csv.DictReader(csvfile)

    # Draw the data rows
    for row in reader:
        # Draw the cells
        canvas.create_text(x + col_widths[0] / 2, y + row_height / 2, text=f"{row['time_casa']}\n{row['time_fora']}")
        x += col_widths[0]
        canvas.create_text(x + col_widths[1] / 2, y + row_height / 2, text=f"{row['dia']} / {row['mes']} / {row['ano']}\n{row['hora']}:{row['minuto']}")
        x += col_widths[1]
        bethouses = f"{row['bethouse1']}({row['odd1']} × R$ {row['aposta1']})\n{row['bethouse2']}({row['odd2']} × R$ {row['aposta2']})"
        if row['bethouse3']:
            bethouses += f"\n{row['bethouse3']}({row['odd3']} × R$ {row['aposta3']})"
        canvas.create_text(x + col_widths[2] / 2, y + row_height / 2, text=bethouses)
        x = 0

        # Draw a rectangle around the row and store its ID
        row_id = canvas.create_rectangle(0, y, sum(col_widths), y + row_height, outline="black", fill="", tags="row")
        row_ids.append(row_id)

        y += row_height

# Function to handle row clicks
def on_row_click(event):
    # Get the ID of the clicked item
    item_id = canvas.find_withtag("current")[0]

    # Check if the item is a row
    if item_id in row_ids:
        # Deselect all rows
        for row_id in row_ids:
            canvas.itemconfigure(row_id, fill="")

        # Select the clicked row
        canvas.itemconfigure(item_id, fill="lightblue")

# Bind the left mouse button click event to the on_row_click function
canvas.tag_bind("row", "<Button-1>", on_row_click)

# Run the main loop
root.mainloop()
