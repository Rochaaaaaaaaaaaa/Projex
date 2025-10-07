import customtkinter as ctk

# --- Color Palette ---
SIDEBAR_BG = "#FFE08A"
MAIN_BG = "#FFFFFF"
FOOTER_BTN = "#D32F2F"
HEADER_RED = "#B71C1C"
HEADER_BLUE = "#1A237E"

ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Queue Status")
app.geometry("600x400")
app.configure(bg=MAIN_BG)

# --- Placeholder for fetching orders from database ---
# Replace this function with actual DB query later
def fetch_orders_placeholder():
    # Simulate live updates
    # You can add or remove orders here for testing dynamic behavior
    return [
        {"transaction_no": 1001, "status": "Preparing"},
        {"transaction_no": 1002, "status": "Serving"},
        {"transaction_no": 1003, "status": "Preparing"},
    ]

# --- Containers ---
transaction_frames = {}
served_transactions = set()

# --- Main scrollable frame ---
main_frame = ctk.CTkScrollableFrame(app, fg_color=MAIN_BG)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# --- Function to remove transaction ---
def remove_transaction(transaction_no):
    frame = transaction_frames.get(transaction_no)
    if frame:
        frame.pack_forget()
        frame.destroy()
        del transaction_frames[transaction_no]
        served_transactions.add(transaction_no)

# --- Update queue display dynamically ---
def update_queue_display():
    global transaction_frames, served_transactions

    # Fetch placeholder orders
    orders_db = fetch_orders_placeholder()

    for order in orders_db:
        t_no = order["transaction_no"]

        # Skip already served and removed transactions
        if t_no in served_transactions:
            continue

        if t_no not in transaction_frames:
            frame = ctk.CTkFrame(main_frame, fg_color=SIDEBAR_BG, corner_radius=10)
            frame.pack(fill="x", padx=10, pady=10)

            ctk.CTkLabel(frame, text=f"Transaction No: {t_no}", font=("Arial", 18, "bold"), text_color=HEADER_RED).pack(anchor="w", padx=10, pady=5)
            status_label = ctk.CTkLabel(frame, text=f"Status: {order['status']}", font=("Arial", 16, "bold"), text_color=FOOTER_BTN)
            status_label.pack(anchor="w", padx=10, pady=5)

            transaction_frames[t_no] = frame

            # Schedule removal if status is 'Serving'
            if order["status"] == "Serving":
                app.after(10000, lambda t=t_no: remove_transaction(t))

    # Remove any orders deleted from DB placeholder
    for t_no in list(transaction_frames.keys()):
        if not any(o["transaction_no"] == t_no for o in orders_db):
            remove_transaction(t_no)

    # Schedule next update
    app.after(2000, update_queue_display)

# Start dynamic update
update_queue_display()
app.mainloop()
