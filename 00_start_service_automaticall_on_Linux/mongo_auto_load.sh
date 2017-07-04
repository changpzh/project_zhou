#!/bin/bash

mytime=15

echo "
=================================================
will update your local mongoDB after $mytime seconds.
use ctrl + c to stop procedure!
================================================="

for (( i=0; i<$mytime; i=i+1 )); do
    count=$(( $mytime - $i ))
    echo $count
    sleep 1
done

file_url="ftp://hzogrvm01.china.nsn-net.net/mongo_backup/"
latest_file_url=`wget -O - $file_url | grep href | sed 's/.*href="\(.*\)">\(.*\)<\/a\>.*/\1/' | tail -1`
latest_file_name=`echo $latest_file_url | awk -F/ '{print $NF}'`
file_name=`echo $latest_file_url | awk -F/ '{print $NF}' | cut -d. -f1`

file_save_path="/tmp"

echo "
+++++++++++++++++++++++++++++++++++++++++++++++++++
  All files in url:$file_url
  ---------------------------
`wget -O - $file_url | grep href | sed 's/.*href="\(.*\)">\(.*\)<\/a\>.*/\1/'`
  ---------------------------
  Latest file is:$latest_file_name
+++++++++++++++++++++++++++++++++++++++++++++++++++"


wget $latest_file_url -P $file_save_path
if [ $? -eq 0 ]; then
    echo "
 =================================================
 Down load file sucessful
 File=$latest_file_url
 =================================================
  
  ------------------------------------------------
  Begin to extract file in $file_save_path
  ------------------------------------------------"
  chmod 777 $file_save_path/$latest_file_name
  tar -xzvf $file_save_path/$latest_file_name -C $file_save_path
  if [ $? -eq 0 ]; then
      echo "
  ------------------------------------------------
  Extract file sucessful in $file_save_path/$latest_file_name
  ------------------------------------------------
  
    **********************************************
    Begin to update data to local mongoDB
    **********************************************"
       cd $file_save_path && mongorestore --drop $file_name
       if [ $? -eq 0 ]; then
           echo "
    **********************************************
    Update data to local mongoDB sucessful
    **********************************************


==================================================
    Congratulation: 
      Latest mongo data $latest_file_name 
      update to your local ENV..
=================================================="
           exit 0
       else
           echo "
    **********************************************
    Update data to local mongoDB Failed
    Fail code = $?
    **********************************************"
    exit 2
       fi
  else
      echo "
  ------------------------------------------------
  Extract file Failed
  File=$latest_file_name
  ------------------------------------------------"
      exit 3
  fi
else
    echo "
 ==================================================
 Down load file Fail
 Fail code = $?
 ================================================="
    exit 4
fi


