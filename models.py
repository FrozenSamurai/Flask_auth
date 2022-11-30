import sqlite3 as sql
from datetime import datetime
from urllib import request
import bcrypt
import secrets
import string
from main import mail, app
import threading
from flask_mail import Message


def insert_user(username, email, password, mobile_no):
    con = sql.connect("database.db")
    current = datetime.now()
    cur = con.cursor()
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    try:
        cur.execute(
            "INSERT INTO users (username, email, password, created_time, mobile_no) VALUES (?,?,?,?,?)", (username, email, hashed, current, mobile_no))
        con.commit()
        con.close()
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(
            "SELECT id, username, email, mobile_no FROM users WHERE email = ?", (email,))
        data = cur.fetchall()
        con.close()
        # print(data)
        return True, "user created successfully", data
    except Exception as e:
        print(str(e))
        con.close()
        return False, str(e)


def login(email, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    try:
        cur.execute(f"SELECT password FROM users where email='{str(email)}'")
        hashed = cur.fetchall()
        con.close()
        if hashed:
            password = password.encode('utf-8')
            if bcrypt.checkpw(password, hashed[0][0]):
                con = sql.connect("database.db")
                cur = con.cursor()
                cur.execute(
                    "SELECT id, username, email, mobile_no FROM users WHERE email = ?", (email,))
                data = cur.fetchall()
                con.close()
                # print(data)
                return True, "Login Successful", data
            else:
                return False, "Login Failed, Incorrect password"
        else:
            return False, "Login Failed, Incorrect Email-id"
    except Exception as e:
        print(str(e))
        con.close()
        return False, str(e)


def mailing(email, newpassword):
    with app.app_context():
        msg = Message(
            f'Your password has been Reset Successfully', recipients=[email])
        msg.body = f'Your new password is : {newpassword}'
        mail.send(msg)


def forget_password(email, username):
    con = sql.connect("database.db")
    cur = con.cursor()
    # try:
    cur.execute(f"SELECT email FROM users where email='{str(email)}'")
    userEmail = cur.fetchall()
    con.close()
    if userEmail:
        res = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                      for i in range(8))
        password = str(res).encode('utf-8')
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute(
            f"""UPDATE users SET password=? WHERE email=? AND username=?""", (hashed, email, username))
        con.commit()
        con.close()
        x = threading.Thread(target=mailing, args=(
            email, str(res),), daemon=True)
        x.start()
        # Send new password as email to user OR as SMS to user.
        # There are different methods for forget password and reset, I used emailing new password method.

        return True, f"Password reset successfully, please check your mail inbox."
    else:
        return False, "Invalid Information"
    # except Exception as e:
    #     print(str(e))
    #     con.close()
    #     return False, str(e)
