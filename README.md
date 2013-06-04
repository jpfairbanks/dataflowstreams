dataflowstreams
===============

Programming environment for streaming data centered computing
# Streaming Estimators
This repo is for my streaming estimators of statistical properties.
We start with the variance estimator which can be used to find outliers when used iteratively.
The goal is to do some data flow based programming which will allow me to comput statistical quantities online or streaming.
I would like to work on building a framework for these computations that allows the programmer to
think about where the data is going and what happens to it at each stage.
Hopefully this is a programming model that is better suited to data analysis. 
Currently most programming environments are computation focused instead of data focused. 

I am particularly interested in getting this to run in a distributed environment so that 
the different components of a program can run on different machines. 
