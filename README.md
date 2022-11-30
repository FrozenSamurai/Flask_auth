# Description

This is an easy and fast way to create _APIs_ for Authentication (Signup, Signin, Forget Password) using `Flask`

## Steps to initialize the app

1. Clone the repository
2. Install the requirements from `requirements.txt` file
3. Run the app - `python3 main.py`

## Components of project

    1. main.py - This is the main file which contains the app and all the routes.
    2. models.py - This file contains the models for the database.
    3. database.db - This is an SQLITE database file.

## Testing APIs using POSTMAN

#### Endpoint: /api/v1/usermng/signup

![image](<./readme-assets/Screenshot%20(1).png>)

###### Storing the `username`, `email`, `password`. Password is stored using encryption including `salts` and `hashing` technique. Hashing is irreversible therefore, the password once stored cannot be decrypted again.

#### Endpoint: /api/v1/usermng/signin

![image](<./readme-assets/Screenshot%20(2).png>)

###### Checking the `email` and `password` from the database. If the `email` and `password` matches, then the user is logged in. Else the `error message` is returned.

#### Endpoint: /api/v1/usermng/forgetPassword

![image](<./readme-assets/Screenshot%20(3).png>)

###### There are different techniques for forget password or reset password like token using `JWT`(JSON Web Token) or `OTP`(One Time Password). I used a simple way to identify the user, by asking the user about the data we have like its username or DoB for authorization, then email user the new password.

#### Endpoint: /api/v1/usermng/resetPassword

![image](<./readme-assets/Screenshot%20(4).png>)

###### Checking the `email` and `password` from the database. If the `email` and `password` matches, then setting the `new_password`. Else the `error message` is returned.

## LICENSE

<a href="LICENSE">MIT</a>© <a href="https://www.github.com/FrozenSamurai">Author: Raj Vijay Jadhav</a>
