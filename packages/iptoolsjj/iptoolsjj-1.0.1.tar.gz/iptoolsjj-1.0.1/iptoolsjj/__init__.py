'''
iptoolsjj 1.0
Copyright (C) 2018  Jaroslaw Jankun jaroslaw.jankun@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

class IP_TOOLS:
    #=======================================================================================
    #gives partial octet of mask, which is not 255 and not 0, for example if number of '1s' is N=7, then we have 128, for 6 : 192, for 5 : 224
    #this is necessary for 'is_in_subnet' and 'dec_to_mask255' methods
    def not_full_octet(self,N,base,P):           
        if N == 1 : return str(base)             # base is 128 , P is 64 ( needs to be so :) )       
        else:
            base+=P
            P=P//2                              # added double slash // for python 3 !
            return self.not_full_octet(N-1,base,P)
    #gives mask in format x.x.x.x from mask in decimal format like 24 or 16 or 23...
    def dec_to_mask255(self,mask_dec):    
        mask255=""                                  
        for x in range(0,4):                        # 4 times because there are 4 octets of mask
            if mask_dec >= 8:
                mask255+="255"
                mask_dec-=8
            elif mask_dec > 0:
                 mask255+=self.not_full_octet(mask_dec,128,64)
                 mask_dec=0
            else: mask255+="0"
                
            if x!=3 : mask255+="." 
        mask_octets = mask255.split('.')            #puts MASK into array of octets
        return mask_octets
    #=======================================================================================
    #changes mask in format: 255.255.255.128 to format: 25
    def mask255_to_dec(self,mask255):
        mask_dec=0
        mask255_octets=mask255.split(".")
        for octet in mask255_octets:
            mask_dec+=self.one_octet(int(octet))
        return mask_dec
    # counts one octet of mask : for example for 128 it gives 1, for 192 it gives 2, for 224 gives 3
    #necessary for method mask255_to_dec
    def one_octet(self,octet,base=128,increment=64,l=1):
        if octet == 0: return 0
        if base == octet : return l
        base+=increment
        increment=increment//2
        l+=1
        return self.one_octet(octet,base,increment,l)

        return(mask_dec+l)
    #=======================================================================================           
    #if 'ip' belongs to subnet 'net', it gives True, otherwise - false
    def is_in_subnet(self,ip,net):                               
       
        if "/" in ip: ip=ip.split("/")[0]   # if 'ip' is also subnet (implicitly smaller, than 'net')
       
        if len(net.split('/')) == 2:
            mask_dec = int(net.split('/')[1])  #this is decimal mask
        net_octet = net.split('.')            #puts subnet ip into array with octets
        net_octet[3]=net_octet[3].split("/")[0]

        ip_octet = ip.split('.')              #puts host ip into array with octets

        mask_octets=self.dec_to_mask255(mask_dec)
        
        net_AND=""                                  #AND of subnet with mask and ip with mask, comparison gives final decision
        for s in range(len(net_octet)): net_AND+= str(int(net_octet[s]) & int(mask_octets[s]))
        ip_AND=""
        for s in range(len(ip_octet)): ip_AND+= str(int(ip_octet[s]) & int(mask_octets[s]))

        if net_AND == ip_AND: return True           
        else : return False

