# Bonus Extensions

This folder contains the bonus extension files for the Mini-HPC and Hybrid HPC-Big Data Clusters project.

## Bonus Extension 1: Fourth VM Node Benchmark

A fourth virtual machine node was added to the Mini-HPC cluster.

Node information:
- Hostname: worker3
- IP address: 192.168.56.13
- Role: Additional MPI worker node

A new hostfile was created to include the fourth node:

master slots=2
worker1 slots=2
worker2 slots=2
worker3 slots=2

This increased the total number of MPI slots from 6 to 8.

Benchmark results:
- 3 nodes / 6 MPI processes: 2.09 seconds
- 4 nodes / 8 MPI processes: 2.39 seconds

The 4-node MPI job completed successfully, but it was not faster than the 3-node run because the dataset was small and the MPI communication overhead was higher than the benefit of adding another node.

## Bonus Extension 2: Prometheus and Grafana Monitoring

A monitoring stack was deployed using Docker Swarm. The stack included:
- Prometheus
- Grafana
- node-exporter

The final Docker service status was:
- monitor_grafana: 1/1
- monitor_prometheus: 1/1
- monitor_node-exporter: 3/3

Prometheus was accessed at:
http://192.168.56.10:9090

Grafana was accessed at:
http://192.168.56.10:3000

The query `up` was used in both Prometheus and Grafana to confirm that the monitored services were active. A value of 1 confirmed that the services were reachable and running successfully.

## Screenshots

The screenshots folder should include:
- 4th VM benchmark comparison screenshot
- Docker service list showing monitoring services
- Prometheus `up` query screenshot
- Grafana Explore `up` query screenshot
