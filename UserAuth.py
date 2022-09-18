#Blueprint
from flask import Blueprint
UserAuth = Blueprint('UserAuth', __name__)

#import
from flask import render_template, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user, current_user
from flask.helpers import flash
from Website_Folder import DATABASEHELPER as DB
from Website_Folder.users import User
from werkzeug.security import generate_password_hash, check_password_hash

#Auth
@UserAuth.route('/signup', methods=['GET','POST'])
def signUpPage():
    #create connection to DB
    conn,cur = DB.createConnCur()

    if request.method == 'POST':
        #search
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

        #get data from form
        email = request.form.get('email')
        userName = request.form.get('userName')
        password = request.form.get('password1')
        password2 = request.form.get('password2')

        #check each data if it matches with standards
        if len(DB.getUserEmail(conn, cur, email)) >0:
            print('email error')
            flash('Email allready exist.', category='Error')
        elif len(DB.getUsername(conn,cur,userName)) >0:
            flash('Username allready exist.', category='Error')
        elif len(userName) <2:
            flash('Username must have more then one character.', category='Error')
        elif password != password2:
            flash('Password dont match.', category='Error')
        elif len(password) <9:
            flash('Password must have more then eight characters.', category='Error')
        else:
            #Hash password
            pHash = generate_password_hash(password)
            #Add to DB
            DB.CreateUser(conn, cur, userName, email,  pHash)
            
            #log in user
            user = User()
            user.email = email
            login_user(user)

            flash('Account created!', category='Success')

            return redirect(url_for('Views.accountPage'))

        return render_template('signup.html', user = current_user)
    else:
        return render_template('signup.html', user = current_user)


@UserAuth.route('/login', methods=['GET','POST'])
def loginPage():
    #create connection to DB
    conn,cur = DB.createConnCur()
    
    #Method used
    if request.method == 'POST':
        #search
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

        #get data from form
        email = request.form.get('email')
        password = request.form.get('password')
        listUserData = DB.selectUser(conn, cur, email)

        #check each data if it matches with standards
        if listUserData == None:
            flash('Email doesnt exist.', category='Error')
            
        elif check_password_hash(listUserData[3], password) == False:
            flash('Password incorrect', category='Error')
            print('password doesnt exist')
        else: 
            #add to DB
            user = User()
            user.email = email
            login_user(user)

            flash('Logged in successfully', category='Success')

            return redirect(url_for('Views.accountPage'))
        
        return render_template('login.html', user = current_user)

    else:
        return render_template('login.html', user = current_user)



@UserAuth.route('/logout')
def logoutPage():
    #Logout user
    logout_user()
    return redirect(url_for('UserAuth.loginPage'))