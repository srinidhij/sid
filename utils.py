#!/usr/bin/python

# Utitlites for simulation of datacenter networking

# author Srinidhi J <srinidhij.21@gmail.com>

# see LICENSE.md for copying

__authors__ = ["Srinidhi J <srinidhij.21@gmail.com>",
               "ShriKrishna Holla <shrikrishna.holla@gmail.com>"]

from random import random, randint, choice
import string
from twowaydict import BiDiDict
import itertools

class VM(object):
    """Class to represent a virtual machine 
    inside a particular datacenter node 
    """
    def __init__(self, rackid, vmid):
        super(VM, self).__init__()

        if not isinstance(rackid,int):
            raise ValueError, "rackid has to be an integer"

        # Assigning an id to the Virtual Machine
        self.vmid = vmid

        # The id of the rack to which this VM belongs
        self.rackid = rackid

        # The IP address of this VM
        self.ip = self.getip()


    def getip(self):
        # TODO: Get ip of the docker container
        return '172.16'+'.'+str(self.rackid)+'.'+str(self.vmid)

    def __str__(self):
        print "R"+self.rackid+"VM"+self.vmid

class Rack(object):
    """Class to represent a datacenter node
    """

    def __init__(self,rackid):
        # The unique id that identifies this rack
        self.rackid = rackid
        # A dictionary of the id and info of VMs that belong to this rack
        self.vmids={}

    def addvm(self):
        """Add a VM to this rack"""
        vmid = 0
        try:
            # TODO: Get VMid when creating a docker container
            vmid = max(self.vmids.keys())+1
        except ValueError:
            vmid = 0

        vm = VM(rackid=self.rackid, vmid=vmid)

        #add it to rack
        # Info of the VM that will be stored in this rack
        self.vmids[vm.vmid] = {
            'id':vm.vmid,
            'ip': vm.ip,
            'rackid': vm.rackid,
            'vmobj':vm
        };
        return vm

    def delvm(self, vmid): 
        if not isinstance(vmid, int):
            raise ValueError('vmid has to be int')

        try:
            # Remove the vm info from the dictionary of vms of this rack
            poppedvm = self.vmids.pop(vmid)
            return poppedvm['ip']
        except KeyError:
            print "Specified vmid doesn't exist"
            return None

    def __str__(self):
        return self.vmids.__str__()

class DataCenter(object):

    def __init__(self):
        # List of ids of all the racks in this container
        self.rackids = []
        super(DataCenter, self).__init__()

    def addrack(self):
        """Method to add racks to the DataCenter. Ids are created sequentially"""
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
    """The class containing Methods that balance the load between different racks of the DataCenter"""
    def __init__(self, no_of_racks):
        super(LoadBalancer, self).__init__()
        # Variable that holds the datacenter object
        self.dc = DataCenter()
        # List of ALL the racks
        self.racks = []
        # Bi directional dictionary of all users and their ips
        self.users = BiDiDict()
        if not no_of_racks or no_of_racks <= 0:
            raise ValueError("Number of racks has to be more than one")
        for x in xrange(0,no_of_racks):
            self.racks.append(self.dc.addrack())

    def newuser(self):
        userid = 0
        try: 
            # Create user
            userid = max(self.users.keys()) + 1
        except ValueError:
            userid = 0
        # Determine suitable rack to spawn the VM in
        suitable_rack = reduce(lambda rack1, rack2:
            rack1 if len(rack1.vmids) <= len(rack2.vmids) else rack2, self.racks)
        newvm = suitable_rack.addvm()
        # Add the user to the dictionary
        self.users[userid] = newvm.ip
        print "User added to rack", suitable_rack.rackid
        
    def remuser(self, rackid, vmid):
        # Get the rackid of the rack that contains the VM which runs the server that is serving the user who just quit
        suitable_rack = filter(lambda rack: rack.rackid == rackid, self.racks)
        if len(suitable_rack) == 0:
            raise ValueError('There are no racks with the given rackid')
        elif len(suitable_rack) > 1:
            raise ValueError('There is more than one rack with the given rackid!')
        else:
            suitable_rack = suitable_rack[0]
        # Stop the VM
        deleted_vm_ip = suitable_rack.delvm(vmid)
        if deleted_vm_ip != None:
            # Get the key based on the value
            user_key = self.users[:deleted_vm_ip]
            self.users.pop(user_key[0])
            print 'User',user_key[0],' quit from rack', suitable_rack.rackid
            self.balance_load()
        else:
            print "Couldn't remove user"

    def stats(self):
        for rack in self.racks:
            print 'Rack',rack.rackid,':',len(rack.vmids),'Users/VMs'
        print self.users

    def balancing_required(self):
        vms_max = self.get_max_min('max')
        vms_min = self.get_max_min('min')
        return True if vms_max - vms_min > 1 else False

    def get_max_min(self, maxormin):
        if maxormin == 'max':
            return max([len(rack.vmids) for rack in self.racks])
        elif maxormin == 'min':
            return min([len(rack.vmids) for rack in self.racks])
        else:
            raise ValueError('maxormin has to be either max or min')

    def balance_load(self):
        # Check whether balancing is required
        if self.balancing_required():
            # The rackids of the heavily loaded rack
            rackfrom = filter(lambda rack:
                len(rack.vmids) == self.get_max_min('max'), self.racks)
            # The rackids of the lightly loaded rack
            rackto = filter(lambda rack:
                len(rack.vmids) == self.get_max_min('min'), self.racks)
            for rf, rt in itertools.izip(rackfrom,rackto):
                targetvm = rf.vmids.itervalues().next()
                # Delete the VM in the heavily loaded rack
                original_ip = rf.delvm(targetvm['id'])
                if original_ip != None:
                    # Get the user key
                    userkey = self.users[:original_ip]
                    # Create a new VM in an appropriate rack (lightly used)
                    newvm = rt.addvm()
                    # Replace old ip entry with new one
                    self.users.replaceVal(original_ip, newvm.ip)
                    print 'Mapped user', userkey, 'from', original_ip, 'to', newvm.ip

def tests():

    lb = LoadBalancer(3)
    for x in xrange(1,11):
        lb.newuser()
    lb.stats()
    lb.remuser(0,2)
    lb.stats()
    lb.remuser(0,1)
    lb.stats()
    lb.remuser(0,0)
    lb.stats()
       
if __name__ == '__main__':
     tests() 
