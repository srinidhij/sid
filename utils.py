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

    def delvm(self, vmid): 
        if not isinstance(vmid, int):
            raise ValueError('vmid has to be int')

        vmidlist = [vm['vmid'] for vm in self.vmids]
        if not vmid in vmidlist:
            raise ValueError('incorrect vmid. Not possible to delete')

        self.vmids = [vm for vm in self.vmids if vm['vmid'] != vmid]

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

class LoadBalancer(object):
    """LoadBalancer"""
    def __init__(self, no_of_racks):
        super(LoadBalancer, self).__init__()
        self.dc = DataCenter()
        self.racks = []
        if not no_of_racks or no_of_racks <= 0:
            raise ValueError("Number of racks has to be more than one")
        for x in xrange(0,no_of_racks):
            self.racks.append(self.dc.addrack())

    def newuser(self):
        suitable_rack = reduce(lambda rack1, rack2:
            rack1 if len(rack1.vmids) <= len(rack2.vmids) else rack2, self.racks)
        suitable_rack.addvm()
        print "User added to rack", suitable_rack.rackid
        
    def remuser(self, rackid, vmid):
        suitable_rack = filter(lambda rack: rack.rackid == rackid, self.racks)
        if len(suitable_rack) == 0:
            raise ValueError('There are no racks with the given rackid')
        elif len(suitable_rack) > 1:
            raise ValueError('There is more than one rack with the given rackid!')
        else:
            suitable_rack = suitable_rack[0]
        suitable_rack.delvm(vmid)
        print 'User quit from', suitable_rack.rackid

    def stats(self):
        for rack in self.racks:
            print 'Rack',rack.rackid,':',len(rack.vmids),'Users/VMs'

def tests():
    # d = DataCenter()
    # r1 = d.addrack()
    # for i in range(10):
    #     r1.addvm()

    # r2 = d.addrack()
    # for i in range(10):
    #     r2.addvm()

    # print r1
    # print '-'*80
    # print r2

    lb = LoadBalancer(3)
    lb.stats()
    for x in xrange(1,11):
        lb.newuser()
    lb.stats()
       
if __name__ == '__main__':
     tests() 
