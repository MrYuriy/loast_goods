from operator import inv, truediv
from pydoc import cli
from select import select
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Adres
from .serializers import GenadresSerializer
import ast
import numpy

class GenadresView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        resolt = []
        inventory = request.data['inventory']
        
        adreses = request.data['adreses']
        resolt = self.adrese_and_qantity(self.inventory_transaction_list(adreses),self.inventory_dict(inventory))
        #print(resolt)
        
        return Response({"list_adreses":  resolt}, status=status.HTTP_200_OK)

    def filter(self, adres):
        #print(adres)
        adres = adres.replace('-','')
        if adres=='':
            return False
        # куветки   K*******  K1204503  // вяти      W**** W0123 // карнизи   D**** D1330 
        if adres[0]=='K' or adres[0]=='W' or adres[0]=='D':
            if adres[1:].isdigit():
                return True
            else:
                return False

        elif (adres[0:1]=="WK" or adres[0:1]=="WS") and adres[2:].isgit():
            return True
            
        # регали    **R****L** 01R2104A10 01R1027A15 01R0517H1
        elif adres!="PARKING" and adres[2]=='R' and adres[7].isalpha():
            if adres[0:2].isdigit() and adres[3:7].isdigit():
                return True
            else:
                return False
        # маси      **M*** 01M242   01M525-20 01M316-03
        elif adres[2]=='M':
            if adres[3:].isdigit():
                return True
            else:
                return False
        elif adres[:8]=="SZYB-ZAM" :
            return True
        elif adres=='INRACK80':
            return True
        else:
            return False

    

    def inventory_transaction_list(self, list_adreses):
        clin_list = []
        if list_adreses[0]==None:
            return clin_list  
        for adres in list_adreses:
            if self.filter(adres) and adres not in clin_list:
                clin_list.append(adres)
        return (clin_list)

    def generate_invenlist(self, inventory):
        inventory_list = []
        #print("OK!!!!!!!!")
        for i in range(0,len(inventory),2):
            #print(inventory[i],inventory[i+1])
            if inventory[i+1] or inventory[i] != None:
                #print(inventory[i],'------',"------",inventory[i+1])
                quantuty = int(inventory[i+1])
                inventory_list.append([inventory[i],int(quantuty)])
            else:
                None
                
        #print(inventory_list)
        return inventory_list

    
    def inventory_dict(self, inventory):
        inventlist = self.generate_invenlist(inventory)
        inventory_dictionary = {}  
        #print('inventory list',inventlist)
        for adresquantity in inventlist:
            adres = str(adresquantity[0])
            quantity = adresquantity[1]
            if self.filter(adres):
                if adres in inventory_dictionary.keys():
                    inventory_dictionary[adres] = inventory_dictionary[adres]+quantity
                else:
                    inventory_dictionary[adres] = quantity
        return (inventory_dictionary)

    def adrese_and_qantity(self, adreses_list, inventory_dictionary):
        resolt = []
        if not adreses_list :
            #print(inventory_dictionary)
            resolt = numpy.array(list(inventory_dictionary.items()))
            #print(resolt)
            resolt = []

            for adres in inventory_dictionary:
                resolt.append(str(adres)+" - "+str(inventory_dictionary[adres]))

            return resolt
        elif not inventory_dictionary:
            return adreses_list
        else: 
            for adres in adreses_list:
                if adres in inventory_dictionary.keys():
                    #print (adres,inventory_dictionary[adres])
                    resolt.append(str(adres)+" - "+str(inventory_dictionary[adres]))

                else:
                    resolt.append(adres)
            for adres_invent in inventory_dictionary.keys():
                if adres_invent not in adreses_list:
                    resolt.append(str(adres_invent)+" - "+str(inventory_dictionary[adres_invent]))
                    #print(adres)
            return (resolt)