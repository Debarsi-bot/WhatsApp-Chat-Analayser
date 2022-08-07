import re
import pandas as pd


def processData(data):
    #pattern = '\d{2}/\d{2}/\d{4},\s\d{2}:\d{2}\s-\s'
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    #store the message as strings
    messages = re.split(pattern, data)[1:] #an extra empty string gets added in front so skip the first element

    #will be converted to timestamps later
    #16/07/2021, 17:14 - 
    messageDates = re.findall(pattern, data)  

    #splitting the timestamps
    date = []
    day = []
    year = []
    month = []
    monthName = []

    hour = []
    minute = []

    for eachDate in messageDates:
        timestamp = pd.to_datetime(eachDate,format='%d/%m/%Y, %H:%M - ')
        date.append(timestamp.date())
        day.append(timestamp.day_name())
        month.append(timestamp.month)
        monthName.append(timestamp.month_name())
        year.append(timestamp.year)
        hour.append(timestamp.hour)
        minute.append(timestamp.minute)

    #split messages into sender and message content
    userPattern = '([\w\W]+?):\s'
    user = [] 
    message = []

    for eachMessage in messages:
    #     print(eachMessage)
        entry = re.split(userPattern, eachMessage)
        entry = [x for x in entry if x!='']
        if(len(entry) == 1):
            user.append("System Notification")
            message.append(entry[0])
        else:
            user.append(entry[0])
            message.append(entry[1])
            
    df = pd.DataFrame({
        'user': user,
        'message': message,
        'date' :date,
        'day' :day,
        'month': month,
        'monthName': monthName,
        'year' : year,
        'hour':hour,
        'minute': minute
    })
    return df
        
