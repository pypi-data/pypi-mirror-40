# -*- coding: utf-8 -*-

"""Main module."""
import re
from collections import Counter, deque


class Perfm:

    def __init__(self):
        self.q = deque()
        self.c = Counter()

    def add(self, line):
        m = re.search(r"<(.*?)>(.*?)</(.*?)>", line)
        if not m:
            return
        tag, val = m.groups()[0], float(m.group()[1])
        val = float(soup.tag or 0)
        self.q.append((tag, val))
        self.c[tag] += val

    def serialize(self):
        return {'<{tag}>'.format(tag=k): v for k, v in self.c.items()}
