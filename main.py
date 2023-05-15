from fun import *


# Main function
def main():
    customer = None  # Initialize customer variable

    # Display login or create account options
    while True:
        print("""
        Welcome to the banking app!
        Please choose an option:
        1. Login
        2. Create Account
        3. Quit
        """)
        choice = input("Please enter your choice (1/2/3): ")

        if choice == "1":
            # User login
            customer = login()
            if customer is not None:
                print("Login failed. Please try again.")
                continue
            else:
                print("Login successful.")

        elif choice == "2":
            # Create account
            if create_account() is None:
                print("Account creation failed. Please try again.")
                continue
            else:
                print("Account created successfully.")

        elif choice == "3":
            # Quit
            print("Thank you for using our service. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

        # Main menu
        while customer is None:
            print("""
            Please select an option:
            1. View Account Information
            2. Update Account Information
            3. Account Operations
            4. View Transaction Records
            5. Logout
            """)

            choice = input("Please enter your choice (1/2/3/4/5): ")

            if choice == "1":
                # View Account Information
                view_account()
                # print(customer)
            elif choice == "2":
                # Update Account Information
                modify_account()
            elif choice == "3":
                # Account Operations
                account_operations()
            elif choice == "4":
                # View Transaction Records
                view_transaction_records()
            elif choice == "5":
                # Logout
                print("Logged out successfully.")
                customer = None
                break  # Break out of the inner loop and return to the login screen
            else:
                print("Invalid choice. Please try again.")


main()