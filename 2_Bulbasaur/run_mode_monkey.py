#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests


def main():
    url = 'http://127.0.0.1:8886/run?mode=monkey'
    response = requests.get(url)
    res_json = response.json()
    print(res_json)


if __name__ == '__main__':
    main()
