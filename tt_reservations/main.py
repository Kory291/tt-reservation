import re
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from tt_reservations.book_times import book_times

DATETIME_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
origins = ["*"]


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
        "hashed_password": "somehash1",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "hashed_password": "somehash2",
        "disabled": True,
    },
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_hash_password(password: str):
    return "somehash" + password


def fake_decode_token(token):
    return get_user(fake_users_db, token)


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
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW_Authenticate": "Bearer"},
        )
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
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}


def main() -> None:
    pass


if __name__ == "__main__":
    main()
