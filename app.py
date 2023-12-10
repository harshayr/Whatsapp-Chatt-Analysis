import streamlit as st
import preprocessor, utils
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()  # we have to convert this file to string initialy it is in bytes format
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    user_list = df["user"].unique().tolist()
    user_list.remove("grp_notification")
    user_list.sort()
    user_list.insert(0,"Overall")



    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    daily_df, month = utils.daily_timeline(selected_user, df)
    month.insert(0, 'All')
    selected_month = st.sidebar.selectbox("Chose Month For daily timeline", month)
    st.title("Top Statistics")
    if st.sidebar.button("Show Analysis"):
        num_msg ,word_count,media_count, link_count, url_list= utils.fetch_status(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)


        with col1:
           st.header("Total msg")
           st.title(num_msg)
        with col2:
            st.header("Total words")
            st.title(word_count)
        with col3:
            st.header("Total media")
            st.title(media_count)
        with col4:
            st.header("Total link")
            st.title(link_count)
            url_list.insert(0,"List of URLS")
            st.selectbox("Links",url_list)


        # timelins
        col1, col2 = st.columns(2)
        with col1:
            st.header("Monthly Analysis")
            time_df = utils.monthly_tiime(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(time_df["timeline"], time_df["msg"], color="green")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Daily Timeline")

            daily_df, month = utils.daily_timeline(selected_user,df)
            if selected_month == "All":
                fig, ax = plt.subplots()
                ax.plot(daily_df["date"], daily_df["msg"], color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            else:
                daily_df = daily_df[daily_df["month"]==selected_month]
                fig, ax = plt.subplots()
                ax.plot(daily_df["date"], daily_df["msg"], color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

         # activity
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            daywise_df = utils.weekday_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(daywise_df["day_name"], daywise_df["count"], color="purple")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            monthwise_df = utils.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthwise_df["month"], monthwise_df["count"], color="orange")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.header("Most Busy Time")
        time_df = utils.time_activity(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(time_df)
        plt.figure(figsize=(20, 10))
        st.pyplot(fig)


        # finding most busy users
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x,new_df = utils.most_busy(df)
            fig,ax = plt.subplots()

            col5,col6 = st.columns(2)

            with col5:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)
            with col6:
                # st.title("User Percentage")
                st.dataframe(new_df)
        else:
            x, new_df = utils.most_busy(df)
            new_df = new_df[new_df["name"] == selected_user]
            x2 = list(new_df["percentage"])
            st.title(f"Percentage of user msgs: {x2[0]}%")


           # wordcloud
        st.title("Wordcloud")
        df_wc = utils.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        st.title("Most frequent word")
        new_df = utils.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(new_df["most_frequent_words"],new_df["word_count"])
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        emoji_df = utils.emojy(selected_user,df)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].iloc[:5],labels = emoji_df[0].iloc[:5], autopct = "%0.2f")
            st.pyplot(fig)















