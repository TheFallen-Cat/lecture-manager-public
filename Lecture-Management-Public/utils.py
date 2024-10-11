from datetime import timedelta, timezone, datetime


# * Getting the current time
def get_current_time() -> str:
    ist_offset = timezone(timedelta(hours=5, minutes=30))

    utc_now = datetime.now(timezone.utc)

    indian_time = utc_now.astimezone(ist_offset)

    return indian_time.strftime("%d %b %H:%M %p")


