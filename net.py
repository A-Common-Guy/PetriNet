
import numpy as np
import pandas as pd

import scipy.optimize as opt


from scipy.linalg import lu
import networkx as nx


class Net:
    def __init__(self, C, M0) -> None:
        self.C=C
        print(self.C)
        self.M0=np.transpose(M0)
        self.shape=self.C.shape
        self.Mvect=[]
        self.G=nx.DiGraph()
        self.num=0
        self.G.add_nodes_from([("M{}".format(0),{"val":np.array2string(self.M0)})])
        self.Mvect.append(self.M0)
        self.mark=[]
        self.mark.append("M0")
        


    def transEnabled(self,M):
        enabledVector=np.zeros(self.shape[1])
        for i in range(self.shape[1]):
            result=np.all((np.add(M,self.C[:,i]))>=0)
            enabledVector[i]=result
        return enabledVector

    def p_reduce(self):
        work=np.transpose(self.C)
        _,triangular=lu(work,permute_l=True)
        reduce=opt._remove_redundancy._remove_redundancy_pivot_dense(triangular, np.zeros(self.shape[1]))
        result=reduce[0]
        rank=np.linalg.matrix_rank(result)
        dimension=result.shape[1]
        solution_dim=dimension-rank
        print(solution_dim)
        return result
        #decompose the matrix

    def t_reduce(self):
        work=np.copy(self.C)
        _,triangular=lu(work,permute_l=True)
        reduce=opt._remove_redundancy._remove_redundancy_pivot_dense(triangular, np.zeros(self.shape[0]))
        result=reduce[0]
        rank=np.linalg.matrix_rank(result)
        dimension=result.shape[1]
        solution_dim=dimension-rank
        print(solution_dim)
        return result
        #decompose the matrix
    
    def simulate(self,M,graph=[],max_iter=1000):   
            enabled=self.transEnabled(M)
            parentnum=self.num
            #print("en=",enabled)
            if not enabled.any():
                #print("No more enabled transitions")
                return None
            for j,trans in enumerate(enabled):
                if trans==1:
                    burst_vect=np.zeros((self.shape[1]))
                    burst_vect[j]=1
                    #print("burst=",burst_vect)
                    Mnew=M+np.dot(self.C,burst_vect)
                    #print("Mnew=",Mnew)
                    found=0
                    marker=0
                    for i in range(len(self.Mvect)):
                        if np.array_equal(self.Mvect[i],Mnew):
                            marker=i
                            found=1
                            break
                    #print("Mvect=",self.Mvect)
                    #print("found=",found)
                    if found==1:
                        self.G.add_edges_from( [ ("M{}".format(parentnum), self.mark[marker], {"weight":1+j}) ])


                    if found==0: 
                        #print("appended")
                        self.Mvect.append(Mnew)
                        self.num+=1
                        self.mark.append("M{}".format(self.num))
                        self.G.add_nodes_from([("M{}".format(self.num),{"val":np.array2string(Mnew)})])
                        self.G.add_edges_from( [ ("M{}".format(parentnum), "M{}".format(self.num), {"weight":1+j}) ])  
                        self.simulate(Mnew,graph,max_iter)
            return None

    
    def sifoni(self):
        preset=np.empty(self.shape[0],dtype=object)
        postset=np.empty(self.shape[0],dtype=object)

        for i in range(self.shape[0]):    
            preset[i]=np.where(self.C[i,:]>0)
            postset[i]=np.where(self.C[i,:]<0)
        for i in range(self.shape[0]):
            pass

    def getGraph(self):
        return self.G

            



    def trappole(self):
        pass




