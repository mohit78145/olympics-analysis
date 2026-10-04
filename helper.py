def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Bronze']+medal_tally['Silver']
    return medal_tally

def year_country(df):
    year = sorted(df['Year'].unique().tolist())
    year.insert(0, 'overall')
    region = sorted(df['region'].dropna().unique().tolist())
    region.insert(0,'Overall')
    return year,region

def fetch_medal(df,year,country):
  flag=0
  temp=df.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event','Medal'])
  if year=='overall' and country=='Overall':
     pass
  if year=='overall' and country!='Overall':
    flag=1
    temp=temp[temp['region']==country]
  if year!='overall' and country=='Overall':
    temp=temp[temp['Year']==year]
  if year!='overall' and country!='Overall':
    temp=temp[(temp['region']==country)&(temp['Year']==year)]
  if flag==1:
        x=temp.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
  else:     
        x=temp.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()  
  x['total']=x['Gold']+x['Bronze']+x['Silver']
  return x

def data_over_time(df,col):
   nation_over_time=df.drop_duplicates(subset=['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
   nation_over_time.rename(columns={'Year':'Edition','count':'No of '+col},inplace=True)
   return nation_over_time 

def most_successful(df,sport):
  temp_df=df.dropna(subset=['Medal'])
  if sport !='Overall':
      temp_df=temp_df[temp_df['Sport']==sport]
  x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport','region']].drop_duplicates('Name')
  x.rename(columns={'count':'Medals'},inplace=True)
  return x

def yearwise_medal_tally(df,country):
  temp_df=df.dropna(subset=['Medal'])
  temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
  new_df=temp_df[temp_df['region']==country]
  final=new_df.groupby('Year')['Medal'].count().reset_index()
  return final

def country_event_heatmap(df,country):
  temp_df=df.dropna(subset=['Medal'])
  temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)
  new_df=temp_df[temp_df['region']==country]
  pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
  return pt

def most_successful_Countrywise(df,country):
  temp_df=df.dropna(subset=['Medal'])
  temp_df=temp_df[temp_df['region']==country]
  x=temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
  x.rename(columns={'count':'Medals'},inplace=True)
  return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final    