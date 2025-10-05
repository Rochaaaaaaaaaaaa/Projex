import customtkinter as ctk

# --- Use the same color palette ---
SIDEBAR_BG = "#FFE08A"
SIDEBAR_TEXT = "#2C2C2C"
MAIN_BG = "#FFFFFF"
SECTION_TITLE = "#F5B400"
FOOTER_BTN = "#D32F2F"
HEADER_RED = "#B71C1C"
HEADER_BLUE = "#1A237E"

ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Queue Status")
app.geometry("600x400")
app.configure(bg=MAIN_BG)

# --- Placeholder for fetching queue/orders from database ---
def fetch_queue():
    # Replace with database query for live updates
    return [
        {"queue_no": 1, "transaction_no": 1001, "status": "Preparing"},
        {"queue_no": 2, "transaction_no": 1002, "status": "Serving"},
        # Add more orders as needed
    ]

queue_orders = fetch_queue()

header_frame = ctk.CTkFrame(app, fg_color=MAIN_BG, corner_radius=0)
header_frame.pack(side="top", fill="x")
ctk.CTkLabel(header_frame, text="QUEUE STATUS", font=("Arial", 28, "bold"), text_color=HEADER_BLUE, fg_color=MAIN_BG).pack(side="left", padx=(40,0), pady=10)

main_frame = ctk.CTkScrollableFrame(app, fg_color=MAIN_BG)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

for order in queue_orders:
    frame = ctk.CTkFrame(main_frame, fg_color=SIDEBAR_BG, corner_radius=10)
    frame.pack(fill="x", padx=10, pady=10)
    ctk.CTkLabel(frame, text=f"Queue No: {order['queue_no']}", font=("Arial", 18, "bold"), text_color=SECTION_TITLE).pack(anchor="w", padx=10, pady=5)
    ctk.CTkLabel(frame, text=f"Transaction No: {order['transaction_no']}", font=("Arial", 14), text_color=HEADER_RED).pack(anchor="w", padx=10)
    ctk.CTkLabel(frame, text=f"Status: {order['status']}", font=("Arial", 14, "bold"), text_color=FOOTER_BTN).pack(anchor="w", padx=10, pady=5)

app.mainloop()