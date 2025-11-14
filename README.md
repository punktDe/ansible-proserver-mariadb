<!-- BEGIN_ANSIBLE_DOCS -->
<!--
Do not edit README.md directly!

This file is generated automatically by aar-doc and will be overwritten.

Please edit meta/argument_specs.yml instead.
-->
# ansible-proserver-mariadb

mariadb role for Proserver

## Supported Operating Systems

- Debian 12
- Ubuntu 24.04, 22.04
- FreeBSD [Proserver](https://infrastructure.punkt.de/de/produkte/proserver.html)

## Role Arguments



Installs and configures MariaDB on Debian/Ubuntu and FreeBSD based systems.

Supports single-node deployments as well as Galera clusters (including garbd arbitrator nodes).

Handles database creation, user management and optional automated backups.

#### Options for `mariadb`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `version` | MariaDB major.minor version to install. Used to build repository URLs and to pick compatible packages. | str | no | 11.8 |
| `prefix` | Base directories for MariaDB configuration files. | dict of 'prefix' options | no | {} |
| `socket` | Path to the MariaDB UNIX socket used by `mysql` CLI modules and health checks. | str | no | {% if ansible_system == 'Linux' %}/run/mysqld/mysqld.sock{% else %}/tmp/mysql.sock{% endif %} |
| `service` | Systemd/rc service name that is controlled by the role. | str | no | {% if ansible_system == 'Linux' %}mysql{% else %}mysql-server{% endif %} |
| `repository` | Optional vendor repository configuration (currently only APT is supported). | dict of 'repository' options | no |  |
| `my.cnf` | Declarative representation of the contents that should end up in `zz-ansible.cnf`. Keys correspond to section names (`mysqld`, `mysqld_safe`, `galera`, ...); nested keys represent option/value pairs. Values set to `null` remove the option from the rendered file. | dict | no |  |
| `database_defaults` | Fallback charset/collation used when a database entry omits explicit values. | dict of 'database_defaults' options | no | {'encoding': 'utf8mb4', 'collation': 'utf8mb4_unicode_ci'} |
| `databases` | Declarative list of databases to create; keys are arbitrary identifiers. Each entry must set `name` and can optionally define `encoding`, `collation`, `import_file`, or a nested `backup` dict with the same shape as `mariadb.backup` for per-database overrides. When `import_file` is present, the local file is uploaded and restored immediately after creation. | dict | no |  |
| `users` | Database users and grants to configure; keys are arbitrary user identifiers. Each entry expects `password`, a `hosts` mapping (values can be strings or lists) and a `privileges` dict whose values follow the `<db>.<table>:priv1,priv2` syntax consumed by `community.mysql.mysql_user`. The role will iterate over every host in `hosts` and apply the merged privilege strings. | dict | no |  |
| `galera` | Settings that control Galera behaviour. | dict of 'galera' options | no | {} |
| `backup` | Controls whether automated dumps are made and when they run. | dict of 'backup' options | no | {} |

#### Options for `mariadb.prefix`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `config` | Parent directory that will contain `conf.d`/`mariadb.conf.d`. Change this only when using custom filesystem layouts. | str | no | {% if ansible_system == 'Linux' %}/etc/mysql{% else %}/usr/local/etc/mysql{% endif %} |

#### Options for `mariadb.repository`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `apt` | Repository definition that will be managed on Debian/Ubuntu hosts. | dict of 'apt' options | no | {} |

#### Options for `mariadb.repository.apt`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `key_url` | URL of the GPG key used to sign the MariaDB packages. | str | no | https://mirror.netcologne.de/mariadb/PublicKey |
| `repository` | deb822 repository URL that will be added through `ansible.builtin.deb822_repository`. You can point this to an internal mirror if required. | str | no | http://mirror.netcologne.de/mariadb/repo/{{ vars.mariadb.version }}/{{ ansible_distribution | lower }} |

#### Options for `mariadb.database_defaults`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `encoding` | Default character set handed to `community.mysql.mysql_db`. | str | no | utf8mb4 |
| `collation` | Default collation for new databases. | str | no | utf8mb4_unicode_ci |

#### Options for `mariadb.galera`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `cluster` | Enable Galera cluster orchestration. | bool | no | False |
| `initializer` | Flag the current node as the bootstrap/seed node. | bool | no | False |
| `arbitrator` | Configure the host as a garbd arbitrator instead of a full data node. | bool | no | False |
| `join` | Tuning knobs for cluster join/health checks (used by `has_joined_cluster.sh`). | dict of 'join' options | no | {} |

#### Options for `mariadb.galera.join`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `max_wait` | Total time in seconds to wait for a node to become ready. | int | no | 300 |
| `check_pause` | Sleep interval (seconds) between readiness checks. | int | no | 1 |

#### Options for `mariadb.backup`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `enabled` | Enables the backup script/timer globally. Databases can override this flag individually via `mariadb.databases.<name>.backup.enabled`. | bool | no | False |
| `timer` | Raw content injected into the `[Timer]` section of `mariadb-backup.timer`. | str | no | OnCalendar=*-*-* 00:00:00
RandomizedDelaySec=6h |
| `mysqldump` | Ordered dictionary of command-line fragments used to build the mysqldump command. Keys are only used for sorting; values are literal CLI arguments. | dict | no | {"0": "mysqldump", "50_single_transaction": "--single-transaction"} |
| `structure_only` | Mapping of table names to booleans; tables set to `true` are exported using `--no-data`. | dict | no |  |
| `compression` | Controls compression of dump files. | dict of 'compression' options | no | {} |
| `dest` | Directory on the target host where dump files are written (permanent location). | str | no | /var/mariadb-backups |
| `send_application_event` | Enables writing structured metrics into `application_event_log` after each backup run. | bool | no | False |
| `application_event_log` | Path to the log file that captures backup metrics when `send_application_event` is enabled. | str | no | /var/log/application_events/MariaDB-Backup.log |

#### Options for `mariadb.backup.compression`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `enabled` | Whether to pipe mysqldump output through the compression command. | bool | no | True |
| `command` | Binary executed when `compression.enabled` is true. | str | no | gzip |
| `extension` | File suffix appended to compressed dumps. | str | no | gz |

## Dependencies
None.

## Installation
Add this role to the requirements.yml of your playbook as follows:
```yaml
roles:
  - name: ansible-proserver-mariadb
    src: https://github.com/punktDe/ansible-proserver-mariadb
```

Afterwards, install the role by running `ansible-galaxy install -r requirements.yml`

## Example Playbook

```yaml
- hosts: all
  roles:
    - name: mariadb
```

<!-- END_ANSIBLE_DOCS -->
