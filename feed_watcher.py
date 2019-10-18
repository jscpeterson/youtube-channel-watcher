import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytube import YouTube
import dateutil.parser
from time import sleep

XML_PARSER = 'lxml-xml'
YOUTUBE_FEED_URL = 'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'
YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v={video_id}'


class FeedWatcher():
     
     def __init__(self):
         pass

     def watch(self, channel_id, last_update=None, check_interval=60, output_path=None):
          """Watches a YouTube feed given a provided channel_id in a very dumb single-threaded manner. Sleeps for check_interval 
          seconds before trying again. Checks every minute by default. Script must be terminated manually."""
          # TODO Get channel id from user name if provided
          feed_url = YOUTUBE_FEED_URL.format(channel_id=channel_id)
          if last_update is None:
               latest_entry = self.get_most_recent_video(feed_url)
               last_update = self.get_video_updated_date(latest_entry)
          print('Last update was: %s' % last_update)
          print('Starting to watch...')
          while True:
               sleep(check_interval)
               print('Checking for new video..')
               latest_entry = self.get_most_recent_video(feed_url)
               if self.get_video_updated_date(latest_entry) > last_update:
                     print('New video uploaded!')
                     self.download_video(latest_entry, output_path)
                     last_update = self.get_video_updated_date(latest_entry)
               else:
                     print('Nothing new.')
                   
     def get_most_recent_video(self, feed_url):
          """Querys the feed for a YouTube channel and returns a soupified XML entry for the most recently updated video."""
          response = requests.get(feed_url)
          assert response.ok, 'Failed to query feed, response: {response_code}'.format(response_code=response.status_code)
          soup = BeautifulSoup(response.content, XML_PARSER)
          return soup.find('entry')

     def get_video_updated_date(self, soup_entry):
          """Returns the updated timestamp on a soupified XML entry as a datetime object."""
          return dateutil.parser.parse(soup_entry.find('updated').contents[0])

     def download_video(self, soup_entry, output_path=None):
         """Downloads a video from a soupified XML entry."""
         video_id = soup_entry.find('videoId').contents[0]
         video_url = YOUTUBE_VIDEO_URL.format(video_id=video_id)
         output = YouTube(video_url).streams.first().download(output_path=output_path)
         print('Saved video to {output}'.format(output=output))

