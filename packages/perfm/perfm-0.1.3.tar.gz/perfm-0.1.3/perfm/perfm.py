# -*- coding: utf-8 -*-

"""Main module."""

from collections import Counter, deque
from bs4 import BeautifulSoup


class Perfm:

    def __init__(self):
        self.q = deque()
        self.c = Counter()

    def add(self, line):
        soup = BeautifulSoup(line, features='lxml').find()
        if not soup:
            return
        tag = soup.name
        val = float(soup.tag or 0)
        self.q.append((tag, val))
        self.c[tag] += val

    def serialize(self):
        return {'<{tag}>'.format(tag=k): v for k, v in self.c.items()}
