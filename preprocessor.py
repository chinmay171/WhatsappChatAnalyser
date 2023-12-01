import re
import pandas as pd


def preprocess(data):
    # Pattern in chat ( Spliting DataTime and Msg)
    # pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s"  for 12 hours format
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s"

    # All msgs we have
    message = re.split(pattern, data)[1:]
    # All date we have
    dates = re.findall(pattern, data)
    # Split Date and Time
    date = []
    times = []
    for i in dates:
        date.append(i.split(" ")[0])
        times.append(i.split(" ")[1])

    # f_date = []
    # for i in date:
    #     f_date.append(i.split(" "))[0]

    time = []
    for i in times:
        time.append(i.split("\u202f")[0])
    # Create DataFrame¶
    df = pd.DataFrame({
        'user_msg': message,
        'date': date,
        'time': time
    })

    # Spliting user name and msg
    user = []
    msg = []
    for i in df['user_msg']:
        x = re.split("([\w\W]+?):\s", i)
        if x[1:]:  # user name
            user.append(x[1])
            msg.append(x[2])
        else:
            user.append('Group Notification')
            msg.append(x[0])

    df['user'] = user
    df['msg'] = msg
    df.drop(columns=['user_msg'], inplace=True)

    # Convert Date Column into DateTime format
    df['date'] = pd.to_datetime(df['date'])
    df['complete_date'] = df['date'].dt.date

    # can be used to display dataframe bit by bit
    df['year_disp'] = df['date'].dt.year
    df['month_num_disp'] = df['date'].dt.month
    df['day_disp'] = df['date'].dt.day

    df['month_name_disp'] = df['date'].dt.month_name()
    df['day_name_disp'] = df['date'].dt.day_name()
    only_hour = []
    only_minute = []
    for i in time:
        only_hour.append(i.split(":")[0])
        only_minute.append(i.split(":")[1])
    df['hour_disp'] = only_hour
    df['minute_disp'] = only_minute

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name_disp', 'hour_disp']]['hour_disp']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(int(hour) + 1))
        else:
            period.append(str(hour) + "-" + str(int(hour) + 1))

    df['period'] = period

    return df