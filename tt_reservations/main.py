import re
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from tt_reservations.book_times import book_times

DATETIME_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$"
origins = [
    "http://80.187.127.138",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/reserve_time", status_code=status.HTTP_201_CREATED)
def reserve_time(
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


def main() -> None:
    pass


if __name__ == "__main__":
    main()
