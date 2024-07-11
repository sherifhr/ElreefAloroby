from flask import Flask, render_template, request, redirect, url_for , session, send_from_directory
from datetime import datetime
import sqlite3, os
from datetime import datetime
from functools import wraps
from flask import redirect, url_for, flash
#app = Flask(__name__, static_url_path='/static/images')
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/static/images'
app.secret_key = 'f5746747a9b7fa1f5dd11963eaf8b22d45d691315703ff88d443bb0abf075c19'
app.config['DATABASE']='Market.db'
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def init_db():
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            phone       TEXT NOT NULL UNIQUE,
            email       TEXT ,
            password    PASSWORD NOT NULL )        """)
    conn.commit()

#Buyers table for registered customers --------------------------
    cursor = conn.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS buyers (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            phone         TEXT NOT NULL,    
            email         TEXT NOT NULL,    
            password      PASSWORD NOT NULL)''')
    conn.commit()     

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farms (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            owner_id    INTEGER ,
            phone       TEXT NOT NULL,
            email       TEXT NOT NULL ,
            address1    TEXT NOT NULL , 
            address2    TEXT        )        """)
    conn.commit()

    cursor= conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products(
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            farm_id        	INTEGER,
            prod_category   TEXT,
            prod_name 	    TEXT,
            package	        TEXT,
            unit_price      INTEGER,
            filename        TEXT,
            stock           INTEGER,
            event_datetime  datetime  )   ''')
    conn.commit()

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            id              INTEGER PRIMARY KEY ,
            buyer_id        INTEGER ,
            farm_id         INTEGER,
            product_id      INTEGER,
            quantity        NUMBER,
            package         TEXT,
            unit_price      NUMBER,
            total_price     NUMBER,
            filename        TEXT,
            event_datetime  datetime,
            order_status    TEXT         )''')
    conn.commit()
        
    cursor = conn.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS orders(
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no    TEXT,  
            order_date  TEXT,
            order_farm  TEXT,
            order_buyer TEXT,  
            order_copy  BLOB  )     ''')
    conn.commit()     
    conn.close()

# Run the init_db function when the app starts up

init_db()

@app.route('/screenshot')
def screenshot():
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    screenshot.close()
    
    #screenshot = ImageGrab.grab(bbox=(50, 50, 1366, 768))
    #screenshot = ImageGrab.grab()
    #screenshot.save("PO.png")
    # Close the screenshot
    #screenshot.close()
    #return redirect(url_for('save_order'))
    return ('ok')

@app.route('/')
#@login_required
def home():
    session.clear()
    login_required
    return render_template('index.html')
    
def verify_credentials1(name, password):
    if name!="" :
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM owners WHERE name = ? AND password = ?", (name, password))
        result = cursor.fetchone()
        conn.close()
        # If a row is returned, the credentials are valid
        if result:
             return True
        else:
            return False

def verify_credentials2(name, password):
    if name!="" :
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buyers WHERE name = ? AND password = ?", (name, password))
        result = cursor.fetchone()
        conn.close()
        # If a row is returned, the credentials are valid
        if result:
            return True
        else:
            return False

def login_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_market'))  # Redirect to login page if user is not logged in
        return route_function(*args, **kwargs)
    return decorated_function

def login_market_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login_market'))  # Redirect to login page if user is not logged in
        return route_function(*args, **kwargs)
    return decorated_function

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get the user data from the form
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        try:
            # Create a new user in the database
            new_user = User(name=name, phone=phone, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()

            # Flash a success message and redirect to the login page
            flash('User created successfully. Please log in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            # Handle any errors that occurred during the sign-up process
            db.session.rollback()
            flash('Error creating user: {}'.format(str(e)), 'danger')
    # Render the sign-up template
    return render_template('sign_up.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name      = request.form['name']
        phone     = request.form['phone']
        email     = request.form['email']
        password  = request.form['password']
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM owners WHERE phone = ?", (phone,))
        count = cursor.fetchone()[0]
        # If the count is 0, the phone number is available; otherwise, it is already used by another user
        if count>0:
            # If the username or email address is already in use, display an error message
            error = 'Phone is already in use'
            return render_template('signup.html', error=error)
        else:
            # If the username and phone  are not in use, create a new user account and store it in the database
            cursor.execute("INSERT INTO owners (name, phone, email, password) VALUES (?, ?,?,?)", (name, phone, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    #session['original_page'] = request.url
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        session['name']= name
        if verify_credentials1(name, password):
            # Set session variables to indicate user is logged in
            session['logged_in']    = True
            session['username']     = name
            
            #return render_template('dashboard.html', id)
            return redirect(url_for('dashboard'))
        else:
            #return session['original_page']
            return render_template('login.html', error='Invalid user name or password')
    else: 
        return render_template('login.html')
 
@app.route('/signup_market', methods=['GET', 'POST'])
def signup_market():
    if request.method == 'POST':
        name      = request.form['name']
        phone     = request.form['phone']
        email     = request.form['email']
        password  = request.form['password']
        
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM buyers WHERE phone = ?", (phone,))
        count = cursor.fetchone()[0]
        # If the count is 0, the phone number is available; otherwise, it is already used by another user
        if count>0:
            # If the username or email address is already in use, display an error message
            error = 'Phone is already in use'
            return render_template('signup_market.html', error=error)
        else:
            # If the username and phone  are not in use, create a new user account and store it in the database
            cursor.execute("INSERT INTO buyers (name, phone, email, password) VALUES (?, ?,?,?)", (name, phone, email, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login_market'))
    return render_template('signup_market.html')

@app.route('/login_market', methods=['GET', 'POST'])
def login_market():
    session.clear()
    #session['original_page'] = request.url
    if request.method == 'POST':
        name  = request.form['name']
 #       phone = request.form['phone']
        password = request.form['password']
        session['username']= name
        if verify_credentials2(name, password):
            # Set session variables to indicate user is logged in
            session['logged_in']    = True
            session['username']     = name
            return redirect(url_for('prod_list')  )
        else:    
            return redirect(url_for('prod_list'))
    else: 
        return render_template('login_market.html')

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
  # return reditect('/')
    #return 'You are logged out !'    
    error = 'you are logged out ok'
    return redirect(url_for('login', error=error))
    #return render_template('logout.html') 

#xxxxxxxxxxxxxxxxxxxxxxxxxxx
def read_products_db():
    try:
        conn = sqlite3.connect('Market.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        product_items=c.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return (product_items)

def read_products_name(prod_id):
    try:
        conn = sqlite3.connect('Market.db')
        c = conn.cursor()
        c.execute("SELECT id, prod_category, prod_name FROM products WHERE id=?", prod_id=prod_id)
        product_item=c.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return (product_item)


def read_product_name(p_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products where id=?" , (p_id,))
    row2 = cursor.fetchone()
    conn.commit()
    conn.close()
    return row2


def read_products_db1(): #------------------
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    query='''
    SELECT 
    products.id, products.farm_id, products.prod_category, 
    products.prod_name, products.package, products.unit_price, 
    products.stock, products.event_datetime,farms.id, farms.name,
    products.filename
    
    FROM products 
    JOIN farms ON products.farm_id=farms.id 
    ORDER BY products.event_datetime DESC;
    '''
    cursor.execute(query)
    prods=cursor.fetchall()
    conn.close()
    if not prods:
        return('No records found')
    else: 
        return prods


def read_farms_from_db():
    items = []
    try:
        conn = sqlite3.connect('Market.db')
        c = conn.cursor()
        #c.execute("CREATE TABLE IF NOT EXISTS buyers (id INTEGER PRIMARY KEY, name TEXT)")
        c.execute("SELECT * FROM farms")
        for row in c.fetchall():
            items.append({'id': row[0], 'name': row[1]})
        conn.close()
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return items

def read_farm_from_db(farm_id):
    conn = sqlite3.connect('Market.db')
    c = conn.cursor()
    c.execute("SELECT * FROM farms WHERE id=?", (farm_id))
    item=c.fetchone()
    return item


def read_farm_name(f_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farms where id=?" , (f_id,))
    row1 = cursor.fetchone()
    #buyer_id=row[0]
    conn.commit()
    conn.close()
    return row1

def read_buyers_from_db():
    items = []
    try:
        conn = sqlite3.connect('Market.db')
        c = conn.cursor()
        #c.execute("CREATE TABLE IF NOT EXISTS buyers (id INTEGER PRIMARY KEY, name TEXT)")
        c.execute("SELECT * FROM buyers")
        for row in c.fetchall():
            items.append({'id': row[0], 'name': row[1]})
        conn.close()
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return items

def read_buyers_table(buyer):
    try:
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM buyers WHERE buyers.name=?', (buyer,))
        row=cursor.fetchone()  #---------------Order buyer info.
        conn.commit()
        conn.close
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return row


#cart items list for buyer name
def read_cart_items_db(buyer):
    try:
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        filter_value=buyer
        print(buyer,'SSSSSS')
        query = '''
        SELECT  
        ROW_NUMBER() OVER () as raw_num, cart_items.id,
        cart_items.buyer_id, cart_items.product_id, 
        cart_items.farm_id, cart_items.quantity, cart_items.unit_price, 
        cart_items.event_datetime, cart_items.order_status, cart_items.filename,
        products.id, products.prod_category, products.prod_name, 
        products.package, 
        farms.id, farms.name, farms.phone,farms.email,buyers.id, buyers.name, buyers.phone 
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id 
        JOIN farms ON products.farm_id = farms.id 
        JOIN buyers ON cart_items.buyer_id = buyers.id
        WHERE buyers.name=?;
        '''
        cursor.execute(query, (filter_value,))
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        print("sssss", rows)
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return (rows)

def read_cart_items_db2(farm):
    try:
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        filter_value = farm
        print(farm, "sherif")
        query = '''
        SELECT 
            cart_items.id, cart_items.buyer_id, cart_items.product_id, cart_items.farm_id, cart_items.quantity, cart_items.unit_price, 
            cart_items.event_datetime,cart_items.order_status,
            products.id, products.prod_category, products.prod_name, 
            products.package,products.unit_price, cart_items.filename,
            farms.id, farms.name, buyers.id, buyers.name
        FROM cart_items 
        JOIN products ON cart_items.product_id=products.id
        JOIN farms ON cart_items.farm_id=farms.id
        JOIN buyers on cart_items.buyer_id=buyers.id
        WHERE farms.name=?;
        '''
        cursor.execute(query, (filter_value,))
        # Process the result set
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return (rows)


#reads all table records
def cart_table_count():
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cart_items")
    count = cursor.fetchone()
    record_count= count[0]
    conn.commit()
    conn.close()
    return record_count

#reads table count for buyer
def cart_table_count1(buyer):
    row3 = read_buyer_id(buyer)
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cart_items WHERE buyer_id=?" , 
                   (row3[0],))
    total_records = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return total_records


def read_buyer_id(buyer):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buyers where name=?" , (buyer,))
    row3 = cursor.fetchone()
    conn.commit()
    conn.close()
    return row3

def read_farm_name(f_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farms where id=?" , (f_id,))
    row1 = cursor.fetchone()
    #buyer_id=row[0]
    conn.commit()
    conn.close()
    return row1


def read_orders_count():
    try:
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        #to get the number of records in orders table
        cursor.execute('SELECT COUNT(*) FROM orders')
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return count


def read_order_from_db(order_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row=cursor.fetchone()
    conn.commit()
    conn.close()
    return row

def read_orders_from_db():
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    rows    = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def read_purchase_order_items1(farm, buyer):
    try:
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        query = '''
        SELECT  
            cart_items.buyer_id, 
            cart_items.product_id, 
            cart_items.farm_id, 
            cart_items.quantity, 
            cart_items.unit_price, 
            cart_items.total_price, 
            cart_items.event_datetime,
            products.prod_category, 
            products.prod_name, 
            products.package, 
            products.unit_price,
            farms.id, 
            farms.name, 
            buyers.id, 
            buyers.name,
            buyers.phone,
            buyers.email
        FROM cart_items 
        JOIN products ON cart_items.product_id=products.id
        JOIN farms ON cart_items.farm_id=farms.id
        JOIN buyers on cart_items.buyer_id=buyers.id
        WHERE farms.name=? AND buyers.name=?  
        '''
        cursor.execute(query, (farm, buyer))
        prods = cursor.fetchall() #-------------Order items-->
        conn.commit()
        conn.close
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return prods
#xxxxxxxxxxxxx

@app.route('/buyer_info/<int:index>')
#@login_required
def buyer_info(index):
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute("SELECT * FROM buyers WHERE buyers.id=?", (index,))
        rows    = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('buyer_info.html', rows=rows)
    
#--Add owner (user)----------------------------------------------------
@app.route('/add_user')
#@login_required
def add_user():
        if session['username']=="admin":
            #return 'user added successfully' 
            return render_template('add_user.html')
        else: 
            return ('You are not authorized')

@app.route('/delete_user/<int:user_id>', methods=['GET', 'POST']) 
@login_required
def delete_user(user_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM owners WHERE id=? ''', (user_id,)  ) 
    conn.commit()
    conn.close()
    return redirect(url_for('prod_list'))

#----customers --------
@app.route('/owners_list')
#@login_required
def owners_list():
    username=session['username']
    if username =='admin' :
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute('SELECT * FROM owners')
        rows    = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('owners_list.html', rows=rows)
    else: return ('Not authorized')

@app.route('/buyers_list')
#@login_required
def buyers_list():
    username=session['username']
    if username =='admin' :
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute('SELECT * FROM buyers')
        rows    = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('buyers_list.html', rows=rows)
    else: return ('Not authorized')


@app.route('/add_product')
#@login_required
def add_product():
    #username=session['username']
    items = read_farms_from_db()    
    return render_template('add_productB.html' , farms=items)    

#----add product by farm owner--->
def add_product(farm_id):
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM farms WHERE id=?", (farm_id,))
    rows    = cursor.fetchone()
    conn.commit()
    conn.close()
    return rows


@app.route('/add_productY<int:farm_id>') 
#@login_required
def add_productY(farm_id):
    rows = add_product(farm_id)
    return render_template('add_productY.html' , rows=rows)    

#--Add product to products table
@app.route('/submit', methods=['POST'])
def submit():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    farm_id        = request.form['farm_id']
    prod_category  = request.form['prod_category']
    prod_name      = request.form['prod_name']
    package        = request.form['package']
    unit_price     = request.form['unit_price']
    stock     = request.form['stock']
    event_datetime  = formatted_datetime                #----------------------
    uploaded_files = request.files.getlist('image_path')
    item_folder = os.path.join("static/images", farm_id)
#----------------------
#    if not os.path.exists(item_folder):
 #      os.makedirs(item_folder)
 #      print(f"item folder '{farm}' created successfully.")
 #   else:
 #       print(f"User folder '{farm}'already exists.")
 #   saved_files = [] # emplty list/array to get list of data
    
    for file in uploaded_files:
            filename = file.filename
            if len(filename)>0 :
                #file.save(os.path.join('static/images/' +'/'+ farm_id +'/'+ filename))
                file.save(os.path.join('static/images/'+filename))
            
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO products
                                    (farm_id, Prod_Category, Prod_Name, unit_price, stock, filename, Package, event_datetime) 
                            VALUES (?,?,?,?,?,?,?,?)''',
                        (farm_id, prod_category, prod_name, unit_price, stock, filename, package, event_datetime,))
    conn.commit()
    conn.close()
    return "Record saved successfully"
#    return render_template('add_productY.html', rows=rows)

#-----------update products data base table
@app.route('/update_product' , methods=['POST']) 
def update_product():  
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    try:
        id              = request.form['id']
        farm_id         = request.form['farm_id']
        prod_category   = request.form['prod_category']
        prod_name       = request.form['prod_name']
        package         = request.form['package']
        unit_price      = request.form['unit_price']
        stock           = request.form['stock']
        event_datetime  = formatted_datetime    #----------------------
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        cursor.execute(''' UPDATE products SET 
            Farm_id=?, prod_category=?, prod_name=?, package=?, Unit_Price=? ,Stock=?, event_datetime=? WHERE id=? ''', 
            ( farm_id, prod_category, prod_name, package, unit_price, stock, event_datetime, id))
        conn.commit()
        conn.close()
        return 'data updated ok'
    except sqlite3.IntegrityError:
       return 'Entry already exists! ... please try again'

#--------function to edit and update products in products table 
@app.route('/edit_product/<int:item_id>') 
def edit_product(item_id):
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()    
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM products WHERE id=? ''', (item_id,)  ) 
    item    = cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template('edit_product.html', item=item)

@app.route('/delete_product/<int:item_id>') 
#@login_required
def delete_product(item_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM products WHERE id=? ''', (item_id,)  ) 
    #need confirm message
    conn.commit()
    conn.close()
    return('item deleted succfully...')
    #return redirect(url_for('prod_list3'))

#-------------List all products on "products page"-------visitors
@app.route('/prod_list')  
def prod_list():
    prods= read_products_db1()
    return render_template('products.html', prods=prods)
    
#------list all products ---------admin user
@app.route('/prod_list1/')  
def prod_list1():
    prods= read_products_db1()
    return render_template('prod_list.html', prods=prods)

#------List farm products for owner -----------------
@app.route('/prod_list2/<int:idx>') 
def prod_list2(idx):
 #   session.clear()
    print(idx)
    filter_value=idx
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()    
    query='''
SELECT 
    products.id, products.farm_id, products.prod_category, 
    products.prod_name, products.package, products.unit_price, 
    products.stock, products.event_datetime,
    farms.id, farms.name
    FROM products 
    JOIN farms ON products.farm_id=farms.id 
    WHERE farms.id = ? ;
    '''
    cursor.execute(query, (filter_value,))
    prods=cursor.fetchall()
    cursor.close()
    conn.close()
    if not prods :
         # Handle the case where the items list is empty
        return ('No products , list is empty')
      #  return render_template('prod_list.html', prods=[])
    else:
        return render_template('prod_list.html', prods=prods)

#-------------Products list for selected farm ------------
@app.route('/prod_list_by_farm', methods=['GET', 'POST'])   
def prod_list_by_farm():
 #   session.clear()
    Fx=request.form['querry-text']
    print(Fx)    
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    query='''
    SELECT 
    products.id, products.farm_id, products.prod_category, products.prod_name, products.package, products.unit_price, products.stock, products.event_datetime,
    farms.id, farms.name
    FROM products 
    JOIN farms ON products.farm_id=farms.id 
    WHERE farms.id = ? ;
    '''
    cursor.execute(query, (Fx,))
    prods    = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('prod_list_a.html', prods=prods)

#--------Products list matches selected category-----------
@app.route('/prod_list_by_products', methods=['GET', 'POST'])   
def prod_list_by_products():
 #   session.clear()
    Fx=request.form['querry-text']
    print(Fx)    
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    query='''
    SELECT 
    products.id, products.farm_id, products.prod_category, products.prod_name, products.package, products.unit_price, products.stock, products.event_datetime,
    farms.id, farms.name
    FROM products 
    JOIN farms ON products.farm_id=farms.id 
    WHERE prod_category = ? ;
    '''
    cursor.execute(query, (Fx,))
    prods = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('prod_list_a.html', prods=prods)

@app.route('/search_by_product')  # 
def search_by_product():
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT prod_category FROM products ''') 
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template('search-input-products.html', rows=rows)

@app.route('/search_by_farm')  # 
def search_by_farm():
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, name FROM farms ''') 
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template('search-input-farm.html', rows=rows)

@app.route('/view_image/<int:item_id>') #Not used
def view_image(item_id):
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id=?", (item_id,))
    #cursor.execute("UPDATE entries SET name=?, email=? WHERE id=?", (user_id,))
    record= cursor.fetchone()
    photo=record[7] 
    prod_name=record[3]
    conn.commit()
    conn.close()
    return render_template('view_image.html', prod_name=prod_name, photo=photo )


#xxxxxxxxxxxxxxxxxxxxxxFARMxxxxxxxxxxxxxxxxxxxx
@app.route('/add_farm')
#@login_required
def add_farm():
    user    =session['username']
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM owners WHERE name=?", (user,))
    rows    = cursor.fetchone()
    conn.commit()
    conn.close()
    #if user =='admin' :
    return render_template('add_farm.html',rows=rows)    
    #else: return ('not authorized')

@app.route('/edit_farm/<int:farm_id>') 
#@login_required
def edit_farm(farm_id):
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM farms WHERE id=?", (farm_id,))
    #cursor.execute("UPDATE farms SET name=?, email=? WHERE id=?", (user_id,))
    user    = cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template('edit_farm.html', user=user)

@app.route('/delete_farm/<int:farm_id>') 
@login_required
def delete_farm(farm_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM farms WHERE id=? ''', (farm_id,)  ) 
    conn.commit()
    conn.close()
    return ('Delete record successfully')
    #return redirect(url_for('cart_items_list'))

@app.route('/farm_list_admin') #original fun
def farm_list_admin():
 #   session.clear()
    user=session['username']
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    cursor.execute('SELECT * FROM farms')
    rows    = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('farm_list.html', rows=rows)
    
@app.route('/farm_list')
def farm_list():
 #   session.clear()
    user=session['username']
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    if user=='admin':
        cursor.execute('SELECT * FROM farms' )
        rows    = cursor.fetchall()
        rows    = rows
        conn.commit()
        conn.close()
        return render_template('farm_list_admin.html', rows=rows)
    else:
        cursor.execute("SELECT * FROM farms where owner like ?" , ('%' + user + '%',))
        rows    = cursor.fetchall()
        rows    = rows
        conn.commit()
        conn.close()
        return render_template('farm_list.html', rows=rows)

 #-------------------Edit/add Farm Record------------------------   
@app.route('/update_new_farm', methods=['POST'])
#@login_required
def update_new_farm():
    try:
        name        =request.form['name']
        owner_id    =request.form['owner_id']
        phone       =request.form['phone']
        email       =request.form['email']
        address1    =request.form['address1']
        address2    =request.form['address2']
        #return address1
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM farms where name like ?" , ('%' + name + '%',))
        
        #cursor.execute("SELECT COUNT(*) FROM farms where name=?" , ('name',))
        COUNT = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        if COUNT >0 :
            return ('farm name exists! please select another name ') 
        else:
            conn    = sqlite3.connect('Market.db')
            cursor  = conn.cursor()
            cursor.execute ('''INSERT INTO farms
            ( name, owner_id, phone, email, address1, address2) 
                VALUES (?,?,?,?, ?, ?)''',
                (name, owner_id, phone, email, address1, address2) )
            conn.commit()
            conn.close()
            return 'Farm saved successfully'
    except sqlite3.IntegrityError:
        return ('Error !')
       
    #return 'Entry already exists in the database ... please try again!'
      #  return redirect(url_for('add_farm'), error='not unique value')

@app.route('/update_farm', methods=['POST'])
#@login_required
def update_farm():
        id      =request.form['id']
        name    =request.form['name']
        owner   =request.form['owner']
        phone   =request.form['phone']
        email   =request.form['email']
        address1 =request.form['address1']
        address2 =request.form['address2']
    
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute("UPDATE farms SET name=?, owner=?, phone=?, email=?, address1=?, address2=? WHERE id=?", (name, owner, phone, email, address1, address2, id))
        conn.commit()   
        conn.close()
        return ('Farm record modified ok')

#xxxxxxxxxxxxxx CART xxxxxxxxxxxx

@app.route('/cart_items_db', methods=['GET', 'POST']) #---ok
def cart_items_db():
    page = request.args.get('/page', 1, type=int)
    per_page = 1
    start_index = (page - 1) * per_page
    current_page=page
    #buyer=request.form['buyers.name']
    buyer=session['username']
    total_records = cart_table_count1(buyer)
    try:
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        query = '''
        SELECT  
        ROW_NUMBER() OVER () as raw_num, cart_items.id,
        cart_items.buyer_id, cart_items.product_id, 
        cart_items.farm_id, cart_items.quantity, cart_items.unit_price, 
        cart_items.event_datetime, cart_items.order_status, cart_items.filename,
        products.id, products.prod_category, products.prod_name, 
        products.package, 
        farms.id, farms.name, farms.phone,farms.email,buyers.id, buyers.name, buyers.phone 
        FROM cart_items
        JOIN products ON cart_items.product_id = products.id 
        JOIN farms ON products.farm_id = farms.id 
        JOIN buyers ON cart_items.buyer_id = buyers.id
        WHERE buyers.name=?
        LIMIT ? OFFSET ?
        '''
        cursor.execute(query, (buyer, per_page, start_index))
        row = cursor.fetchall()
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Error reading items from database:", e)
    return render_template('cart_items_db.html', total_records=total_records,row=row, current_page=current_page, buyer=buyer)

#--list for all cart items - admin
@app.route('/cart_items_list') #---ok
def cart_items_list():
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    query = '''
    SELECT 
    cart_items.id, cart_items.buyer_id, cart_items.product_id, 
    cart_items.farm_id, cart_items.quantity, cart_items.unit_price, 
    cart_items.event_datetime, cart_items.order_status, cart_items.filename,
    products.id, products.prod_category, products.prod_name, products.package, buyers.name,
    farms.id, farms.name 
    FROM cart_items
    JOIN products ON cart_items.product_id = products.id 
    JOIN farms  ON cart_items.farm_id = farms.id 
    JOIN buyers ON cart_items.buyer_id = buyers.id 
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    if not rows:
        return('No records found')
    else: 
        return render_template('cart_items_list.html',  rows=rows)
  
#--list for cart items - buyer
@app.route('/cart_items_list1<buyer>') #-- ok
#@login_required
def cart_items_list1(buyer):
    rows = read_cart_items_db(buyer)
    items = read_farms_from_db() 
    if not rows:
        return('No records in PO list')
    else: 
        return render_template('cart_items_list1.html',  rows=rows, items=items)

#---cart items for farm owners ---    
@app.route('/cart_items_list2<farm>') #-- ok
#@login_required
def cart_items_list2(farm):
    rows = read_cart_items_db2(farm)
    items = read_buyers_from_db() #function read buyers table
    if not rows:
        return('No records in PO list')
    else: 
        return render_template('cart_items_list2.html',  rows=rows, farm=farm, items=items)

@app.route('/add_to_cart/<int:item_id>', methods=['GET', 'POST'])
#@login_required
def add_to_cart(item_id):
 #   buyer=request.form['buyer']
    buyer=session['username']
    item_id=item_id
    #event_datetime=formatted_datetime
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    filter_value=item_id
    print(filter_value)
    query = '''
    SELECT 
    products.id, products.farm_id, products.prod_category, products.prod_name, products.package, products.unit_price, products.filename, 
    farms.id, farms.name
    FROM products
    JOIN farms ON products.farm_id = farms.id
    WHERE products.id=?;
    '''
    #cursor.execute(query)
    cursor.execute(query, (filter_value,))
    rows=cursor.fetchone()
    print(rows)
    conn.commit()
    conn.close()
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute(''' SELECT * from buyers  WHERE name=?''', (session['username'],))
    user = cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template('add_to_cart.html', rows=rows, user=user)

@app.route('/edit_cartY1/<int:item_id>')
#@login_required
def edit_cartY1(item_id):
 #  buyer=request.form['buyer']
    buyer=session['username']
    #event_datetime=formatted_datetime
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    filter_value = item_id
    query = '''
    SELECT 
    cart_items.id, cart_items.buyer_id, cart_items.product_id, cart_items.farm_id, cart_items.quantity, cart_items.unit_price, cart_items.event_datetime, cart_items.order_status, 
    products.id, products.prod_category ,products.prod_name, products.package,     
    farms.id, farms.name, 
    buyers.id, buyers.name
    FROM cart_items 
    JOIN farms ON cart_items.farm_id=farms.id
    JOIN buyers on cart_items.buyer_id=buyers.id
    JOIN products on cart_items.product_id=products.id
    WHERE cart_items.id=?;
    '''
    cursor.execute(query, (filter_value,))
    item =cursor.fetchone()
    conn.commit()
    conn.close()
    return render_template('edit_cart.html', item=item)

@app.route('/save_cart')
@login_required
def save_cart(item_id):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        cursor.execute(''' SELECT * from cart_items  WHERE id=?''', (item_id,))
        #event_datetime=formatted_datetime
        rows = cursor.fetchone()
        conn.commit()
        conn.close()
        return render_template('add_to_cart.html', rows=rows)

#--------add new items to cart table ?
@app.route('/update_cartY' , methods=['GET', 'POST']) #OK
@login_required
def update_cartY():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    try:
        buyer_id      = request.form['buyer_id']
        farm_id       = request.form['farm_id']
        product_id    = request.form['id']
        quantity      = request.form['quantity']
        unit_price    = request.form['unit_price']
        package       = request.form['package']
        order_status  = request.form['order_status']
        filename     = request.form['filename']
        event_datetime  = formatted_datetime
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO cart_items (
        buyer_id, product_id, farm_id, quantity, package, unit_price,order_status, filename, event_datetime) 
                VALUES (?,?,?,?,?,?,?,?,?)""",  ( buyer_id, product_id,farm_id, quantity, package, unit_price, order_status,filename, event_datetime,))
        conn.commit()
        conn.close()
        return ('item saved successfully ')
    except sqlite3.IntegrityError:
           return 'Entry error in the database ... please try again!'

#---update existing items in table
@app.route('/update_cartY1' , methods=['GET', 'POST']) 
def update_cartY1():  
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
    id  = request.form['id']
    farm_id         = request.form['farm_id']
    product_id      = request.form['product_id']
    buyer_id        = request.form['buyer_id']
    package         = request.form['package']
    unit_price      = request.form['unit_price']
    quantity        = request.form['quantity']
    order_status    = request.form['order_status']
#   filename     = request.form['filename']
    event_datetime  =formatted_datetime    
    try:
        conn = sqlite3.connect('Market.db')
        cursor = conn.cursor()
        cursor.execute(''' UPDATE cart_items SET 
            Farm_id=?,  Product_id=?, buyer_id=?, Package=?, Unit_Price=? ,quantity=?, order_status=?, event_datetime=? WHERE id=? ''', 
            ( farm_id, product_id, buyer_id,  package, unit_price, quantity, order_status, event_datetime, id))
        conn.commit()
        conn.close()
      # Check if the update was successful
        if cursor.rowcount > 0:
            return {'message': 'Record updated successfully'}, 200
        else:
            return {'message': 'No Record found with the given ID'}, 404
    except: 
        return 'Entry already exists in the database ... please try again!'

@app.route('/delete_item_from_cart/<int:item_id>') 
def delete_item_from_cart(item_id):
    print(item_id, "SSSSSS sherif")
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM cart_items WHERE id=? ''', (item_id,)  ) 
    conn.commit()
    conn.close()
    return('item deleted sussfully')

#xxxxxxxxxxxxxxxxxxxxxxxx
@app.route('/order_status') 
def order_status():
   return('order status')

@app.route('/create_purchase_order', methods =['GET', 'POST']) 
def create_purchase_order():
    farm = request.form['item-dropdown'] #selected farm
    buyer= request.form['buyer']
    count=read_orders_count()
    current_date = datetime.now().strftime('%Y%m%d')
    current_time = datetime.now().strftime('%H%M')
    order_no ='PO'+'-'+ current_time +'-'+ str(count+1)
    order_date = current_date
    prods= read_purchase_order_items1(farm, buyer)
    row  = read_buyers_table(buyer)
    return render_template('purchase_order.html', farm=farm, prods=prods, row=row, order_no=order_no, order_date=order_date)

@app.route('/save_order', methods =['GET', 'POST'] ) #------->
def save_order():
    order_no  =request.form['order_no']
    order_date=request.form['order_date']
    order_farm=request.form['order_farm']
    order_buyer=request.form['order_buyer']
    return render_template('save_order.html', order_no=order_no, order_date=order_date, order_farm=order_farm, order_buyer=order_buyer )

@app.route('/save_order1', methods =['GET', 'POST'] )
def save_order1():
    order_no  =request.form['order_no']
    order_date=request.form['order_date']
    order_farm=request.form['order_farm']
    order_buyer=request.form['order_buyer']
    print(order_farm)
    uploaded_files = request.files.getlist('image_path')
    for file in uploaded_files:
        filename = file.filename
        if len(filename)>0 :
            file.save(os.path.join('static/images/'+filename))
    #order_copy= filename
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders(order_no, order_date, order_farm, order_buyer, order_copy) VALUES (?, ?, ?, ?, ?)", (order_no, order_date, order_farm, order_buyer, filename))
    conn.commit()
    conn.close()
    return ("Order successfully saved to Data Base")
    #return render_template('save_order.html')  

@app.route('/view_order/<int:order_id>')
def view_order(order_id):
    row= read_order_from_db(order_id)
    return render_template('view_order.html', row=row)


@app.route('/view_orders_list')
def view_orders_list():
    rows= read_orders_from_db()
    return render_template('orders_list.html', rows=rows)


@app.route('/delete_order/<int:order_id>', methods=['GET', 'POST']) 
@login_required
def delete_order(order_id):
    conn = sqlite3.connect('Market.db')
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM orders WHERE id=? ''', (order_id,)  ) 
    conn.commit()
    conn.close()
    return redirect(url_for('view_orders_list'))

#xxxxxxxxxxxxxxxxxxxxxxxxxxx
#----------------Galary -------
@app.route('/image_area')
def image_area():
    return render_template('image_area.html')
  
@app.route('/view_gallery_images')
def view_gallery_images():
    
    image_folder = 'static/images' 
    image_files = os.listdir(image_folder)
    return render_template('view_gallery.html', image_files=image_files)

@app.route('/images/<path:filename>')
def get_image(filename):
    image_folder ='static/images-prod/'  
    return send_from_directory(image_folder, filename)

#xxxxxxxxxxxxxxxxxxxxxxxx

@app.route('/dashboard')
def dashboard():
    name=session['username']
    if name=='admin' :
        return render_template('dashboard_admin.html')
    else : 
        conn    = sqlite3.connect('Market.db')
        cursor  = conn.cursor()
        cursor.execute("SELECT id, name FROM owners where name=?" , (name,))
        rows = cursor.fetchone()
        conn.commit()
        print(rows)
        #return ('ok')
        cursor  = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM farms where owner_id=?" , (rows[0],))
        count = cursor.fetchone()
        record_count=count[0]
        conn.commit()
        #print(record_count)
        if record_count == 0 :
            return render_template('dashboard_new.html') # no farm registered to user's name
        else:
            conn    = sqlite3.connect('Market.db')
            cursor  = conn.cursor()
            cursor.execute("SELECT * FROM farms where owner_id=?" , (rows[0],))
            nos    = cursor.fetchone()
            cursor.close()
            conn.close()
            print(nos)           
            return render_template('dashboard_owners.html', nos=nos )
            #return ('ok') 


@app.route('/user_farm')
def user_farm():
    #session.clear()
    #if not session.get('logged_in'):
    user=session['username']
    conn    = sqlite3.connect('Market.db')
    cursor  = conn.cursor()
    cursor.execute("SELECT * FROM farms where owner like ?" , ('%' + user+ '%',))
    rows = cursor.fetchone()
    conn.commit()
    conn.close()
    #return rows[2], rows[2]
    return render_template ('dashboard_owners.html', rows=rows)

@app.route('/map-page')
def map():
    return render_template('map-page.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

#if __name__ == '__main__':
 #      app.run(debug=True)
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)