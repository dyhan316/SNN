#! /bin/bash


script_path=`pwd`
path=/Users/eunmi/Desktop/connectome/sample_data

source ~/.bashrc

for sub in  `ls $path`
do 
    sub_path=${path}/${sub}
    echo $sub_path
    python3 get_freeview_utils_2.py -sub_path $sub_path
done



