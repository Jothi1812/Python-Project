import mysql.connector
from tabulate import tabulate

# Function to create tables
def create_tables(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        rollno INT PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        institution VARCHAR(255) -- New column for institution
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sap (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rollno INT,
        event_type VARCHAR(50),
        won BOOLEAN,
        inside INT,
        outside INT,
        premiere INT,
        institution VARCHAR(255), -- New column for institution
        FOREIGN KEY (rollno) REFERENCES student(rollno)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS paper (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rollno INT,
        event_type VARCHAR(50),
        won BOOLEAN,
        inside INT,
        outside INT,
        premiere INT,
        institution VARCHAR(255), -- New column for institution
        FOREIGN KEY (rollno) REFERENCES student(rollno)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS project (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rollno INT,
        event_type VARCHAR(50),
        won BOOLEAN,
        inside INT,
        outside INT,
        premiere INT,
        institution VARCHAR(255), -- New column for institution
        FOREIGN KEY (rollno) REFERENCES student(rollno)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coding (
        id INT AUTO_INCREMENT PRIMARY KEY,
        rollno INT,
        event_type VARCHAR(50),
        won BOOLEAN,
        inside INT,
        outside INT,
        premiere INT,
        institution VARCHAR(255), -- New column for institution
        FOREIGN KEY (rollno) REFERENCES student(rollno)
    )
    """)


# Function to add institution name for a student
def add_institution_name(cursor, rollno, institution_name):
    cursor.execute("UPDATE student SET institution = %s WHERE rollno = %s", (institution_name, rollno))

# Function to get institution name for a student
def get_institution_name(cursor, rollno):
    cursor.execute(f"SELECT institution FROM student WHERE rollno = {rollno}")
    return cursor.fetchone()[0]

# Function to check if a table is empty
def is_table_empty(cursor, table_name):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    return cursor.fetchone()[0] == 0

# Function to get student details
def get_student_details(cursor, rollno):
    cursor.execute(f"SELECT * FROM student WHERE rollno = {rollno}")
    return cursor.fetchone()

# Function to add SAP data
def add_sap_data(cursor, rollno, event_type, won, inside, outside, premiere, inst):
    cursor.execute("INSERT INTO sap (rollno, event_type, won, inside, outside, premiere, institution) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (rollno, event_type, won, inside, outside, premiere, inst))
    
# Function to add Paper data
def add_paper_data(cursor, rollno, event_type, won, inside, outside, premiere, inst):
    cursor.execute("INSERT INTO paper (rollno, event_type, won, inside, outside, premiere, institution) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (rollno, event_type, won, inside, outside, premiere, inst))

# Function to add Project data
def add_project_data(cursor, rollno, event_type, won, inside, outside, premiere, inst):
    cursor.execute("INSERT INTO project (rollno, event_type, won, inside, outside, premiere, institution) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (rollno, event_type, won, inside, outside, premiere, inst))

# Function to add Coding data
def add_coding_data(cursor, rollno, event_type, won, inside, outside, premiere, inst):
    cursor.execute("INSERT INTO coding (rollno, event_type, won, inside, outside, premiere, institution) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (rollno, event_type, won, inside, outside, premiere, inst))    

# Function to display table data
def display_table_data(cursor, table_name, rollno=None):
    if rollno:
        cursor.execute(f"SELECT * FROM {table_name} WHERE rollno = {rollno}")
    else:
        cursor.execute(f"SELECT * FROM {table_name}")
    table_data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to display total SAP points
def display_total_sap_points(cursor, rollno):
    cursor.execute(f"SELECT event_type, SUM(inside + outside + premiere) as total_points FROM sap WHERE rollno = {rollno} GROUP BY event_type")
    table_data = cursor.fetchall()
    headers = [desc[0] for desc in cursor.description]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

# Function to allow admin to view a specific student's SAP data
def view_specific_student_sap(cursor):
    rollno_to_view = int(input("Enter the roll number to view SAP data: "))
    display_table_data(cursor, 'sap', rollno_to_view)
    display_total_sap_points(cursor,rollno_to_view)

# Main program
def main():
    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="XXXX",
        database="pythondb"
    )

    cursor = connection.cursor()

    # Create tables if not exists
    create_tables(cursor)

    # Ask if admin
    is_admin = input("Are you an admin? (yes/no): ").lower() == 'yes'

    if is_admin:
        password = input("Enter password: ")
        if password != "Advisor":
            print("Incorrect password. Exiting...")
            return

        while True:
            print("\nAdmin Menu:")
            print("1. View SAP")
            print("2. View Paper")
            print("3. View Project")
            print("4. View Coding")
            print("5. View SAP for a Specific Student")
            print("6. Exit")

            option = input("Enter your choice: ")

            if option == '1':
                display_table_data(cursor, 'sap')
            elif option == '2':
                display_table_data(cursor, 'paper')
            elif option == '3':
                display_table_data(cursor, 'project')
            elif option == '4':
                display_table_data(cursor, 'coding')
            elif option == '5':
                view_specific_student_sap(cursor)
            elif option == '6':
                break
            else:
                print("Invalid option. Please try again.")

    else:
        rollno = int(input("Enter your roll number: "))
        student_details = get_student_details(cursor, rollno)

        if student_details is None:
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            institution_name = input("Enter the institution name: ")  # Ask for institution name
            cursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s)", (rollno, name, email, institution_name))

        while True:
            print("\nUser Menu:")
            print("1. Add SAP Data")
            print("2. View SAP Data")
            print("3. Exit")

            option = input("Enter your choice: ")

            if option == '1':
                event_type = input("Enter event type (1.Paper presentation 2.Project Presentation 3.Coding): ")
                if event_type in ['1', '2', '3']:
                    inst = input('\nEnter the institution name you participated: ')

                    won = input("Did you win? (yes/no): ").lower() == 'yes'
                    inside, outside, premiere = 0, 0, 0
                   
                    if won:
                        venue = input("Inside? (yes/no): ").lower()
                        if venue == 'yes':
                            inside = int(input("Enter points for winning inside: "))
                        elif venue == 'no':
                            venue1 = input("Outside? (yes/no): ").lower()
                            if venue1 == 'no':
                                premiere = int(input("Enter points for winning premiere outside: "))
                            else:
                                outside = int(input("Enter points for winning outside: "))
                    else:
                        venue = input("Inside? (yes/no): ").lower()
                        if venue == 'yes':
                            inside = int(input("Enter points for participating inside: "))
                        elif venue == 'no':
                            venue1 = input("Outside? (yes/no): ").lower()
                            if venue1 == 'no':
                                premiere = int(input("Enter points for participating premiere outside: "))
                            else:
                                outside = int(input("Enter points for participating outside: "))

                    add_sap_data(cursor, rollno, event_type, won, inside, outside, premiere, inst)
                    if event_type == '1':
                        add_paper_data(cursor, rollno, event_type, won, inside, outside, premiere, inst)
                    elif event_type == '2':
                        add_project_data(cursor, rollno, event_type, won, inside, outside, premiere, inst)
                    elif event_type == '3':
                        add_coding_data(cursor, rollno, event_type, won, inside, outside, premiere, inst)
                else:
                    print("Invalid event type. Please try again.")
            elif option == '2':
                display_table_data(cursor, 'sap', rollno)
                display_total_sap_points(cursor, rollno)
            elif option == '3':
                break
            else:
                print("Invalid option. Please try again.")

    # Commit and close connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
