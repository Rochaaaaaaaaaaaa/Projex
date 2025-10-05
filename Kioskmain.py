import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import functools

# --- Updated Color Palette (based on your image) ---
SIDEBAR_BG = "#FFE08A"        # Light yellow
SIDEBAR_BTN = "#A7E3C4"       # Mint green
SIDEBAR_TEXT = "#2C2C2C"      # Dark gray
MAIN_BG = "#FFFFFF"           # White
SECTION_TITLE = "#F5B400"     # Orange-yellow
FOOTER_BTN = "#D32F2F"        # Red
FOOTER_TEXT = "#FFFFFF"       # White
HEADER_RED = "#B71C1C"        # Deep red
HEADER_BLUE = "#1A237E"       # Navy blue

# Initialize window
ctk.set_appearance_mode("light")
app = ctk.CTk()
app.title("Kiosk System")
app.geometry("1000x600")
app.configure(bg=MAIN_BG)  # Set main background to white

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
ctk.CTkLabel(
    header_frame,
    text="MAR GIERO ",
    font=("Arial", 28, "bold"),
    text_color=HEADER_RED,
    fg_color=MAIN_BG
).pack(side="left", padx=(40,0), pady=10)
ctk.CTkLabel(
    header_frame,
    text="RESTAURANT",
    font=("Arial", 28, "bold"),
    text_color=HEADER_BLUE,
    fg_color=MAIN_BG
).pack(side="left", pady=10)

# --- Left Navigation Bar ---
nav_frame = ctk.CTkFrame(app, width=200, corner_radius=20, fg_color=SIDEBAR_BG)
nav_frame.pack(side="left", fill="y", padx=0, pady=0)

nav_label = ctk.CTkLabel(nav_frame, text="MENU", font=("Arial", 20, "bold"), text_color=SIDEBAR_TEXT)
nav_label.pack(pady=(30, 10))

nav_btns = []
for category in products.keys():
    btn = ctk.CTkButton(
        nav_frame,
        text=category,
        width=180,
        height=50,
        fg_color=SIDEBAR_BTN,
        text_color=SIDEBAR_TEXT,
        font=("Arial", 16, "bold"),
        corner_radius=10,
        hover_color=MAIN_BG,
        command=lambda c=category: load_category(c)
    )
    nav_btns.append(btn)

for btn in nav_btns:
    btn.pack(expand=True, pady=15)

main_frame = ctk.CTkScrollableFrame(app, fg_color=MAIN_BG)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# --- Footer Buttons ---
footer_frame = ctk.CTkFrame(app, height=60, corner_radius=0, fg_color=MAIN_BG)
footer_frame.pack(side="bottom", fill="x")

def cancel_order():
    global cart
    cart = []
    messagebox.showinfo("Cancel", "Order has been cancelled.")
    show_best_seller_page()

def show_review_window():
    global review_win

    def refresh_review():
        for widget in review_win.winfo_children():
            widget.destroy()
        ctk.CTkLabel(review_win, text="Order Review", font=("Arial", 16, "bold"), text_color=FOOTER_BTN).pack(pady=10)
        items_frame = ctk.CTkFrame(review_win, fg_color=MAIN_BG)
        items_frame.pack(pady=10, fill="both", expand=True)
        total = 0
        for idx, item in enumerate(cart):
            item_frame = ctk.CTkFrame(items_frame, fg_color=SIDEBAR_BG)
            item_frame.pack(fill="x", pady=5, padx=10)
            ctk.CTkLabel(item_frame, text=item['name'], width=120, text_color=FOOTER_BTN, font=("Arial", 12, "bold")).pack(side="left")
            ctk.CTkLabel(item_frame, text=f"₱{item['price']}", width=60, text_color=HEADER_BLUE, font=("Arial", 12)).pack(side="left")
            qty_var = ctk.IntVar(value=item['qty'])

            def update_qty(new_qty, i=idx):
                if new_qty < 1:
                    return
                cart[i]['qty'] = new_qty
                refresh_review()

            def delete_item(i=idx):
                del cart[i]
                refresh_review()

            ctk.CTkButton(item_frame, text="-", width=30, fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, command=lambda i=idx: update_qty(cart[i]['qty'] - 1, i)).pack(side="left", padx=2)
            ctk.CTkLabel(item_frame, textvariable=qty_var, width=30, text_color=FOOTER_BTN).pack(side="left", padx=2)
            ctk.CTkButton(item_frame, text="+", width=30, fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=lambda i=idx: update_qty(cart[i]['qty'] + 1, i)).pack(side="left", padx=2)
            ctk.CTkButton(item_frame, text="Delete", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, width=60, command=lambda i=idx: delete_item(i)).pack(side="left", padx=10)
            total += item['price'] * item['qty']
        ctk.CTkLabel(review_win, text=f"Total: ₱{total}", font=("Arial", 14), text_color=HEADER_BLUE).pack(pady=10)

    if review_win is not None and review_win.winfo_exists():
        review_win.destroy()
        review_win = None
        return
    review_win = ctk.CTkToplevel(app)
    review_win.title("Review Order")
    review_win.geometry("400x400")
    review_win.configure(bg=MAIN_BG)
    refresh_review()

transaction_number = 1000  # Start from 1000 or any number you want
customer_number = 500  # Start from 500 or any number you want

def show_payment_window():
    global transaction_number, customer_number
    payment_win = ctk.CTkToplevel(app)
    payment_win.title("Payment")
    payment_win.geometry("400x320")
    payment_win.configure(bg=MAIN_BG)
    total = sum(item['price'] * item['qty'] for item in cart)
    ctk.CTkLabel(payment_win, text="Proceed to Payment", font=("Arial", 16, "bold"), text_color=FOOTER_BTN).pack(pady=10)
    ctk.CTkLabel(payment_win, text=f"Total Amount: ₱{total}", font=("Arial", 14), text_color=HEADER_BLUE).pack(pady=10)
    ctk.CTkLabel(payment_win, text=f"Transaction No: {transaction_number + 1}", font=("Arial", 12, "bold"), text_color=SECTION_TITLE).pack(pady=5)

    payment_type_var = ctk.StringVar(value="Cash")
    ctk.CTkLabel(payment_win, text="Select Payment Method:", font=("Arial", 12, "bold"), text_color=FOOTER_BTN).pack(pady=5)
    cash_radio = ctk.CTkRadioButton(payment_win, text="Cash", variable=payment_type_var, value="Cash", text_color=SIDEBAR_TEXT)
    cashless_radio = ctk.CTkRadioButton(payment_win, text="Cashless", variable=payment_type_var, value="Cashless", text_color=SIDEBAR_TEXT)
    cash_radio.pack(pady=2)
    cashless_radio.pack(pady=2)

    def complete_transaction():
        global transaction_number, customer_number, cart, review_win
        transaction_number += 1
        # No database code, just show message
        if payment_type_var.get() == "Cash":
            messagebox.showinfo("Payment", f"Payment Successful!\nTransaction No: {transaction_number}")
            cart.clear()  # Reset the order info
            if review_win is not None and review_win.winfo_exists():
                review_win.destroy()
                review_win = None
            payment_win.destroy()
        else:
            show_cashless_options()

    def show_cashless_options():
        for widget in payment_win.winfo_children():
            widget.destroy()
        ctk.CTkLabel(payment_win, text="Select Cashless Option", font=("Arial", 14, "bold"), text_color=FOOTER_BTN).pack(pady=10)
        def show_bank_qr():
            for widget in payment_win.winfo_children():
                widget.destroy()
            ctk.CTkLabel(payment_win, text="Scan Bank QR", font=("Arial", 14, "bold"), text_color=HEADER_BLUE).pack(pady=10)
            ctk.CTkLabel(payment_win, text="[Bank QR Here]", font=("Arial", 16), text_color=SECTION_TITLE).pack(pady=20)
            ctk.CTkButton(payment_win, text="Done", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=lambda: finish_cashless()).pack(pady=10)
        def show_gcash_qr():
            for widget in payment_win.winfo_children():
                widget.destroy()
            ctk.CTkLabel(payment_win, text="Scan GCash QR", font=("Arial", 14, "bold"), text_color=HEADER_BLUE).pack(pady=10)
            ctk.CTkLabel(payment_win, text="[GCash QR Here]", font=("Arial", 16), text_color=SECTION_TITLE).pack(pady=20)
            ctk.CTkButton(payment_win, text="Done", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=lambda: finish_cashless()).pack(pady=10)
        ctk.CTkButton(payment_win, text="Bank Payment", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=show_bank_qr).pack(pady=10)
        ctk.CTkButton(payment_win, text="GCash Payment", fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, command=show_gcash_qr).pack(pady=10)

    def finish_cashless():
        global transaction_number
        messagebox.showinfo("Payment", f"Cashless Payment Successful!\nTransaction No: {transaction_number}")
        payment_win.destroy()

    ctk.CTkButton(payment_win, text="Pay Now", fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, font=("Arial", 14, "bold"), command=complete_transaction).pack(pady=20)

cancel_btn = ctk.CTkButton(
    footer_frame,
    text="Cancel",
    height=40,
    width=150,
    fg_color=FOOTER_BTN,
    text_color=FOOTER_TEXT,
    font=("Arial", 14, "bold"),
    corner_radius=10,
    hover_color=SECTION_TITLE,
    command=cancel_order
)
cancel_btn.pack(side="left", padx=40, pady=10)

review_btn = ctk.CTkButton(
    footer_frame,
    text="Review",
    height=40,
    width=150,
    fg_color=FOOTER_BTN,
    text_color=FOOTER_TEXT,
    font=("Arial", 14, "bold"),
    corner_radius=10,
    hover_color=SECTION_TITLE,
    command=show_review_window
)
review_btn.pack(side="left", padx=40, pady=10)

pay_btn = ctk.CTkButton(
    footer_frame,
    text="Payment",
    height=40,
    width=150,
    fg_color=FOOTER_BTN,
    text_color=FOOTER_TEXT,
    font=("Arial", 14, "bold"),
    corner_radius=10,
    hover_color=SECTION_TITLE,
    command=show_payment_window
)
pay_btn.pack(side="left", padx=40, pady=10)

# --- Functions ---
def load_category(category):
    for widget in main_frame.winfo_children():
        widget.destroy()
    display_products(products[category])

def add_to_cart(product, qty):
    cart.append({"name": product['name'], "price": product['price'], "qty": qty})

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
    
    def increase():
        qty_var.set(qty_var.get() + 1)
    
    def decrease():
        if qty_var.get() > 1:
            qty_var.set(qty_var.get() - 1)
    
    ctk.CTkButton(selector_frame, text="-", width=30, fg_color=FOOTER_BTN, text_color=FOOTER_TEXT, command=decrease).pack(side="left", padx=5)
    ctk.CTkLabel(selector_frame, textvariable=qty_var, text_color=HEADER_BLUE).pack(side="left", padx=5)
    ctk.CTkButton(selector_frame, text="+", width=30, fg_color=HEADER_BLUE, text_color=FOOTER_TEXT, command=increase).pack(side="left", padx=5)
    ctk.CTkButton(selector_frame, text="Add to Order", fg_color=SECTION_TITLE, text_color=SIDEBAR_TEXT, font=("Arial", 12, "bold"), command=lambda: add_to_cart(product, qty_var.get())).pack(side="left", padx=10)
    return selector_frame

def show_best_seller_page():
    for widget in main_frame.winfo_children():
        widget.destroy()

    # --- Best Seller Section ---
    best_seller_label = ctk.CTkLabel(main_frame, text="Best Seller", font=("Arial", 18, "bold"), text_color=HEADER_BLUE)
    best_seller_label.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 0))

    best_sellers = [
        {"name": "Fried Chicken", "price": 120, "image": None},
        {"name": "Coke", "price": 50, "image": None},
        {"name": "Chicken Combo", "price": 180, "image": None},
    ]
    for col in range(3):
        main_frame.grid_columnconfigure(col, weight=1)
    for idx, product in enumerate(best_sellers):
        frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=MAIN_BG)
        frame.grid(row=1, column=idx, padx=20, pady=10, sticky="nsew")
        img_label = ctk.CTkLabel(frame, text="", image=sample_img)
        img_label.pack(pady=5)
        ctk.CTkLabel(frame, text=product['name'], font=("Arial", 14, "bold"), text_color=HEADER_BLUE).pack(pady=2)
        ctk.CTkLabel(frame, text=f"₱{product['price']}", font=("Arial", 12), text_color=FOOTER_BTN).pack(pady=2)
        ctk.CTkButton(
            frame,
            text="Select",
            fg_color=SECTION_TITLE,
            text_color=SIDEBAR_TEXT,
            font=("Arial", 12, "bold"),
            corner_radius=8,
            command=functools.partial(add_to_cart, product, 1)
        ).pack(pady=5)

    # --- Combo Meal Section ---
    combo_label = ctk.CTkLabel(main_frame, text="Combo Meal", font=("Arial", 18, "bold"), text_color=SECTION_TITLE)
    combo_label.grid(row=2, column=0, columnspan=3, sticky="ew", padx=10, pady=(20, 0))

    combo_meals = [
        {"name": "Burger Combo", "price": 160, "image": None},
        {"name": "Chicken Combo", "price": 180, "image": None},
        {"name": "Pork BBQ Combo", "price": 170, "image": None},
    ]
    for idx, product in enumerate(combo_meals):
        frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=MAIN_BG)
        frame.grid(row=3, column=idx, padx=20, pady=10, sticky="nsew")
        img_label = ctk.CTkLabel(frame, text="", image=sample_img)
        img_label.pack(pady=5)
        ctk.CTkLabel(frame, text=product['name'], font=("Arial", 14, "bold"), text_color=SECTION_TITLE).pack(pady=2)
        ctk.CTkLabel(frame, text=f"₱{product['price']}", font=("Arial", 12), text_color=FOOTER_BTN).pack(pady=2)
        ctk.CTkButton(
            frame,
            text="Select",
            fg_color=SECTION_TITLE,
            text_color=SIDEBAR_TEXT,
            font=("Arial", 12, "bold"),
            corner_radius=8,
            command=functools.partial(add_to_cart, product, 1)
        ).pack(pady=5)

    # --- Mix and Match Section ---
    mix_label = ctk.CTkLabel(main_frame, text="Mix and Match Combo", font=("Arial", 18, "bold"), text_color=FOOTER_BTN)
    mix_label.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=(20, 0))

    mix_and_match = [
        {"name": "Fruit Salad", "price": 85, "image": None},
        {"name": "Caesar Salad", "price": 90, "image": None},
        {"name": "Iced Tea", "price": 40, "image": None},
    ]
    for idx, product in enumerate(mix_and_match):
        frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=MAIN_BG)
        frame.grid(row=5, column=idx, padx=20, pady=10, sticky="nsew")
        img_label = ctk.CTkLabel(frame, text="", image=sample_img)
        img_label.pack(pady=5)
        ctk.CTkLabel(frame, text=product['name'], font=("Arial", 14, "bold"), text_color=FOOTER_BTN).pack(pady=2)
        ctk.CTkLabel(frame, text=f"₱{product['price']}", font=("Arial", 12), text_color=HEADER_BLUE).pack(pady=2)
        ctk.CTkButton(
            frame,
            text="Select",
            fg_color=SECTION_TITLE,
            text_color=SIDEBAR_TEXT,
            font=("Arial", 12, "bold"),
            corner_radius=8,
            command=functools.partial(add_to_cart, product, 1)
        ).pack(pady=5)
# Load default category
show_best_seller_page()

app.mainloop()