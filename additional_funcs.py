from datetime import datetime, timedelta

def set_expirey():
    current_time = datetime.now()
    expirey_time = current_time + timedelta(hours=1)
    expirey_time_str = expirey_time.strftime("%H%M%S%f")
    return int(expirey_time_str)

