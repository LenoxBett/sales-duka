# from flask import Flask,render_template

# app = Flask(__name__)

# @app.route('/')
# def sales():
#     return render_template("sales.html")

# @app.route('/products')
# def prods():
#     return render_template("products.html")

# @app.route("/dashboard")
# def dash():
#     return render_template("dashboard.html")

# app.run(debug=True)

from flask import Flask,flash,render_template,request,redirect,url_for
from database import get_data,prof_per_prod,profit_per_day,sales_per_day,sales_per_prod,check_email,check_email_pass,insert_user
from flask import session

# flask instance

app = Flask(__name__)
app.secret_key = "betika"
@app.route("/")
def index():
    if 'email' not in session:
        return redirect(url_for('login'))
        # return render_template("base.html")

@app.route("/home")
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

# products render a products.html file
@app.route("/products")
def products():
    if 'email' not in session:
        return redirect(url_for('login'))
    products = get_data("products")
    return render_template("products.html",prods=products)


# dashboard and render
@app.route("/dashboard")
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    p_product = prof_per_prod()
    p_day = profit_per_day()
    s_day = sales_per_day()
    s_prod  = sales_per_prod()
    # print(p_product)
    # print(p_day)
    # print(s_day)
    print(s_prod)
    p_name = []
    p_profit = []
    day = []
    d_profit = []
    sales_day = []
    sales_prod = []
    x = []
    y = []
    for i in p_product:
        p_name.append(i[0])
        p_profit.append(float(i[1]))
    
    for i in p_day:
        day.append(str(i[0]))
        d_profit.append(float(i[1]))

    for i in s_day:
        sales_day.append(str(i[0]))
        sales_prod.append(float(i[1]))

    for i in s_prod:
        x.append(i[0])
        y.append(float(i[1]))
    return render_template("dashboard.html",name=p_name,profit=p_profit,day = day,d_profit=d_profit,pro_name=x,pro_sales=y,sales_prod=sales_prod)


@app.route("/sales")
def sales():
    if 'email' not in session:
        return redirect(url_for('login'))
    sales = get_data("sales")
    products = get_data("products")
    return render_template("sales.html",sales=sales,prods=products)

@app.route("/login", methods=["POST", "GET"])
def login():
        # get form data
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

    # check email existence only if email is not None
    # if email:
        ch_email = check_email(email)

        if ch_email == None:
            flash("email does not exist, please register")
            return redirect(url_for("register"))
        else:
            ch_pass = check_email_pass(email, password)
            if len(ch_pass) < 1:
                flash("incorrect email or password")
            else:
                session ['email'] = email
                flash("login successful")
                return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/register")
def register():
        # get form data
    if request.method == "POST":
        f_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        # insert user
        c_email = check_email(email)
        if c_email == None:
            new_user = (f_name,email,password)
            insert_user(new_user)
            flash("registered successfully")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/products')
def prods():
    return render_template("products.html")

@app.route("/contact-us")
def contact():
    return render_template("contact-us.html")

@app.route("/my-account")
def my_acc():
    return render_template("my-account.html")

@app.route("/shop")
def shop():
    return render_template("shop.html")

@app.route("/shop-details")
def shop_details():
    return render_template("shop-detail.html")

@app.route("/check-out")
def check():
    return render_template("checkout.html")

@app.route("/about")
def about():
    return render_template("about.html")

app.run(debug=True)