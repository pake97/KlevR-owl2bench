#!/bin/bash
# all reasoner commands

#the OWL2Bench.jar was created from the source code given in the github repository.

#make sure the other files: TBoxes and RandomName.xlsx are present in the same directory as OWL2Bench.jar 


for profile in EL #QL RL #DL
do
	for mode in 1 2 3
	do
		for objects in  50 #100 200 500 1000 2000 5000 10000
		do
			for inc in True False
			do
				python3 klevRDatasetGenerator.py /resources/dataset/CLEVR_v1.0/scenes/CLEVR_train_scenes.json /resources/dataset/CLEVR_v1.0/scenes/CLEVR_val_scenes.json 1 $objects $mode $inc $profile 
				rm ABox.owl
			done
		done
	done
done

