# Arbitrator

## Two-node cluster example with additional arbitrator node using garbd

This is a special case of a two-node cluster that will not result in a split-brain scenario, because of the arbitrator node. 
The arbitrator node does not store the actual data, but will record the positions and vote in the quorum. 

Please be sure you read [galera's documentation](https://galeracluster.com/library/kb/two-node-clusters.html) for this case and understand the consequences, before using this. 

host_vars/db1.yaml:
```yaml
---
mariadb:
  cms:
    hosts: 172.17.78.1
  galera:
    cluster: True
    initializer: True
``` 
This node is the initializer, which means the cluster is bootstrapped on this node and the other nodes join into the bootstrapped cluster.

host_vars/db2.yaml:
```yaml
---
mariadb:
  users:
    cms:
      hosts:
        cms: 172.17.78.2
  galera:
    cluster: True
``` 

host_vars/db3.yaml:
```yaml
---
mariadb:
  users:
    cms:
      hosts:
        cms: 172.17.78.3
  galera:
    cluster: True
    arbitrator: True
``` 
Now you can run your playbook and the cluster will be set up
