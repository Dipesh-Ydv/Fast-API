from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import create_access_token, verify_token
from models import UserInDB
from utils import verify_password, get_user

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

@app.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = get_user(form_data.username)
    if not user_dict: 
        raise HTTPException(status_code=400, detail= "Invalid Username")
    if not verify_password(form_data.password, user_dict['hashed_password']):
        raise HTTPException(status_code=400, detail= 'Invaild Password')
    
    access_token = create_access_token(data= {'sub': form_data.username})
    return {'access_token': access_token, 'token_type': 'bearer'}
    
@app.get('/user')
def read_user(token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    return {'username': username}
