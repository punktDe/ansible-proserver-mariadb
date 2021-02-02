#!/usr/bin/env python3
import unittest
from typing import Iterable


class MariaDB:
    @staticmethod
    def subelem_dicts_to_list(dicts, path):
        result = []
        for dictelem in dicts:
            subelem = dictelem
            for pathelem in path.split("."):
                prev_subelem = subelem
                subelem = subelem[pathelem]
            prev_subelem[pathelem] = sum(
                [
                    x if isinstance(x, Iterable) and not isinstance(x, str) else [x]
                    for x in subelem.values()
                ],
                [],
            )
            result.append(dictelem)
        return result


class MariaDBTest(unittest.TestCase):
    def test_subelem_dicts_to_list(self):
        self.assertEqual(
            MariaDB.subelem_dicts_to_list(
                [
                    {
                        "a": {
                            "b": {
                                "c": "g1",
                                "d": "h1",
                            }
                        }
                    },
                    {
                        "a": {
                            "b": {
                                "e": "i1",
                                "f": [
                                    "j1",
                                    "k1",
                                    "l1",
                                ],
                            }
                        }
                    },
                ],
                "a.b",
            ),
            [
                {
                    "a": {
                        "b": [
                            "g1",
                            "h1",
                        ]
                    }
                },
                {
                    "a": {
                        "b": [
                            "i1",
                            "j1",
                            "k1",
                            "l1",
                        ]
                    }
                },
            ],
        )


class FilterModule(object):
    def filters(self):
        return {"mariadb_subelem_dicts_to_list": MariaDB.subelem_dicts_to_list}


if __name__ == "__main__":
    unittest.main()
