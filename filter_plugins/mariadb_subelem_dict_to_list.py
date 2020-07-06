import itertools


def mariadb_subelem_dicts_to_list(dicts, path):
    result = []
    for dictelem in dicts:
        subelem = dictelem
        for pathelem in path.split('.'):
            prev_subelem = subelem
            subelem = subelem[pathelem]
        prev_subelem[pathelem] = list(itertools.chain.from_iterable(subelem.values()))
        result.append(dictelem)
    return result


def mariadb_subelem_dicts_to_list_test():
    result = mariadb_subelem_dicts_to_list([
        {
            'a': {
                'b': {
                    'c': 'g',
                    'd': 'h',
                }
            }
        },
        {
            'a': {
                'b': {
                    'e': 'i',
                    'f': [
                        'j',
                        'k',
                        'l',
                    ],
                }
            }
        }
    ], 'a.b')
    return result, result == [
        {
            'a': {
                'b': [
                    'g',
                    'h',
                ]
            }
        },
        {
            'a': {
                'b': [
                    'i',
                    'j',
                    'k',
                    'l',
                ]
            }
        }
    ]


class FilterModule(object):
    def filters(self):
        return {
            'mariadb_subelem_dicts_to_list': mariadb_subelem_dicts_to_list
        }


if __name__ == '__main__':
    print(mariadb_subelem_dicts_to_list_test())
