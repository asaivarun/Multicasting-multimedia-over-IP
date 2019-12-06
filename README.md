Design decisions (based on the current bitrate: 1382 bps)
BUFSIZE
time.sleep
Quesize in setsockopt, it is 1 followed by 10 zeros
install ffmpeg

pre-process the video using ffmpeg, command given in lab4's pdf
using the ffmpeg command on the video will also give you the bitrate, you can use it to display the bitrate statically on the console or pass it through the log file on different ports.
You can also compile a transcription .srt file with ffmpeg when doing the video, that can give subtitles when playing the video, have done that already for the phineas and ferb videos (bigfoot and toy factory from Youtube)

Usage
sender : python mcast.py -s multicast_addr path/to/video.mp4  

receiver : python mcast.py -r multicast_addr | ffplay -


Try arranging a router to test, using phone's hotspot is ok, but there would be a lot of packet drop as it has a very small queue size

for the interface, once the video is playing, use p/space to play/pause
ESC/q to quit
f for fullscreen
use the arrow keys to seek, cannot go forward as it is live, but can go to the starting of the video, even while it is buffering and can go to the live spot as well.
Works smoothly, like a charm, has all the features you will find on Youtube's live feature
