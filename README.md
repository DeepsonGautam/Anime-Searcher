## Anime Info CLI
basically a simple terminal app where you can search for anime and get all the details without opening a browser 

# requirements
python 3.10+ (yeah… match/case stuff… even if it’s not really used anymore lol)
internet connection
that’s literally it, no extra installs or anything
how to run

# just do:
python anime.py

# what it does
you type in an anime name, it searches it using the MyAnimeList data (through the Jikan API), then shows you a list of results.

# you pick one, and boom — you get:
score
number of episodes
studios
genres
synopsis
trailer link (if there is one)

# after that, there’s a little menu where you can go deeper:
characters → shows main characters + their japanese voice actors
staff → directors, writers, etc
recommendations → similar anime people suggest (and you can open those too)

# how to use it
run the script
press 1 to search
type an anime name
pick a number from the results
read the info
use the menu at the bottom to explore more
press 0 anytime to go back

# notes
it uses the free Jikan API (basically an unofficial MyAnimeList API), so yeah sometimes it can be a bit slow
if you get a network error, just run it again, it happens
press Ctrl + C anytime if you wanna quit
