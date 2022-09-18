#DATABASEHELPER
#import#####################################################################
import sqlite3
import pymssql
from itertools import *

#functions##################################################################
def createConnCur():
    #Create connection with the database
    conn = pymssql.connect('10.0.0.8','CSREMOTE','Test123','linkd')
    #conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.0.0.8;PORT=1433;DATABASE=linkd;UID=CSREMOTE;PWD=Test123')

    #print('Connected to database')
    #Create a cursor object
    cur= conn.cursor()
    #print('Cursor created')


    return conn,cur

#functions##################################################################
def createConnCurSQL():
    #Create connection with the database
    conn = sqlite3.connect('WebAppdb.db')

    #Create a cursor object
    cur= conn.cursor()

    return conn,cur


#Methode to create table
def createTable(conn,cur):
    try:
        qr = """CREATE TABLE links(
        linkid INTEGER IDENTITY(1,1) PRIMARY KEY,
        userid INTEGER,
        linkitem nvarchar(MAX),
        linktitle nvarchar(MAX),
        category nvarchar(MAX),
        );
        """
        
        cur.execute(qr)
        conn.commit()
        print('Table created successfully')
    except:
        print('Error in operation: Creating Table')
        conn.rollback()

#Delete table
def deleteTable(conn, cur):
    try:
        qr = """DROP TABLE links;
        """
        cur.execute(qr)
        conn.commit()
        print('Table deleted successfully')
    except:
        print('Error in operation')
        conn.rollback()


#Specif table: User########################################################
#Delete a record in the table
def crudDeleteUser(conn,cur):
    try:
        qrDelete = """DELETE FROM users WHERE userid=3
        ;
        """
        cur.execute(qrDelete)
        conn.commit()
        print('Record Deleted successfully')
    except:
        print('Error in operation CrudDeleteUser')
        conn.rollback()


#Select User
def selectUser(conn,cur,email):
    try:
        qr = """SELECT * FROM users WHERE email LIKE %s
        ;
        """
        qrtuple = (email,)
        cur.execute(qr,qrtuple)

        user = cur.fetchone()
        try:
            if len(user) > 0:
                return user
        except:
            return None

    except:
        print('Error in operation: SelectUser')
        conn.rollback()


#Get User ID
def getUserID(conn,cur,email):
    try:
        qr = """SELECT userid FROM users WHERE email LIKE %s
        ;
        """
        qrtuple = (email,)
        cur.execute(qr,qrtuple)
        user_id = cur.fetchone()

        if user_id:
            return user_id[0]
        else:
            return True
    except:
        print('Error in operation: GetUserEmail')
        conn.rollback()

#Get Username with email
def getUserName(conn,cur,email):
    try:
        print('GetID email: ', email)
        qr = """SELECT username FROM users WHERE email LIKE %s
        ;
        """
        qrtuple = (email,)
        cur.execute(qr,qrtuple)
        user_id = cur.fetchone()

        if user_id:
            return user_id[0]
        else:
            return True
    except:
        print('Error in operation: GetUserEmail')
        conn.rollback()


#Create a record in the table
def CreateUser(conn, cur, email, username, password):
    try:
        qr = """INSERT INTO users VALUES(%s,%s,%s)
        ;
        """
        qrtuple = (email, username, password,)
        cur.execute(qr,qrtuple)
        conn.commit()
        print('Record added successfully')
    except:
        print('Error in operation CrudCreateUser')
        conn.rollback()


#Get User email
def getUserEmail(conn,cur,email):
    try:
        qr = """SELECT email FROM users WHERE email LIKE %s
        ;
        """
        qrtuple = (email,)
        cur.execute(qr,qrtuple)

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))
        #print('GetUsermail fetch: ', listedfetch)

        return listedfetch
    except:
        print('Error in operation: GetUserEmail')
        conn.rollback()

#Get User Username
def getUsername(conn,cur,username):
    try:
        qr = """SELECT username FROM users WHERE username LIKE %s
        ;
        """
        qrtuple = (username,)
        cur.execute(qr,qrtuple)

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))
        #print('listedfetchusername: ', listedfetch)

        return listedfetch
    except:
        print('Error in operation: GetUsername')
        conn.rollback()


#Get User email
def getUserPassword(conn,cur,email):
    try:
        qr = """SELECT password FROM users WHERE email LIKE %s
        ;
        """
        qrtuple = (email,)
        cur.execute(qr,qrtuple)

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))
        #print('listedfetchPass: ', listedfetch)

        return listedfetch
    except:
        print('Error in operation: GetUserPassword')
        conn.rollback()

#Get User Username
def checkUsername(conn,cur,username):
    try:
        qr = """SELECT username FROM users WHERE username LIKE %s
        ;
        """
        qrtuple = (username,)
        cur.execute(qr,qrtuple)

        userName= cur.fetchall()
        if len(userName) >0:
            return True
        else:
            return False
    except:
        print('Error in operation: check Username')
        conn.rollback()

#Get User Username
def getUsernameID(conn,cur,username):
    try:
        qr = """SELECT userid FROM users WHERE username LIKE %s
        ;
        """
        qrtuple = (username,)
        cur.execute(qr,qrtuple)

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))

        return listedfetch
    except:
        print('Error in operation: GetUsername')
        conn.rollback()

#Get User Username
def getAllUser(conn,cur):
    try:
        qr = """SELECT username,userid FROM users ORDER BY username DESC
        ;
        """
        cur.execute(qr,)

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))
        print('GetAllUser: ', listedfetch)

        return fetch
    except:
        print('Error in operation: GetAllUser')
        conn.rollback()

#Specif table: Link########################################################
#Methode to create linktable
def createTableLink(conn,cur):
    try:
        qr = """CREATE TABLE links(
        linkid INTEGER IDENTITY(1,1) PRIMARY KEY,
        userid INTEGER,
        linkitem nvarchar(MAX),
        linktitle nvarchar(MAX),
        category nvarchar(MAX),
        linkicon nvarchar(MAX)
        );
        """
        
        cur.execute(qr)
        conn.commit()
        print('Table created successfully')
    except:
        print('Error in operation: Creating Table')
        conn.rollback()

#Create a record in the table
def addLink(conn, cur, userid, linkitem, linktitle,linkcat, linkicon):
    try:
        qr = """INSERT INTO links VALUES(%s,%s,%s,%s,%s)
        ;
        """
        qrtuple = (userid, linkitem, linktitle, linkcat, linkicon)
        cur.execute(qr,qrtuple)
        conn.commit()
        print('Record added successfully')
    except:
        print('Error in operation: addLink')
        conn.rollback()


#Update a record in the linktable
def updateLink(conn, cur, linkitem, linktitle, linkcat, linkicon, linkID):
    try:
        qr = """UPDATE links SET 
        linkitem=%s,
        linktitle=%s,
        category=%s,
        linkicon=%s
        WHERE linkid LIKE %s
        ;
        """
        qrtuple = (linkitem, linktitle, linkcat, linkicon,linkID)
        cur.execute(qr,qrtuple)
        conn.commit()
        print('Record Updated Successfully')
    except:
        print('Error in operation: UpdateLink')
        conn.rollback()


#Delete a record in the link table
def DeleteLink(conn,cur, linkid):
    try:
        qrDelete = """DELETE FROM links WHERE linkid LIKE %s
        ;
        """
        qrtuple = (linkid,)
        cur.execute(qrDelete, qrtuple)
        conn.commit()
        print('Link Deleted successfully')
    except:
        print('Error in operation DeleteLink')
        conn.rollback()


#Select link order by desc
def getLink(conn,cur,userid):
    try:
        qr = """SELECT * FROM links WHERE userid LIKE %s ORDER BY linkid
        ;
        """
        qrtuple = (userid,)
        cur.execute(qr,qrtuple)

        link = cur.fetchall()
        

        return link
    except:
        print('Error in operation: GetUserlink')
        conn.rollback()

#Select one link order by desc
def getLinkItem(conn,cur,linkid):
    try:
        qr = """SELECT * FROM links WHERE linkid LIKE %s
        ;
        """
        qrtuple = (linkid,)
        cur.execute(qr,qrtuple)

        link = cur.fetchall()
        linkList = list(chain(*link))
        print('linkItem : ', linkList)

        return linkList
    except:
        print('Error in operation: GetLinkItem')
        conn.rollback()

#Check if  link item exist
def linkItemExist(db, cur, linkid):
    try:
        qr = """SELECT * FROM links WHERE linkid LIKE %s
        ;
        """
        qrtuple = (linkid,)
        cur.execute(qr,qrtuple)
        linkItem= cur.fetchall()
        if len(linkItem) >0:
            return True
        else:
            return False
    except:
        print('Error in operation Check if linkItem exist')
        db.rollback()

#Follow########################################################
#Methode to create  Followtable
def createTableFollow(conn,cur):
    try:
        qr = """CREATE TABLE follow(
        followerid INTEGER,
        followedid INTEGER
        );
        """
        
        cur.execute(qr)
        conn.commit()
        print('Table created successfully')
    except:
        print('Error in operation: Creating Table')
        conn.rollback()

#Create a record in the table
def userFollow(conn, cur, followerid, followedid):
    try:
        qr = """INSERT INTO follow VALUES(%s,%s)
        ;
        """
        qrtuple = (followerid, followedid,)
        cur.execute(qr,qrtuple)
        conn.commit()
        print('Record added successfully')
    except:
        print('Error in operation userFollow')
        conn.rollback()

#Create a record in the table
def userUnFollow(conn, cur, followerid, followedid):
    try:
        qr = """DELETE FROM follow WHERE followerid=%s AND followedid=%s
        ;
        """
        qrtuple = (followerid, followedid,)
        cur.execute(qr,qrtuple)
        conn.commit()
        print('Record deleted successfully')
    except:
        print('Error in operation userUnFollow')
        conn.rollback()

#check if user follow
def checkUserFollow(conn,cur,followerid):
    try:
        qr = """SELECT followedid FROM follow WHERE followerid LIKE %s
        ;
        """
        qrtuple = (followerid,)
        cur.execute(qr,qrtuple)

        followedidT= cur.fetchall()
        followedidList = list(chain(*followedidT))
        return followedidList
    except:
        print('Error in operation: checkUserFollow')
        conn.rollback()

#check if user following
def UserFollowing(conn,cur,followerid):
    try:
        qr = """SELECT followerid FROM follow WHERE followerid LIKE %s
        ;
        """
        qrtuple = (followerid,)
        cur.execute(qr,qrtuple)

        followedidT= cur.fetchall()
        followedidList = list(chain(*followedidT))
        return followedidList
    except:
        print('Error in operation: UserFollowing')
        conn.rollback()

#check if user follower
def UserFollowers(conn,cur,followedid):
    try:
        qr = """SELECT followedid FROM follow WHERE followedid LIKE %s
        ;
        """
        qrtuple = (followedid,)
        cur.execute(qr,qrtuple)

        followedidT= cur.fetchall()
        followedidList = list(chain(*followedidT))
        return followedidList
    except:
        print('Error in operation: UserFollowers')
        conn.rollback()


#Search########################################################
#Search User by Username
def searchUser(conn,cur, searchItem):
    try:

        cur.execute("""SELECT username,userid FROM users WHERE username LIKE %s ORDER by username DESC
        ;
        """,str(searchItem + '%'))

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))
        print('searchUser: ', listedfetch)

        return fetch
    except:
        print('Error in operation: GetAllUser')
        conn.rollback()

#Search Following########################################################
#Search User by Username
def FollowingUserInfo(conn,cur, userid):
    try:
        qr = """SELECT username,userid FROM users WHERE userid = %s ORDER by username DESC
        ;
        """
        qrtuple = (userid,)
        cur.execute(qr, qrtuple)

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))
        #print('FollowingUserInfo: ', listedfetch)

        return fetch
    except:
        print('Error in operation: FollowingUserInfo')
        conn.rollback()

#Get User Username
def getAllUserFollowing(conn,cur,userid):
    try:
        qr = """SELECT followedid FROM follow WHERE followerid=%s
        ;
        """
        qrtuple = (userid,)
        cur.execute(qr,qrtuple)

        fetch = cur.fetchall()
        listedfetch = list(chain(*fetch))
        #print('getAllUserFollowing: ', listedfetch)

        return fetch
    except:
        print('Error in operation: getAllUserFollowing')
        conn.rollback()

#Picture########################################################
#Methode to create Picture table
def createTablePicture(conn,cur):
    try:
        qr = """CREATE TABLE picture(
        userid INTEGER,
        urlpp nvarchar(MAX),
        urlbg nvarchar(MAX)
        );
        """
        
        cur.execute(qr)
        conn.commit()
        print('Table created successfully')
    except:
        print('Error in operation: Creating Table')
        conn.rollback()

#Check if  URLpp  exist
def URLExist(db, cur, userid):
    try:
        qr = """SELECT urlpp,urlbg FROM picture WHERE userid LIKE %s
        ;
        """
        qrtuple = (userid,)
        cur.execute(qr,qrtuple)
        urlItem= cur.fetchall()
        if len(urlItem) >0:
            return True
        else:
            return False
    except:
        print('Error in operation: URLExist')
        db.rollback()

#Check if  URLpp  exist
def getURLPpBg(db, cur, userid):
    try:
        qr = """SELECT urlpp,urlbg FROM picture WHERE userid LIKE %s
        ;
        """
        qrtuple = (userid,)
        cur.execute(qr,qrtuple)
        urlItem= cur.fetchall()
        urlItemList = list(chain(*urlItem))
        return urlItemList
    except:
        print('Error in operation: getURLPpBg')
        db.rollback()


#Create a record in the table
def addURL(conn, cur, userid, URLpp, URLbg):
    try:
        qr = """INSERT INTO picture VALUES(%s,%s,%s)
        ;
        """
        qrtuple = (userid, URLpp, URLbg)
        cur.execute(qr,qrtuple)
        conn.commit()
        print('Record added successfully')
    except:
        print('Error in operation: addURL')
        conn.rollback()


#Update a record in the linktable
def updateURL(conn, cur, userid, URLpp, URLbg):
    try:
        qr = """UPDATE picture SET 
        urlpp=%s,
        urlbg=%s WHERE userid = %s
        ;
        """
        qrtuple = (URLpp, URLbg, userid)
        print('URLpp: ', URLpp)
        cur.execute(qr,qrtuple)
        conn.commit()
        print('Record Updated Successfully')
    except:
        print('Error in operation: updateURL')
        conn.rollback()