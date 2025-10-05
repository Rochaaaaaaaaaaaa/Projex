import customtkinter as ctk
from tkinter import messagebox

# --- Use the same color palette ---
SIDEBAR_BG = "#FFE08A"
SIDEBAR_BTN = "#A7E3C4"
SIDEBAR_TEXT = "#2C2C2C"
MAIN_BG = "#FFFFFF"
SECTION_TITLE = "#F5B400"
FOOTER_BTN = "#D32F2F"
FOOTER_TEXT = "#FFFFFF"
HEADER_RED = "#B71C1C"
HEADER_BLUE = "#1A237E"

ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Counter Area")
app.geometry("1000x600")
app.configure(bg=MAIN_BG)

# --- Local orders data ---
orders = [
    {"transaction_no": 1001, "items": [("Coke", 2), ("Fried Chicken", 1)], "total": 220, "status": "Pending", "queue_no": None},
    {"transaction_no": 1002, "items": [("Iced Tea", 1), ("Burger Combo", 1)], "total": 200, "status": "Pending", "queue_no": None},
]

next_queue_no = 1 + max([o["queue_no"] or 0 for o in orders], default=0)

def update_order_status(order, new_status, status_label):
    order["status"] = new_status
    status_label.configure(text=f"Status: {order['status']}")
    messagebox.showinfo("Status Updated", f"Order {order['transaction_no']} is now {new_status}.")

def confirm_order(order, queue_label, status_label):
    global next_queue_no
    if order["queue_no"] is None:
        order["queue_no"] = next_queue_no
        next_queue_no += 1
        queue_label.configure(text=f"Queue No: {order['queue_no']}")
        order["status"] = "Preparing"
        status_label.configure(text=f"Status: {order['status']}")
        messagebox.showinfo("Confirm", f"Order {order['transaction_no']} confirmed!\nQueue No: {order['queue_no']}")

# --- UI ---
header_frame = ctk.CTkFrame(app, fg_color=MAIN_BG, corner_radius=0)
header_frame.pack(side="top", fill="x")
ctk.CTkLabel(header_frame, text="COUNTER VIEW", font=("Arial", 28, "bold"), text_color=HEADER_BLUE, fg_color=MAIN_BG).pack(side="left", padx=(40,0), pady=10)

main_frame = ctk.CTkScrollableFrame(app, fg_color=MAIN_BG)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

for order in orders:
    order_frame = ctk.CTkFrame(main_frame, fg_color=SIDEBAR_BG, corner_radius=10)
    order_frame.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(order_frame, text=f"Transaction No: {order['transaction_no']}", font=("Arial", 16, "bold"), text_color=HEADER_RED).pack(anchor="w", padx=10, pady=5)
    for item_name, qty in order["items"]:
        ctk.CTkLabel(order_frame, text=f"{item_name} x{qty}", font=("Arial", 14), text_color=SIDEBAR_TEXT).pack(anchor="w", padx=20)
    ctk.CTkLabel(order_frame, text=f"Total: ₱{order['total']}", font=("Arial", 14, "bold"), text_color=HEADER_BLUE).pack(anchor="w", padx=10, pady=5)
    queue_label = ctk.CTkLabel(order_frame, text=f"Queue No: {order['queue_no'] if order['queue_no'] else 'Not assigned'}", font=("Arial", 12, "bold"), text_color=SECTION_TITLE)
    queue_label.pack(anchor="w", padx=10, pady=2)
    status_label = ctk.CTkLabel(order_frame, text=f"Status: {order['status']}", font=("Arial", 12, "bold"), text_color=FOOTER_BTN)
    status_label.pack(anchor="w", padx=10, pady=2)
    ctk.CTkButton(order_frame, text="Confirm Order", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT,
                  command=lambda o=order, ql=queue_label, sl=status_label: confirm_order(o, ql, sl)).pack(anchor="e", padx=10, pady=5)
    ctk.CTkButton(order_frame, text="Set Preparing", fg_color=SECTION_TITLE, text_color=SIDEBAR_TEXT,
                  command=lambda o=order, sl=status_label: update_order_status(o, "Preparing", sl)).pack(anchor="e", padx=10, pady=2)
    ctk.CTkButton(order_frame, text="Set Serving", fg_color=SIDEBAR_BTN, text_color=SIDEBAR_TEXT,
                  command=lambda o=order, sl=status_label: update_order_status(o, "Serving", sl)).pack(anchor="e", padx=10, pady=2)

app.mainloop()