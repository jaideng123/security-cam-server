python sender.py | ffmpeg -f rawvideo -pixel_format bgr24 -video_size 1280x720 -framerate 10 -i - -f lavfi -i anullsrc  -acodec aac  -f flv -c:v h264_omx -b:v 500k "rtmp://a.rtmp.youtube.com/live2/$YOUTUBEKEY"
