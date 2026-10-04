import streamlit as st
import pandas as pd
import prepocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df=prepocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu=st.sidebar.radio(
    'Select an option',
    ['medal tally','overall analysis','country-wise analysis','athlete wise analysis']
)
# st.dataframe(df)

if user_menu=='medal tally':
    st.sidebar.header('Medal Tally')
    year,country=helper.year_country(df)
    selected_year=st.sidebar.selectbox("Select year",year)
    selected_country=st.sidebar.selectbox("Select country",country)
    x=helper.fetch_medal(df,selected_year,selected_country)
    # medal_tally=helper.medal_tally(df)
    if selected_year=='overall ' and selected_country=='Overall':
        st.title("Overall tally")
    if selected_year!='overall ' and selected_country=='Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_year=='overall ' and selected_country!='Overall':
        st.title(selected_country+" overall performance")
    if selected_year!='overall ' and selected_country!='Overall':
        st.title(selected_country+" performane in "+str(selected_year)+" Olympics")
    st.table(x)

if user_menu=='overall analysis':
    edition=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]  
    sports=df['Sport'].unique().shape[0]  
    events=df['Event'].unique().shape[0]  
    athletes=df['Name'].unique().shape[0]  
    nation=df['region'].unique().shape[0]  

    st.title("Top Statistics")
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Editions")
        st.title(edition)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nation)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nation_over_time=helper.data_over_time(df,'region')
    st.title("Participating Nations over the years")
    fig=px.line(nation_over_time,x='Edition',y='No of region')
    st.plotly_chart(fig)

    event_over_time=helper.data_over_time(df,'Event')
    st.title("Events over the years")
    fig=px.line(event_over_time,x='Edition',y='No of Event')
    st.plotly_chart(fig)

    athletes_over_time=helper.data_over_time(df,'Name')
    st.title("Athletes over the years")
    fig=px.line(athletes_over_time,x='Edition',y='No of Name')
    st.plotly_chart(fig)

    st.title("No of event over time(Every Year)")
    fig,ax=plt.subplots(figsize=(20,20))
    x=df.drop_duplicates(subset=['Year','Event','Sport'])
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu=='country-wise analysis':
    st.sidebar.title('Country wise analysis')
    region = sorted(df['region'].dropna().unique().tolist())
    country=st.sidebar.selectbox("Select country",region)
    country_df=helper.yearwise_medal_tally(df,country)   
    fig=px.line(country_df,x='Year',y='Medal')
    st.title(country+" Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(country+" excels in the following sports")
    pt=helper.country_event_heatmap(df,country)
    fig,ax=plt.subplots(figsize=(20,20))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    top10=helper.most_successful_Countrywise(df,country)
    st.title("Top 10 athletes of "+country)
    st.table(top10)

if user_menu == 'athlete wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)    

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig) 

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
