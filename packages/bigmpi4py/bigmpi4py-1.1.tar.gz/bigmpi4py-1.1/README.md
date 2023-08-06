# BigMPI4py

BigMPI4py is a module developed based on Lisando Dalcin's implementation of Message Passing 
Interface (MPI for short) for python, MPI4py (https://mpi4py.readthedocs.io), which allows for
parallelization of data structures within python code. 

Although many of the common cases of parallelization can be solved with MPI4py alone, there
are cases were big data structures cannot be distributed across cores within MPI4py 
infrastructure. This limitation is well known for MPI4py and happens due to the fact that MPI 
calls have a buffer limitation of 2GB entries. 

In order to solve this problem, some solutions exist, like dividing the datasets in "chunks" that
satisfy the data size criterion, or using other MPI implementations such as BigMPI 
(https://github.com/jeffhammond/BigMPI). BigMPI requires both understanding
the syntax of BigMPI, as well as having to adapt python scripts to BigMPI, which can be 
difficult and requires knowledge of C-based programming languages, of which many users have a 
lack of. Then, the "chunking" strategy can be used in Python, but has to be adapted manually for 
data types and, in many cases, the number of elements that each node will receive which, in order
to circumvent the 2 GB problem, can be difficult.

BigMPI4py adapts the "chunking" strategy of data, being able to automatically distribute 
the most common python
data types used in python, such as numpy arrays, pandas dataframes, lists, nested lists, 
or lists of 
arrays and dataframes. Therefore, users of BigMPI4py can automatically parallelize their 
pipelines by calling BigMPI4py's functions with their data.

So far, BigMPI4py implements certain MPI's collective communication operations, like
`MPI.Comm.scatter()`, `MPI.Comm.bcast()`, `MPI.Comm.gather()` or `MPI.Comm.allgather()`, which 
are the most commonly used ones in parallelization.  BigMPI4py also implements point-to-point 
communication operation `MPI.Comm.sendrecv()`.

BigMPI4py also detects whether a vectorized parallelization using `MPI.Comm.Scatterv()` and 
`MPI.Comm.Gatherv()` operations can be used, saving time for object communication. 

Check out the tutorial notebook to see how to use BigMPI4py.

Also, look up our paper in bioRxiv to see how the software works.
https://www.biorxiv.org/content/early/2019/01/17/517441

Alex M. Ascensión and Marcos J. Araúzo-Bravo. BigMPI4py: Python module for parallelization of Big Data objects; bioRxiv, (2019). doi: 10.1101/517441. 

