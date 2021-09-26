run: 
	python formatInput.py -a Nashville | ./jgraph -P | ps2pdf - map1.pdf
	python formatInput.py -a TNMap | ./jgraph -P | ps2pdf - map2.pdf
	python formatInput.py -a Knoxville -z .5 | ./jgraph -P | ps2pdf - map3.pdf
	python formatInput.py -a Knoxville -b Nashville | ./jgraph -P | ps2pdf - map4.pdf
	python formatInput.py -a Memphis -b Knoxville | ./jgraph -P | ps2pdf - map5.pdf
