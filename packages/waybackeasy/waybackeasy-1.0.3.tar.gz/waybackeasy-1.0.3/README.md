# Waybackeasy
The insanely simple way to interface with the Waybackmachine.

# Installation
pip install waybackeasy

# Use
import waybackeasy
waybackeasy.get("https://news.ycombinator.com/", "27.05.2016")


This will get return the html of one of the snapshot of news.ycombinator.com that the
Waybackmachine took on the 27th May of 2016.


Note: For now dd.mm.yyyy is the only dateformat that is supported. I am planning to improve
this and add more options in good time.

For questions, bug-reports and feature-requests write me - joseikowsky@gmail.com
