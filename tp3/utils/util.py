#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def opendata(pathname):
    res = []
    with open(pathname,'r') as f:
        for line in f:
            line = line.lstrip()
            #on filtre les lignes d'infos
            if line and not (line[0]=="@" or line[0]=="%"):
                line = line.rstrip()
                #on separe les valeurs
                vals = line.split(",")
                #on cast en float
                vals = map(float,vals)
                #on ajoute a la liste des resultat
                res.append(tuple(vals))
    return res
    




if __name__ == "__main__":
    if len(sys.argv)<2:
        print sys.argv[0] + " pathToFile"
    else :
        
        data = opendata(sys.argv[1])
        print data
        
