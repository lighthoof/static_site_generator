import datetime as dt

def log(log_text):
    timestamp = dt.datetime.now()
    date = dt.date.today()
    with open(f"{date}.log", "a") as log:
        log.write(f"{timestamp} : {log_text}\n")