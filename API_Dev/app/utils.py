#  This for hashing the password 
# what we are doing hewre is we are saving the password as hased in the db . then we the user login in at that time it put his password . which we take and then we hash
#it and compare it with thhased passwordd saved in the db and the check  if it maches and then sign in the user 
from passlib.context import CryptContext 

pwd_context = CryptContext(schemes=['bcrypt'],deprecated ="auto")



def hash(password : str):
    return pwd_context.hash(password)



def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)