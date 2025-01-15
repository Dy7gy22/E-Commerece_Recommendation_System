from flask import Flask, render_template, request,jsonify, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
app = Flask(__name__)


 # load files===========================================================================================================
trending_products = pd.read_csv("trending_products.csv")
train_data = pd.read_csv("all_data.csv")


# List of predefined image URLs
random_image_urls =list(train_data.iloc[:10]['ImageURL'])

# Recommendations functions============================================================================================
# Function to truncate product name used to o shorten long strings so they don’t exceed the visual space allocated for them
def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."
    else:
        return text

  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Lhouc1234'
app.config['MYSQL_DB'] = 'Mydatabase'
  
mysql = MySQL(app)



def content_based_recommendations(train_data, item_name, top_n=10):
    # Check if the item name exists in the training data
    if item_name not in train_data['Name'].values:
        print(f"Item '{item_name}' not found in the training data.")
        return pd.DataFrame()

    # Create a TF-IDF vectorizer for item descriptions
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Apply TF-IDF vectorization to item descriptions
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Name'])

    # Calculate cosine similarity between items based on descriptions
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    # Find the index of the item
    item_index = train_data[train_data['Name'] == item_name].index[0]

    # Get the cosine similarity scores for the item
    similar_items = list(enumerate(cosine_similarities_content[item_index]))

    # Sort similar items by similarity score in descending order
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    # Get the top N most similar items (excluding the item itself)
    top_similar_items = similar_items[1:top_n+1]

    # Get the indices of the top similar items
    recommended_item_indices = [x[0] for x in top_similar_items]

    # Get the details of the top similar items
    recommended_items_details = train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]

    return recommended_items_details
@app.route("/")
def index():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html',trending_products=trending_products.head(8),truncate = truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price = random.choice(price))

@app.route("/main")
def main():
    message = "Please provide a valid product name and number."
    return render_template('main.html', message=message, content_based_rec=train_data,truncate=truncate)
    

# routes
@app.route("/index")
def indexredirect():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(price))

@app.route('/signin', methods =['GET', 'POST'])
def login():
    trending_products = pd.read_csv("trending_products.csv")
    
    if request.method == 'POST' and 'signinUsername' in request.form and 'signinPassword' in request.form:
        username = request.form['signinUsername']
        password = request.form['signinPassword']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['id']
            session['name'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            # Create a list of random image URLs for each product
            return render_template('main.html', message=message, content_based_rec=train_data,truncate=truncate)
        else:
            message = 'Please enter correct email / password !'
            # Create a list of random image URLs for each product
            random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
            price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
            return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                                    random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                                    signup_message=message
                                    )
'''''  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

'''
  
@app.route('/signup', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form :
        userName = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO signup VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            flash('You have successfully registered!', 'success')  # Add success message
            # Create a list of random image URLs for each product
            random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
            price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
            return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                               signup_message='User signed up successfully!'
                               )
           
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                            random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                            signup_message='User signed up successfully!'
                               )
"""""
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['userid'],))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM chat_history WHERE user_id = %s', (session['userid'],))
        chats = cursor.fetchall()
        return render_template('profile.html', account=account, chats=chats)
    return redirect(url_for('login'))


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    
""""" 
@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    prod = request.form.get('prod')
    nbr = request.form.get('nbr')

    if not prod or not nbr or not nbr.isdigit():
        message = "Please provide a valid product name and number."
        return render_template('main.html', message=message, content_based_rec=pd.DataFrame())
    
    nbr = int(nbr)
    content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

    if content_based_rec.empty:
        message = "No recommendations available for this product."
        return render_template('main.html', message=message, content_based_rec=pd.DataFrame())
    
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(content_based_rec))]
    prices = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]
    return render_template('main.html', content_based_rec=content_based_rec, truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(prices))

# Add this new route in your Flask application
@app.route("/cart_recommendations", methods=['POST'])
def cart_recommendations():
    product_name = request.json.get('productName')
    if not product_name:
        return jsonify({"error": "No product name provided"}), 400
    
    # Get recommendations using the existing function
    recommendations = content_based_recommendations(train_data, product_name, top_n=4)
    
    if recommendations.empty:
        return jsonify({"error": "No recommendations found"}), 404
    
    # Convert recommendations to a format suitable for JSON
    recommendations_list = []
    for _, product in recommendations.iterrows():
        recommendations_list.append({
            "name": truncate(product['Name'], 12),
            "brand": product['Brand'],
            "reviewCount": product['ReviewCount'],
            "rating": product['Rating'],
            "imageUrl": product['ImageURL']
        })
    
    return jsonify({"recommendations": recommendations_list})

if __name__=='__main__':
    app.run(debug=True)