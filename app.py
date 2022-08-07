import streamlit as st
import pandas as pd
import dataProcessing
import utility
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.header("Get analysis of your whatsapp chats")
st.markdown("""<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True) 
uploaded_file = st.sidebar.file_uploader("Insert whatsapp chat")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = dataProcessing.processData(data)
    uniqueUsers = utility.getUniqueUsers(df)
    uniqueUsers.insert(0, "Everyone")

    user = st.sidebar.selectbox(
        'Select user',
        uniqueUsers)

    #get the analysis of data
    if st.sidebar.button("Show Analysis"):
        #show analysis of chat wrt user selected
        totalMessages, listOfWords, listOfLinks, totalMedia = utility.getSelectedUserData(df,user)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total messages")
            st.title(totalMessages)

        with col2:
            st.header("Total Words")
            st.title(len(listOfWords))

        with col3:
            st.header("Total Links")
            st.title(len(listOfLinks))

        with col4:
            st.header("Media Shared")
            st.title(totalMedia)
    
        with st.expander("Show Links Shared"):
            for link in listOfLinks:
                st.write(link)

        #the following graphs are shown only if overall statistics are needed and not individual user

     
        if(user == 'Everyone'):
            col1, col2 = st.columns(2)
            #get total messages by every user and plot it
            #uniqueUsers[1:] , we skip the first element which corresponds to all users
            with col1:
                st.header("Message Distribution By User")
                totalMessageGroupedByUser = utility.getTotalMessagesGroupedByUser(df,uniqueUsers[1:])
                fig, ax = plt.subplots()
                ax.tick_params(axis='x', rotation=90)
                ax.bar(uniqueUsers[1:], totalMessageGroupedByUser)
                st.pyplot(fig)

            #show percentage of messages by users
            with col2:
                percentageByUser = []
                for i in range (1, len(uniqueUsers)):
                    percentageByUser.append(round((totalMessageGroupedByUser[i-1] / totalMessages)*100, 2))

                percentDf  = pd.DataFrame({'User' :uniqueUsers[1:], 'Percent': percentageByUser})

                #This will make the index no longer the numbering, but the indicated column
                percentDf.set_index('User', inplace=True)
                st.header("Percentage Distribution")
                st.dataframe(percentDf) 


        #show distribution of messages by day of week and month
        col1, col2 = st.columns(2)
        with col1:
            st.header("Activity wrt day of week")
            mostActiveDaysOfWeek = utility.getMostActiveDaysOfWeek(df,user)
            days = mostActiveDaysOfWeek.keys()
            activity = list(mostActiveDaysOfWeek.values())
            fig, ax = plt.subplots()
            ax.tick_params(axis='x', rotation=90)
            ax.bar(days, activity)
            st.pyplot(fig)
        
        with col2:
            st.header("Activity wrt month")
            mostActiveMonths = utility.getMostActiveMonths(df,user)
            months = mostActiveMonths.keys()
            activity = list(mostActiveMonths.values())
            fig, ax = plt.subplots()
            ax.tick_params(axis='x', rotation=90)
            ax.bar(months, activity)
            st.pyplot(fig)



        

    