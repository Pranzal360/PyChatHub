from datetime import datetime, timedelta

def set_expirey():
    current_time = datetime.now()
    print(current_time)
    expirey_time = current_time + timedelta(hours=1)
    expirey_time_str = expirey_time.strftime("%H%M%S")
    return int(expirey_time_str)

