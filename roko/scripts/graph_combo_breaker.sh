#!/bin/bash

declare -a label=( "true" "false" )
declare -a module=( "specific" "general" "social" "meta" "health" "learning" "none" )

for i in "${label[@]}"
do
	for j in "${module[@]}"
	do 
		if [ $i == "true" ]
		then 
			l="labelled"
		else
			l="unlabelled"
		fi
		filename="${l}_${j}.txt"
		python grapher.py dialogues.txt $i $j > "${l}_txt/${filename}"
	done
done
		
