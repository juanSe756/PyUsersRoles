import cx_Oracle
from datetime import datetime

class OracleDBManager:
    def __init__(self):
        self.connection = cx_Oracle.connect("username/password@localhost:port/servicename")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def convert_to_excel_date(self, normal_date):
        self.cursor.callproc("convert_to_excel_date", [normal_date, cx_Oracle.NUMBER])
        excel_date = self.cursor.fetchone()[0]
        return excel_date

    def convert_to_normal_date(self, excel_date):
        self.cursor.callproc("convert_to_normal_date", [excel_date, cx_Oracle.DATE])
        normal_date = self.cursor.fetchone()[0]
        return normal_date

    def validate_credentials(self, username, password):
        self.cursor.callproc("validate_credentials", [username, password, cx_Oracle.NUMBER])
        is_valid = self.cursor.fetchone()[0]
        return bool(is_valid)
    
    def encrypt_password(self, password):
        hashed_password = self.cursor.var(cx_Oracle.STRING)
        self.cursor.callproc("encrypt_password", [password, hashed_password])
        return hashed_password.getvalue()
    
    def get_user_roles(self, nickname):
        roles_cursor = self.cursor.var(cx_Oracle.CURSOR)
        self.cursor.callproc("get_user_roles", [nickname, roles_cursor])
        roles = roles_cursor.getvalue()
        role_names = [row[0] for row in roles]
        return role_names
    def get_all_roles(self):
        roles_cursor = self.cursor.var(cx_Oracle.CURSOR)
        self.cursor.callproc("get_all_roles", [roles_cursor])
        roles = roles_cursor.getvalue()
        role_names = [row[0] for row in roles]
        return role_names
    

    
def display_roles(self, nickname):
    roles = self.db_manager.get_user_roles(nickname)
    print("Available roles:")
    for i, role in enumerate(roles, 1):
        print(f"{i}. {role}")
    return roles

def select_role(self, roles):
    while True:
        try:
            selection = int(input("Select a rol: "))
            if 1 <= selection <= len(roles):
                return roles[selection - 1]
            else:
                print("Invalid selection. Please enter a valid role number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def register(db_manager, Admin=False):
    username = input("Enter your name: ")
    last_name = input("Enter your last name: ")
    password = input("Enter a password: ")
    hashed_password = db_manager.encrypt_password(password)
    nickname = username.lower() + "." + last_name.lower()
    photo = input("Enter the path to your photo: ")
    user_register_date = db_manager.convert_to_excel_date(datetime.now())
    newuser_role = 2
    if Admin:
        newuser_role = select_role(db_manager.get_all_roles())
    # TODO: Add the user to users and users_roles tables with a default role of 'user'

def login(db_manager):
    nickname = input("Enter your nickname: ")
    password = input("Enter your password: ")
    valid = db_manager.validate_credentials(nickname, password)
    if valid == 1:
        roles = display_roles(nickname)
        if roles:
            selected_role = select_role(roles)
            print("loginned as", nickname, "#", selected_role)
        return True, nickname, selected_role
    elif valid == 0:
        print("Invalid credentials. Please try again.")
        return False
    else:
        print("User not found. Please register.")
        return False
def show_user_menu(db_manager):
            # TODO: Implement the user menu functionality
            pass
def show_admin_menu(db_manager):
    print("1. Create a new user")
    print("2. Update a user")
    print("3. Delete a user")
    print("4. Show all users")
    print("5. Search for a user")
    print("6. Logout")
    choice = input("Enter your choice: ")
    if choice == "1":
        register(db_manager, True)
    elif choice == "2":
        # TODO: Update a user
        pass
    elif choice == "3":
        # TODO: Delete a user
        pass
    elif choice == "4":
        # TODO: Show all users
        pass
    elif choice == "5":
        # TODO: Search for a user
        pass
    elif choice == "6":
        # TODO: Logout
        pass
    else:
        print("Invalid choice. Please enter a valid option.")
if __name__ == "__main__":
    db_manager = OracleDBManager()
    while True:
        print("\nWelcome:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            logined, nickname, rol = login(db_manager)
            if logined:
                if rol == "admin":
                    show_admin_menu(db_manager)
                if rol == "user":
                    show_user_menu(db_manager)
        elif choice == "2":
            register(db_manager)
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
