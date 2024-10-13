import re
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import jwt
import bcrypt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from tt_reservations.book_times import book_times

DATETIME_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
origins = ["*"]

# openssl rand -hex 32
SECRET_KEY = "5ad07eb704bb3ae2d992480009e07be0e98ce8a85539b0b07db31ff52c145205"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "hashed_password": b'$2b$12$34h5Ks3z3agxDWY51tQe4ulX9/RBzMOIWQ5CJsBZB85hAs9fBumVa',
        "disabled": False,
    },
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password

def authenticate_user(fake_db, username: str, password: str) -> User | Literal[False]:
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if not user:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


@app.post("/reserve_time", status_code=status.HTTP_201_CREATED)
def reserve_time(
    token: Annotated[str, Depends(oauth2_scheme)],
    start_time: Annotated[
        str, Query(title="time you want to start practice at", pattern=DATETIME_PATTERN)
    ] = None,
    end_time: Annotated[
        str | None,
        Query(title="time you want to end practice at", pattern=DATETIME_PATTERN),
    ] = None,
    time_delta: Annotated[
        str | None,
        Query(
            title="duration after which you would like to end practice",
            pattern=r"^(\d\.?\d?H|\d+M)$",
        ),
    ] = None,
) -> dict:
    start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    if end_time:
        end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
    if time_delta:
        if re.match(r"^\d+M$", time_delta):
            time_delta = timedelta(minutes=int(time_delta[:-1]))
        elif re.match(r"\d\.?\d?H", time_delta):
            time_delta = timedelta(hours=float(time_delta[:-1]))
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="bad format for time_delta",
            )
    if end_time and time_delta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_time and time_delta cannot be provided at the same time",
        )
    try:
        book_times(start_time=start_time, end_time=end_time, time_delta=time_delta)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return {"message": "time reserved"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password", 
            headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


def main() -> None:
    pass


if __name__ == "__main__":
    main()
