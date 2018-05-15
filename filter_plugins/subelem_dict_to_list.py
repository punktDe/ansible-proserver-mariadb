def subelem_dicts_to_list(dicts, path):
    result = []
    for dictelem in dicts:
        subelem = dictelem
        for pathelem in path.split('.'):
            prev_subelem = subelem
            subelem = subelem[pathelem]
        prev_subelem[pathelem] = list(subelem.values())
        result.append(dictelem)
    return result


def subelem_dicts_to_list_test():
    result = subelem_dicts_to_list([
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
                    'f': 'j',
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
                ]
            }
        }
    ]


class FilterModule(object):
    def filters(self):
        return {
            'subelem_dicts_to_list': subelem_dicts_to_list
        }


if __name__ == '__main__':
    print(subelem_dicts_to_list_test())
