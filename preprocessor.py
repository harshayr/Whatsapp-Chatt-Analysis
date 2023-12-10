import re
import pandas as pd



def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    msg = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({"msg": msg, "msg_date": dates})
    df["msg_date"] = pd.to_datetime(df["msg_date"], format="%m/%d/%y, %H:%M - ")
    user = []
    mssage = []
    for msg in df["msg"]:
        entry = re.split("([\w\W]+?):\s", msg)
        if entry[1:]:
            user.append(entry[1])
            mssage.append(entry[2])
        else:
            user.append("grp_notification")
            mssage.append(entry[0])
    df["user"] = user
    df["msg"] = mssage
    df["year"] = df["msg_date"].dt.year
    df["month"] = df["msg_date"].dt.month_name()
    df["day"] = df["msg_date"].dt.day
    df["hour"] = df["msg_date"].dt.hour
    df["minute"] = df["msg_date"].dt.minute
    return df
