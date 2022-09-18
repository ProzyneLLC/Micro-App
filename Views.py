#Blueprint
from operator import or_
from os import extsep, link
import re
from flask import render_template, request, Blueprint, redirect, session, url_for
from flask_login import login_required, current_user
from flask.helpers import flash
from werkzeug.utils import import_string
from Website_Folder import DATABASEHELPER as DB
import validators

Views = Blueprint('Views', __name__)

#Acc
@Views.route('/account', methods=['GET','POST'])
@login_required
def accountPage():
    #get information about current user
    conn,cur= DB.createConnCur()

    useremail = current_user.email
    userid = DB.getUserID(conn, cur, useremail)
    userName = DB.getUserName(conn, cur, useremail)
    
    if request.method == 'POST':
        #search
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

        if request.form.get('savePp'):
            URLpp = request.form.get('URLpp')

            if DB.URLExist(conn, cur, userid):
                urlbg = DB.getURLPpBg(conn, cur,userid)[1]
                DB.updateURL(conn, cur,userid,URLpp,urlbg)
                return redirect(url_for('Views.accountPage'))
            else:
                print('addURL: ')
                DB.addURL(conn, cur, userid,URLpp,'')
                return redirect(url_for('Views.accountPage'))

        if request.form.get('saveChanges'):
            flash('Comming soon', category='Error')

    #image
    if DB.URLExist(conn, cur, userid):
        if DB.getURLPpBg(conn, cur,userid)[0] == '':
            image = 'https://cdn.iconscout.com/icon/free/png-256/account-avatar-profile-human-man-user-30448.png'
            imagelink = ''
        else:
            image =  DB.getURLPpBg(conn, cur,userid)[0]
            imagelink = DB.getURLPpBg(conn, cur,userid)[0]
    else:
        image = 'https://cdn.iconscout.com/icon/free/png-256/account-avatar-profile-human-man-user-30448.png'
        imagelink = ''
    return render_template('account.html', user = current_user, imagefile = image, linkAv = imagelink, email_box = useremail, username = userName, personal= (DB.getUserName(conn,cur,current_user.email)))


#Links
@Views.route('/links', methods=['GET','POST'])
@login_required
def linksPage():
    #DB
    conn, cur = DB.createConnCur()
    #DB.deleteTable(conn,cur)
    #DB.createTableLink(conn,cur)

    #Get userID
    useremail = current_user.email
    userid = DB.getUserID(conn, cur, useremail)

    #Get link items
    linkList = DB.getLink(conn, cur, userid)

    if request.method == 'POST':

        if request.form.get('addLink'):
            return redirect(url_for('Views.editLinkPage'))

        if request.form.get('deleteLink'):
            linkID = request.form.get('deleteLink')
            DB.DeleteLink(conn, cur, linkID)
            return redirect(url_for('Views.linksPage'))

        if request.form.get('editLink'):
            linkID = request.form.get('editLink')
            return redirect(url_for('Views.editLinkPage', linkID = linkID))

        if request.form.get('saveBg'):
            URLbg = request.form.get('URLbg')

            if DB.URLExist(conn, cur, userid):
                urlpp = DB.getURLPpBg(conn, cur,userid)[0]
                DB.updateURL(conn, cur,userid,urlpp,URLbg)
                return redirect(url_for('Views.linksPage'))
            else:
                print('addURL: ')
                DB.addURL(conn, cur, userid,'',URLbg)
                return redirect(url_for('Views.linksPage'))

        #search
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

    #image Background
    if DB.URLExist(conn, cur, userid):
        if DB.getURLPpBg(conn, cur,userid)[1] == '':
            imagebg = 'https://static.thenounproject.com/png/17840-200.png'
            imagelink = ''
        else:
            imagebg =  DB.getURLPpBg(conn, cur,userid)[1]
            imagelink = DB.getURLPpBg(conn, cur,userid)[1]
    else:
        imagebg = 'https://static.thenounproject.com/png/17840-200.png'
        imagelink = ''



    return render_template('links.html', user = current_user, linkAv = imagelink, imageBG = imagebg, linkList = linkList, personal= (DB.getUserName(conn,cur,current_user.email)))


#Edit Links
@Views.route('/editLink', methods=['GET','POST'])
@login_required
def editLinkPage():
    #DB
    conn, cur = DB.createConnCur()

    if request.method == 'POST':
        #search
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

        useremail = current_user.email
        userid = DB.getUserID(conn, cur, useremail)

        #Forms
        linktitle = request.form.get('linkTitle')
        linkitem = request.form.get('linkItem')
        linkcat = request.form.get('linkCat')
        linkicon = request.form.get('URLIcon')

        if request.form.get('saveChanges'):
            #check forms:
            if len(linktitle) < 5:
                flash('Link title is to short!', category='Error')
            elif len(linkitem ) < 5:
                flash('Link URL is to short!', category='Error')
            else:
                
                if linkicon == '':
                    linkicon = 'https://cliply.co/wp-content/uploads/2019/12/371903520_SOCIAL_ICONS_TRANSPARENT_400px.gif'

                try:
                    DB.linkItemExist(conn, cur, request.args['linkID'])
                    DB.updateLink(conn, cur, linkitem, linktitle, linkcat, linkicon, request.args['linkID'])
                    return redirect(url_for('Views.linksPage'))
                except:
                    DB.addLink(conn, cur, userid,linkitem, linktitle, linkcat, linkicon)
                    return redirect(url_for('Views.linksPage'))
        elif request.form.get('goBack'):

            return redirect(url_for('Views.linksPage'))




    try:
        if request.args['linkID']:
            linkItems = DB.getLinkItem(conn, cur, request.args['linkID'])
            linkListTitle = linkItems[3]
            linkListURL = linkItems[2]
            linkListCat = linkItems[4]
            linkListIcon = linkItems[5]
            linkListIconText = linkItems[5]
    except:
        #get information about current user
        linkListTitle = ''
        linkListURL = ''
        linkListCat = ''
        linkListIcon = 'https://cliply.co/wp-content/uploads/2019/12/371903520_SOCIAL_ICONS_TRANSPARENT_400px.gif'
        linkListIconText = ''

    return render_template('editLink.html', user = current_user, imageicon = linkListIcon, imageiconText = linkListIconText, linkTitle = linkListTitle, link = linkListURL, linkCat = linkListCat, personal= (DB.getUserName(conn,cur,current_user.email)))



#Personal page
@Views.route('/<username>', methods=['GET','POST'])
def personalPage(username):
    conn,cur = DB.createConnCur()

    if DB.checkUsername(conn, cur, username):
        userid = DB.getUsernameID(conn, cur, username)[0]
        

        #Get link items
        linkList = DB.getLink(conn, cur, userid)
        

        #image
        if DB.URLExist(conn,cur,userid):
            imageB = DB.getURLPpBg(conn, cur,userid)[1]
            imageP = DB.getURLPpBg(conn, cur,userid)[0]
        else:
            imageB = ''
            imageP = 'https://cdn.iconscout.com/icon/free/png-256/account-avatar-profile-human-man-user-30448.png'
        
        #logged in user
        if current_user.is_authenticated:
            currentUserID = DB.getUserID(conn, cur, current_user.email)
            followedList = DB.checkUserFollow(conn,cur,currentUserID)

            #check if user is following
            if userid in followedList: 
                userFollowing = True
            else:
                userFollowing = False


        else:
            userFollowing = False

        #Get following and followers count 
        followersCount = len(DB.UserFollowers(conn,cur,userid))
        followingCount = len(DB.UserFollowing(conn,cur,userid))


        

        if request.method == 'POST':
            if request.form.get('LinkButton'):
                linkUrl = request.form.get('LinkButton')
                return redirect(linkUrl)

            if request.form.get('follow'):
                if current_user.is_authenticated:
                    if currentUserID == userid:
                        flash('Cant follow yourself!', category='Error')
                    else:
                        DB.userFollow(conn,cur,currentUserID,userid)

                    return redirect(url_for('Views.personalPage', username = username) )
                else:
                    flash('Create an account first!', category='Error')
                    return redirect(url_for('UserAuth.signUpPage'))

            
            if request.form.get('unfollow'):
                DB.userUnFollow(conn,cur,currentUserID,userid)
                return redirect(url_for('Views.personalPage', username = username) )

            if request.form.get('notification'):
                flash('Comming soon!', category='Error')
                return redirect(url_for('Views.personalPage', username = username) )
            
            #search
            if request.form.get('searchBTN'):
                searchForm = request.form.get('searchItem')
                if searchForm == '':
                    searchForm = 'all'

                print('searchform: ', searchForm)
                
                return redirect(url_for('Views.searchPage', searchItem = searchForm) )

        
        return render_template('personal.html', user=current_user, imageBackground = imageB, imageProfile = imageP, userName =username, linklist= linkList, follow = userFollowing, following = followingCount, followers = followersCount)

    else:
        return redirect(url_for('homePage'))


#Search page
@Views.route('/searchPage/<searchItem>', methods=['GET','POST'])
def searchPage(searchItem):
    conn,cur = DB.createConnCur()
    NewUserLsit = []
    defaultAv = 'https://cdn.iconscout.com/icon/free/png-256/account-avatar-profile-human-man-user-30448.png'

    if searchItem == 'all':
        userList = DB.getAllUser(conn,cur)
        print('userList: ', userList)
    else:
        userList = DB.searchUser(conn,cur,searchItem)
        print('userList: ', userList)
        if len(userList)>0:
            pass
        else:
            flash('No search result', category='Error')

    if request.method == 'POST':
        if request.form.get('profile'):
            userName = request.form.get('profile')
            return redirect(url_for('Views.personalPage', username = userName) )

        #search bar
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'

            print('searchform: ', searchForm)
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )

    #image PP
    for i in userList:
        PPbgList = DB.getURLPpBg(conn,cur,i[1])
        if len(PPbgList) == 0:
            NewUserLsit.append(i + (defaultAv,))
        else:
            NewUserLsit.append(i + (PPbgList[0],))


    return render_template('search.html', user=current_user, userList = NewUserLsit)




@Views.route('/following/<usersearch>', methods=['GET','POST'])
def followingPage(usersearch):
    conn, cur = DB.createConnCur()
    currentUserID = DB.getUserID(conn, cur, current_user.email)
    UserList=[]
    NewUserLsit = []
    defaultAv = 'https://cdn.iconscout.com/icon/free/png-256/account-avatar-profile-human-man-user-30448.png'

    if usersearch == 'all':
        userList = DB.getAllUserFollowing(conn,cur,currentUserID)
        for i in userList:
            UserList.append(DB.FollowingUserInfo(conn,cur,i[0])[0])

    else:
        UserList = DB.searchUser(conn,cur,usersearch)
        print('userList: ',UserList)
        if len(UserList)>0:
            pass
        else:
            flash('No search result', category='Error')

    #image PP
    for i in UserList:
        PPbgList = DB.getURLPpBg(conn,cur,i[1])
        print('PPbgList: ', PPbgList)
        if len(PPbgList) == 0:
            NewUserLsit.append(i + (defaultAv,))
        else:
            NewUserLsit.append(i + (PPbgList[0],))

    if request.method == 'POST':
        if request.form.get('profileFollow'):
            userName = request.form.get('profileFollow')
            print('userName',userName)
            return redirect(url_for('Views.personalPage', username = userName) )

        if request.form.get('searchBTNFollow'):
            searchForm = request.form.get('searchFollow')
            if searchForm == '':
                searchForm = 'all'                
            
            return redirect(url_for('Views.followingPage', usersearch = searchForm) )
            
        #search bar
        if request.form.get('searchBTN'):
            searchForm = request.form.get('searchItem')
            if searchForm == '':
                searchForm = 'all'
            
            return redirect(url_for('Views.searchPage', searchItem = searchForm) )
            






    return render_template('following.html', user=current_user, userList = NewUserLsit, personal= (DB.getUserName(conn,cur,current_user.email)))