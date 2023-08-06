# -*- coding: utf-8 -*-

"""Console script for perfm."""
import sys
import click
from perfm.perfm import Perfm
import subprocess



def process_log(s, f, res):
    p = Perfm()
    if s == 'file':
        output = open(f, 'r').read()
    else:
        output = res.stdout
    for line in output.split('\n'):
        p.add(line)
    return p


@click.command()
@click.option('--s', default='std', help='data stats source')
@click.option('--f', default='output.xml', help='data stats file name')
@click.argument('func_call_args', nargs=-1)
def main(s, f, func_call_args):
    res = subprocess.run(func_call_args, shell=True, check=True, stdout=subprocess.PIPE)
    p = process_log(s, f, res)
    print(p.serialize())



if __name__ == "__main__":
    main()
