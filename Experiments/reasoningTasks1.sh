#!/bin/bash
# Reasoner commands
# the reported time was an average of results obtained in 5 iterations. Since, the results could be Time-outs, memory errors or other errors, the average was performed manually.

#for reasoner in hermit pellet openllet jfact
#do

#	for profile in OWL2EL OWL2QL OWL2RL OWL2DL
#	do
#		for task in consistency realisation classification
#		do
#			for univ in 1 2 5 10 20 50 100 200
#			do
#				for i in 1 2 3 4 5
#				do
#					sleep 5
#					file_path=
#					file_name="$file_path$profile-$univ.owl"



					
#					timeout 5400 java -jar $reasoner.jar $file_name $task

#					echo "Finished Reasoner: $reasoner File: $profile-$univ.owl Task: $task University: $univ Iteration: $i"
#				done
#			done
#		done
#	done
#done


for reasoner in hermit pellet openllet jfact
do
	for task in consistency realisation classification
	do
		for profile in EL #QL RL #DL
		do
			for mode in 1D 2D 3D
			do
				for objects in  50 #100 200 500 1000 2000 5000 10000
				do
					for inc in True False
					do
						for i in 1 2 3 4 5
						do
							sleep 5
							file_name=""
							if [ "$inc" = True ]
							then
								file_name="$objects$mode$profile-inconsistent-KlevR.owl"
							else
								file_name="$objects$mode$profile-KlevR.owl"
							fi
							
							timeout 5400 java -jar $reasoner.jar $file_name $task

							echo "Finished Reasoner: $reasoner File: $profile-$univ.owl Task: $task University: $univ Iteration: $i"
						done
					done
				done
			done
		done
	done
done








