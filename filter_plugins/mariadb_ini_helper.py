def mariadb_ini_helper(sections):
    result = []
    for section, options in sections.items():
        for option, value in options.items():
            result.append({
                'section': section,
                'option': option,
                'value': value,
            })
    return result


def mariadb_ini_helper_test():
    result = mariadb_ini_helper({
        'mysqld': {
            'max_allowed_packet': '16M',
            'innodb_buffer_pool_size': '2G',
        },
        'mysqldump': {
            'max_allowed_packet': '64M',
        }
    })
    return result, result == [
        {
            'section': 'mysqld',
            'option': 'max_allowed_packet',
            'value': '16M'
        },
        {
            'section': 'mysqld',
            'option': 'innodb_buffer_pool_size',
            'value': '2G'
        },
        {
            'section': 'mysqldump',
            'option': 'max_allowed_packet',
            'value': '64M'
        },
    ]


class FilterModule(object):
    def filters(self):
        return {
            'mariadb_ini_helper': mariadb_ini_helper
        }


if __name__ == '__main__':
    print(mariadb_ini_helper_test())
