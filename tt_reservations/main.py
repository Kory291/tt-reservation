import os
import re
from datetime import datetime, timedelta

from playwright.sync_api import Playwright, sync_playwright, Locator
from tt_reservations.exceptions import TimeSlotNotAvailableError

STANDARD_YEAR = 1900
STANDARD_MONTH = 1
STANDARD_DAY = 1

def run(playwright: Playwright) -> None:
    firefox = playwright.firefox
    browser = firefox.launch(headless=False)
    page = browser.new_page()
    page.goto(os.environ.get("TT_PAGE"))
    anchors = page.locator("a")
    deny_button = anchors.filter(has_text="Accept all")
    deny_button.click()
    list_of_timeslots = page.locator("a").filter(
        has_text=re.compile(r".*.\d{2}:\d{2}\s?-\s?\d{2}:\d{2}.*")
    )
    selectable_timeslots = [
        datetime.strptime(re.search(r"\d{2}:\d{2}", timeslot).group(), "%H:%M")
        for timeslot in list_of_timeslots.all_inner_texts()
    ]
    desired_timeslots = select_times(
        datetime(STANDARD_YEAR, STANDARD_MONTH, STANDARD_DAY, 18, 0),
        timedelta(hours=2)
    )
    reserve_time(desired_timeslots[0] - timedelta(hours=6), list_of_timeslots)
    for desired_timeslot in desired_timeslots:
        try:
            reserve_time(desired_timeslot, list_of_timeslots)
        except TimeSlotNotAvailableError as e:
            print(e)
    browser.close()

def reserve_time(desired_timeslot: datetime, anchors: Locator) -> None:
    if not isinstance(desired_timeslot, datetime):
        raise TypeError("desired_timeslot must be a datetime object")
    if not isinstance(anchors, Locator):
        raise TypeError("anchors must be a Locator object")
    
    anchor = anchors.filter(has_text=desired_timeslot.strftime("%H:%M"))
    if anchor.count() == 0:
        raise TimeSlotNotAvailableError(f"Time slot {desired_timeslot.strftime('%H:%M')} is not available")
    anchor.click()


def select_times(start_time: datetime, time_delta: timedelta=None, end_time: datetime=None) -> list[datetime]:
    # some preleminary checks
    if not isinstance(start_time, datetime):
        raise TypeError("start_time must be a datetime object")
    if time_delta and not isinstance(time_delta, timedelta):
        raise TypeError("time_delta must be a timedelta object")
    if end_time and not isinstance(end_time, datetime):
        raise TypeError("end_time must be a datetime object")
    if time_delta and end_time:
        raise ValueError("time_delta and end_time cannot be used together")
    
    # check reasonable times -> regard training times (not before 5 pm and after 10 pm)
    if start_time.hour < 17:
        raise ValueError("start_time must be after 5 pm")
    if start_time.hour > 22:
        raise ValueError("start_time must be before 10 pm")
    
    if time_delta:
        end_time = start_time + time_delta
    
    # fix timeslot to previous half hour
    if start_time.minute < 30 and start_time.minute > 0:
        start_time = start_time.replace(minute=0)
    if start_time.minute == 0:
        pass
    else:
        start_time.replace(minute=30)
    
    # fix end_time to next half hour
    if end_time.minute < 30 and end_time.minute > 0:
        end_time = end_time.replace(minute=30)
    elif end_time.minute == 0:
        pass
    else:
        end_time = end_time.replace(minute=0) + timedelta(hours=1)
    
    # create list of timeslots
    return [start_time + timedelta(minutes=30*i) for i in range((end_time - start_time).seconds // (60*30))]
    


def main() -> None:
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
