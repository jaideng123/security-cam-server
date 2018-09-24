ffserver -f server.conf -d &
python sender.py | ffmpeg -f rawvideo -pixel_format rgb24 -video_size 640x480 -framerate 30 -i - -c:v libx264 http://localhost:8554/feed1.ffm