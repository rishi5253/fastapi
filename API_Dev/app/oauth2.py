from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schema,database,model
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

#secrete _key
#alogo
#expiation time - this defin thetime for how the user will be loged in as user cannot be login for whole time 
'''
How does HS256 work?
HS256 uses a secret key to create and verify the JWT signature.
1. Header: Specifies the algorithm as HS256.
2. Payload: Contains data such as the user's ID or role.
3. Signature: Uses the secret key and SHA-256 hashing to create a signature.                                                                                                                      
'''
SECRATE_KEY = "09d25e04h94dwq9dphn48rph48crh843rcmru93urr64738ntrc47tn78o4m5tlslt94yt5p2lsd"
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTE  = 30 


def create_access_token(data : dict):
    to_encode = data.copy()
   
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRATE_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token,SECRATE_KEY,algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schema.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception

    return token_data
## this will take the token automatically and verify the token 

def get_current_user(token : str = Depends(oauth2_schema),db : Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials",headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception) 
    user = db.query(model.Users).filter(model.Users.id== token.id).first()
    
    return user

