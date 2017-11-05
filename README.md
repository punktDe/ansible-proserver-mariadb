# [proserver-ansible-mariadb](https://github.com/punktDe/proserver-ansible-mariadb)

Ansible role to configure MariaDB on a proServer.

## Requirements

- A proServer
- Ansible >=2.4.0
- Ansible option `hash_behaviour` set to `merge`

## Configuration

**1)** Add the role to your playbook.
You could add this repository as submodule to your Ansible project's Git repository.

```
git submodule add https://github.com/punktDe/proserver-ansible-mariadb.git roles/mariadb
```

```yaml
---
- name: mariadb
  hosts: all
  become: yes
  roles:
    - mariadb
```

**2)** Configure what databases you'd like to have (in host vars, group vars or wherever).

```yaml
---
mariadb:
  databases:
    cms:
      name: mydb
  users:
    cms:
      username: myuser
      password: mypass
      hosts:
        cms: localhost
      privileges:
        cms_all: "mydb.*:all"
```

With these variables the role will ensure that

- there is a database `mydb`
- there is a user `myuser@localhost` with password `mypass`
- `myuser` has all privileges on `mydb`

The value `cms` and `cms_all` is never used.
You can use it to override previously defined variables
(e.g. override options from group vars in host vars).

Let's assume the example above comes from your group vars and
the example below comes from your host vars.

```yaml
---
mariadb:
  users:
    cms:
      hosts:
        cms: 172.17.78.2
      privileges:
        cms_all:
        cms_readall: "mydb.*:select,show view"
```

The role would ensure that

- there is a database `mydb`
- there is a user `myuser@172.17.78.2` with password `mypass`
- `myuser` has read privileges (`create` and `show view`) on `mydb`

## Full example

This example shows all available variables.

```yaml
---
mariadb:
  database_defaults:
    encoding: utf8mb4
    collation: utf8mb4_unicode_ci
  databases:
    example_db:
      encoding: utf8mb4
      collation: utf8mb4_unicode_ci
      name: example
  users:
    example_user:
      username: example
      password: example
      hosts:
        example_host: localhost
      privileges:
        example_privilege: "example.*:all"
```
