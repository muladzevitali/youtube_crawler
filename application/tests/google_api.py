from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey='AIzaSyD8heSjUM_fVvxV1Mr9clw1hEDx8Ya0VPU')
search_results = youtube.search().list(q='pagode', part='snippet', type='video',
                                       order='viewCount', maxResults=50).execute()

video_meta = youtube.videos().list(part='snippet', id='_Yhyp-_hX2s').execute()
video_meta
parts = ['contentDetails', 'topicDetails', 'player']