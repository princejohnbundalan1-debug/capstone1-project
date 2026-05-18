import sys
import random

# --- Temporary DATABASE Using Dictionary phyton ---
users = {
    "admin": {"password": "password123", "email": "admin@example.com", "role": "admin"}
}

customers = []
sales = []

# --- STATE ---
current_user = None

def generate_otp():
    return str(random.randint(100000, 999999))

def login():
    global current_user
    print("\n=== H2Ops System Login ===")
    print("Hint: login with username 'admin' and password 'password123'")
    username = input("Username: ")
    password = input("Password: ")
    
    if username in users and users[username]["password"] == password:
        otp = generate_otp()
        print(f"\n[SYSTEM] An OTP has been generated for {users[username]['email']}.")
        print(f"--- BYPASS OTP FOR TESTING: {otp} ---")
        
        entered_otp = input("\nEnter OTP to continue: ")
        if entered_otp == otp:
            current_user = username
            print("\nLogin successful!")
            return True
        else:
            print("\nInvalid OTP.")
            return False
    else:
        print("\nInvalid username or password.")
        return False

def add_customer():
    print("\n=== Add Customer ===")
    name = input("Name: ")
    phone = input("Phone: ")
    address = input("Address: ")
    customers.append({"id": len(customers) + 1, "name": name, "phone": phone, "address": address})
    print("Customer added successfully!")

def view_customers():
    print("\n=== Customer List ===")
    if not customers:
        print("No customers found.")
        return
    for c in customers:
        print(f"[{c['id']}] {c['name']} - {c['phone']} - {c['address']}")

def add_sale():
    print("\n=== Record Sale ===")
    if not customers:
        print("Please add a customer first.")
        return
        
    view_customers()
    try:
        customer_id = int(input("Enter Customer ID: "))
    except ValueError:
        print("Invalid input.")
        return
        
    gallons = input("Number of Gallons: ")
    try:
        total_price = float(gallons) * 35.0  # Assume 35 pesos per gallon
    except ValueError:
        print("Invalid gallons amount.")
        return
        
    sales.append({
        "id": len(sales) + 1,
        "customer_id": customer_id,
        "gallons": gallons,
        "total_price": total_price,
        "recorded_by": current_user
    })
    print(f"Sale recorded! Total: Php {total_price:.2f}")

def view_sales():
    print("\n=== Sales List ===")
    if not sales:
        print("No sales found.")
        return
    for s in sales:
        print(f"[{s['id']}] Customer ID: {s['customer_id']} | Gallons: {s['gallons']} | Total: Php {s['total_price']:.2f} | By: {s['recorded_by']}")

def main_menu():
    global current_user
    while True:
        print(f"\n=== H2Ops Main Menu (User: {current_user}) ===")
        print("1. View Customers")
        print("2. Add Customer")
        print("3. View Sales")
        print("4. Record Sale")
        print("5. Logout")
        print("6. Exit Prototype")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == '1':
            view_customers()
        elif choice == '2':
            add_customer()
        elif choice == '3':
            view_sales()
        elif choice == '4':
            add_sale()
        elif choice == '5':
            current_user = None
            print("Logged out.")
            break
        elif choice == '6':
            print("Exiting prototype...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

def main():
    print("Welcome to the H2Ops CLI Prototype!")
    while True:
        if current_user is None:
            if login():
                main_menu()
        else:
            main_menu()

if __name__ == "__main__":
    main()
