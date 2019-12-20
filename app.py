# import classes from flask module
from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, request, session, flash
from carDAO import carDAO
from accessoriesDAO import accessoriesDAO
from functools import wraps # use for login required function

# https://www.youtube.com/watch?v=BnBjhmspw4c&feature=youtu.be this video helped me write this code

# create application object
app = Flask(__name__, static_url_path='', static_folder='.')

app.secret_key = "my precious" #need a secret key for sessions to work properly, protects the session from being accessed

# login required decorator 
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hello, World!"

# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    return render_template('home.html') #render home page

# Route for handling the login page logic https://realpython.com/introduction-to-flask-part-2-creating-a-login-page/
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

#create route for logout confirm page
@app.route('/loggedout')
def loggedout():
    return render_template('logged-out.html') # render a template

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)   
    flash('You were just logged out!')
    return redirect(url_for('loggedout'))

#app route for interlinking within the site
@app.route('/carviewer')
def carviewer():
    return render_template('carviewer.html')

@app.route('/accessories')
def accessories():
    return render_template('accessories.html')    

#curl "http://127.0.0.1:5000/cars"
@app.route('/cars')
def getAll():
    #print("in getall")
    results = carDAO.getAll()
    return jsonify(results)

#curl "http://127.0.0.1:5000/cars/2"
@app.route('/cars/<int:id>')
def findById(id):
    foundcar = carDAO.findByID(id)

    return jsonify(foundcar)

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Make\":\"hello\",\"Model\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/cars
@app.route('/cars', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    car = {
        "Make": request.json['Make'],
        "Model": request.json['Model'],
        "Price": request.json['Price'],
    }
    values =(car['Make'],car['Model'],car['Price'])
    newId = carDAO.create(values)
    car['id'] = newId
    return jsonify(car)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Make\":\"hello\",\"Model\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/cars/1
@app.route('/cars/<int:id>', methods=['PUT'])
def update(id):
    foundcar = carDAO.findByID(id)
    if not foundcar:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Make' in reqJson:
        foundcar['Make'] = reqJson['Make']
    if 'Model' in reqJson:
        foundcar['Model'] = reqJson['Model']
    if 'Price' in reqJson:
        foundcar['Price'] = reqJson['Price']
    values = (foundcar['Make'],foundcar['Model'],foundcar['Price'],foundcar['id'])
    carDAO.update(values)
    return jsonify(foundcar)
        

    

@app.route('/cars/<int:id>' , methods=['DELETE'])
def delete(id):
    carDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)