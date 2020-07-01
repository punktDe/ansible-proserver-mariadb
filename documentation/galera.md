# Galera Cluster 

You can use this role to cluster multiple MariaDB servers using [Galera](https://galeracluster.com). 
Please consider reading [Galera's documentation](https://galeracluster.com/library/training/tutorials/getting-started.html) first, 
to get a basic understanding of how Galera works.

## Three-node cluster example
This is the simplest version of a cluster. It has to have at least three nodes for quorum reasons. 

Say we have three nodes in our inventory: `db01`, `db02` and `db03`. Additionally we put them into a group called `db`. Now we have to configure the database setting like above but with additional cluster variables. 

So we put the definitions for the database we want to create on the cluster into the group_vars of `db`:

group_vars/db.yaml: 
```yaml
mariadb:
  users:
    cms:
      privileges:
        cms_all:
        cms_readall: "mydb.*:select,show view"
  my.cnf:
    mysqld:
       binlog_format: ROW
    galera:
      wsrep_on: "ON"
      wsrep_provider: /usr/lib/libgalera_smm.so
      wsrep_cluster_name: '"galera-dev-cluster1"'
      wsrep_cluster_address: "\"gcomm://172.17.78.1,172.17.78.2,172.27.78.3\""
  galera:
    cluster_nodes: 172.17.78.1,172.17.78.2,172.27.78.3
```
Note the settings for my.cnf.

Now we configure the settings for the individual hosts:

host_vars/db1.yaml:
```yaml
---
mariadb:
  cms:
    hosts: 172.17.78.1
  galera:
    cluster: yes
    initializer: yes
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
    cluster: yes
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
    cluster: yes
``` 
Now you can run your playbook and the cluster will be set up

## Two-node cluster example with additional arbitrator node using garbd

This is a special case of a two-node cluster that will not result in a split-brain scenario, because of the arbitrator node. 
The arbitrator node does not store the actual data, but will record the positions and vote in the quorum. 

Please be sure you read [Galera's documentation](https://galeracluster.com/library/kb/two-node-clusters.html) for this case and understand the consequences, before using this. 

host_vars/db1.yaml:
```yaml
---
mariadb:
  cms:
    hosts: 172.17.78.1
  galera:
    cluster: yes
    initializer: yes
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
    cluster: yes
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
    cluster: yes
    arbitrator: yes
``` 
Now you can run your playbook and the cluster will be set up
