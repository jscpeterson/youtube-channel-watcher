# youtube-channel-watcher
## Purpose
While running, this script will monitor a YouTube channel and archive any newly uploaded videos as soon as it detects them.
## Usage
1. It is recommended to run in a virtualenv.   
  `virtualenv -p python3 venv`  
  `source venv/bin/activate`  
2. Install requirements.  
  `pip install -r requirements.txt`
3. Run Python
4. `from feed_watcher import FeedWatcher`  
   `FeedWatcher.watch(channel_id=None, username=None, last_update=None, check_interval=60, output_path=None)`
    * *channel_id* = The channel ID, i.e `UCJKt_QVDyUbqdm3ag_py2eQ`. Required if username not provided.
    * *username* = The username of the channel owner, i.e *Kuokka77*. Required if channel_id not provided.
    * *last_update* = The minimum datetime to check for new updates. If not provided, the script will use the updated date of the last uploaded video.
    * *check_interval* = Interval of time for the script to run in seconds. Script runs every minute by default.
    * *output_path* = The filepath to save new videos to. By default the directory the script is run from.
    
Currently this is only a very simple single-threaded script that must be terminated manually. To run in the background I suggest using `tmux`. 
## Dependencies
 * pytube (specifically, [this](https://github.com/bigg215/pytube) fork as the latest version of pytube has 403 issues)
 * requests
 * BeautifulSoup
 * lxml XML parser
