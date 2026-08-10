from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
import sqlite3
import os

# =========================================================
# FLASK CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "foodrescue123"

# =========================================================
# GMAIL EMAIL CONFIGURATION
# =========================================================

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

# Gmail account used to SEND emails
app.config["MAIL_USERNAME"] = os.environ.get(
    "MAIL_USERNAME",
    "smartfoodrescue03@gmail.com"
)

# Gmail APP PASSWORD - NOT your normal Gmail password
app.config["MAIL_PASSWORD"] = os.environ.get(
    "MAIL_PASSWORD"
)

app.config["MAIL_DEFAULT_SENDER"] = (
    "Smart Food Rescue",
    app.config["MAIL_USERNAME"]
)

mail = Mail(app)

print("====================================")
print("Smart Food Rescue Email System")
print("====================================")
print("Sender email:", app.config["MAIL_USERNAME"])

if app.config["MAIL_PASSWORD"]:
    print("Gmail App Password loaded successfully!")
else:
    print("WARNING: MAIL_PASSWORD is not set!")

# =========================================================
# UPDATE OLD DATE RECORDS
# =========================================================

try:
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

except Exception as e:
    print("Date update error:", e)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():

    conn = sqlite3.connect(
        "food_rescue.db",
        timeout=10
    )

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# SEND EMAIL HELPER
# =========================================================

def send_email(to_email, subject, body):

    try:

        if not to_email:
            print("EMAIL FAILED: Empty email address")
            return False

        if not app.config["MAIL_PASSWORD"]:
            print("EMAIL FAILED: MAIL_PASSWORD is not configured")
            return False

        msg = Message(
            subject=subject,
            sender=app.config["MAIL_USERNAME"],
            recipients=[to_email]
        )

        msg.body = body

        mail.send(msg)

        print("EMAIL SENT:", to_email)

        return True

    except Exception as e:

        print("EMAIL FAILED")
        print("EMAIL:", to_email)
        print("ERROR:", repr(e))

        return False


# =========================================================
# SEND EMAIL TO ALL NGOs
# =========================================================

def send_email_to_ngos(
    food_name,
    quantity,
    location,
    donor
):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT email
        FROM users
        WHERE role='NGO'
        AND email IS NOT NULL
        AND email != ''
    """)

    ngos = cur.fetchall()

    conn.close()

    print("NGOs found:", len(ngos))

    body = f"""
Hello NGO,

A new food donation has been added.

Donation Details:

Food Name : {food_name}
Quantity  : {quantity}
Location  : {location}
Donor     : {donor}

Please login to Smart Food Rescue Network
and accept this donation.

Thank You.

Smart Food Rescue Network
"""

    for ngo in ngos:

        send_email(
            ngo["email"],
            "🍽 New Food Donation Available",
            body
        )


# =========================================================
# SEND ACCEPTANCE EMAIL TO DONOR
# =========================================================

def send_accept_email(donation_id):

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
    """, (donation_id,))

    data = cur.fetchone()

    conn.close()

    if not data:

        print("Donor email not found")

        return

    food_name = data["food_name"]
    quantity = data["quantity"]
    location = data["location"]
    donor = data["donor"]
    email = data["email"]

    body = f"""
Hello {donor},

Great news! 🎉

Your food donation has been accepted by an NGO.

Donation Details:

Food     : {food_name}
Quantity : {quantity}
Location : {location}

Thank you for helping reduce food waste.

❤️ Smart Food Rescue Network
"""

    send_email(
        email,
        "🎉 Your Food Donation Has Been Accepted",
        body
    )


# =========================================================
# SEND EMAIL TO ALL VOLUNTEERS
# =========================================================

def send_email_to_volunteers(donation_id):

    conn = get_db()
    cur = conn.cursor()

    # Get donation information

    cur.execute("""
        SELECT
            food_name,
            quantity,
            location,
            donor
        FROM donations
        WHERE id=?
    """, (donation_id,))

    donation = cur.fetchone()

    if not donation:

        conn.close()

        print("Donation not found")

        return

    # Get volunteers

    cur.execute("""
        SELECT email
        FROM users
        WHERE role='Volunteer'
        AND email IS NOT NULL
        AND email != ''
    """)

    volunteers = cur.fetchall()

    conn.close()

    print("Volunteers found:", len(volunteers))

    body = f"""
Hello Volunteer,

A food donation has been accepted by an NGO.

Donation Details:

Food     : {donation["food_name"]}
Quantity : {donation["quantity"]}
Location : {donation["location"]}
Donor    : {donation["donor"]}

Please login to Smart Food Rescue Network
and deliver this food.

Thank You.

Smart Food Rescue Network
"""

    for volunteer in volunteers:

        send_email(
            volunteer["email"],
            "🚚 New Food Delivery Task",
            body
        )


# =========================================================
# SEND DELIVERY EMAIL TO ALL NGOs
# =========================================================

def send_delivery_email(donation_id):

    conn = get_db()
    cur = conn.cursor()

    # Get donation information

    cur.execute("""
        SELECT
            food_name,
            quantity,
            location
        FROM donations
        WHERE id=?
    """, (donation_id,))

    donation = cur.fetchone()

    if not donation:

        conn.close()

        print("Donation not found")

        return

    # Get NGOs

    cur.execute("""
        SELECT email
        FROM users
        WHERE role='NGO'
        AND email IS NOT NULL
        AND email != ''
    """)

    ngos = cur.fetchall()

    conn.close()

    print("NGOs found:", len(ngos))

    body = f"""
Hello NGO,

The food donation has been successfully delivered.

Donation Details:

Food     : {donation["food_name"]}
Quantity : {donation["quantity"]}
Location : {donation["location"]}

Thank you for helping the community.

Smart Food Rescue Network
"""

    for ngo in ngos:

        send_email(
            ngo["email"],
            "✅ Food Donation Delivered",
            body
        )


# =========================================================
# HOME PAGE
# =========================================================

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


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users
            (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            password,
            role
        ))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM users
            WHERE email=? AND password=?
        """, (
            email,
            password
        ))

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


# =========================================================
# DONOR DASHBOARD
# =========================================================

@app.route("/donor")
def donor():

    if (
        "user" not in session
        or session.get("role") != "Donor"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM donations
        ORDER BY id DESC
    """)

    donations = cur.fetchall()

    conn.close()

    return render_template(
        "donor_dashboard.html",
        donations=donations
    )


# =========================================================
# DONATE FOOD
# =========================================================

@app.route("/donate", methods=["GET", "POST"])
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

        cur.execute("""
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
            (?, ?, ?, ?, ?, datetime('now','localtime'))
        """, (
            food_name,
            quantity,
            location,
            donor,
            "Pending"
        ))

        conn.commit()
        conn.close()

        # Send email AFTER donation is saved

        send_email_to_ngos(
            food_name,
            quantity,
            location,
            donor
        )

        return redirect("/donor")

    return render_template("donate_food.html")


# =========================================================
# NGO DASHBOARD
# =========================================================

@app.route("/ngo", methods=["GET", "POST"])
def ngo():

    if (
        "user" not in session
        or session.get("role") != "NGO"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        location = request.form["location"]

        cur.execute("""
            SELECT *
            FROM donations
            WHERE location LIKE ?
            ORDER BY id DESC
        """, (
            "%" + location + "%",
        ))

    else:

        cur.execute("""
            SELECT *
            FROM donations
            ORDER BY id DESC
        """)

    donations = cur.fetchall()

    conn.close()

    return render_template(
        "ngo_dashboard.html",
        donations=donations
    )


# =========================================================
# ACCEPT DONATION
# =========================================================

@app.route("/accept/<int:id>")
def accept(id):

    if (
        "user" not in session
        or session.get("role") != "NGO"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE donations
        SET status=?
        WHERE id=?
    """, (
        "Accepted",
        id
    ))

    conn.commit()
    conn.close()

    # Email donor

    send_accept_email(id)

    # Email volunteers

    send_email_to_volunteers(id)

    return redirect("/ngo")


# =========================================================
# VOLUNTEER DASHBOARD
# =========================================================

@app.route("/volunteer")
def volunteer():

    if (
        "user" not in session
        or session.get("role") != "Volunteer"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM donations
        WHERE status='Accepted'
        ORDER BY id DESC
    """)

    donations = cur.fetchall()

    conn.close()

    return render_template(
        "volunteer_dashboard.html",
        donations=donations
    )


# =========================================================
# DELIVER FOOD
# =========================================================

@app.route("/deliver/<int:id>")
def deliver(id):

    if (
        "user" not in session
        or session.get("role") != "Volunteer"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE donations
        SET status=?
        WHERE id=?
    """, (
        "Delivered",
        id
    ))

    conn.commit()
    conn.close()

    # Email NGOs

    send_delivery_email(id)

    return redirect("/volunteer")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin():

    if (
        "user" not in session
        or session.get("role") != "Admin"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")

    total_users = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role='Donor'
    """)

    total_donors = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role='NGO'
    """)

    total_ngos = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role='Volunteer'
    """)

    total_volunteers = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM donations
    """)

    total_donations = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM donations
        WHERE status='Pending'
    """)

    pending = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM donations
        WHERE status='Accepted'
    """)

    accepted = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM donations
        WHERE status='Delivered'
    """)

    delivered = cur.fetchone()[0]

    cur.execute("""
        SELECT *
        FROM donations
        ORDER BY id DESC
    """)

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


# =========================================================
# ADMIN DONORS
# =========================================================

@app.route("/admin/donors")
def admin_donors():

    if (
        "user" not in session
        or session.get("role") != "Admin"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email
        FROM users
        WHERE role='Donor'
    """)

    donors = cur.fetchall()

    conn.close()

    return render_template(
        "donors.html",
        donors=donors
    )


# =========================================================
# ADMIN NGOs
# =========================================================

@app.route("/admin/ngos")
def admin_ngos():

    if (
        "user" not in session
        or session.get("role") != "Admin"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email
        FROM users
        WHERE role='NGO'
    """)

    ngos = cur.fetchall()

    conn.close()

    return render_template(
        "ngos.html",
        ngos=ngos
    )


# =========================================================
# ADMIN VOLUNTEERS
# =========================================================

@app.route("/admin/volunteers")
def admin_volunteers():

    if (
        "user" not in session
        or session.get("role") != "Admin"
    ):

        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email
        FROM users
        WHERE role='Volunteer'
    """)

    volunteers = cur.fetchall()

    conn.close()

    return render_template(
        "volunteers.html",
        volunteers=volunteers
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template("about.html")


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact")
def contact():

    return render_template("contact.html")


# =========================================================
# FAQ
# =========================================================

@app.route("/faq")
def faq():

    return render_template("faq.html")


# =========================================================
# REQUEST FOOD
# =========================================================

@app.route("/request")
def request_food():

    return render_template("request_food.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )