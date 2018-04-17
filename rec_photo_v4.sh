#!/bin/bash

sec=9

#DATE=$(date+"%Y-%m-%d_%H%M%S")
#raspistill -op 175 -vf -hf -o /home/pi/server/flask_blog/app/static/cam/$DATE.jpg
#raspistill -op 125 -w 1280 -h 720 -o /home/pi/server/flask_blog/app/static/cam/img_$DATE.jpg

raspistill -op 155 -w 1280 -h 720 -o /home/pi/server/flask_blog/app/static/cam/img_"$(date)".jpg

sleep $sec

#rm /home/pi/server/flask_blog/app/static/cam/*

# op - непрозрачность, когда снимаем

