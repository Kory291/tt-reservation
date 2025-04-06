import re
import time
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from tt_reservations.auth.methods import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    load_users_from_file,
    oauth2_scheme,
)
from tt_reservations.auth.models import Token, User
from tt_reservations.auth.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from tt_reservations.book_times import book_times, get_eligable_times

DATETIME_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    user = authenticate_user(
        load_users_from_file(), form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        not_after=time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@app.get("/available_timeslots", status_code=status.HTTP_200_OK)
def get_available_timeslots(
    token: Annotated[str, Depends(oauth2_scheme)],
):
    timeslots = get_eligable_times()
    return {"available_timeslots": timeslots}


def main() -> None:
    pass


if __name__ == "__main__":
    main()
