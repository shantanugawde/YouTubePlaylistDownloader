from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import *
from pytube import YouTube
import os
import click
import re
import atexit

base_url = "https://www.youtube.com"
bs_obj = None
pl_title = ""
queue_set = None
resolution = ""


@click.command()
@click.option('--plurl', help='Complete URL of the playlist to be downloaded')
@click.option('--res', default='360p', help='Specify required resolution, such as 480p')
def download_videos(plurl, res):
    if re.search("^http[s|]://www.youtube.com/playlist.*",plurl) is None:
        print("Invalid YouTube Playlist URL")
        exit()
    else:
        global queue_set, resolution
        resolution = res
        vid_set = get_links(plurl)
        queue_set = get_queue()
        if queue_set is None:
            print("All videos in this playlist have been downloaded")
            exit()
        else:
            if len(queue_set) == 0:
                queue_set = vid_set
            download_set()


# Check for directory structure and get queued videos
def get_queue():
    q_set = set()

    if os.path.isdir(pl_title) is False:
        os.makedirs(str(pl_title))
        open(pl_title + "/queue.txt", "w")

    else:
        if os.path.exists(pl_title + "/queue.txt"):
            with open(pl_title + "/queue.txt") as q_file:
                for l in q_file:
                    q_set.add(l.strip())
        else:
            return None

    return q_set


# Get links of all videos on page
def get_links(pl_url):
    global bs_obj, pl_title
    links = set()
    page = urlopen(pl_url)
    try:
        bs_obj = BeautifulSoup(page.read(), "html.parser")
        pl_title = bs_obj.title.get_text().strip().replace("\n - YouTube", "").replace(" ", "_")
        rows = bs_obj.findAll("", {"class": "pl-video-title"})
        for row in rows:
            vid_url = row.a.attrs['href']
            if base_url not in vid_url:
                vid_url = urljoin(base_url, vid_url)

            links.add(vid_url)
        return links
    except Exception as inst:
        print(inst)
        print("Could not access page")
        exit()
        return None


# Download videos from a set
def download_set():
    global queue_set, resolution
    done_set = set()
    assert isinstance(queue_set, set)
    for link in queue_set:
        try:
            yt = YouTube(link)
            print("Downloading ", yt.filename)
            vid = yt.get('mp4', resolution)

            # Empty list
            if str(vid) == "<class 'list'>":
                print("Video is not available in specified resolution\n")
            else:
                vid.download(os.getcwd()+"\\"+pl_title)
                done_set.add(link)
        except Exception as inst:
            print(inst)
            print("Skipping to next video")
            print()
    queue_set = queue_set.difference(done_set)


# Clean-up
@atexit.register
def save_queue():
    if os.path.exists(pl_title):
        q_file = open(pl_title + "/queue.txt", "w")
        assert isinstance(queue_set, set)
        for l in queue_set:
            q_file.write(str(l)+"\n")
        q_file.close()


if __name__ == '__main__':
    download_videos()
