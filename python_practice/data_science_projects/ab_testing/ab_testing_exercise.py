import pandas as pd

ad_clicks = pd.read_csv('ad_clicks.csv')
print(ad_clicks.head())

#counting the number of users by source
view_source = ad_clicks.groupby('utm_source').user_id.count().reset_index()
print(view_source)

#create True/False column-- True id ad_click_timestamp is not null and False if it is null
ad_clicks['is_click'] = ~ad_clicks.ad_click_timestamp.isnull()

#number of people who clicked on ads by each source
clicks_by_source = ad_clicks.groupby(['utm_source', 'is_click']).user_id.count().reset_index()
print(clicks_by_source)

#pivots data to make it easier to view
clicks_pivot = clicks_by_source.pivot(columns = 'is_click', index= 'utm_source', values= 'user_id').reset_index()
print(clicks_pivot)

#create new column to view % of users who clicked on the add by source
clicks_pivot['percent_clicked'] = clicks_pivot[True]/ (clicks_pivot[True] + clicks_pivot[False])
print(ad_clicks.head())

#shows how many users saw each ad
group_info = ad_clicks.groupby('experimental_group').user_id.count().reset_index()
print(group_info)

#percent of users who clicked on ad by day. pivoted to better show data.
percent_click = ad_clicks.groupby(['experimental_group', 'is_click']).user_id.count().reset_index()
percent_click_pivot = percent_click.pivot(columns = 'is_click', index = 'experimental_group', values = 'user_id').reset_index()
print(percent_click_pivot)

#group a percentages and pivot
a_clicks= ad_clicks[ad_clicks.experimental_group == 'A']
a_clicks_pivot = a_clicks.groupby(['is_click', 'day']).user_id.count().reset_index().pivot(columns = 'is_click', index = 'day', values = 'user_id').reset_index()
a_clicks_pivot['percent_clicked'] = a_clicks_pivot[True]/ (a_clicks_pivot[True] + a_clicks_pivot[False])
print(a_clicks_pivot)

#group b percentages and pivot
b_clicks= ad_clicks[ad_clicks.experimental_group == 'B']
b_clicks_pivot = b_clicks.groupby(['is_click', 'day']).user_id.count().reset_index().pivot(columns = 'is_click', index = 'day', values = 'user_id').reset_index()
b_clicks_pivot['percent_clicked'] = b_clicks_pivot[True]/ (b_clicks_pivot[True] + b_clicks_pivot[False])
print(b_clicks_pivot)

#I suggest the use of Ad A. Overall, it has a higher percentage of user engagement.
