#! /bin/bash


script_path=`pwd`
path=/Users/eunmi/Desktop/connectome/sample_data

source ~/.bashrc

for sub in  `ls $path`
do 
    sub_path=${path}/${sub}
    echo $sub_path
    #python3 get_freeview_utils.py -sub_path $sub_path   
    #cd $sub_path #has to go here direclty for some reason
    #freeview -cmd cmd_txt.txt
    #cd $script_path #goes back

    #python get_freeview_utils.py -sub_path /Users/eunmi/Desktop/connectome/sample_data/sub-140989
    #sdkljfsdlkjf #intentially to raise error 
done



