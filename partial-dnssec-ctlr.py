from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *


def main():
    return  if_(match(dstip=IPAddr('10.0.0.1')), fwd(1),
                if_(match(dstip=IPAddr('10.0.0.2')), fwd(2), 
                    fwd(3)))

