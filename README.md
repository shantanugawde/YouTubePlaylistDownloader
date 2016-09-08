# YouTube Playlist Downloader
ytpldownloader.py is a simple Python3 script which downloads all the videos in a playlist in mp4 format.
## Guide
Use pip to install dependencies.
```
pip -r install requirements.txt
```
Specify playlist URL, directory path to download the playlist to, and resolution to download playlist.

Default resolution is 480p and default directory is the current working directory.

URL should be of the form https://www.youtube.com/playlist?=<param_value> or https://www.youtube.com/playlist?list=<param_value>
```
python ytpldownloader.py --plurl=<playlist_url> --res=<resolution>
```

Downloads can be stopped by hitting *CTRL-C* or an equivalent combination.

To resume the download, specify the path where the playlist directory exists. 
## Warning

Do not tamper with the queue.txt file.

You will be violating YouTube's Terms and Conditions by using this script.
