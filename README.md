# Mini-HPC and Hybrid HPC-Big Data Clusters Project

## Objective
This project demonstrates the creation of a Mini-HPC cluster and a Hybrid HPC-Big Data cluster using VirtualBox, Ubuntu Server, OpenMPI, Docker Swarm, and Apache Spark.

## Task 1: Mini-HPC Cluster using MPI
A three-node cluster was created using:
- master
- worker1
- worker2

OpenMPI and mpi4py were used to run distributed Python machine learning jobs.

Task 1 files:
- hostfile
- distributed_mnist.py
- distributed_gene_analysis.py
- bioinfo_data/leukemia_expression.csv

## Task 2: Hybrid HPC + Big Data Cluster using Docker Swarm and Spark
Docker Swarm was initialized on the master node, and worker nodes joined the Swarm cluster. Apache Spark was deployed using a Docker stack.

Task 2 files:
- spark-stack.yml
- distributed_gene_expression_analysis.py

## Results
The MPI distributed ML jobs completed successfully with an average score of 1.0.

The PySpark bioinformatics ML job completed successfully using Spark master and Spark workers. The dataset contained 200 samples and 20 gene features, and the final test accuracy was 1.0.

## Screenshots
The screenshots folder should include:
- VM/network setup
- SSH connection
- MPI outputs
- Docker Swarm node list
- Spark service status
- PySpark job output
