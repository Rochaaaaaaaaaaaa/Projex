import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# === DATABASE PLACEHOLDER SECTION ===
"""
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",
            database="kiosk_system"
        )
        if connection.is_connected():
            print("Connected to database")
            return connection
    except Error as e:
        print("Error connecting to database:", e)
        return None

def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(\"""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                transaction_no INT NOT NULL,
                customer_no INT NOT NULL,
                total_amount DECIMAL(10,2),
                payment_type VARCHAR(20),
                order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        \""")
        cursor.execute(\"""
            CREATE TABLE IF NOT EXISTS order_items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                product_name VARCHAR(100),
                price DECIMAL(10,2),
                quantity INT,
                FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
            )
        \""")
        connection.commit()
        print("Tables ready")
    except Error as e:
        print("Error creating tables:", e)

def save_order(connection, transaction_no, customer_no, cart, payment_type):
    try:
        cursor = connection.cursor()
        total_amount = sum(item['price'] * item['qty'] for item in cart)
        cursor.execute(
            "INSERT INTO orders (transaction_no, customer_no, total_amount, payment_type) VALUES (%s,%s,%s,%s)",
            (transaction_no, customer_no, total_amount, payment_type)
        )
        order_id = cursor.lastrowid
        for item in cart:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_name, price, quantity) VALUES (%s,%s,%s,%s)",
                (order_id, item['name'], item['price'], item['qty'])
            )
        connection.commit()
        print("Order saved to database")
    except Error as e:
        print("Error saving order:", e)

# db_connection = create_connection()
# if db_connection:
#     create_tables(db_connection)
"""

# ============================================================

# --- Updated Color Palette ---
SIDEBAR_BG = "#FFE08A"
SIDEBAR_BTN = "#A7E3C4"
SIDEBAR_TEXT = "#2C2C2C"
MAIN_BG = "#FFFFFF"
SECTION_TITLE = "#F5B400"
FOOTER_BTN = "#D32F2F"
FOOTER_TEXT = "#FFFFFF"
HEADER_RED = "#B71C1C"
HEADER_BLUE = "#1A237E"

# Initialize window
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Kiosk System")
app.geometry("1000x600")
app.configure(bg=MAIN_BG)

# --- Data ---
products = {
    "Beverage": [
        {"name": "Coke", "price": 50, "image": None},
        {"name": "Sprite", "price": 45, "image": None},
        {"name": "Iced Tea", "price": 40, "image": None},
    ],
    "Meat": [
        {"name": "Fried Chicken", "price": 120, "image": None},
        {"name": "Pork BBQ", "price": 110, "image": None},
        {"name": "Beef Steak", "price": 150, "image": None},
    ],
    "Combo Meal": [
        {"name": "Chicken Combo", "price": 180, "image": None},
        {"name": "Burger Combo", "price": 160, "image": None},
    ],
    "Salad": [
        {"name": "Caesar Salad", "price": 90, "image": None},
        {"name": "Fruit Salad", "price": 85, "image": None},
    ]
}

# --- Order storage ---
cart = []
review_win = None

# --- Sample Image ---
def get_sample_image():
    img = Image.new("RGB", (80, 80), color=SIDEBAR_BTN)
    return ImageTk.PhotoImage(img)

sample_img = get_sample_image()

# --- Header ---
header_frame = ctk.CTkFrame(app, fg_color=MAIN_BG, corner_radius=0)
header_frame.pack(side="top", fill="x")
ctk.CTkLabel(header_frame, text="MAR GIERO ", font=("Arial", 28, "bold"), text_color=HEADER_RED, fg_color=MAIN_BG).pack(side="left", padx=(40,0), pady=10)
ctk.CTkLabel(header_frame, text="RESTAURANT", font=("Arial", 28, "bold"), text_color=HEADER_BLUE, fg_color=MAIN_BG).pack(side="left", pady=10)

# --- Left Navigation Bar ---
nav_frame = ctk.CTkFrame(app, width=200, corner_radius=20, fg_color=SIDEBAR_BG)
nav_frame.pack(side="left", fill="y", padx=0, pady=0)

nav_label = ctk.CTkLabel(nav_frame, text="MENU", font=("Arial", 20, "bold"), text_color=SIDEBAR_TEXT)
nav_label.pack(pady=(30, 10))

def load_category(category):
    for widget in main_frame.winfo_children():
        widget.destroy()
    display_products(products[category])

nav_btns = []
for category in products.keys():
    btn = ctk.CTkButton(nav_frame, text=category, width=180, height=50, fg_color=SIDEBAR_BTN, text_color=SIDEBAR_TEXT,
                        font=("Arial", 16, "bold"), corner_radius=10, hover_color=MAIN_BG, command=lambda c=category: load_category(c))
    nav_btns.append(btn)

for btn in nav_btns:
    btn.pack(expand=True, pady=15)

main_frame = ctk.CTkScrollableFrame(app, fg_color=MAIN_BG)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# --- Footer Buttons ---
footer_frame = ctk.CTkFrame(app, height=60, corner_radius=0, fg_color=MAIN_BG)
footer_frame.pack(side="bottom", fill="x")

# --- Payment button state updater ---
def update_payment_button_state():
    if cart:
        pay_btn.configure(state="normal", fg_color=HEADER_BLUE)
    else:
        pay_btn.configure(state="disabled", fg_color=FOOTER_BTN)

def cancel_order():
    global cart
    cart = []
    messagebox.showinfo("Cancel", "Order has been cancelled.")
    load_category("Beverage")
    update_payment_button_state()

def center_window(window, parent):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    x = parent.winfo_rootx() + (parent_width // 2) - (width // 2)
    y = parent.winfo_rooty() + (parent_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

# --- Review Window ---
review_win = None
def close_review():
    global review_win
    if review_win is not None and review_win.winfo_exists():
        review_win.destroy()
    review_win = None

def show_review_window():
    global review_win
    if review_win is not None and review_win.winfo_exists():
        review_win.destroy()
        review_win = None
        return

    review_win = ctk.CTkToplevel(app)
    review_win.title("Review Order")
    review_win.geometry("420x480")
    review_win.configure(bg=MAIN_BG)
    review_win.transient(app)
    review_win.grab_set()

    def refresh_review():
        for widget in review_win.winfo_children():
            widget.destroy()
        ctk.CTkLabel(review_win, text="Order Review", font=("Arial", 16, "bold"), text_color=FOOTER_BTN).pack(pady=10)
        items_frame = ctk.CTkScrollableFrame(review_win, fg_color=MAIN_BG, height=300)
        items_frame.pack(pady=10, fill="both", expand=True)
        total = 0
        for idx, item in enumerate(cart):
            item_frame = ctk.CTkFrame(items_frame, fg_color=SIDEBAR_BG)
            item_frame.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(item_frame, text=item['name'], width=140, text_color=FOOTER_BTN, font=("Arial", 12, "bold")).pack(side="left")
            ctk.CTkLabel(item_frame, text=f"₱{item['price']}", width=60, text_color=HEADER_BLUE, font=("Arial", 12)).pack(side="left")
            qty_var = ctk.IntVar(value=item['qty'])

            def update_qty(new_qty, i=idx):
                if new_qty < 1: return
                cart[i]['qty'] = new_qty
                refresh_review()
                update_payment_button_state()

            def delete_item(i=idx):
                del cart[i]
                refresh_review()
                update_payment_button_state()

            ctk.CTkButton(item_frame, text="-", width=30, fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, command=lambda i=idx: update_qty(cart[i]['qty'] - 1, i)).pack(side="left", padx=2)
            ctk.CTkLabel(item_frame, textvariable=qty_var, width=30, text_color=FOOTER_BTN).pack(side="left", padx=2)
            ctk.CTkButton(item_frame, text="+", width=30, fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=lambda i=idx: update_qty(cart[i]['qty'] + 1, i)).pack(side="left", padx=2)
            ctk.CTkButton(item_frame, text="Delete", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, width=60, command=lambda i=idx: delete_item(i)).pack(side="left", padx=10)
            total += item['price'] * item['qty']

        ctk.CTkLabel(review_win, text=f"Total: ₱{total}", font=("Arial", 14), text_color=HEADER_BLUE).pack(pady=6)
        ctk.CTkButton(review_win, text="Close", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT,
                      font=("Arial", 12, "bold"), command=close_review).pack(pady=10)

    refresh_review()
    center_window(review_win, app)
    review_win.lift()

# --- Payment window ---
transaction_number = 1000
customer_number = 500

def show_payment_window():
    if not cart:
        messagebox.showwarning("No Order", "Please add items before proceeding to payment!")
        return

    global transaction_number, customer_number, review_win
    payment_win = ctk.CTkToplevel(app)
    payment_win.title("Payment")
    payment_win.geometry("420x380")
    payment_win.configure(bg=MAIN_BG)
    payment_win.transient(app)
    payment_win.grab_set()

    total = sum(item['price'] * item['qty'] for item in cart)
    ctk.CTkLabel(payment_win, text="Proceed to Payment", font=("Arial", 16, "bold"), text_color=FOOTER_BTN).pack(pady=10)
    ctk.CTkLabel(payment_win, text=f"Total Amount: ₱{total}", font=("Arial", 14), text_color=HEADER_BLUE).pack(pady=6)
    ctk.CTkLabel(payment_win, text=f"Transaction No: {transaction_number + 1}", font=("Arial", 12, "bold"), text_color=SECTION_TITLE).pack(pady=6)

    payment_type_var = ctk.StringVar(value="Cash")
    ctk.CTkLabel(payment_win, text="Select Payment Method:", font=("Arial", 12, "bold"), text_color=FOOTER_BTN).pack(pady=4)
    ctk.CTkRadioButton(payment_win, text="Cash", variable=payment_type_var, value="Cash", text_color=SIDEBAR_TEXT).pack(pady=2)
    ctk.CTkRadioButton(payment_win, text="Cashless", variable=payment_type_var, value="Cashless", text_color=SIDEBAR_TEXT).pack(pady=2)

    def complete_transaction():
        global transaction_number, cart, review_win
        transaction_number += 1

        # === DATABASE SAVE PLACEHOLDER ===
        # if db_connection:
        #     save_order(db_connection, transaction_number, customer_number, cart, payment_type_var.get())
        
        if payment_type_var.get() == "Cash":
            messagebox.showinfo("Payment", f"Payment Successful!\nTransaction No: {transaction_number}")
            cart.clear()
            if review_win is not None and review_win.winfo_exists():
                review_win.destroy()
                review_win = None
            payment_win.destroy()
            payment_win.grab_release()
            update_payment_button_state()
        else:
            show_cashless_options(payment_win)

    def show_cashless_options(parent_win):
        for widget in parent_win.winfo_children():
            widget.destroy()
        ctk.CTkLabel(parent_win, text="Select Cashless Option", font=("Arial", 14, "bold"), text_color=FOOTER_BTN).pack(pady=10)
        def show_bank_qr():
            for widget in parent_win.winfo_children():
                widget.destroy()
            ctk.CTkLabel(parent_win, text="Scan Bank QR", font=("Arial", 14, "bold"), text_color=HEADER_BLUE).pack(pady=10)
            ctk.CTkLabel(parent_win, text="[Bank QR Here]", font=("Arial", 16), text_color=SECTION_TITLE).pack(pady=20)
            ctk.CTkButton(parent_win, text="Done", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=lambda: finish_cashless(parent_win)).pack(pady=10)
        def show_gcash_qr():
            for widget in parent_win.winfo_children():
                widget.destroy()
            ctk.CTkLabel(parent_win, text="Scan GCash QR", font=("Arial", 14, "bold"), text_color=HEADER_BLUE).pack(pady=10)
            ctk.CTkLabel(parent_win, text="[GCash QR Here]", font=("Arial", 16), text_color=SECTION_TITLE).pack(pady=20)
            ctk.CTkButton(parent_win, text="Done", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=lambda: finish_cashless(parent_win)).pack(pady=10)
        ctk.CTkButton(parent_win, text="Bank Payment", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=show_bank_qr).pack(pady=10)
        ctk.CTkButton(parent_win, text="GCash Payment", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, command=show_gcash_qr).pack(pady=10)
        ctk.CTkButton(parent_win, text="Cancel", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, command=lambda: [parent_win.destroy(), parent_win.grab_release()]).pack(pady=10)

    def finish_cashless(parent_win):
        global transaction_number, cart, review_win

        # === DATABASE SAVE PLACEHOLDER ===
        # if db_connection:
        #     save_order(db_connection, transaction_number, customer_number, cart, payment_type_var.get())

        messagebox.showinfo("Payment", f"Cashless Payment Successful!\nTransaction No: {transaction_number}")
        cart.clear()
        if review_win is not None and review_win.winfo_exists():
            review_win.destroy()
        review_win = None
        parent_win.destroy()
        parent_win.grab_release()
        update_payment_button_state()

    ctk.CTkButton(payment_win, text="Pay Now", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, font=("Arial", 14, "bold"), command=complete_transaction).pack(pady=16)
    ctk.CTkButton(payment_win, text="Cancel", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, font=("Arial", 12, "bold"), width=100, command=lambda: [payment_win.destroy(), payment_win.grab_release()]).pack(pady=(0, 10))
    center_window(payment_win, app)
    payment_win.lift()

# Footer action buttons
cancel_btn = ctk.CTkButton(footer_frame, text="Cancel", height=40, width=150, fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, font=("Arial", 14, "bold"), corner_radius=10, hover_color=SECTION_TITLE, command=cancel_order)
cancel_btn.pack(side="left", padx=40, pady=10)

review_btn = ctk.CTkButton(footer_frame, text="Review", height=40, width=150, fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, font=("Arial", 14, "bold"), corner_radius=10, hover_color=SECTION_TITLE, command=show_review_window)
review_btn.pack(side="left", padx=40, pady=10)

pay_btn = ctk.CTkButton(footer_frame, text="Payment", height=40, width=150, fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, font=("Arial", 14, "bold"), corner_radius=10, hover_color=SECTION_TITLE, command=show_payment_window)
pay_btn.pack(side="left", padx=40, pady=10)
pay_btn.configure(state="disabled")  # Initially disabled

# --- Functions for product listing & selection ---
def add_to_cart(product, qty):
    for item in cart:
        if item['name'] == product['name']:
            item['qty'] += qty
            update_payment_button_state()
            return
    cart.append({"name": product['name'], "price": product['price'], "qty": qty})
    update_payment_button_state()

def display_products(product_list):
    columns = 3
    for col in range(columns):
        main_frame.grid_columnconfigure(col, weight=1)
    for index, product in enumerate(product_list):
        frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=MAIN_BG)
        row = index // columns
        col = index % columns
        frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        frame.selector = None
        img_label = ctk.CTkLabel(frame, text="", image=sample_img)
        img_label.pack(pady=5)
        ctk.CTkLabel(frame, text=product['name'], font=("Arial", 14, "bold"), text_color=HEADER_BLUE).pack(pady=2)
        ctk.CTkLabel(frame, text=f"₱{product['price']}", font=("Arial", 12), text_color=FOOTER_BTN).pack(pady=2)

        def toggle_selector(f=frame, p=product):
            if hasattr(f, "selector") and f.selector is not None:
                f.selector.destroy()
                f.selector = None
            else:
                f.selector = show_quantity_selector(f, p)

        ctk.CTkButton(frame, text="Select", fg_color=SECTION_TITLE, text_color=SIDEBAR_TEXT, font=("Arial", 12, "bold"), corner_radius=8, command=toggle_selector).pack(pady=5)

def show_quantity_selector(parent, product):
    selector_frame = ctk.CTkFrame(parent, fg_color=SIDEBAR_BG)
    selector_frame.pack(pady=(5, 10))
    qty_var = ctk.IntVar(value=1)

    def increase(): qty_var.set(qty_var.get() + 1)
    def decrease(): 
        if qty_var.get() > 1: qty_var.set(qty_var.get() - 1)

    ctk.CTkButton(selector_frame, text="-", width=30, fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, command=decrease).pack(side="left", padx=5)
    ctk.CTkLabel(selector_frame, textvariable=qty_var, text_color=HEADER_BLUE).pack(side="left", padx=5)
    ctk.CTkButton(selector_frame, text="+", width=30, fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=increase).pack(side="left", padx=5)
    ctk.CTkButton(selector_frame, text="Add to Order", fg_color=SECTION_TITLE, text_color=SIDEBAR_TEXT, font=("Arial", 12, "bold"), command=lambda: add_to_cart(product, qty_var.get())).pack(side="left", padx=10)
    return selector_frame

# Load default category
load_category("Beverage")
app.mainloop()
