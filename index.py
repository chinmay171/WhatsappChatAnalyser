import streamlit as st
import preprocessor
import functions
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a File")

if uploaded_file is None:
    st.markdown('''Please export your WhatsApp chat (without media), whether it be a group chat or an individual/private chat, then click on "Browse Files" and upload it to this platform.''')
    st.markdown('''Afterward, kindly proceed to click on the "Analyse" button. This action will generate a variety of insights concerning your conversation.''')
    st.markdown(''' You will have the option to select the type of analysis, whether it is an overall analysis or one that specifically focuses on particular participants' analysis.''')
    st.markdown('Thank You!')
    st.markdown('Kashish-Muskan-Mohit-Chinmay')

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # st.write(bytes_data)

    # converting bytes into text
    data = bytes_data.decode('utf-8')

    # show text data
    # st.text(data)

    # DataFrame
    df = preprocessor.preprocess(data)

    # show dataframe
    st.title("Data I recieved!!!")
    st.dataframe(df)

    # fetch unique user
    user_details = df['user'].unique().tolist()
    # remove Group Notifications
    if 'Group Notification' in user_details:
        user_details.remove('Group Notification')
    # sorting list
    user_details.sort()
    # insert overall option
    user_details.insert(0, 'OverAll')

    # drop down to select user
    selected_user = st.sidebar.selectbox('Show Analysis as:', user_details)

    if st.sidebar.button('Analyse'):

        num_msgs, num_med, link, words = functions.fetch_stats(selected_user, df)

        # overall statistics
        st.title('OverAll Basic Statistics')
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('No. of Messages')
            st.subheader(num_msgs)
        with col2:
            st.header('Words Count')
            st.subheader(words)
        with col3:
            st.header('Media Shared')
            st.subheader(num_med)
        with col4:
            st.header('Link Shared')
            st.subheader(link)

        # monthly timeline
        timeline = functions.monthly_timeline(selected_user, df)
        st.title('Monthly Timeline')

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['msg'], color='maroon')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # daily timeline
        timeline = functions.daily_timeline(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['date'], timeline['msg'], color='purple')
        plt.xticks(rotation=90)
        st.pyplot(fig)


        # active map
        st.title('Activity Maps')
        # col1, col2 = st.columns(2)

        active_month_df, month_list, month_msg_list, active_day_df, day_list, day_msg_list = functions.activity_map(selected_user, df)
        # with col1:
            # active month
        st.header('Most Active Month')
        fig, ax = plt.subplots()
        ax.bar(active_month_df['month'], active_month_df['msg'])
        ax.bar(month_list[month_msg_list.index(max(month_msg_list))], max(month_msg_list), color='green', label = 'Highest')
        ax.bar(month_list[month_msg_list.index(min(month_msg_list))], min(month_msg_list), color='red', label = 'Lowest')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # with col2:
            # active day
        st.header('Most Active Day')
        fig, ax = plt.subplots()
        ax.bar(active_day_df['day'], active_day_df['msg'])
        ax.bar(day_list[day_msg_list.index(max(day_msg_list))], max(day_msg_list), color='green', label='Highest')
        ax.bar(day_list[day_msg_list.index(min(day_msg_list))], min(day_msg_list), color='red', label='Lowest')
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # st.title("Weekly Activity Map")
        # user_heatmap = functions.activity_heatmap(selected_user,df)
        # fig,ax = plt.subplots()
        # ax = sns.heatmap(user_heatmap)
        # plt.yticks(rotation='horizontal')
        # st.pyplot(fig)
        # ValueError: zero-size array to reduction operation fmin which has no identity

        # most chatiest user
        if selected_user == 'OverAll':
            st.title('Most Active Users')

            x, percent = functions.most_chaty(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x, color='cyan')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(percent)

        # WordCloud
        df_wc = functions.create_wordcloud(selected_user, df)
        st.title('Word Cloud')

        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = functions.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most Common Words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = functions.emoji_helper(selected_user,df)
        if emoji_df.empty is False:
            st.title("Emoji Analysis")
            col1,col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df)
            with col2:
                fig,ax = plt.subplots()
                ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
                st.pyplot(fig)
        else:
            st.title("damm, no emojis!!! might be emotionally blind")

        st.text(' ')
        st.text(' ')

        st.text('🛠️ by ~ Kashish-Muskan-Mohit-Chinmay')