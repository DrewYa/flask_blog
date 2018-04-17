#!/bin/bash

for ((i=0; i<3; i++))
do
	rm /home/pi/server/flask_blog/app/static/cam/$i.jpg
done