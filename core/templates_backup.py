# core/templates.py
"""قوالب موحدة - تستخدمها جميع الوكلاء في كلا الوضعين"""

import textwrap

class Templates:
    
    @staticmethod
    def config():
        return textwrap.dedent('''
            # config.py
            import os
            from dotenv import load_dotenv

            load_dotenv()

            DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
            APP_NAME = "My Application"
            DEBUG = os.getenv("DEBUG", "False").lower() == "true"
        ''')
    
    @staticmethod
    def database():
        """قالب database.py - SQLite (تخزين دائم)"""
        return textwrap.dedent('''
            # database.py
            import os
            import sqlite3
            from datetime import datetime
            from typing import List, Dict, Any

            DB_PATH = os.getenv("DATABASE_PATH", "app.db")

            def get_db_connection():
                """إنشاء اتصال بقاعدة البيانات"""
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                return conn

            def init_db():
                """تهيئة قاعدة البيانات وإنشاء الجداول"""
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                conn.close()

            # تهيئة قاعدة البيانات عند بدء التطبيق
            init_db()

            def get_all_items() -> List[Dict[str, Any]]:
                """جلب جميع العناصر"""
                conn = get_db_connection()
                items = conn.execute("SELECT * FROM items ORDER BY id DESC").fetchall()
                conn.close()
                return [dict(item) for item in items]

            def get_item_by_id(item_id: int) -> Dict[str, Any]:
                """جلب عنصر محدد بالمعرف"""
                conn = get_db_connection()
                item = conn.execute("SELECT * FROM items WHERE id = ?", (item_id,)).fetchone()
                conn.close()
                return dict(item) if item else None

            def add_item(name: str, description: str = "") -> Dict[str, Any]:
                """إضافة عنصر جديد"""
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO items (name, description) VALUES (?, ?)",
                    (name, description)
                )
                conn.commit()
                item_id = cursor.lastrowid
                conn.close()
                return get_item_by_id(item_id)

            def update_item(item_id: int, **kwargs) -> bool:
                """تحديث عنصر"""
                conn = get_db_connection()
                updates = ", ".join([f"{key} = ?" for key in kwargs.keys()])
                values = list(kwargs.values()) + [item_id]
                
                conn.execute(f"UPDATE items SET {updates} WHERE id = ?", values)
                conn.commit()
                conn.close()
                return True

            def delete_item(item_id: int) -> bool:
                """حذف عنصر"""
                conn = get_db_connection()
                conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
                conn.commit()
                conn.close()
                return True
        ''')
    
    @staticmethod
    def helpers(project_type, item_name):
        # ========== الأنواع الجديدة ==========
        if project_type == "invoice":
            return Templates.helpers_invoice()
        if project_type == "appointment":
            return Templates.helpers_appointment()
        if project_type == "workout":
            return Templates.helpers_workout()
        if project_type == "meal":
            return Templates.helpers_meal()
        if project_type == "blog":
            return Templates.helpers_blog()
        
        # ========== قالب Library Manager ==========
        if project_type == "library":
            return textwrap.dedent('''
                # helpers.py
                # Library Manager - Book Management System
                import sqlite3
                from datetime import datetime

                DB_PATH = "library.db"

                def get_db_connection():
                    conn = sqlite3.connect(DB_PATH)
                    conn.row_factory = sqlite3.Row
                    return conn

                def init_db():
                    conn = get_db_connection()
                    conn.execute("""
                        CREATE TABLE IF NOT EXISTS books (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            author TEXT NOT NULL,
                            isbn TEXT,
                            year INTEGER,
                            publisher TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """)
                    conn.commit()
                    conn.close()

                init_db()

                def get_books():
                    conn = get_db_connection()
                    books = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
                    conn.close()
                    return [dict(book) for book in books]

                def get_book(book_id):
                    conn = get_db_connection()
                    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
                    conn.close()
                    return dict(book) if book else None

                def add_book(title: str, author: str, isbn: str = "", year: int = 0, publisher: str = ""):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO books (title, author, isbn, year, publisher) VALUES (?, ?, ?, ?, ?)",
                        (title, author, isbn, year, publisher)
                    )
                    conn.commit()
                    book_id = cursor.lastrowid
                    conn.close()
                    return get_book(book_id)

                def update_book(book_id: int, **kwargs):
                    conn = get_db_connection()
                    fields = ", ".join([f"{key} = ?" for key in kwargs.keys()])
                    values = list(kwargs.values()) + [book_id]
                    conn.execute(f"UPDATE books SET {fields} WHERE id = ?", values)
                    conn.commit()
                    conn.close()
                    return True

                def delete_book(book_id: int):
                    conn = get_db_connection()
                    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
                    conn.commit()
                    conn.close()
                    return True
            ''')
        
        # ========== القوالب العامة (task, contact, product, expense) ==========
        items_name = f"{item_name}s"
        
        return textwrap.dedent(f'''
            # helpers.py
            from database import get_all_items, get_item_by_id, add_item, update_item, delete_item

            def get_{items_name}():
                """جلب جميع {items_name}"""
                return get_all_items()

            def get_{item_name}({item_name}_id):
                """جلب {item_name} محدد"""
                return get_item_by_id({item_name}_id)

            def add_{item_name}(name: str, description: str = ""):
                """إضافة {item_name} جديد"""
                return add_item(name=name, description=description)

            def update_{item_name}({item_name}_id: int, **kwargs):
                """تحديث {item_name}"""
                return update_item({item_name}_id, **kwargs)

            def delete_{item_name}({item_name}_id):
                """حذف {item_name}"""
                return delete_item({item_name}_id)
        ''')
    
    @staticmethod
    def main(project_type, item_name):
        # ========== الأنواع الجديدة ==========
        if project_type == "invoice":
            return Templates.main_invoice()
        if project_type == "appointment":
            return Templates.main_appointment()
        if project_type == "workout":
            return Templates.main_workout()
        if project_type == "meal":
            return Templates.main_meal()
        if project_type == "blog":
            return Templates.main_blog()
        
        # ========== قالب Library Manager ==========
        if project_type == "library":
            return textwrap.dedent('''
                # main.py
                import streamlit as st
                import sys
                import os

                sys.path.insert(0, os.path.dirname(__file__))

                from helpers import get_books, add_book, delete_book

                st.set_page_config(page_title="📚 Library Manager", layout="wide")
                st.title("📚 Library Manager")

                with st.sidebar:
                    st.header("Add New Book")
                    with st.form("add_form"):
                        title = st.text_input("Book Title")
                        author = st.text_input("Author")
                        isbn = st.text_input("ISBN (optional)")
                        year = st.number_input("Year", min_value=0, max_value=2026, step=1)
                        publisher = st.text_input("Publisher (optional)")
                        submitted = st.form_submit_button("Add Book")
                        
                        if submitted and title and author:
                            add_book(title=title, author=author, isbn=isbn, year=year, publisher=publisher)
                            st.success(f"Added: {title}")
                            st.rerun()

                st.header("Books List")
                books = get_books()

                if not books:
                    st.info("No books yet. Add one from the sidebar!")
                else:
                    for book in books:
                        with st.expander(f"📖 {book['title']} - {book['author']}"):
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**ISBN:** {book.get('isbn', 'N/A')}")
                                st.write(f"**Year:** {book.get('year', 'N/A')}")
                                st.write(f"**Publisher:** {book.get('publisher', 'N/A')}")
                            with col2:
                                if st.button("Delete", key=book['id']):
                                    delete_book(book['id'])
                                    st.rerun()

                st.caption("Powered by AgentForge")
            ''')
        
        # ========== القوالب العامة (task, contact, product) ==========
        items_name = f"{item_name}s"
        titles = {"task": "📝 Task Manager", "contact": "📞 Contact Book", "product": "📦 Inventory"}
        title = titles.get(project_type, f"📱 {item_name.title()} Manager")
        
        return textwrap.dedent(f'''
            # main.py
            import streamlit as st
            import sys
            import os

            sys.path.insert(0, os.path.dirname(__file__))

            from helpers import get_{items_name}, add_{item_name}, delete_{item_name}

            st.set_page_config(page_title="{title}", layout="wide")
            st.title("{title}")

            with st.sidebar:
                st.header("Add New")
                with st.form("add_form"):
                    name = st.text_input("Name")
                    description = st.text_area("Description")
                    if st.form_submit_button("Add"):
                        add_{item_name}(name=name, description=description)
                        st.rerun()

            st.header(f"{items_name.title()} List")
            items = get_{items_name}()

            if not items:
                st.info("No items yet. Add one from the sidebar!")
            else:
                for item in items:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"**{{item.get('name')}}**")
                        if item.get("description"):
                            st.caption(item.get("description"))
                    with col2:
                        if st.button("Delete", key=item.get("id")):
                            delete_{item_name}(item.get("id"))
                            st.rerun()

            st.caption("Powered by AgentForge")
        ''')
    
    @staticmethod
    def start_bat():
        return '@echo off\nstreamlit run main.py\npause'
    
    @staticmethod
    def detect_type(description):
        desc = description.lower()
        
        # ========== الأنواع الجديدة ==========
        if any(w in desc for w in ['invoice', 'billing', 'فاتورة', 'فواتير']):
            return "invoice", "invoice"
        if any(w in desc for w in ['appointment', 'booking', 'موعد', 'حجز']):
            return "appointment", "appointment"
        if any(w in desc for w in ['workout', 'exercise', 'تمرين', 'تمارين']):
            return "workout", "workout"
        if any(w in desc for w in ['meal', 'calorie', 'food', 'وجبة', 'سعرة']):
            return "meal", "meal"
        if any(w in desc for w in ['blog', 'post', 'article', 'مدونة', 'مقال']):
            return "blog", "blog"
        
        # ========== الأنواع الحالية ==========
        if any(w in desc for w in ['book', 'library', 'author', 'isbn', 'كتاب', 'مكتبة']):
            return "library", "book"
        if any(w in desc for w in ['contact', 'address', 'phone', 'جهة', 'عنوان']):
            return "contact", "contact"
        if any(w in desc for w in ['task', 'todo', 'reminder', 'مهمة', 'مهام']):
            return "task", "task"
        if any(w in desc for w in ['product', 'inventory', 'منتج', 'مخزون']):
            return "product", "product"
        
        return "general", "item"
    
    @staticmethod
    def detect_item_name(description, project_type):
        """استخراج اسم العنصر"""
        if project_type == "contact":
            return "contact"
        if project_type == "task":
            return "task"
        if project_type == "product":
            return "product"
        if project_type == "library":
            return "book"
        return "item"
    
    # ========== دوال إضافية للقوالب الجديدة ==========
    
    @staticmethod
    def helpers_library():
        """قالب مكتبة - نسخة منفصلة"""
        return textwrap.dedent('''
            # helpers.py
            import sqlite3

            DB_PATH = "library.db"

            def get_db_connection():
                conn = sqlite3.connect(DB_PATH)
                conn.row_factory = sqlite3.Row
                return conn

            def init_db():
                conn = get_db_connection()
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        isbn TEXT,
                        year INTEGER,
                        publisher TEXT
                    )
                """)
                conn.commit()
                conn.close()

            init_db()

            def get_books():
                conn = get_db_connection()
                books = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
                conn.close()
                return [dict(book) for book in books]

            def add_book(title, author, isbn="", year=0, publisher=""):
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (title, author, isbn, year, publisher) VALUES (?, ?, ?, ?, ?)",
                    (title, author, isbn, year, publisher)
                )
                conn.commit()
                book_id = cursor.lastrowid
                conn.close()
                return {"id": book_id, "title": title, "author": author}

            def delete_book(book_id):
                conn = get_db_connection()
                conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
                conn.commit()
                conn.close()
                return True
        ''')
    
    @staticmethod
    def main_library():
        """قالب واجهة مكتبة - نسخة منفصلة"""
        return textwrap.dedent('''
            # main.py
            import streamlit as st
            import sys
            import os

            sys.path.insert(0, os.path.dirname(__file__))

            from helpers import get_books, add_book, delete_book

            st.set_page_config(page_title="📚 Library Manager", layout="wide")
            st.title("📚 Library Manager")

            with st.sidebar:
                st.header("Add New Book")
                with st.form("add_form"):
                    title = st.text_input("Book Title")
                    author = st.text_input("Author")
                    isbn = st.text_input("ISBN (optional)")
                    year = st.number_input("Year", min_value=0, max_value=2026, step=1)
                    publisher = st.text_input("Publisher (optional)")
                    submitted = st.form_submit_button("Add Book")
                    
                    if submitted and title and author:
                        add_book(title=title, author=author, isbn=isbn, year=year, publisher=publisher)
                        st.success(f"Added: {title}")
                        st.rerun()

            st.header("Books List")
            books = get_books()

            if not books:
                st.info("No books yet. Add one from the sidebar!")
            else:
                for book in books:
                    with st.expander(f"📖 {book['title']} - {book['author']}"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**ISBN:** {book.get('isbn', 'N/A')}")
                            st.write(f"**Year:** {book.get('year', 'N/A')}")
                            st.write(f"**Publisher:** {book.get('publisher', 'N/A')}")
                        with col2:
                            if st.button("Delete", key=book['id']):
                                delete_book(book['id'])
                                st.rerun()

            st.caption("Powered by AgentForge")
        ''')
    @staticmethod
    def helpers_invoice():
        return '''# helpers.py - Invoice System
    import sqlite3
    from datetime import datetime

    DB_PATH = "invoices.db"

    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                amount REAL NOT NULL,
                due_date TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    init_db()

    def get_invoices():
        conn = get_db_connection()
        invoices = conn.execute("SELECT * FROM invoices ORDER BY id DESC").fetchall()
        conn.close()
        return [dict(inv) for inv in invoices]

    def add_invoice(customer_name, amount, due_date=""):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO invoices (customer_name, amount, due_date) VALUES (?, ?, ?)",
            (customer_name, amount, due_date)
        )
        conn.commit()
        inv_id = cursor.lastrowid
        conn.close()
        return {"id": inv_id, "customer_name": customer_name, "amount": amount}

    def update_invoice_status(inv_id, status):
        conn = get_db_connection()
        conn.execute("UPDATE invoices SET status = ? WHERE id = ?", (status, inv_id))
        conn.commit()
        conn.close()
        return True

    def delete_invoice(inv_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM invoices WHERE id = ?", (inv_id,))
        conn.commit()
        conn.close()
        return True
    '''

    @staticmethod
    def main_invoice():
        return '''# main.py - Invoice System
    import streamlit as st
    import sys
    import os

    sys.path.insert(0, os.path.dirname(__file__))

    from helpers import get_invoices, add_invoice, update_invoice_status, delete_invoice

    st.set_page_config(page_title="💰 Invoice System", layout="wide")
    st.title("💰 Invoice System")

    with st.sidebar:
        st.header("Add New Invoice")
        with st.form("add_form"):
            customer_name = st.text_input("Customer Name")
            amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
            due_date = st.date_input("Due Date")
            submitted = st.form_submit_button("Add Invoice")
            if submitted and customer_name and amount > 0:
                add_invoice(customer_name, amount, str(due_date))
                st.success(f"Added: {customer_name}")
                st.rerun()

    st.header("Invoices List")
    invoices = get_invoices()

    if not invoices:
        st.info("No invoices yet. Add one from the sidebar!")
    else:
        for inv in invoices:
            with st.expander(f"🧾 {inv['customer_name']} - ${inv['amount']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Due Date:** {inv.get('due_date', 'N/A')}")
                    st.write(f"**Status:** {inv.get('status', 'pending')}")
                with col2:
                    if st.button("Mark Paid", key=inv['id']):
                        update_invoice_status(inv['id'], 'paid')
                        st.rerun()
                    if st.button("Delete", key=f"del_{inv['id']}"):
                        delete_invoice(inv['id'])
                        st.rerun()

    st.caption("Powered by AgentForge")
    '''
    @staticmethod
    def helpers_appointment():
        return '''# helpers.py - Appointment Booking
    import sqlite3

    DB_PATH = "appointments.db"

    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                service TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                status TEXT DEFAULT 'scheduled'
            )
        """)
        conn.commit()
        conn.close()

    init_db()

    def get_appointments():
        conn = get_db_connection()
        appointments = conn.execute("SELECT * FROM appointments ORDER BY date, time").fetchall()
        conn.close()
        return [dict(app) for app in appointments]

    def add_appointment(customer_name, service, date, time):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (customer_name, service, date, time) VALUES (?, ?, ?, ?)",
            (customer_name, service, date, time)
        )
        conn.commit()
        app_id = cursor.lastrowid
        conn.close()
        return {"id": app_id, "customer_name": customer_name}

    def delete_appointment(app_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM appointments WHERE id = ?", (app_id,))
        conn.commit()
        conn.close()
        return True
    '''

    @staticmethod
    def main_appointment():
        return '''# main.py - Appointment Booking
    import streamlit as st
    import sys
    import os

    sys.path.insert(0, os.path.dirname(__file__))

    from helpers import get_appointments, add_appointment, delete_appointment

    st.set_page_config(page_title="📅 Appointment Booking", layout="wide")
    st.title("📅 Appointment Booking")

    with st.sidebar:
        st.header("Book Appointment")
        with st.form("add_form"):
            customer_name = st.text_input("Customer Name")
            service = st.selectbox("Service", ["Consultation", "Meeting", "Support", "Other"])
            date = st.date_input("Date")
            time = st.time_input("Time")
            submitted = st.form_submit_button("Book")
            if submitted and customer_name:
                add_appointment(customer_name, service, str(date), str(time))
                st.success(f"Booked: {customer_name}")
                st.rerun()

    st.header("Appointments List")
    appointments = get_appointments()

    if not appointments:
        st.info("No appointments yet. Book one from the sidebar!")
    else:
        for app in appointments:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{app['customer_name']}** - {app['service']}")
                st.caption(f"📅 {app['date']} at {app['time']}")
            with col2:
                if st.button("Cancel", key=app['id']):
                    delete_appointment(app['id'])
                    st.rerun()

    st.caption("Powered by AgentForge")
    '''
    @staticmethod
    def helpers_workout():
        return '''# helpers.py - Workout Tracker
    import sqlite3
    from datetime import datetime

    DB_PATH = "workouts.db"

    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                exercise TEXT NOT NULL,
                sets INTEGER,
                reps INTEGER,
                weight REAL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    init_db()

    def get_workouts():
        conn = get_db_connection()
        workouts = conn.execute("SELECT * FROM workouts ORDER BY date DESC").fetchall()
        conn.close()
        return [dict(w) for w in workouts]

    def add_workout(exercise, sets, reps, weight):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workouts (exercise, sets, reps, weight) VALUES (?, ?, ?, ?)",
            (exercise, sets, reps, weight)
        )
        conn.commit()
        workout_id = cursor.lastrowid
        conn.close()
        return {"id": workout_id, "exercise": exercise}

    def delete_workout(workout_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM workouts WHERE id = ?", (workout_id,))
        conn.commit()
        conn.close()
        return True
    '''

    @staticmethod
    def main_workout():
        return '''# main.py - Workout Tracker
    import streamlit as st
    import sys
    import os

    sys.path.insert(0, os.path.dirname(__file__))

    from helpers import get_workouts, add_workout, delete_workout

    st.set_page_config(page_title="🏋️ Workout Tracker", layout="wide")
    st.title("🏋️ Workout Tracker")

    with st.sidebar:
        st.header("Log Workout")
        with st.form("add_form"):
            exercise = st.text_input("Exercise")
            col1, col2 = st.columns(2)
            with col1:
                sets = st.number_input("Sets", min_value=1, step=1)
            with col2:
                reps = st.number_input("Reps", min_value=1, step=1)
            weight = st.number_input("Weight (kg)", min_value=0.0, step=0.5)
            submitted = st.form_submit_button("Log Workout")
            if submitted and exercise:
                add_workout(exercise, sets, reps, weight)
                st.success(f"Logged: {exercise}")
                st.rerun()

    st.header("Workout History")
    workouts = get_workouts()

    if not workouts:
        st.info("No workouts logged yet. Start from the sidebar!")
    else:
        for w in workouts:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{w['exercise']}** - {w['sets']} sets x {w['reps']} reps")
                if w['weight'] > 0:
                    st.caption(f"🏋️ Weight: {w['weight']} kg")
            with col2:
                if st.button("Delete", key=w['id']):
                    delete_workout(w['id'])
                    st.rerun()

    st.caption("Powered by AgentForge")
    '''
    @staticmethod
    def helpers_meal():
        return '''# helpers.py - Meal Tracker
    import sqlite3
    from datetime import datetime

    DB_PATH = "meals.db"

    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meal_name TEXT NOT NULL,
                calories INTEGER,
                meal_type TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    init_db()

    def get_meals():
        conn = get_db_connection()
        meals = conn.execute("SELECT * FROM meals ORDER BY date DESC").fetchall()
        conn.close()
        return [dict(m) for m in meals]

    def add_meal(meal_name, calories, meal_type):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO meals (meal_name, calories, meal_type) VALUES (?, ?, ?)",
            (meal_name, calories, meal_type)
        )
        conn.commit()
        meal_id = cursor.lastrowid
        conn.close()
        return {"id": meal_id, "meal_name": meal_name}

    def delete_meal(meal_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM meals WHERE id = ?", (meal_id,))
        conn.commit()
        conn.close()
        return True
    '''

    @staticmethod
    def main_meal():
        return '''# main.py - Meal Tracker
    import streamlit as st
    import sys
    import os

    sys.path.insert(0, os.path.dirname(__file__))

    from helpers import get_meals, add_meal, delete_meal

    st.set_page_config(page_title="🍽️ Meal Tracker", layout="wide")
    st.title("🍽️ Meal Tracker")

    with st.sidebar:
        st.header("Log Meal")
        with st.form("add_form"):
            meal_name = st.text_input("Meal/Food")
            calories = st.number_input("Calories", min_value=0, step=10)
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
            submitted = st.form_submit_button("Log Meal")
            if submitted and meal_name and calories > 0:
                add_meal(meal_name, calories, meal_type)
                st.success(f"Logged: {meal_name}")
                st.rerun()

    st.header("Today's Meals")
    meals = get_meals()

    if not meals:
        st.info("No meals logged yet. Start from the sidebar!")
    else:
        total_calories = 0
        for m in meals:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{m['meal_name']}** - {m['calories']} cal")
                st.caption(f"🍽️ {m['meal_type']}")
            with col2:
                if st.button("Delete", key=m['id']):
                    delete_meal(m['id'])
                    st.rerun()
            total_calories += m['calories']
        
        st.metric("Total Calories Today", f"{total_calories} cal")

    st.caption("Powered by AgentForge")
    '''
    @staticmethod
    def helpers_blog():
        return '''# helpers.py - Blog Platform
    import sqlite3
    from datetime import datetime

    DB_PATH = "blog.db"

    def get_db_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db():
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    init_db()

    def get_posts():
        conn = get_db_connection()
        posts = conn.execute("SELECT * FROM posts ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(p) for p in posts]

    def add_post(title, content, category=""):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (title, content, category) VALUES (?, ?, ?)",
            (title, content, category)
        )
        conn.commit()
        post_id = cursor.lastrowid
        conn.close()
        return {"id": post_id, "title": title}

    def delete_post(post_id):
        conn = get_db_connection()
        conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()
        return True
    '''

    @staticmethod
    def main_blog():
        return '''# main.py - Blog Platform
    import streamlit as st
    import sys
    import os

    sys.path.insert(0, os.path.dirname(__file__))

    from helpers import get_posts, add_post, delete_post

    st.set_page_config(page_title="📝 Blog Platform", layout="wide")
    st.title("📝 Blog Platform")

    with st.sidebar:
        st.header("Write New Post")
        with st.form("add_form"):
            title = st.text_input("Title")
            content = st.text_area("Content", height=200)
            category = st.selectbox("Category", ["General", "Tech", "Lifestyle", "Health", "Other"])
            submitted = st.form_submit_button("Publish")
            if submitted and title and content:
                add_post(title, content, category)
                st.success(f"Published: {title}")
                st.rerun()

    st.header("Recent Posts")
    posts = get_posts()

    if not posts:
        st.info("No posts yet. Write your first post from the sidebar!")
    else:
        for post in posts:
            with st.expander(f"📄 {post['title']}"):
                st.write(post['content'])
                st.caption(f"📂 Category: {post.get('category', 'General')} | 🕒 {post.get('created_at', '')[:10]}")
                if st.button("Delete", key=post['id']):
                    delete_post(post['id'])
                    st.rerun()

    st.caption("Powered by AgentForge")
    '''