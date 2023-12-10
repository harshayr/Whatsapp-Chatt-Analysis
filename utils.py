from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

f = open("stop_hinglish.txt","r")
stopwords = f.read()
stopwords = stopwords.split()


def monthly_tiime(selected_user,df):
    if selected_user == "Overall":
        df["month_num"] = df["msg_date"].dt.month
        x = df.groupby(["year", "month_num", "month"]).count()["msg"].reset_index()
        timeline = []
        for i in range(x.shape[0]):
            timeline.append(x["month"][i] + "-" + str(x["year"][i]))
        x["timeline"] = timeline
    else:
        df["month_num"] = df["msg_date"].dt.month
        df = df[df["user"]==selected_user]
        x = df.groupby(["year", "month_num", "month"]).count()["msg"].reset_index()
        timeline = []
        for i in range(x.shape[0]):
            timeline.append(x["month"][i] + "-" + str(x["year"][i]))
        x["timeline"] = timeline

    return x

def daily_timeline(selected_user,df):
    if selected_user == "Overall":
        df["date"] = df["msg_date"].dt.date
        daily_msg = df.groupby(["month", "date"]).count()["msg"].reset_index()
        month = list(daily_msg["month"].unique())
    else:
        df["date"] = df["msg_date"].dt.date
        df = df[df["user"] == selected_user]
        daily_msg = df.groupby(["month", "date"]).count()["msg"].reset_index()
        month = list(daily_msg["month"].unique())
    return daily_msg, month

def weekday_activity(selected_user,df):
    if selected_user =="Overall":
        df["day_name"] = df["msg_date"].dt.day_name()
        daywise_df = df["day_name"].value_counts().reset_index()
    else:
        df["day_name"] = df["msg_date"].dt.day_name()
        df = df[df["user"]==selected_user]
        daywise_df = df["day_name"].value_counts().reset_index()
    return daywise_df

def month_activity(selected_user,df):
    if selected_user =="Overall":
        monthwise_df = df["month"].value_counts().reset_index()
    else:
        df = df[df["user"]==selected_user]
        monthwise_df = df["month"].value_counts().reset_index()
    return monthwise_df

def time_activity(selected_user,df):
    if selected_user == "Overall":
        period = []
        for hour in df["hour"]:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))
        df["period"] = period
        pivot_table = df.pivot_table(index="day_name", columns="period", values="msg", aggfunc="count").fillna(0)
    else:
        df = df[df["user"] == selected_user]
        period = []
        for hour in df["hour"]:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))
        df["period"] = period
        pivot_table = df.pivot_table(index="day_name", columns="period", values="msg", aggfunc="count").fillna(0)
    return pivot_table



def emojy(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"]==selected_user]
    emojis = []
    for msg in df["msg"]:
        emojis.extend([c for c in msg if c in emoji.EMOJI_DATA])
    emojis_df = pd.DataFrame(Counter(emojis).most_common())
    return emojis_df


def media_count(selected_user,df):
    if selected_user == "Overall":
        df = df[df["msg"] == "<Media omitted>\n"]
        mediafile_count = df.shape[0]
        return mediafile_count
    else:
        x = df[df["user"] == selected_user]
        mediafile_count = x[x["msg"] == "<Media omitted>\n"].shape[0]
        return mediafile_count

def most_busy(df):
    x = df["user"].value_counts().head()
    new_df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"user": "name", "count": "percentage"})

    return x,new_df

def create_wordcloud(selected_user,df):
    if selected_user =="Overall":
        wc = WordCloud(width=500,height=500,min_font_size=10,background_color="white")
        df_wc = wc.generate(df["msg"].str.cat(sep = " "))

    else:
        df = df[df["user"]==selected_user]
        wc = WordCloud(width=500, height=500, min_font_size=10, background_color="white")
        df_wc = wc.generate(df["msg"].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    if selected_user == "Overall":
        # 1 remove grp notification
        indx = list(df[df["user"] == "grp_notification"].index)
        new_df = df.drop(indx)
        # 2 remove media ommited
        indx = list(df[df["msg"] == "<Media omitted>\n"].index)
        new_df = new_df.drop(indx)
        # 3 remove stopwords
        word = []
        for w in new_df["msg"]:
            word.extend(w.split())

        nonstp_hindi = []
        for w in word:
            if w not in stopwords:
                nonstp_hindi.append(w)
         # count of frequency of number

        keys = []
        for i in range(len(Counter(nonstp_hindi).most_common(20))):
            x = Counter(nonstp_hindi).most_common(20)[i][0]
            keys.append(x)
        values = []
        for i in range(len(Counter(nonstp_hindi).most_common(20))):
            x = Counter(nonstp_hindi).most_common(20)[i][1]
            values.append(x)

        new_df = pd.DataFrame({"most_frequent_words": keys, "word_count": values})
    else:
        # 1 remove grp notification
        indx = list(df[df["user"] == "grp_notification"].index)
        new_df = df.drop(indx)
        # 2 remove media ommited
        indx = list(df[df["msg"] == "<Media omitted>\n"].index)
        new_df = new_df.drop(indx)
        new_df = new_df[new_df["user"]==selected_user]

        word = []
        for w in new_df["msg"]:
            word.extend(w.split())

        nonstp_hindi = []
        for w in word:
            if w not in stopwords:
                nonstp_hindi.append(w)
          # count of frequency of number

        keys = []
        for i in range(len(Counter(nonstp_hindi).most_common(20))):
            x = Counter(nonstp_hindi).most_common(20)[i][0]
            keys.append(x)
        values = []
        for i in range(len(Counter(nonstp_hindi).most_common(20))):
            x = Counter(nonstp_hindi).most_common(20)[i][1]
            values.append(x)

        new_df = pd.DataFrame({"most_frequent_words": keys, "word_count": values})
    return new_df




def fetch_status(selected_user,df):
    if selected_user == "Overall":
        # msg count
        num_msg = df.shape[0]
        # word count
        word = []
        for msg in df["msg"]:
            word.extend(msg.split())
        word_count = len(word)
        #media count
        mediafile_count = media_count(selected_user,df)

        # url count
        urls = []
        extract = URLExtract()
        for i in df["msg"]:
            x = extract.find_urls(i)
            urls.extend(x)
        url_count = len(urls)

        return num_msg, word_count,mediafile_count,url_count,urls
    else:
        # msg count
        num_msg = df[df["user"] == selected_user].shape[0]
        # word count
        text = []
        x = df["msg"].groupby(df["user"])
        for msg in x.get_group(selected_user):
            text.extend(msg.split())
        word_count = len(text)
        # media count
        mediafile_count = media_count(selected_user, df)

        #url cout
        url_df = df[df["user"]==selected_user]
        urls = []
        extract = URLExtract()
        for i in url_df["msg"]:
            x = extract.find_urls(i)
            urls.extend(x)
        url_count = len(urls)

        return num_msg,word_count,mediafile_count,url_count,urls







