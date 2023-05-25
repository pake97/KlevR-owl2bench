./dataset.sh >dataset.log

#for reasoning tasks on hermit pellet openllet and jfact
./reasoningTasks1.sh >hermitpelletopenlletjfact.log

grep -B 1 -i "Finished Reasoner:" hermitpelletopenlletjfact.log >reasoningTimeHermiTPelletOpenlletJFact.log