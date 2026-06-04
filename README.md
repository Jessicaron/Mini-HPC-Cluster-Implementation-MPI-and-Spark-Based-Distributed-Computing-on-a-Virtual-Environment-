
# Mini-HPC Cluster Implementation: MPI and Spark-Based Distributed Computing

A distributed computing and bioinformatics project that demonstrates how to build a Mini High-Performance Computing (HPC) cluster using **Ubuntu Server virtual machines**, **OpenMPI**, **Docker Swarm**, and **Apache Spark** for distributed machine learning and bioinformatics workflows.


# Name
Jessica Amgad Anis  ID 231001218 
Abdalrahman Mohamed Abdo  ID 231001347 
Merna Ashraf Daneal   ID:221000689 
---

## 📌 Project Overview

This project builds a Mini-HPC cluster composed of:

- **1 Master Node**
- **2 Worker Nodes**

The cluster was implemented using **Oracle VirtualBox** with Ubuntu Server 20.04 virtual machines connected through a private Host-only network. Distributed jobs were executed using:

- **OpenMPI + mpi4py**
- **Docker Swarm**
- **Apache Spark**
- **PySpark**

The project demonstrates distributed machine learning and bioinformatics analysis using both MPI and Spark frameworks.

---

# 🏗️ Cluster Architecture

| Node | Role | IP Address |
|---|---|---|
| master | Cluster Manager | 192.168.56.10 |
| worker1 | Compute Node | 192.168.56.11 |
| worker2 | Compute Node | 192.168.56.12 |

All nodes communicate using a Host-only private network (`192.168.56.0/24`).

---

# ⚙️ Technologies Used

- Ubuntu Server 20.04 LTS
- Oracle VirtualBox
- OpenMPI
- mpi4py
- Python 3
- Scikit-learn
- Pandas
- NumPy
- Docker
- Docker Swarm
- Apache Spark 3.5.0
- PySpark

---

# 🎯 Project Objectives

The main goals of this project were:

- Build a Mini-HPC cluster using Virtual Machines
- Configure distributed networking between nodes
- Enable passwordless SSH communication
- Execute distributed MPI-based machine learning jobs
- Deploy a Spark cluster using Docker Swarm
- Run distributed bioinformatics analysis using Spark

---

# 🖥️ Virtual Machine Configuration

Each VM was configured with:

| Resource | Configuration |
|---|---|
| OS | Ubuntu Server 20.04 |
| RAM | 4096 MB |
| CPU | 2 Processors |
| Disk | 20 GB |
| Disk Type | VDI |
| Storage | Dynamically Allocated |

---

# 🌐 Networking Setup

The nodes were connected using a **Host-only Adapter** inside VirtualBox.

## Network Range

```bash
192.168.56.0/24
```

## Connectivity Testing

```bash
ping worker1
ping worker2
```

All nodes successfully communicated with `0% packet loss`.

---

# 🔐 Passwordless SSH Setup

SSH key authentication was configured from the master node to worker nodes.

## Generate SSH Key

```bash
ssh-keygen -t rsa
```

## Copy Public Key

```bash
ssh-copy-id user@worker1
ssh-copy-id user@worker2
```

## Test SSH Connection

```bash
ssh user@worker1
hostname
```

This allowed MPI jobs to launch automatically across nodes without password prompts.

---

# 📦 OpenMPI & Python Environment Setup

The following packages were installed on all nodes:

```bash
sudo apt update
sudo apt install openmpi-bin libopenmpi-dev python3 python3-pip -y
pip3 install mpi4py scikit-learn pandas numpy
```

## Verify MPI Installation

```bash
mpirun --version
```

---

# 📝 Hostfile Configuration

A hostfile was created to define MPI nodes and processing slots.

## hostfile

```bash
master slots=2
worker1 slots=2
worker2 slots=2
```

Total MPI slots: **6**

---

# 📊 Dataset Information

## 1. Digits Dataset

- Built-in scikit-learn dataset
- Used for distributed digit classification

## 2. Gene Expression Dataset

- File: `leukemia_expression.csv`
- 200 samples
- 20 gene expression features
- Diagnosis label for classification

---

# 🧠 Distributed MPI Machine Learning Job

## Script

```bash
distributed_mnist.py
```

## Run Command

```bash
mpirun -np 6 --hostfile hostfile \
--mca btl_tcp_if_include enp0s8 \
--mca oob_tcp_if_include enp0s8 \
--mca btl ^openib \
--wdir /tmp/hpc \
python3 distributed_mnist.py
```

## Output

```bash
Scores from all nodes: [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
Average score: 1.0
```

---

# 🧬 Distributed MPI Bioinformatics Job

## Script

```bash
distributed_gene_analysis.py
```

## Run Command

```bash
mpirun -np 6 --hostfile ~/hostfile \
--mca btl_tcp_if_include enp0s8 \
--mca oob_tcp_if_include enp0s8 \
--mca btl ^openib \
--wdir /tmp/hpc \
python3 distributed_gene_analysis.py
```

## Output

```bash
Bioinformatics scores from all nodes:
[1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

Average score: 1.0
```

---

# 🐳 Docker Swarm Setup

Docker was installed on all nodes and a Docker Swarm cluster was initialized.

## Initialize Swarm

```bash
sudo docker swarm init --advertise-addr 192.168.56.10
```

## Add Worker Nodes

```bash
sudo docker swarm join --token <TOKEN> 192.168.56.10:2377
```

## Verify Cluster

```bash
sudo docker node ls
```

---

# ⚡ Spark Cluster Deployment

Apache Spark was deployed using Docker Swarm.

## Docker Image

```bash
spark:3.5.0
```

## Deploy Stack

```bash
sudo docker stack deploy -c spark-stack.yml hpc
```

## Verify Services

```bash
sudo docker service ls
```

Expected output:

```bash
hpc_spark-master   1/1
hpc_spark-worker   2/2
```

---

# 🔬 Distributed Spark Bioinformatics Job

## Script

```bash
distributed_gene_expression_analysis.py
```

## Spark Submit Command

```bash
spark-submit \
--master spark://spark-master:7077 \
--executor-memory 512m \
--driver-memory 512m \
--total-executor-cores 2 \
distributed_gene_expression_analysis.py
```

## Output

```bash
Distributed Spark ML completed successfully
Bioinformatics dataset rows: 200
Number of gene features: 20
Test accuracy: 1.0
```

---

# 📈 Results Summary

| Job | Framework | Result |
|---|---|---|
| Distributed Digit Classification | MPI | Accuracy = 1.0 |
| Distributed Gene Expression | MPI | Accuracy = 1.0 |
| Distributed Gene Expression | Spark | Accuracy = 1.0 |

---

# ⚠️ Limitations

- All nodes ran on the same physical machine
- No execution time measurements were recorded
- Small dataset partitions caused unrealistically perfect scores
- Screenshots referenced in the report were missing

---

# 🛠️ MPI Troubleshooting

An MPI communication issue occurred because OpenMPI attempted to use multiple network interfaces.

## Solution

```bash
--mca btl_tcp_if_include enp0s8
--mca oob_tcp_if_include enp0s8
--mca btl ^openib
```

This forced MPI to use only the Host-only network interface.

---

# 📂 Project Structure

```bash
project_hpc_hybrid_cluster/
│
├── hostfile
├── distributed_mnist.py
├── distributed_gene_analysis.py
├── distributed_gene_expression_analysis.py
├── spark-stack.yml
├── bioinfo_data/
│   └── leukemia_expression.csv
├── screenshots/
├── setup_log.txt
└── Final_Report.md
```

---

# 🚀 Future Improvements

- Use physical or cloud-based nodes
- Add execution time benchmarking
- Use real-world biological datasets
- Implement cross-validation and global testing
- Add monitoring and resource visualization tools

---

# 📚 References

- OpenMPI Documentation
- mpi4py Documentation
- Scikit-learn Documentation
- Apache Spark Documentation
- Docker Swarm Documentation
- Ubuntu Server Documentation
- Oracle VirtualBox Documentation
