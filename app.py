# from flask import Flask, render_template, request, redirect, session
# from flask_mail import Mail, Message
# import sqlite3
# import os

# conn = sqlite3.connect("food_rescue.db")
# cur = conn.cursor()

# cur.execute("""
#     UPDATE donations
#     SET created_at = datetime('now', 'localtime')
#     WHERE created_at IS NULL
# """)

# conn.commit()
# conn.close()

# print("Date and time updated successfully!")

# app = Flask(__name__)
# app.secret_key = "foodrescue123"

# # ==========================
# # EMAIL CONFIGURATION
# # ==========================

# app.config["MAIL_SERVER"] = "smtp.gmail.com"
# app.config["MAIL_PORT"] = 587
# app.config["MAIL_USE_TLS"] = True

# app.config["MAIL_USERNAME"] = "smartfoodrescue03@gmail.com"
# app.config["MAIL_PASSWORD"] = "tnkn hfiu ikbh pluc"

# app.config["MAIL_DEFAULT_SENDER"] = "smartfoodrescue03@gmail.com"

# mail = Mail(app)


# # --------------------------
# # Database Connection
# # --------------------------
# def get_db():
#     conn = sqlite3.connect(
#         "food_rescue.db",
#         timeout=10
#     )
#     conn.row_factory = sqlite3.Row
#     return conn

# # ==========================
# # SEND EMAIL TO ALL NGOs
# # ==========================

# # ==========================
# # SEND EMAIL TO ALL NGOs
# # ==========================
# def send_email_to_ngos(food_name, quantity, location, donor):

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute(
#         "SELECT email FROM users WHERE role='NGO'"
#     )

#     ngos = cur.fetchall()

#     conn.close()

#     for ngo in ngos:

#         try:

#             msg = Message(
#                 subject="🍽 New Food Donation Available",
#                 recipients=[ngo["email"]]
#             )

#             msg.body = f"""
# Hello NGO,

# A new food donation has been added.

# Food Name : {food_name}

# Quantity : {quantity}

# Location : {location}

# Donor : {donor}

# Please login to Smart Food Rescue Network
# to accept this donation.

# Thank You.
# """

#             mail.send(msg)

#         except Exception as e:
#             print("Email Error:", e)

        

# # --------------------------
# # Home
# # --------------------------
# @app.route("/")
# def home():

#     conn = get_db()
#     cur = conn.cursor()

#     # Total Donors
#     cur.execute("SELECT COUNT(*) FROM users WHERE role='Donor'")
#     total_donors = cur.fetchone()[0]

#     # Total NGOs
#     cur.execute("SELECT COUNT(*) FROM users WHERE role='NGO'")
#     total_ngos = cur.fetchone()[0]

#     # Total Volunteers
#     cur.execute("SELECT COUNT(*) FROM users WHERE role='Volunteer'")
#     total_volunteers = cur.fetchone()[0]

#     # Delivered Donations
#     cur.execute("SELECT COUNT(*) FROM donations WHERE status='Delivered'")
#     total_delivered = cur.fetchone()[0]

#     conn.close()

#     return render_template(
#         "index.html",
#         total_donors=total_donors,
#         total_ngos=total_ngos,
#         total_volunteers=total_volunteers,
#         total_delivered=total_delivered
#     )

# # --------------------------
# # Register
# # --------------------------
# @app.route("/register", methods=["GET", "POST"])
# def register():

#     if request.method == "POST":

#         name = request.form["name"]
#         email = request.form["email"]
#         password = request.form["password"]
#         role = request.form["role"]

        

#         conn = get_db()
#         cur = conn.cursor()

#         cur.execute(
#             "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
#             (name, email, password, role)
#         )

#         conn.commit()
#         conn.close()

#         return redirect("/login")

#     return render_template("register.html")


# # --------------------------
# # Login
# # --------------------------
# @app.route("/login", methods=["GET", "POST"])
# def login():

#     if request.method == "POST":

#         email = request.form["email"]
#         password = request.form["password"]

#         conn = get_db()
#         cur = conn.cursor()

#         cur.execute(
#             "SELECT * FROM users WHERE email=? AND password=?",
#             (email, password)
#         )

#         user = cur.fetchone()

#         conn.close()

#         if user:

#             session["user"] = user["name"]
#             session["role"] = user["role"]

#             if user["role"] == "Donor":
#                 return redirect("/donor")

#             elif user["role"] == "NGO":
#                 return redirect("/ngo")

#             elif user["role"] == "Volunteer":
#                 return redirect("/volunteer")

#             elif user["role"] == "Admin":
#                 return redirect("/admin")

#         return "Invalid Email or Password"

#     return render_template("login.html")
# # --------------------------
# # Donor Dashboard
# # --------------------------
# @app.route("/donor")
# def donor():

#     # Security
#     if "user" not in session or session.get("role") != "Donor":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("SELECT * FROM donations ORDER BY id DESC")

#     donations = cur.fetchall()

#     conn.close()

#     return render_template(
#         "donor_dashboard.html",
#         donations=donations
#     )


# # --------------------------
# # Donate Food
# # --------------------------
# @app.route("/donate", methods=["GET", "POST"])
# def donate():

#     if "user" not in session:
#         return redirect("/login")

#     if request.method == "POST":

#         food_name = request.form["food_name"]
#         quantity = request.form["quantity"]
#         location = request.form["location"]

#         donor = session["user"]

#         conn = get_db()
#         cur = conn.cursor()

#         cur.execute("""
#     INSERT INTO donations
#     (food_name, quantity, location, donor, status, created_at)
#     VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'))
# """, (food_name, quantity, location, donor, "Pending"))

#         conn.commit()

#         # Send email to all NGOs
#         send_email_to_ngos(
#             food_name,
#             quantity,
#             location,
#             donor
#         )

#         conn.close()

#         return redirect("/donor")

#     return render_template("donate_food.html")

# # --------------------------
# # NGO Dashboard
# # --------------------------
# @app.route("/ngo", methods=["GET", "POST"])
# def ngo():

#     # Security
#     if "user" not in session or session.get("role") != "NGO":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     if request.method == "POST":

#         location = request.form["location"]

#         cur.execute(
#             "SELECT * FROM donations WHERE location LIKE ?",
#             ('%' + location + '%',)
#         )

#     else:

#         cur.execute("SELECT * FROM donations ORDER BY id DESC")

#     donations = cur.fetchall()

#     conn.close()

#     return render_template(
#         "ngo_dashboard.html",
#         donations=donations
#     )


# def send_accept_email(id):

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT 
#             d.food_name,
#             d.quantity,
#             d.location,
#             d.donor,
#             u.email
#         FROM donations d
#         JOIN users u ON d.donor = u.name
#         WHERE d.id=?
#     """, (id,))

#     data = cur.fetchone()
#     conn.close()

#     if not data:
#         print("Donation or donor email not found.")
#         return

#     food_name, quantity, location, donor, email = data

#     msg = Message(
#         "🎉 Your Food Donation Has Been Accepted!",
#         sender=app.config["MAIL_USERNAME"],
#         recipients=[email]
#     )

#     msg.body = f"""
# Hello {donor},

# Great news! 🎉

# Your food donation has been accepted by an NGO.

# Donation Details
# --------------------------
# Food: {food_name}
# Quantity: {quantity}
# Location: {location}

# Thank you for helping reduce food waste and feed people in need.

# ❤️ Smart Food Rescue Network
# """

#     mail.send(msg)

#     print("Acceptance email sent successfully to:", email)
# # --------------------------
# # Accept Donation
# # --------------------------
# @app.route("/accept/<int:id>")
# def accept(id):

#     if "user" not in session or session.get("role") != "NGO":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute(
#         "UPDATE donations SET status=? WHERE id=?",
#         ("Accepted", id)
#     )

#     conn.commit()

#     # Send email to donor
#     send_accept_email(id)

#     # Send email to volunteers
#     send_email_to_volunteers(id)

#     conn.close()

#     return redirect("/ngo")
# # --------------------------
# # Volunteer Dashboard
# # --------------------------
# @app.route("/volunteer")
# def volunteer():

#     # Security
#     if "user" not in session or session.get("role") != "Volunteer":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute(
#         "SELECT * FROM donations WHERE status='Accepted' ORDER BY id DESC"
#     )

#     donations = cur.fetchall()

#     conn.close()

#     return render_template(
#         "volunteer_dashboard.html",
#         donations=donations
#     )


# # --------------------------
# # Deliver Food
# # --------------------------
# @app.route("/deliver/<int:id>")
# def deliver(id):

#     if "user" not in session or session.get("role") != "Volunteer":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#    cur.execute(
#     "UPDATE donations SET status=? WHERE id=?",
#     ("Delivered", id)
# )

# conn.commit()

# send_delivery_email(id)

# conn.close()

#     return redirect("/volunteer")


# # --------------------------
# # Admin Dashboard
# # --------------------------
# # --------------------------
# # Admin Dashboard
# # --------------------------
# # --------------------------
# # Admin Dashboard
# # --------------------------
# @app.route("/admin")
# def admin():

#     if "user" not in session or session.get("role") != "Admin":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     # ---------------- Dashboard Counts ---------------- #

#     cur.execute("SELECT COUNT(*) FROM users")
#     total_users = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM users WHERE role='Donor'")
#     total_donors = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM users WHERE role='NGO'")
#     total_ngos = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM users WHERE role='Volunteer'")
#     total_volunteers = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM donations")
#     total_donations = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM donations WHERE status='Pending'")
#     pending = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM donations WHERE status='Accepted'")
#     accepted = cur.fetchone()[0]

#     cur.execute("SELECT COUNT(*) FROM donations WHERE status='Delivered'")
#     delivered = cur.fetchone()[0]

#     # ---------------- Recent Donations ---------------- #

#     cur.execute("""
#         SELECT
#             id,
#             food_name,
#             quantity,
#             location,
#             donor,
#             status,
#             created_at
#         FROM donations
#         ORDER BY id DESC
#     """)

#     donations = cur.fetchall()

#     conn.close()

#     return render_template(
#         "admin_dashboard.html",

#         total_users=total_users,
#         total_donors=total_donors,
#         total_ngos=total_ngos,
#         total_volunteers=total_volunteers,

#         total_donations=total_donations,
#         pending=pending,
#         accepted=accepted,
#         delivered=delivered,

#         donations=donations
#     )

# @app.route("/admin/donors")
# def admin_donors():

#     if "user" not in session or session.get("role") != "Admin":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT id, name, email
#         FROM users
#         WHERE role='Donor'
#         ORDER BY id DESC
#     """)

#     donors = cur.fetchall()

#     conn.close()

#     return render_template("donors.html", donors=donors)

# @app.route("/admin/ngos")
# def admin_ngos():

#     if "user" not in session or session.get("role") != "Admin":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT id, name, email
#         FROM users
#         WHERE role='NGO'
#         ORDER BY id DESC
#     """)

#     ngos = cur.fetchall()

#     conn.close()

#     return render_template("ngos.html", ngos=ngos)

# @app.route("/admin/volunteers")
# def admin_volunteers():

#     if "user" not in session or session.get("role") != "Admin":
#         return redirect("/login")

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT id, name, email
#         FROM users
#         WHERE role='Volunteer'
#         ORDER BY id DESC
#     """)

#     volunteers = cur.fetchall()

#     conn.close()

#     return render_template("volunteers.html", volunteers=volunteers)



# def send_email_to_volunteers(id):

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT 
#             d.food_name,
#             d.quantity,
#             d.location,
#             d.donor
#         FROM donations d
#         WHERE d.id=?
#     """, (id,))

#     donation = cur.fetchone()

#     cur.execute("""
#         SELECT email FROM users 
#         WHERE role='Volunteer'
#     """)

#     volunteers = cur.fetchall()

#     conn.close()

#     if not donation:
#         return


#     for volunteer in volunteers:

#         try:

#             msg = Message(
#                 subject="🚚 New Food Delivery Task",
#                 recipients=[volunteer["email"]]
#             )

#             msg.body = f"""
# Hello Volunteer,

# A food donation has been accepted.

# Donation Details:

# Food : {donation["food_name"]}
# Quantity : {donation["quantity"]}
# Location : {donation["location"]}
# Donor : {donation["donor"]}

# Please login and deliver this food.

# Thank You,
# Smart Food Rescue Network
# """

#             mail.send(msg)

#         except Exception as e:
#             print("Volunteer Email Error:", e)



#             def send_delivery_email(id):

#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#         SELECT 
#             d.food_name,
#             d.quantity,
#             d.location
#         FROM donations d
#         WHERE d.id=?
#     """,(id,))

#     donation = cur.fetchone()

#     cur.execute("""
#         SELECT email FROM users
#         WHERE role='NGO'
#     """)

#     ngos = cur.fetchall()

#     conn.close()

#     if not donation:
#         return

#     for ngo in ngos:

#         try:

#             msg = Message(
#                 subject="✅ Food Donation Delivered",
#                 recipients=[ngo["email"]]
#             )

#             msg.body = f"""
# Hello NGO,

# The food donation has been successfully delivered.

# Food:
# {donation["food_name"]}

# Quantity:
# {donation["quantity"]}

# Location:
# {donation["location"]}

# Thank you.

# Smart Food Rescue Network
# """

#             mail.send(msg)

#         except Exception as e:
#             print("Delivery Email Error:", e)


# # --------------------------
# # About
# # --------------------------
# @app.route("/about")
# def about():
#     return render_template("about.html")


# # --------------------------
# # Contact
# # --------------------------
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")


# # --------------------------
# # FAQ
# # --------------------------
# @app.route("/faq")
# def faq():
#     return render_template("faq.html")


# # --------------------------
# # Request Food
# # --------------------------
# @app.route("/request")
# def request_food():
#     return render_template("request_food.html")


# # --------------------------
# # Logout
# # --------------------------
# @app.route("/logout")
# def logout():

#     session.clear()

#     return redirect("/")


# # --------------------------
# # Run Application
# # --------------------------
# if __name__ == "__main__":
#     app.run(debug=True)



from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
import sqlite3
import os


# ==========================
# UPDATE OLD DATE RECORDS
# ==========================

conn = sqlite3.connect("food_rescue.db")
cur = conn.cursor()

cur.execute("""
UPDATE donations
SET created_at = datetime('now','localtime')
WHERE created_at IS NULL
""")

conn.commit()
conn.close()

print("Date and time updated successfully!")


# ==========================
# FLASK CONFIGURATION
# ==========================

app = Flask(__name__)

app.secret_key = "foodrescue123"


# ==========================
# EMAIL CONFIGURATION
# ==========================

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True

# For local testing
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

app.config["MAIL_DEFAULT_SENDER"] = "smartfoodrescue03@gmail.com"


mail = Mail(app)



# ==========================
# DATABASE CONNECTION
# ==========================

def get_db():

    conn = sqlite3.connect(
        "food_rescue.db",
        timeout=10
    )

    conn.row_factory = sqlite3.Row

    return conn

# ==========================
# SEND EMAIL TO ALL NGOs
# ==========================

def send_email_to_ngos(food_name, quantity, location, donor):

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT email FROM users WHERE role='NGO'"
    )

    ngos = cur.fetchall()

    conn.close()


    for ngo in ngos:

        try:

            msg = Message(
                subject="🍽 New Food Donation Available",
                recipients=[ngo["email"]]
            )


            msg.body = f"""
Hello NGO,

A new food donation has been added.

Food Name : {food_name}
Quantity : {quantity}
Location : {location}
Donor : {donor}

Please login to Smart Food Rescue Network
and accept this donation.

Thank You.
"""


            mail.send(msg)

            print("NGO email sent:", ngo["email"])


        except Exception as e:

            print("NGO Email Error:", e)



# ==========================
# SEND EMAIL TO DONOR
# ==========================

def send_accept_email(id):

    conn = get_db()
    cur = conn.cursor()


    cur.execute("""
        SELECT
            d.food_name,
            d.quantity,
            d.location,
            d.donor,
            u.email

        FROM donations d

        JOIN users u
        ON d.donor = u.name

        WHERE d.id=?
    """, (id,))


    data = cur.fetchone()

    conn.close()


    if not data:

        print("Donor email not found")

        return



    food_name, quantity, location, donor, email = data



    msg = Message(
        subject="🎉 Your Food Donation Has Been Accepted",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email]
    )


    msg.body = f"""
Hello {donor},

Great news! 🎉

Your food donation has been accepted by an NGO.

Donation Details:

Food : {food_name}
Quantity : {quantity}
Location : {location}


Thank you for reducing food waste.

❤️ Smart Food Rescue Network
"""


    mail.send(msg)


    print("Donor email sent:", email)





# ==========================
# SEND EMAIL TO VOLUNTEERS
# ==========================

def send_email_to_volunteers(id):

    conn = get_db()
    cur = conn.cursor()


    cur.execute("""
        SELECT
            food_name,
            quantity,
            location,
            donor

        FROM donations

        WHERE id=?
    """,(id,))


    donation = cur.fetchone()



    cur.execute("""
        SELECT email
        FROM users
        WHERE role='Volunteer'
    """)


    volunteers = cur.fetchall()


    conn.close()



    if not donation:

        return



    for volunteer in volunteers:


        try:


            msg = Message(
                subject="🚚 New Food Delivery Task",
                recipients=[volunteer["email"]]
            )


            msg.body = f"""
Hello Volunteer,

A donation has been accepted.

Food:
{donation["food_name"]}

Quantity:
{donation["quantity"]}

Location:
{donation["location"]}

Donor:
{donation["donor"]}


Please login and deliver this food.

Thank You,
Smart Food Rescue Network
"""


            mail.send(msg)


            print("Volunteer email sent:", volunteer["email"])



        except Exception as e:

            print("Volunteer Email Error:", e)






# ==========================
# SEND DELIVERY EMAIL TO NGO
# ==========================

def send_delivery_email(id):

    conn = get_db()
    cur = conn.cursor()



    cur.execute("""
        SELECT
            food_name,
            quantity,
            location

        FROM donations

        WHERE id=?

    """,(id,))


    donation = cur.fetchone()



    cur.execute("""
        SELECT email
        FROM users
        WHERE role='NGO'

    """)


    ngos = cur.fetchall()


    conn.close()



    if not donation:

        return



    for ngo in ngos:


        try:


            msg = Message(
                subject="✅ Food Donation Delivered",
                recipients=[ngo["email"]]
            )


            msg.body = f"""
Hello NGO,

The food donation has been successfully delivered.

Food:
{donation["food_name"]}

Quantity:
{donation["quantity"]}

Location:
{donation["location"]}


Thank you for helping the community.

Smart Food Rescue Network
"""


            mail.send(msg)


            print("Delivery email sent:", ngo["email"])



        except Exception as e:

            print("Delivery Email Error:", e)


            # ==========================
# HOME PAGE
# ==========================

@app.route("/")
def home():

    conn = get_db()
    cur = conn.cursor()


    cur.execute(
        "SELECT COUNT(*) FROM users WHERE role='Donor'"
    )
    total_donors = cur.fetchone()[0]


    cur.execute(
        "SELECT COUNT(*) FROM users WHERE role='NGO'"
    )
    total_ngos = cur.fetchone()[0]


    cur.execute(
        "SELECT COUNT(*) FROM users WHERE role='Volunteer'"
    )
    total_volunteers = cur.fetchone()[0]


    cur.execute(
        "SELECT COUNT(*) FROM donations WHERE status='Delivered'"
    )
    total_delivered = cur.fetchone()[0]


    conn.close()


    return render_template(
        "index.html",
        total_donors=total_donors,
        total_ngos=total_ngos,
        total_volunteers=total_volunteers,
        total_delivered=total_delivered
    )



# ==========================
# REGISTER
# ==========================

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":


        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]


        conn = get_db()
        cur = conn.cursor()


        cur.execute(
            """
            INSERT INTO users
            (name,email,password,role)
            VALUES(?,?,?,?)
            """,
            (name,email,password,role)
        )


        conn.commit()
        conn.close()


        return redirect("/login")



    return render_template("register.html")





# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":


        email = request.form["email"]
        password = request.form["password"]


        conn = get_db()
        cur = conn.cursor()



        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email=? AND password=?
            """,
            (email,password)
        )


        user = cur.fetchone()


        conn.close()



        if user:


            session["user"] = user["name"]
            session["role"] = user["role"]



            if user["role"] == "Donor":

                return redirect("/donor")


            elif user["role"] == "NGO":

                return redirect("/ngo")


            elif user["role"] == "Volunteer":

                return redirect("/volunteer")


            elif user["role"] == "Admin":

                return redirect("/admin")



        return "Invalid Email or Password"



    return render_template("login.html")






# ==========================
# DONOR DASHBOARD
# ==========================

@app.route("/donor")
def donor():


    if "user" not in session or session.get("role")!="Donor":

        return redirect("/login")



    conn = get_db()
    cur = conn.cursor()



    cur.execute(
        """
        SELECT *
        FROM donations
        ORDER BY id DESC
        """
    )


    donations = cur.fetchall()


    conn.close()



    return render_template(
        "donor_dashboard.html",
        donations=donations
    )






# ==========================
# DONATE FOOD
# ==========================

@app.route("/donate", methods=["GET","POST"])
def donate():


    if "user" not in session:

        return redirect("/login")



    if request.method == "POST":


        food_name = request.form["food_name"]

        quantity = request.form["quantity"]

        location = request.form["location"]

        donor = session["user"]



        conn = get_db()
        cur = conn.cursor()



        cur.execute(
            """
            INSERT INTO donations
            (
            food_name,
            quantity,
            location,
            donor,
            status,
            created_at
            )

            VALUES
            (?,?,?,?,?,datetime('now','localtime'))

            """,
            (
            food_name,
            quantity,
            location,
            donor,
            "Pending"
            )
        )



        conn.commit()



        send_email_to_ngos(
            food_name,
            quantity,
            location,
            donor
        )



        conn.close()



        return redirect("/donor")



    return render_template("donate_food.html")







# ==========================
# NGO DASHBOARD
# ==========================

@app.route("/ngo", methods=["GET","POST"])
def ngo():


    if "user" not in session or session.get("role")!="NGO":

        return redirect("/login")



    conn = get_db()
    cur = conn.cursor()



    if request.method == "POST":


        location = request.form["location"]


        cur.execute(
            """
            SELECT *
            FROM donations
            WHERE location LIKE ?
            """,
            ('%'+location+'%',)
        )



    else:


        cur.execute(
            """
            SELECT *
            FROM donations
            ORDER BY id DESC
            """
        )



    donations = cur.fetchall()


    conn.close()



    return render_template(
        "ngo_dashboard.html",
        donations=donations
    )







# ==========================
# ACCEPT DONATION
# ==========================

@app.route("/accept/<int:id>")
def accept(id):


    if "user" not in session or session.get("role")!="NGO":

        return redirect("/login")



    conn = get_db()
    cur = conn.cursor()



    cur.execute(
        """
        UPDATE donations
        SET status=?
        WHERE id=?
        """,
        ("Accepted",id)
    )



    conn.commit()



    # Email donor

    send_accept_email(id)



    # Email volunteers

    send_email_to_volunteers(id)



    conn.close()



    return redirect("/ngo")

# ==========================
# VOLUNTEER DASHBOARD
# ==========================

@app.route("/volunteer")
def volunteer():


    if "user" not in session or session.get("role")!="Volunteer":

        return redirect("/login")



    conn = get_db()
    cur = conn.cursor()



    cur.execute(
        """
        SELECT *
        FROM donations
        WHERE status='Accepted'
        ORDER BY id DESC
        """
    )


    donations = cur.fetchall()


    conn.close()



    return render_template(
        "volunteer_dashboard.html",
        donations=donations
    )





# ==========================
# DELIVER FOOD
# ==========================

@app.route("/deliver/<int:id>")
def deliver(id):


    if "user" not in session or session.get("role")!="Volunteer":

        return redirect("/login")



    conn = get_db()
    cur = conn.cursor()



    cur.execute(
        """
        UPDATE donations
        SET status=?
        WHERE id=?
        """,
        ("Delivered",id)
    )



    conn.commit()



    # Email NGO after delivery

    send_delivery_email(id)



    conn.close()



    return redirect("/volunteer")






# ==========================
# ADMIN DASHBOARD
# ==========================

@app.route("/admin")
def admin():


    if "user" not in session or session.get("role")!="Admin":

        return redirect("/login")



    conn = get_db()
    cur = conn.cursor()



    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]


    cur.execute(
        "SELECT COUNT(*) FROM users WHERE role='Donor'"
    )
    total_donors = cur.fetchone()[0]


    cur.execute(
        "SELECT COUNT(*) FROM users WHERE role='NGO'"
    )
    total_ngos = cur.fetchone()[0]


    cur.execute(
        "SELECT COUNT(*) FROM users WHERE role='Volunteer'"
    )
    total_volunteers = cur.fetchone()[0]



    cur.execute(
        "SELECT COUNT(*) FROM donations"
    )
    total_donations = cur.fetchone()[0]



    cur.execute(
        "SELECT COUNT(*) FROM donations WHERE status='Pending'"
    )
    pending = cur.fetchone()[0]



    cur.execute(
        "SELECT COUNT(*) FROM donations WHERE status='Accepted'"
    )
    accepted = cur.fetchone()[0]



    cur.execute(
        "SELECT COUNT(*) FROM donations WHERE status='Delivered'"
    )
    delivered = cur.fetchone()[0]



    cur.execute(
        """
        SELECT *
        FROM donations
        ORDER BY id DESC
        """
    )


    donations = cur.fetchall()


    conn.close()



    return render_template(
        "admin_dashboard.html",

        total_users=total_users,

        total_donors=total_donors,

        total_ngos=total_ngos,

        total_volunteers=total_volunteers,

        total_donations=total_donations,

        pending=pending,

        accepted=accepted,

        delivered=delivered,

        donations=donations
    )






# ==========================
# ADMIN DONORS
# ==========================

@app.route("/admin/donors")
def admin_donors():


    if "user" not in session or session.get("role")!="Admin":

        return redirect("/login")



    conn=get_db()
    cur=conn.cursor()



    cur.execute(
        """
        SELECT id,name,email
        FROM users
        WHERE role='Donor'
        """
    )


    donors=cur.fetchall()


    conn.close()


    return render_template(
        "donors.html",
        donors=donors
    )





# ==========================
# ADMIN NGOs
# ==========================

@app.route("/admin/ngos")
def admin_ngos():


    if "user" not in session or session.get("role")!="Admin":

        return redirect("/login")



    conn=get_db()
    cur=conn.cursor()



    cur.execute(
        """
        SELECT id,name,email
        FROM users
        WHERE role='NGO'
        """
    )


    ngos=cur.fetchall()


    conn.close()


    return render_template(
        "ngos.html",
        ngos=ngos
    )





# ==========================
# ADMIN VOLUNTEERS
# ==========================

@app.route("/admin/volunteers")
def admin_volunteers():


    if "user" not in session or session.get("role")!="Admin":

        return redirect("/login")



    conn=get_db()
    cur=conn.cursor()



    cur.execute(
        """
        SELECT id,name,email
        FROM users
        WHERE role='Volunteer'
        """
    )


    volunteers=cur.fetchall()


    conn.close()


    return render_template(
        "volunteers.html",
        volunteers=volunteers
    )





# ==========================
# ABOUT
# ==========================

@app.route("/about")
def about():

    return render_template("about.html")





# ==========================
# CONTACT
# ==========================

@app.route("/contact")
def contact():

    return render_template("contact.html")





# ==========================
# FAQ
# ==========================

@app.route("/faq")
def faq():

    return render_template("faq.html")





# ==========================
# REQUEST FOOD
# ==========================

@app.route("/request")
def request_food():

    return render_template("request_food.html")






# ==========================
# LOGOUT
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")





# ==========================
# RUN APPLICATION
# ==========================

if __name__ == "__main__":

    app.run(debug=True)