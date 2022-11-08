#! /bin/bash

#given the localhost url the loging is desplayd, the first page is the login page without entering to the system there is no way to get to the homepage


#when user nevigate to other pages the desplay changes


#when loging in the app redirect us to the homepage


#in the homepage all posts are shown


# in the posts page there is an option to add new post and all posts are shown


# in the edit/delete page there is an option to change/delete post and all posts are shown



# pip install pytest
# pip install selenium
#https://youtu.be/wTGKOgOJbEk


resp=$(curl http://app:5000/ -Is | grep -c "HTTP/1.1 200")
while [[ resp -ne 1 ]]
do
    if [[ resp -eq 1 ]]; then
		echo "pass"
		exit 0
	fi
    sleep 2
	resp=$(curl http://app:5000/ -Is | grep -c "HTTP/1.1 200")
done