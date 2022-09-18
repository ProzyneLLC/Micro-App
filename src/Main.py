#imports###################################################
from flask import render_template, request, redirect,url_for
from flask_login import current_user
from Website_Folder import create_app, DATABASEHELPER as DB
import os


#init######################################################
app = create_app()


#routes####################################################
#Home
@app.route('/', methods=['GET','POST'])
def homePage():
    conn, cur = DB.createConnCur()

    #Method used
    if request.method == 'POST':
        #search
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

    try:
        personal= (DB.getUserName(conn,cur,current_user.email))
    except:
        personal = ''


    return render_template('home.html', user = current_user,personal = personal)

#privacy
@app.route('/privacy', methods=['GET','POST'])
def privacyPage():
    conn, cur = DB.createConnCur()
    
    #Method used
    if request.method == 'POST':
        #search
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

    try:
        personal= (DB.getUserName(conn,cur,current_user.email))
    except:
        personal = ''

    return render_template('privacypolice.html', user = current_user, personal = personal)


###########################################################
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port , debug=True)