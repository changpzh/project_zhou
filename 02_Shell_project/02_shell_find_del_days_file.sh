#!/bin/bash

#remove-file: check whether if dir exist or not, if exist then remove all files in that directory which before given days.
echo "
please enter the directory which you want to remove:
"
echo "
pay attention: the input pattern must like:
	- windows os: /cygdrive/C/Temp/FZM_TLF15A [days]
	- Linux os: [your_path] [days]
"

echo -n "Enter a directory and days->"
read given_path given_day

default_day=30
if [[ -d $given_path ]]; then
	if cd $given_path; then
		if [[ $given_day =~ ^[0-9]+$ ]]; then
			echo "you want to delete files in '$given_path'"
			echo "you want to delete files before '$given_day' days"
			find $given_path -type f -mtime +${given_day} | xargs rm -rf
			#find $given_path -type d -mtime +${given_day} | xargs rm -rf
			#rm -rf *
			echo "delete FILEs success"
		else
			echo "you want to delete files in '$given_path'"
			echo "you want to delete files by default $default_day days"
			find $given_path -type f -mtime +${default_day} | xargs rm -rf
			#find $given_path -type d -mtime +${default_day} | xargs rm -rf
			#rm -rf *
			echo "delete FILEs by before default 30 days success"
		fi	
	else
		echo "cannot cd to '$given_path'" >&2
		exit 1
	fi	
else
	echo "No such file directory." >&2
	exit 2
fi

