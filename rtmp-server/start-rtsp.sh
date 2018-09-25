ffserver -f server.conf -d &
python sender.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size 640x480 -framerate 10 -i - -c:v libx264 http://localhost:8554/feed1.ffm