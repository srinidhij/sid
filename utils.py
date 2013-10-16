#!/usr/bin/python

# Utitlites for simulation of datacenter networking

# author Srinidhi J <srinidhij.21@gmail.com>

# see LICENSE.md for copying

__author__ = "Srinidhi J <srinidhij.21@gmail.com>"

from random import random, randint, choice
import string

class VM(object):
    """Class to represent a virtual machine 
    inside a particular datacenter node 
    """
    def __init__(self, rackid, vmid=None, ip=None):
        super(VM, self).__init__()

        if not isinstance(rackid,int):
            raise ValueError, "rackid has to be an integer"

        self.rackid = rackid

        if vmid is None:
            pass
            #create a random vmid          
        
        if ip is None:
            pass
            #random ip

    def genrandip(self):
        ipstr = ''
        for i in range(4):
            ipstr += str(choice(range(1,256)))+'.'
        return ipstr[:-1]

class Rack(object):
    """Class to represent a datacenter node
    """
    def __init__(self, rackid=None):
        super(Rack, self).__init__()
        
        if rackid is None:
           #create a random rackid
            rackid = randint(1,100)
 
        self.rackid = rackid    
        self.vms = list()

    def addvm(self, vm=None):
        
        if vm is None:
            vm = VM(rackid=self.rackid)

        if not isinstance(vm,VM):
            pass
            #raise error

        #add it to rack
        tmp['vmid'] = vm.vmid
        tmp['ip'] = vm.ip
        tmp['rackid'] = vm.rackid
        self.vms.append(tmp)
    
    def delvm(self, vm): 
        if not isinstance(vm,VM):
            pass
            #raise error

        #if not vm in data:
            #raise

def tests():
    tvm = VM(rackid=0)
    for i in range(10):
        print tvm.genrandip()
       
if __name__ == '__main__':
     tests() 