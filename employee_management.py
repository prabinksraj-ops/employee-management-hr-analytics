import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from mysql.connector import Error
import os
import csv
from datetime import datetime
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


# ============================================================
# COLORS
# ============================================================

NAVY = "#102A43"
NAVY_DARK = "#071A2B"

BLUE = "#2563EB"
BLUE_DARK = "#1D4ED8"
LIGHT_BLUE = "#EFF6FF"

GREEN = "#16A34A"
GREEN_DARK = "#15803D"
LIGHT_GREEN = "#F0FDF4"

RED = "#DC2626"
RED_DARK = "#B91C1C"
LIGHT_RED = "#FEF2F2"

ORANGE = "#EA580C"
LIGHT_ORANGE = "#FFF7ED"

PURPLE = "#7C3AED"
LIGHT_PURPLE = "#F5F3FF"

WHITE = "#FFFFFF"
BLACK = "#111827"

LIGHT_BG = "#F3F6FA"
LIGHT_GRAY = "#F8FAFC"

GRAY = "#627D98"
BORDER = "#D9E2EC"
DARK_TEXT = "#243B53"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("Employee Management & HR Analytics System")
root.geometry("1450x820")
root.minsize(1150, 700)
root.configure(bg=LIGHT_BG)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            return connection

    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Unable to connect to MySQL.\n\n{e}"
        )

    return None


# ============================================================
# CREATE EMPLOYEE LOGIN TABLE
# ============================================================

def create_login_table():

    connection = get_connection()

    if connection is None:
        return

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee_login (
                Employee_ID VARCHAR(10) PRIMARY KEY,
                Password VARCHAR(100) NOT NULL,
                FOREIGN KEY (Employee_ID)
                REFERENCES employees(Employee_ID)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )
        """)

        connection.commit()

        # Create login for existing employees
        cursor.execute("SELECT Employee_ID FROM employees")

        employees = cursor.fetchall()

        for row in employees:

            employee_id = str(row[0]).upper()

            cursor.execute(
                "SELECT Employee_ID FROM employee_login WHERE Employee_ID = %s",
                (employee_id,)
            )

            exists = cursor.fetchone()

            if not exists:

                default_password = employee_id.lower() + "@123"

                try:
                    cursor.execute(
                        """
                        INSERT INTO employee_login
                        (Employee_ID, Password)
                        VALUES (%s, %s)
                        """,
                        (employee_id, default_password)
                    )

                except Error:
                    pass

        connection.commit()

    except Error as e:

        messagebox.showerror(
            "Database Error",
            f"Could not create employee login table.\n\n{e}"
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# CLEAR MAIN WINDOW
# ============================================================

def clear_root():

    for widget in root.winfo_children():
        widget.destroy()


# ============================================================
# COMMON BUTTON
# ============================================================

def create_button(parent, text, command, bg, width=14):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=WHITE,
        activebackground=bg,
        activeforeground=WHITE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        cursor="hand2",
        width=width,
        height=1,
        padx=10,
        pady=7
    )


# ============================================================
# LOGIN CHOICE PAGE
# ============================================================

def show_login_choice():

    clear_root()

    root.title("Login - Employee Management System")

    main = tk.Frame(root, bg=LIGHT_BG)
    main.pack(fill="both", expand=True)

    # Header
    header = tk.Frame(
        main,
        bg=NAVY_DARK,
        height=100
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="EMPLOYEE MANAGEMENT & HR ANALYTICS",
        bg=NAVY_DARK,
        fg=WHITE,
        font=("Segoe UI", 24, "bold")
    ).pack(pady=(22, 3))

    tk.Label(
        header,
        text="Secure employee management system",
        bg=NAVY_DARK,
        fg="#CBD5E1",
        font=("Segoe UI", 11)
    ).pack()

    # Center
    center = tk.Frame(
        main,
        bg=LIGHT_BG
    )
    center.pack(expand=True)

    tk.Label(
        center,
        text="Welcome",
        bg=LIGHT_BG,
        fg=NAVY,
        font=("Segoe UI", 28, "bold")
    ).pack(pady=(10, 5))

    tk.Label(
        center,
        text="Select your login type",
        bg=LIGHT_BG,
        fg=GRAY,
        font=("Segoe UI", 12)
    ).pack(pady=(0, 30))

    cards = tk.Frame(center, bg=LIGHT_BG)
    cards.pack()

    # Admin card
    admin_card = tk.Frame(
        cards,
        bg=WHITE,
        width=330,
        height=230,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    admin_card.grid(row=0, column=0, padx=20)
    admin_card.pack_propagate(False)

    tk.Label(
        admin_card,
        text="🔐",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI Emoji", 42)
    ).pack(pady=(20, 5))

    tk.Label(
        admin_card,
        text="ADMIN LOGIN",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 17, "bold")
    ).pack()

    tk.Label(
        admin_card,
        text="Manage employees and HR data",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 10)
    ).pack(pady=5)

    create_button(
        admin_card,
        "Admin Login",
        show_admin_login,
        BLUE,
        20
    ).pack(pady=12)

    # Employee card
    employee_card = tk.Frame(
        cards,
        bg=WHITE,
        width=330,
        height=230,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    employee_card.grid(row=0, column=1, padx=20)
    employee_card.pack_propagate(False)

    tk.Label(
        employee_card,
        text="👤",
        bg=WHITE,
        fg=GREEN,
        font=("Segoe UI Emoji", 42)
    ).pack(pady=(20, 5))

    tk.Label(
        employee_card,
        text="EMPLOYEE LOGIN",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 17, "bold")
    ).pack()

    tk.Label(
        employee_card,
        text="View your employee information",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 10)
    ).pack(pady=5)

    create_button(
        employee_card,
        "Employee Login",
        show_employee_login,
        GREEN,
        20
    ).pack(pady=12)

    tk.Label(
        main,
        text="Employee Management & HR Analytics System",
        bg=LIGHT_BG,
        fg=GRAY,
        font=("Segoe UI", 9)
    ).pack(side="bottom", pady=15)


# ============================================================
# ADMIN LOGIN
# ============================================================

def show_admin_login():

    clear_root()

    root.title("Admin Login")

    frame = tk.Frame(root, bg=LIGHT_BG)
    frame.pack(fill="both", expand=True)

    card = tk.Frame(
        frame,
        bg=WHITE,
        width=450,
        height=540,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(
        card,
        text="🔐",
        bg=WHITE,
        fg=BLUE,
        font=("Segoe UI Emoji", 45)
    ).pack(pady=(28, 3))

    tk.Label(
        card,
        text="ADMIN LOGIN",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 22, "bold")
    ).pack()

    tk.Label(
        card,
        text="Login to access administration",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 10)
    ).pack(pady=(5, 25))

    tk.Label(
        card,
        text="Username",
        bg=WHITE,
        fg=DARK_TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=55)

    username_entry = tk.Entry(
        card,
        font=("Segoe UI", 12),
        bg=LIGHT_GRAY,
        fg=BLACK,
        relief="solid",
        bd=1
    )
    username_entry.pack(
        fill="x",
        padx=55,
        pady=(5, 18),
        ipady=7
    )

    tk.Label(
        card,
        text="Password",
        bg=WHITE,
        fg=DARK_TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=55)

    password_entry = tk.Entry(
        card,
        font=("Segoe UI", 12),
        bg=LIGHT_GRAY,
        fg=BLACK,
        show="*",
        relief="solid",
        bd=1
    )
    password_entry.pack(
        fill="x",
        padx=55,
        pady=(5, 25),
        ipady=7
    )

    def admin_login():

        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            show_admin_dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid admin username or password."
            )

    create_button(
        card,
        "LOGIN",
        admin_login,
        BLUE,
        20
    ).pack(pady=(0, 8))

    create_button(
        card,
        "← Back",
        show_login_choice,
        GRAY,
        20
    ).pack(pady=(0, 10))

    tk.Label(
        card,
        text="Use Back to return to Login Choice",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 9)
    ).pack(pady=(2, 0))

    username_entry.focus()


# ============================================================
# EMPLOYEE LOGIN
# ============================================================

def show_employee_login():

    clear_root()

    root.title("Employee Login")

    frame = tk.Frame(root, bg=LIGHT_BG)
    frame.pack(fill="both", expand=True)

    card = tk.Frame(
        frame,
        bg=WHITE,
        width=450,
        height=490,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)

    tk.Label(
        card,
        text="👤",
        bg=WHITE,
        fg=GREEN,
        font=("Segoe UI Emoji", 45)
    ).pack(pady=(30, 5))

    tk.Label(
        card,
        text="EMPLOYEE LOGIN",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 22, "bold")
    ).pack()

    tk.Label(
        card,
        text="Login using your Employee ID",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 10)
    ).pack(pady=(5, 30))

    tk.Label(
        card,
        text="Employee ID",
        bg=WHITE,
        fg=DARK_TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=55)

    employee_id_entry = tk.Entry(
        card,
        font=("Segoe UI", 12),
        bg=LIGHT_GRAY,
        fg=BLACK,
        relief="solid",
        bd=1
    )
    employee_id_entry.pack(
        fill="x",
        padx=55,
        pady=(5, 18),
        ipady=7
    )

    tk.Label(
        card,
        text="Password",
        bg=WHITE,
        fg=DARK_TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=55)

    password_entry = tk.Entry(
        card,
        font=("Segoe UI", 12),
        bg=LIGHT_GRAY,
        fg=BLACK,
        show="*",
        relief="solid",
        bd=1
    )
    password_entry.pack(
        fill="x",
        padx=55,
        pady=(5, 25),
        ipady=7
    )

    def employee_login():

        employee_id = employee_id_entry.get().strip().upper()
        password = password_entry.get().strip()

        if not employee_id or not password:

            messagebox.showwarning(
                "Missing Information",
                "Please enter Employee ID and Password."
            )
            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT Employee_ID
                FROM employee_login
                WHERE Employee_ID = %s
                AND Password = %s
                """,
                (employee_id, password)
            )

            result = cursor.fetchone()

            if result:

                show_employee_dashboard(employee_id)

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid Employee ID or Password."
                )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()

    create_button(
        card,
        "LOGIN",
        employee_login,
        GREEN,
        20
    ).pack(pady=5)

    create_button(
        card,
        "← Back",
        show_login_choice,
        GRAY,
        20
    ).pack(pady=10)

    employee_id_entry.focus()


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def show_admin_dashboard():

    clear_root()

    root.title("Admin Dashboard")

    # Header
    header = tk.Frame(
        root,
        bg=NAVY_DARK,
        height=90
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    title_frame = tk.Frame(header, bg=NAVY_DARK)
    title_frame.pack(side="left", padx=30, pady=15)

    tk.Label(
        title_frame,
        text="📊  ADMIN DASHBOARD",
        bg=NAVY_DARK,
        fg=WHITE,
        font=("Segoe UI", 22, "bold")
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text="Employee & HR overview",
        bg=NAVY_DARK,
        fg="#CBD5E1",
        font=("Segoe UI", 10)
    ).pack(anchor="w")

    create_button(
        header,
        "Logout",
        show_login_choice,
        RED,
        10
    ).pack(side="right", padx=25, pady=25)

    # Main
    main = tk.Frame(
        root,
        bg=LIGHT_BG
    )
    main.pack(fill="both", expand=True, padx=25, pady=25)

    # Get statistics
    total_employees = 0
    department_count = 0
    average_salary = 0
    total_salary = 0
    new_joiners = 0
    departments = []

    connection = get_connection()

    if connection:

        try:

            cursor = connection.cursor()

            cursor.execute(
                "SELECT COUNT(*) FROM employees"
            )
            total_employees = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(DISTINCT Department) FROM employees"
            )
            department_count = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COALESCE(AVG(Salary),0) FROM employees"
            )
            average_salary = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COALESCE(SUM(Salary),0) FROM employees"
            )
            total_salary = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM employees
                WHERE YEAR(DOJ) = YEAR(CURDATE())
                """
            )
            new_joiners = cursor.fetchone()[0]

            cursor.execute(
                """
                SELECT Department, COUNT(*)
                FROM employees
                GROUP BY Department
                ORDER BY COUNT(*) DESC
                """
            )

            departments = cursor.fetchall()

        except Error:
            pass

        finally:

            cursor.close()
            connection.close()

    # Dashboard cards
    cards_frame = tk.Frame(
        main,
        bg=LIGHT_BG
    )
    cards_frame.pack(fill="x")

    def dashboard_card(
        parent,
        column,
        icon,
        title,
        value,
        bg,
        icon_bg
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        icon_frame = tk.Frame(
            card,
            bg=icon_bg,
            width=65,
            height=65
        )
        icon_frame.pack(
            side="left",
            padx=18,
            pady=18
        )
        icon_frame.pack_propagate(False)

        tk.Label(
            icon_frame,
            text=icon,
            bg=icon_bg,
            fg=bg,
            font=("Segoe UI Emoji", 28)
        ).pack(expand=True)

        info = tk.Frame(
            card,
            bg=WHITE
        )
        info.pack(
            side="left",
            pady=15
        )

        tk.Label(
            info,
            text=title,
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            info,
            text=value,
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

    dashboard_card(
        cards_frame,
        0,
        "👥",
        "Total Employees",
        str(total_employees),
        BLUE,
        LIGHT_BLUE
    )

    dashboard_card(
        cards_frame,
        1,
        "🏢",
        "Departments",
        str(department_count),
        PURPLE,
        LIGHT_PURPLE
    )

    dashboard_card(
        cards_frame,
        2,
        "💰",
        "Average Salary",
        f"₹{float(average_salary):,.0f}",
        ORANGE,
        LIGHT_ORANGE
    )

    dashboard_card(
        cards_frame,
        3,
        "💵",
        "Total Salary",
        f"₹{float(total_salary):,.0f}",
        GREEN,
        LIGHT_GREEN
    )

    dashboard_card(
        cards_frame,
        4,
        "🆕",
        "New Joiners",
        str(new_joiners),
        GREEN,
        LIGHT_GREEN
    )

    # Bottom section
    bottom = tk.Frame(
        main,
        bg=LIGHT_BG
    )
    bottom.pack(
        fill="both",
        expand=True,
        pady=(25, 0)
    )

    # Department distribution
    department_frame = tk.Frame(
        bottom,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    department_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 12)
    )

    tk.Label(
        department_frame,
        text="Department Distribution",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 15, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(18, 3)
    )

    tk.Label(
        department_frame,
        text="Number of employees in each department",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 9)
    ).pack(
        anchor="w",
        padx=20
    )

    chart_area = tk.Frame(
        department_frame,
        bg=WHITE
    )
    chart_area.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    max_count = 1

    if departments:
        max_count = max(item[1] for item in departments)

    for department, count in departments:

        row = tk.Frame(
            chart_area,
            bg=WHITE
        )
        row.pack(
            fill="x",
            pady=7
        )

        tk.Label(
            row,
            text=str(department),
            bg=WHITE,
            fg=DARK_TEXT,
            font=("Segoe UI", 10, "bold"),
            width=14,
            anchor="w"
        ).pack(side="left")

        bar_bg = tk.Frame(
            row,
            bg="#E5E7EB",
            height=20
        )
        bar_bg.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        bar = tk.Frame(
            bar_bg,
            bg=BLUE,
            height=20
        )

        bar_width = max(
            10,
            int((count / max_count) * 100)
        )

        bar.place(
            relx=0,
            rely=0,
            relwidth=count / max_count,
            relheight=1
        )

        tk.Label(
            row,
            text=str(count),
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 10, "bold"),
            width=5
        ).pack(side="right")

    # Quick actions
    actions_frame = tk.Frame(
        bottom,
        bg=WHITE,
        width=350,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    actions_frame.pack(
        side="right",
        fill="y"
    )
    actions_frame.pack_propagate(False)

    tk.Label(
        actions_frame,
        text="Quick Actions",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 15, "bold")
    ).pack(
        anchor="w",
        padx=25,
        pady=(20, 5)
    )

    tk.Label(
        actions_frame,
        text="Manage employee records",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 9)
    ).pack(
        anchor="w",
        padx=25,
        pady=(0, 20)
    )

    create_button(
        actions_frame,
        "👥  Employee Management",
        show_employee_management,
        BLUE,
        25
    ).pack(pady=8)

    create_button(
        actions_frame,
        "🔎  Search Employee",
        search_employee_window,
        PURPLE,
        25
    ).pack(pady=8)

    create_button(
        actions_frame,
        "📋  View All Employees",
        show_all_employees,
        GREEN,
        25
    ).pack(pady=8)

    create_button(
        actions_frame,
        "🔄  Refresh Dashboard",
        show_admin_dashboard,
        NAVY,
        25
    ).pack(pady=8)


# ============================================================
# VIEW ALL EMPLOYEES
# ============================================================

def show_all_employees():

    clear_root()

    root.title("View All Employees")

    # Simple header with only Back button
    header = tk.Frame(
        root,
        bg=NAVY_DARK,
        height=75
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="📋  ALL EMPLOYEE DETAILS",
        bg=NAVY_DARK,
        fg=WHITE,
        font=("Segoe UI", 21, "bold")
    ).pack(side="left", padx=25, pady=18)

    create_button(
        header,
        "← Back",
        show_admin_dashboard,
        GRAY,
        12
    ).pack(side="right", padx=25, pady=17)

    main = tk.Frame(root, bg=LIGHT_BG)
    main.pack(fill="both", expand=True, padx=15, pady=15)

    table_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    table_frame.pack(fill="both", expand=True)

    columns = [
        "Employee_ID", "Name", "DOB", "DOJ", "Gender",
        "Department", "Designation", "Salary", "Contact",
        "Email", "Address"
    ]

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "ViewAll.Treeview",
        background=WHITE,
        foreground=BLACK,
        rowheight=32,
        fieldbackground=WHITE,
        font=("Segoe UI", 9)
    )

    style.configure(
        "ViewAll.Treeview.Heading",
        background=NAVY,
        foreground=WHITE,
        font=("Segoe UI", 9, "bold"),
        padding=8
    )

    style.map(
        "ViewAll.Treeview",
        background=[("selected", BLUE)],
        foreground=[("selected", WHITE)]
    )

    # Treeview container with BOTH scrollbars
    tree_container = tk.Frame(table_frame, bg=WHITE)
    tree_container.pack(fill="both", expand=True, padx=12, pady=12)

    tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        style="ViewAll.Treeview",
        selectmode="browse"
    )

    widths = {
        "Employee_ID": 110,
        "Name": 160,
        "DOB": 110,
        "DOJ": 110,
        "Gender": 90,
        "Department": 140,
        "Designation": 160,
        "Salary": 110,
        "Contact": 130,
        "Email": 220,
        "Address": 260
    }

    for column in columns:
        tree.heading(column, text=column.replace("_", " "))
        tree.column(
            column,
            width=widths[column],
            minwidth=80,
            anchor="w",
            stretch=False
        )

    scroll_y = ttk.Scrollbar(
        tree_container,
        orient="vertical",
        command=tree.yview
    )

    scroll_x = ttk.Scrollbar(
        tree_container,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    tree_container.grid_rowconfigure(0, weight=1)
    tree_container.grid_columnconfigure(0, weight=1)

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT
                Employee_ID, Name, DOB, DOJ, Gender,
                Department, Designation, Salary, Contact,
                Email, Address
            FROM employees
            ORDER BY Employee_ID
            """
        )

        rows = cursor.fetchall()

        for row in rows:
            values = list(row)
            if values[2] is not None:
                values[2] = str(values[2])
            if values[3] is not None:
                values[3] = str(values[3])
            tree.insert("", "end", values=values)

    except Error as e:
        messagebox.showerror(
            "Database Error",
            f"Could not load employees.\n\n{e}"
        )

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()

    # Press Escape to return to dashboard
    root.bind("<Escape>", lambda event: show_admin_dashboard())


# ============================================================
# EMPLOYEE MANAGEMENT
# ============================================================

def show_employee_management():

    clear_root()

    root.title("Employee Management")

    # ========================================================
    # HEADER
    # ========================================================

    header = tk.Frame(
        root,
        bg=NAVY_DARK,
        height=90
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    left_header = tk.Frame(
        header,
        bg=NAVY_DARK
    )
    left_header.pack(
        side="left",
        padx=25,
        pady=15
    )

    tk.Label(
        left_header,
        text="👥  EMPLOYEE MANAGEMENT",
        bg=NAVY_DARK,
        fg=WHITE,
        font=("Segoe UI", 21, "bold")
    ).pack(anchor="w")

    tk.Label(
        left_header,
        text="Add, update, delete and manage employee records",
        bg=NAVY_DARK,
        fg="#CBD5E1",
        font=("Segoe UI", 9)
    ).pack(anchor="w")

    create_button(
        header,
        "← Dashboard",
        show_admin_dashboard,
        GRAY,
        12
    ).pack(
        side="right",
        padx=25,
        pady=25
    )

    # ========================================================
    # ACTION BUTTONS
    # ========================================================

    action_bar = tk.Frame(
        root,
        bg=WHITE,
        height=65,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    action_bar.pack(
        fill="x",
        padx=15,
        pady=(15, 8)
    )
    action_bar.pack_propagate(False)

    # ========================================================
    # CONTENT
    # ========================================================

    content = tk.Frame(
        root,
        bg=LIGHT_BG
    )
    content.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )

    # ========================================================
    # EMPLOYEE FORM
    # ========================================================

    form_frame = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    form_frame.pack(
        fill="x",
        pady=(0, 10)
    )

    tk.Label(
        form_frame,
        text="EMPLOYEE DETAILS",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 14, "bold")
    ).grid(
        row=0,
        column=0,
        columnspan=6,
        sticky="w",
        padx=20,
        pady=(15, 10)
    )

    entries = {}

    fields = [
        "Employee ID",
        "Name",
        "DOB",
        "DOJ",
        "Gender",
        "Department",
        "Designation",
        "Salary",
        "Contact",
        "Email",
        "Address"
    ]

    # 6 columns
    for i in range(6):
        form_frame.grid_columnconfigure(
            i,
            weight=1
        )

    def add_field(
        field_name,
        row,
        column,
        columnspan=1
    ):

        tk.Label(
            form_frame,
            text=field_name,
            bg=WHITE,
            fg=DARK_TEXT,
            font=("Segoe UI", 9, "bold")
        ).grid(
            row=row,
            column=column,
            sticky="w",
            padx=(20, 5),
            pady=(5, 2)
        )

        entry = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bg=LIGHT_GRAY,
            fg=BLACK,
            relief="solid",
            bd=1
        )

        entry.grid(
            row=row + 1,
            column=column,
            columnspan=columnspan,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 8),
            ipady=5
        )

        entries[field_name] = entry

    add_field("Employee ID", 1, 0)
    add_field("Name", 1, 1)
    add_field("DOB", 1, 2)
    add_field("DOJ", 1, 3)
    add_field("Gender", 1, 4)
    add_field("Department", 1, 5)

    add_field("Designation", 3, 0)
    add_field("Salary", 3, 1)
    add_field("Contact", 3, 2)
    add_field("Email", 3, 3)
    add_field("Address", 3, 4, 2)

    # ========================================================
    # TREEVIEW
    # ========================================================

    table_frame = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    table_frame.pack(
        fill="both",
        expand=True
    )

    table_header = tk.Frame(
        table_frame,
        bg=WHITE
    )
    table_header.pack(
        fill="x",
        padx=15,
        pady=(10, 5)
    )

    tk.Label(
        table_header,
        text="ALL EMPLOYEE DETAILS",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 14, "bold")
    ).pack(side="left")

    count_label = tk.Label(
        table_header,
        text="Total: 0",
        bg=WHITE,
        fg=BLUE,
        font=("Segoe UI", 10, "bold")
    )
    count_label.pack(side="right")

    tree_container = tk.Frame(
        table_frame,
        bg=WHITE
    )
    tree_container.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=(0, 15)
    )

    columns = [
        "Employee_ID",
        "Name",
        "DOB",
        "DOJ",
        "Gender",
        "Department",
        "Designation",
        "Salary",
        "Contact",
        "Email",
        "Address"
    ]

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Treeview",
        background=WHITE,
        foreground=BLACK,
        rowheight=30,
        fieldbackground=WHITE,
        font=("Segoe UI", 9)
    )

    style.configure(
        "Treeview.Heading",
        background=NAVY,
        foreground=WHITE,
        font=("Segoe UI", 9, "bold"),
        padding=7
    )

    style.map(
        "Treeview",
        background=[
            ("selected", BLUE)
        ],
        foreground=[
            ("selected", WHITE)
        ]
    )

    tree = ttk.Treeview(
        tree_container,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    widths = {
        "Employee_ID": 90,
        "Name": 140,
        "DOB": 100,
        "DOJ": 100,
        "Gender": 80,
        "Department": 110,
        "Designation": 140,
        "Salary": 100,
        "Contact": 120,
        "Email": 190,
        "Address": 220
    }

    for column in columns:

        tree.heading(
            column,
            text=column.replace("_", " ")
        )

        tree.column(
            column,
            width=widths.get(column, 120),
            minwidth=70,
            anchor="w"
        )

    scroll_y = ttk.Scrollbar(
        tree_container,
        orient="vertical",
        command=tree.yview
    )

    scroll_x = ttk.Scrollbar(
        tree_container,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    scroll_y.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    scroll_x.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    tree_container.grid_rowconfigure(
        0,
        weight=1
    )

    tree_container.grid_columnconfigure(
        0,
        weight=1
    )

    # ========================================================
    # FORM FUNCTIONS
    # ========================================================

    def clear_form():

        for entry in entries.values():
            entry.delete(0, tk.END)

        entries["Employee ID"].focus()

        for item in tree.selection():
            tree.selection_remove(item)

    def load_employees():

        for item in tree.get_children():
            tree.delete(item)

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    Employee_ID,
                    Name,
                    DOB,
                    DOJ,
                    Gender,
                    Department,
                    Designation,
                    Salary,
                    Contact,
                    Email,
                    Address
                FROM employees
                ORDER BY Employee_ID
                """
            )

            rows = cursor.fetchall()

            for row in rows:

                formatted_row = list(row)

                # Format dates
                if formatted_row[2] is not None:
                    formatted_row[2] = str(formatted_row[2])

                if formatted_row[3] is not None:
                    formatted_row[3] = str(formatted_row[3])

                tree.insert(
                    "",
                    "end",
                    values=formatted_row
                )

            count_label.config(
                text=f"Total: {len(rows)}"
            )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                f"Could not load employees.\n\n{e}"
            )

        finally:

            cursor.close()
            connection.close()

    def add_employee():

        values = {
            field: entries[field].get().strip()
            for field in fields
        }

        employee_id = values["Employee ID"].upper()
        name = values["Name"]

        if not employee_id or not name:

            messagebox.showwarning(
                "Missing Information",
                "Employee ID and Name are required."
            )
            return

        dob = values["DOB"] if values["DOB"] else None
        doj = values["DOJ"] if values["DOJ"] else None
        salary = values["Salary"] if values["Salary"] else None

        # Validate date
        for date_value, label in [
            (dob, "DOB"),
            (doj, "DOJ")
        ]:

            if date_value:

                try:
                    datetime.strptime(
                        date_value,
                        "%Y-%m-%d"
                    )

                except ValueError:

                    messagebox.showerror(
                        "Invalid Date",
                        f"{label} must be in YYYY-MM-DD format."
                    )
                    return

        # Validate salary
        if salary:

            try:
                float(salary)

            except ValueError:

                messagebox.showerror(
                    "Invalid Salary",
                    "Salary must be a number."
                )
                return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO employees
                (
                    Employee_ID,
                    Name,
                    DOB,
                    DOJ,
                    Gender,
                    Department,
                    Designation,
                    Salary,
                    Contact,
                    Email,
                    Address
                )
                VALUES
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    employee_id,
                    name,
                    dob,
                    doj,
                    values["Gender"],
                    values["Department"],
                    values["Designation"],
                    salary,
                    values["Contact"],
                    values["Email"],
                    values["Address"]
                )
            )

            # Create employee login
            default_password = employee_id.lower() + "@123"

            cursor.execute(
                """
                INSERT INTO employee_login
                (Employee_ID, Password)
                VALUES (%s, %s)
                """,
                (
                    employee_id,
                    default_password
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                f"Employee {employee_id} added successfully.\n\n"
                f"Employee Login\n"
                f"ID: {employee_id}\n"
                f"Password: {default_password}"
            )

            clear_form()
            load_employees()

        except Error as e:

            connection.rollback()

            messagebox.showerror(
                "Add Employee Failed",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()

    def update_employee():

        employee_id = entries["Employee ID"].get().strip().upper()

        if not employee_id:

            messagebox.showwarning(
                "Select Employee",
                "Please select an employee from the table."
            )
            return

        values = {
            field: entries[field].get().strip()
            for field in fields
        }

        dob = values["DOB"] if values["DOB"] else None
        doj = values["DOJ"] if values["DOJ"] else None
        salary = values["Salary"] if values["Salary"] else None

        if dob:

            try:
                datetime.strptime(
                    dob,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid DOB",
                    "DOB must be YYYY-MM-DD."
                )
                return

        if doj:

            try:
                datetime.strptime(
                    doj,
                    "%Y-%m-%d"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid DOJ",
                    "DOJ must be YYYY-MM-DD."
                )
                return

        if salary:

            try:
                float(salary)

            except ValueError:

                messagebox.showerror(
                    "Invalid Salary",
                    "Salary must be a number."
                )
                return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE employees
                SET
                    Name = %s,
                    DOB = %s,
                    DOJ = %s,
                    Gender = %s,
                    Department = %s,
                    Designation = %s,
                    Salary = %s,
                    Contact = %s,
                    Email = %s,
                    Address = %s
                WHERE Employee_ID = %s
                """,
                (
                    values["Name"],
                    dob,
                    doj,
                    values["Gender"],
                    values["Department"],
                    values["Designation"],
                    salary,
                    values["Contact"],
                    values["Email"],
                    values["Address"],
                    employee_id
                )
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Employee updated successfully."
            )

            load_employees()

        except Error as e:

            connection.rollback()

            messagebox.showerror(
                "Update Failed",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()

    def delete_employee():

        employee_id = entries["Employee ID"].get().strip().upper()

        if not employee_id:

            messagebox.showwarning(
                "Select Employee",
                "Please select an employee first."
            )
            return

        answer = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {employee_id}?"
        )

        if not answer:
            return

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM employees
                WHERE Employee_ID = %s
                """,
                (employee_id,)
            )

            connection.commit()

            messagebox.showinfo(
                "Deleted",
                f"Employee {employee_id} deleted successfully."
            )

            clear_form()
            load_employees()

        except Error as e:

            connection.rollback()

            messagebox.showerror(
                "Delete Failed",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()

    def download_csv():

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    Employee_ID,
                    Name,
                    DOB,
                    DOJ,
                    Gender,
                    Department,
                    Designation,
                    Salary,
                    Contact,
                    Email,
                    Address
                FROM employees
                ORDER BY Employee_ID
                """
            )

            rows = cursor.fetchall()

            if not rows:

                messagebox.showinfo(
                    "No Data",
                    "There are no employees to download."
                )
                return

            file_path = filedialog.asksaveasfilename(
                title="Save Employee CSV",
                defaultextension=".csv",
                initialfile="employee_details.csv",
                filetypes=[
                    ("CSV files", "*.csv"),
                    ("All files", "*.*")
                ]
            )

            if not file_path:
                return

            with open(
                file_path,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(columns)

                for row in rows:
                    writer.writerow(row)

            messagebox.showinfo(
                "Download Complete",
                f"CSV file saved successfully.\n\n{file_path}"
            )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        except Exception as e:

            messagebox.showerror(
                "CSV Error",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()

    # ========================================================
    # ACTION BUTTONS
    # IMPORTANT: FUNCTIONS ARE DEFINED BEFORE BUTTONS
    # ========================================================

    create_button(
        action_bar,
        "➕ ADD",
        add_employee,
        GREEN,
        12
    ).pack(
        side="left",
        padx=(15, 5),
        pady=10
    )

    create_button(
        action_bar,
        "✏ UPDATE",
        update_employee,
        BLUE,
        12
    ).pack(
        side="left",
        padx=5,
        pady=10
    )

    create_button(
        action_bar,
        "🗑 DELETE",
        delete_employee,
        RED,
        12
    ).pack(
        side="left",
        padx=5,
        pady=10
    )

    create_button(
        action_bar,
        "🧹 CLEAR",
        clear_form,
        GRAY,
        12
    ).pack(
        side="left",
        padx=5,
        pady=10
    )

    create_button(
        action_bar,
        "📥 DOWNLOAD CSV",
        download_csv,
        NAVY,
        17
    ).pack(
        side="left",
        padx=5,
        pady=10
    )

    # ========================================================
    # TREEVIEW CLICK
    # ========================================================

    def select_employee(event):

        selected = tree.selection()

        if not selected:
            return

        values = tree.item(
            selected[0],
            "values"
        )

        for index, field in enumerate(fields):

            entries[field].delete(
                0,
                tk.END
            )

            if index < len(values):

                entries[field].insert(
                    0,
                    str(values[index])
                )

    tree.bind(
        "<<TreeviewSelect>>",
        select_employee
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    load_employees()


# ============================================================
# SEARCH EMPLOYEE
# ============================================================

def search_employee_window():

    clear_root()

    root.title("Search Employee")

    header = tk.Frame(
        root,
        bg=NAVY_DARK,
        height=90
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="🔎  SEARCH EMPLOYEE",
        bg=NAVY_DARK,
        fg=WHITE,
        font=("Segoe UI", 21, "bold")
    ).pack(
        side="left",
        padx=25,
        pady=25
    )

    create_button(
        header,
        "← Dashboard",
        show_admin_dashboard,
        GRAY,
        12
    ).pack(
        side="right",
        padx=25,
        pady=25
    )

    main = tk.Frame(
        root,
        bg=LIGHT_BG
    )
    main.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=25
    )

    search_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    search_frame.pack(
        fill="x",
        pady=(0, 15)
    )

    tk.Label(
        search_frame,
        text="Employee ID",
        bg=WHITE,
        fg=DARK_TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(
        side="left",
        padx=(20, 5),
        pady=20
    )

    search_entry = tk.Entry(
        search_frame,
        font=("Segoe UI", 11),
        width=25,
        bg=LIGHT_GRAY,
        relief="solid",
        bd=1
    )
    search_entry.pack(
        side="left",
        padx=5,
        pady=20,
        ipady=5
    )

    result_frame = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    result_frame.pack(
        fill="both",
        expand=True
    )

    columns = [
        "Employee_ID",
        "Name",
        "DOB",
        "DOJ",
        "Gender",
        "Department",
        "Designation",
        "Salary",
        "Contact",
        "Email",
        "Address"
    ]

    # Search result table with vertical and horizontal scrollbars
    table_frame = tk.Frame(
        result_frame,
        bg=WHITE
    )
    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=15
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        yscrollcommand=lambda *args: y_scrollbar.set(*args),
        xscrollcommand=lambda *args: x_scrollbar.set(*args)
    )

    y_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    x_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=tree.xview
    )

    for column in columns:

        tree.heading(
            column,
            text=column.replace("_", " ")
        )

        tree.column(
            column,
            width=150,
            minwidth=100,
            stretch=False
        )

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    y_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    x_scrollbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )

    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    def search():

        employee_id = search_entry.get().strip().upper()

        if not employee_id:

            messagebox.showwarning(
                "Search",
                "Enter Employee ID."
            )
            return

        for item in tree.get_children():
            tree.delete(item)

        connection = get_connection()

        if connection is None:
            return

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    Employee_ID,
                    Name,
                    DOB,
                    DOJ,
                    Gender,
                    Department,
                    Designation,
                    Salary,
                    Contact,
                    Email,
                    Address
                FROM employees
                WHERE Employee_ID = %s
                """,
                (employee_id,)
            )

            row = cursor.fetchone()

            if row:

                tree.insert(
                    "",
                    "end",
                    values=row
                )

            else:

                messagebox.showinfo(
                    "Not Found",
                    f"No employee found with ID {employee_id}."
                )

        except Error as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:

            cursor.close()
            connection.close()

    create_button(
        search_frame,
        "🔎 SEARCH",
        search,
        PURPLE,
        12
    ).pack(
        side="left",
        padx=10,
        pady=20
    )

    create_button(
        search_frame,
        "CLEAR",
        lambda: search_entry.delete(0, tk.END),
        GRAY,
        10
    ).pack(
        side="left",
        padx=5,
        pady=20
    )

    search_entry.focus()


# ============================================================
# DOWNLOAD ALL EMPLOYEES CSV
# ============================================================

def download_all_employees_csv():

    connection = get_connection()

    if connection is None:
        return

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                Employee_ID,
                Name,
                DOB,
                DOJ,
                Gender,
                Department,
                Designation,
                Salary,
                Contact,
                Email,
                Address
            FROM employees
            ORDER BY Employee_ID
            """
        )

        rows = cursor.fetchall()

        if not rows:

            messagebox.showinfo(
                "No Data",
                "No employee records found."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Download Employee Data",
            defaultextension=".csv",
            initialfile="employee_details.csv",
            filetypes=[
                ("CSV files", "*.csv")
            ]
        )

        if not file_path:
            return

        with open(
            file_path,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Employee_ID",
                "Name",
                "DOB",
                "DOJ",
                "Gender",
                "Department",
                "Designation",
                "Salary",
                "Contact",
                "Email",
                "Address"
            ])

            writer.writerows(rows)

        messagebox.showinfo(
            "Success",
            "Employee data downloaded successfully."
        )

    except Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

    finally:

        cursor.close()
        connection.close()


# ============================================================
# EMPLOYEE DASHBOARD
# ============================================================

def show_employee_dashboard(employee_id):

    clear_root()

    root.title(f"Employee Dashboard - {employee_id}")

    # ========================================================
    # HEADER
    # ========================================================
    header = tk.Frame(
        root,
        bg=NAVY_DARK,
        height=90
    )
    header.pack(fill="x")
    header.pack_propagate(False)

    title_frame = tk.Frame(header, bg=NAVY_DARK)
    title_frame.pack(side="left", padx=30, pady=15)

    tk.Label(
        title_frame,
        text="👤  EMPLOYEE DASHBOARD",
        bg=NAVY_DARK,
        fg=WHITE,
        font=("Segoe UI", 21, "bold")
    ).pack(anchor="w")

    tk.Label(
        title_frame,
        text=f"Employee ID: {employee_id}",
        bg=NAVY_DARK,
        fg="#CBD5E1",
        font=("Segoe UI", 10)
    ).pack(anchor="w")

    create_button(
        header,
        "Logout",
        show_login_choice,
        RED,
        10
    ).pack(side="right", padx=25, pady=25)

    # ========================================================
    # MAIN AREA
    # ========================================================
    main = tk.Frame(root, bg=LIGHT_BG)
    main.pack(fill="both", expand=True, padx=35, pady=25)

    # Fetch employee information
    connection = get_connection()
    employee = None

    if connection:
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    Employee_ID,
                    Name,
                    DOB,
                    DOJ,
                    Gender,
                    Department,
                    Designation,
                    Salary,
                    Contact,
                    Email,
                    Address
                FROM employees
                WHERE Employee_ID = %s
                """,
                (employee_id,)
            )
            employee = cursor.fetchone()
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if cursor:
                cursor.close()
            connection.close()

    if employee is None:
        error_card = tk.Frame(
            main,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        error_card.pack(fill="x", pady=30)

        tk.Label(
            error_card,
            text="Employee information not found.",
            bg=WHITE,
            fg=RED,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=35)
        return

    # ========================================================
    # WELCOME CARD
    # ========================================================
    welcome = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    welcome.pack(fill="x", pady=(0, 18))

    left_welcome = tk.Frame(welcome, bg=WHITE)
    left_welcome.pack(side="left", fill="both", expand=True, padx=25, pady=18)

    tk.Label(
        left_welcome,
        text=f"Welcome, {employee[1]} 👋",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 20, "bold")
    ).pack(anchor="w")

    tk.Label(
        left_welcome,
        text="Your employee information is shown below.",
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(3, 0))

    tk.Label(
        welcome,
        text=str(employee[0]),
        bg=LIGHT_BLUE,
        fg=BLUE,
        font=("Segoe UI", 12, "bold"),
        padx=18,
        pady=10
    ).pack(side="right", padx=25, pady=22)

    # ========================================================
    # SUMMARY CARDS
    # ========================================================
    summary = tk.Frame(main, bg=LIGHT_BG)
    summary.pack(fill="x", pady=(0, 18))

    for col in range(3):
        summary.grid_columnconfigure(col, weight=1)

    summary_items = [
        ("Department", employee[5] or "-", BLUE, LIGHT_BLUE),
        ("Designation", employee[6] or "-", PURPLE, LIGHT_PURPLE),
        ("Salary", f"₹{float(employee[7]):,.2f}" if employee[7] is not None else "-", GREEN, LIGHT_GREEN)
    ]

    for col, (label, value, fg, bg) in enumerate(summary_items):
        card = tk.Frame(
            summary,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        card.grid(row=0, column=col, sticky="nsew", padx=6)

        tk.Label(
            card,
            text=label,
            bg=WHITE,
            fg=GRAY,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(14, 2))

        tk.Label(
            card,
            text=str(value),
            bg=bg,
            fg=fg,
            font=("Segoe UI", 13, "bold"),
            padx=12,
            pady=7
        ).pack(anchor="w", padx=18, pady=(0, 14))

    # ========================================================
    # EMPLOYEE DETAILS CARD
    # ========================================================
    details = tk.Frame(
        main,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    details.pack(fill="both", expand=True)

    tk.Label(
        details,
        text="📋  PERSONAL & EMPLOYMENT DETAILS",
        bg=WHITE,
        fg=NAVY,
        font=("Segoe UI", 14, "bold")
    ).grid(row=0, column=0, columnspan=4, sticky="w", padx=25, pady=(20, 15))

    for col in range(4):
        details.grid_columnconfigure(col, weight=1)

    fields = [
        ("Employee ID", employee[0]),
        ("Name", employee[1]),
        ("Date of Birth", employee[2]),
        ("Date of Joining", employee[3]),
        ("Gender", employee[4]),
        ("Department", employee[5]),
        ("Designation", employee[6]),
        ("Contact", employee[8]),
        ("Email", employee[9])
    ]

    for i, (label, value) in enumerate(fields):
        row = 1 + (i // 3) * 2
        col = (i % 3) * 1

        value = "" if value is None else str(value)

        box = tk.Frame(
            details,
            bg=LIGHT_GRAY,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        box.grid(
            row=row,
            column=col,
            rowspan=2,
            sticky="nsew",
            padx=8,
            pady=7
        )

        tk.Label(
            box,
            text=label,
            bg=LIGHT_GRAY,
            fg=GRAY,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=12, pady=(8, 2))

        tk.Label(
            box,
            text=value,
            bg=LIGHT_GRAY,
            fg=DARK_TEXT,
            font=("Segoe UI", 10, "bold"),
            anchor="w",
            justify="left",
            wraplength=250
        ).pack(anchor="w", padx=12, pady=(0, 8), fill="x")

    # Address gets a full-width section at the bottom.
    address_row = 8

    address_box = tk.Frame(
        details,
        bg=LIGHT_GRAY,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    address_box.grid(
        row=address_row,
        column=0,
        columnspan=3,
        sticky="nsew",
        padx=8,
        pady=(7, 20)
    )

    tk.Label(
        address_box,
        text="Address",
        bg=LIGHT_GRAY,
        fg=GRAY,
        font=("Segoe UI", 8, "bold")
    ).pack(anchor="w", padx=12, pady=(8, 2))

    tk.Label(
        address_box,
        text="" if employee[10] is None else str(employee[10]),
        bg=LIGHT_GRAY,
        fg=DARK_TEXT,
        font=("Segoe UI", 10, "bold"),
        anchor="w",
        justify="left",
        wraplength=800
    ).pack(anchor="w", padx=12, pady=(0, 10), fill="x")


# ============================================================
# START APPLICATION
# ============================================================

def start_application():

    create_login_table()

    show_login_choice()


# ============================================================
# RUN
# ============================================================

start_application()

root.mainloop()




