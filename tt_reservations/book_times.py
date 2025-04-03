import os
import random
import re
import time
from datetime import datetime, timedelta
from typing import Any

from playwright.sync_api import Locator, Page, Playwright, expect, sync_playwright

from tt_reservations.exceptions import TimeSlotNotAvailableError

STANDARD_YEAR = 1900
STANDARD_MONTH = 1
STANDARD_DAY = 1


def get_eligable_timeslots(page: Any):
    anchors = page.locator("a")


def run(
    playwright: Playwright,
    start_time: datetime,
    end_time: datetime = None,
    time_delta: timedelta = None,
) -> None:
    firefox = playwright.firefox
    browser = firefox.launch()
    page = browser.new_page()
    page.goto(f"{os.getenv('TT_PAGE')}{start_time.strftime('%d.%m.%Y')}")
    anchors = page.locator("a")
    deny_button = anchors.filter(has_text="Accept all")
    deny_button.click()

    desired_timeslots = select_times(
        start_time=start_time, time_delta=time_delta, end_time=end_time
    )
    # TODO: check if chosen timeslot are present for booking
    for desired_timeslot in desired_timeslots:
        try:
            reserve_time(desired_timeslot, page)
        except TimeSlotNotAvailableError as e:
            print(e)
    browser.close()


def reserve_time(desired_timeslot: datetime, page: Page) -> None:
    if not isinstance(desired_timeslot, datetime):
        raise TypeError("desired_timeslot must be a datetime object")
    if not isinstance(page, Page):
        raise TypeError("page must be a Page object")

    list_of_timeslots = page.locator("a").filter(
        has_text=re.compile(r".*.\d{2}:\d{2}\s?-\s?\d{2}:\d{2}.*")
    )
    selectable_timeslots = [
        datetime.strptime(re.search(r"\d{2}:\d{2}", timeslot).group(), "%H:%M")
        for timeslot in list_of_timeslots.all_inner_texts()
    ]
    form = page.locator("form").filter(has_text=re.compile("Vorname"))
    if not form.count() == 1:
        raise ValueError("Could not find singular form. Please excuse")
    try:
        chose_time_slot(desired_timeslot, list_of_timeslots)
        fill_form(form)
    except Exception as e:
        print(e)


def chose_time_slot(desired_timeslot: datetime, anchors: Locator) -> None:
    if not isinstance(desired_timeslot, datetime):
        raise TypeError("desired_timeslot must be a datetime object")
    if not isinstance(anchors, Locator):
        raise TypeError("anchors must be a Locator object")

    time_string = desired_timeslot.strftime("%H:%M")
    anchor = anchors.filter(has_text=re.compile(rf"{time_string}\s?-"))
    if anchor.count() == 0:
        raise TimeSlotNotAvailableError(
            f"Time slot {desired_timeslot.strftime('%H:%M')} is not available"
        )
    anchor.click()


def fill_form(
    form: Locator,
    first_name: str = None,
    last_name: str = None,
    telephone_number: str = None,
    email: str = None,
):
    if not first_name:
        first_name = os.environ.get("FIRST_NAME")
    if not last_name:
        last_name = os.environ.get("LAST_NAME")
    if not telephone_number:
        telephone_number = os.environ.get("TELEPHONE_NUMBER")
    if not email:
        email = os.environ.get("EMAIL")

    fields = form.locator("label")
    first_name_field = form.locator('input[name="prename1"]')
    last_name_field = form.locator('input[name="familyname1"]')
    telephone_number_field = form.locator('input[name="phone"]')
    email_field = form.locator('input[name="email"]')
    publish_data_checkbox = form.locator('input[name="publishDataCheckbox"]')
    accept_button = form.get_by_role("button").filter(has_text="Buchung vornehmen")

    first_name_field.fill(first_name)
    last_name_field.fill(last_name)
    telephone_number_field.fill(telephone_number)
    email_field.fill(email)
    publish_data_checkbox.check()
    accept_button.click()
    time.sleep(random.randint(1, 11) / 10)


def select_times(
    start_time: datetime, time_delta: timedelta = None, end_time: datetime = None
) -> list[datetime]:
    # some preleminary checks
    print(start_time, end_time, time_delta)
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
    elif start_time.minute > 30:
        start_time.replace(minute=30)

    # fix end_time to next half hour
    if end_time.minute < 30 and end_time.minute > 0:
        end_time = end_time.replace(minute=30)
    elif end_time.minute > 30:
        end_time = end_time.replace(minute=0) + timedelta(hours=1)

    # create list of timeslots
    return [
        start_time + timedelta(minutes=30 * i)
        for i in range((end_time - start_time).seconds // (60 * 30))
    ]


def book_times(
    start_time: datetime, end_time: datetime = None, time_delta: timedelta = None
):
    with sync_playwright() as playwright:
        run(playwright, start_time, end_time, time_delta)
