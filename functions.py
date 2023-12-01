# importing class URLExtract from urlextract
# import streamlit
from urlextract import URLExtract
# importing class WordCloud from wordcloud
from wordcloud import WordCloud
# creating object of URLExtract class
extract = URLExtract()
#importing emoji
import emoji
#importing pandas
import pandas as pd
from collections import Counter

def fetch_stats(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    # number of msgs
    num_msgs = df.shape[0]
    # number of words
    words = []
    for msg in df['user']:
       words.extend(msg.split())
    # number of media
    num_med = df[df['msg'] == '<Media omitted>\n'].shape[0]

    # number of links
    link = []
    for msg in df['msg']:
        link.extend(extract.find_urls(msg))

    return num_msgs, num_med, len(link), len(words)


def monthly_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month'])['msg'].count().reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


# daily timeline
def daily_timeline(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    timeline = df.groupby('date')['msg'].count().reset_index()
    return timeline


def activity_map(selected_user, df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    active_month_df = df.groupby('month')['msg'].count().reset_index()
    month_list = active_month_df['month'].tolist()
    month_msg_list = active_month_df['msg'].tolist()

    active_day_df = df.groupby('day')['msg'].count().reset_index()
    day_list = active_day_df['day'].tolist()
    day_msg_list = active_day_df['msg'].tolist()

    return active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list


def most_chaty(df):
    x = df['user'].value_counts().head()

    percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2)
    return x, percent

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['msg'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['msg'] = temp['msg'].apply(remove_stop_words)
    df_wc = wc.generate(temp['msg'].str.cat(sep=" "))
    return df_wc

# def activity_heatmap(selected_user,df):

#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     user_heatmap = df.pivot_table(index='day_name_disp', columns='period', values='msg', aggfunc='count').fillna(0)

#     return user_heatmap


def most_common_words(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['msg'] != '<Media omitted>\n']
    words = []

    for message in temp['msg']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'OverAll':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['msg']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    
    # streamlit.dataframe(emoji_df)

    return emoji_df
