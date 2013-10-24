#!/usr/bin/python

# Utitlites for simulation of datacenter networking

# author Srinidhi J <srinidhij.21@gmail.com>

# see LICENSE.md for copying

__authors__ = ["Srinidhi J <srinidhij.21@gmail.com>",
               "ShriKrishna Holla <shrikrishna.holla@gmail.com>"]

from random import random, randint, choice
import string

class VM(object):
    """Class to represent a virtual machine 
    inside a particular datacenter node 
    """
    vmids = []
    def __init__(self, rackid, vmid):
        super(VM, self).__init__()

        if not isinstance(rackid,int):
            raise ValueError, "rackid has to be an integer"

        self.vmid = vmid
        self.rackid = rackid
        self.ip = self.getip()


    def getip(self):
        return '172.16'+'.'+str(self.rackid)+'.'+str(self.vmid)

class Rack(object):
    """Class to represent a datacenter node
    """

    def __init__(self,rackid):
        self.rackid = rackid
        self.vmids=[]
    def addvm(self):
        vmid = 0
        if len(self.vmids) == 0:
            vmid = 0
        else:
            vmid = self.vmids[-1]['vmid']+1

        vm = VM(rackid=self.rackid, vmid=vmid)

        #add it to rack
        vminfo = {}

        vminfo['vmid'] = vm.vmid
        vminfo['ip'] = vm.ip
        vminfo['rackid'] = vm.rackid
        self.vmids.append(vminfo)

    def delvm(self, vm): 
        if not isinstance(vm,VM):
            pass
            #raise error

        #if not vm in data:
            #raise

    def __str__(self):
        return self.vmids.__str__()

class DataCenter(object):

    def __init__(self):
        self.rackids = []
        super(DataCenter, self).__init__()

    def addrack(self):
        rackid = 0
        if len(self.rackids) == 0:
            rackid = 0
            self.rackids.append(rackid)
        else:
            rackid = self.rackids[-1]+1
            self.rackids.append(rackid)
        rack = Rack(rackid)
        return rack


def tests():
    d = DataCenter()
    r1 = d.addrack()
    for i in range(10):
        r1.addvm()

    r2 = d.addrack()
    for i in range(10):
        r2.addvm()

    print r1
    print '-'*80
    print r2
       
if __name__ == '__main__':
     tests() 
