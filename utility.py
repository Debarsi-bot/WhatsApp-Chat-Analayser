import pandas as pd
from urlextract import URLExtract

def getUniqueUsers(df):
    uniqueUsers = df['user'].unique().tolist()
    uniqueUsers.remove('System Notification')
    uniqueUsers.sort()
    return uniqueUsers

#ret
def getSelectedUserData(df , user):
    #total messages sent in chat
    extractor = URLExtract()
    if user != 'Everyone' :
        df = df[df['user'] == user]
    totalMessagesSent = len(df['user'])+1
    listOfWords = []
    listofLinks = []
    totalMedia = 0
    for sentence in df['message']:
        if(sentence == "<Media omitted>\n"):
            totalMedia = totalMedia + 1
        else:
            listOfWords.extend(sentence.split())
            url = extractor.find_urls(sentence)
            if(len(url) != 0):
                listofLinks.append(url[0])
    

    return totalMessagesSent, listOfWords, listofLinks, totalMedia

#the function receives as argument the data frame and list of unique users in sorted order
#the output list contains n elements if length of arg uniqueUsers is n
#let getTotalMessagesGroupedByUser be output list
#getTotalMessagesGroupedByUser[i] corresponds to total messages sent by uniqueUsers[i]
def getTotalMessagesGroupedByUser(df, uniqueUsers):
    totalMessageGroupedByUser = []
    for user in uniqueUsers:
        totalMessageGroupedByUser.append(len(df[df['user'] == user]))   
    return totalMessageGroupedByUser


#tod0 :   most active days, most active months
#get the no of messages sent each day of week
def getMostActiveDaysOfWeek(df, user):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if user is not 'Everyone':
        df = df[df['user'] == user]
    mostActiveDaysOfWeek = dict.fromkeys(days,0)
   
    for i in df['day']:
        mostActiveDaysOfWeek[i] += 1
    return mostActiveDaysOfWeek

#get number of messages ent each month
def getMostActiveMonths(df, user):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    if user is not 'Everyone':
        df = df[df['user'] == user]
    mostActiveMonths = dict.fromkeys(months,0)
   
    for i in df['monthName']:
        mostActiveMonths[i] += 1
    return mostActiveMonths