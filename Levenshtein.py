import numpy as np

class Lev_dist:
    def __init__(self, source, target):
        assert isinstance(source,str), 'The type of source must be str.' 
        assert isinstance(target,str), 'The type of target must be str.'
        self.source = source
        self.target = target

    def get_distance(self,alternative_version=False):
        '''
        Compute the Levenshtein distance between 2 words
        
        Parameters
        ----------
        alternative_version : bool
            When True, the alternative version of Levenshtein metric 
            is used, otherwise the standard metric.
        
        Returns
        -------
        distance : int 
            Minimum number of editing operations (like insertion, deletion,
            substitution) needed to transform one string into another.
            All these operations have cost of 1 in standard metric.
            ************************************************************
            In an alternative version, each insertion and deletion has a 
            cost of 1 and substitutions are not allowed.(This is equivalent to 
            allowing substitutions, but giving each substitution a cost of 2 since
            any substitution can be represented by one insertion and one deletion).
        '''
        assert isinstance(alternative_version,bool), 'The type of alternative_version must be bool.'
        
        n,m = len(self.source), len(self.target)
        D = np.zeros(shape=(n+1,m+1),dtype=int)
        
        # Initialization.
        D[:,0] = range(n+1)
        D[0,:] = range(m+1)
        
        cost_of_substitution = 2 if alternative_version else 1
        # Recurrence relation.
        for i in range(1,n+1):
            for j in range(1,m+1):
                D[i,j] = min(D[i-1,j] + 1,
                             D[i,j-1] + 1,
                             D[i-1,j-1] + (cost_of_substitution if self.source[i-1]!=self.target[j-1] else 0))
                
        return D[n,m]   
    
    def get_backtrace(self):
        '''
        Compute the alignment (minimum edit path) between 2 words
        by using a backtrace
        
        Returns
        -------
        result : str 
            Minimum cost alignment operations.
        '''
        n,m = len(self.source), len(self.target)
        D = np.zeros(shape=(n+1,4,m+1),dtype=int)
        D[0][0] = range(m+1)
        D[:,0,0] = range(n+1)

        for i in range(1,n+1):
            for j in range(1,m+1):
                del_cost, ins_cost, subs_cost = D[i-1,0,j]+1, D[i,0,j-1]+1, D[i-1,0,j-1]+(2 if self.source[i-1]!=self.target[j-1] else 0) 
                D[i,0,j] = min(del_cost,ins_cost,subs_cost)
                if D[i,0,j] == subs_cost:
                    D[i,1,j] = 1          # 1 - substitution
                if D[i,0,j] == del_cost:
                    D[i,2,j] = 2          # 2 - deletion
                if D[i,0,j] == ins_cost:
                    D[i,3,j] = 3          # 3 - insertion
       
        # Performing a backtrace.
        operations,i,j = [],n,m
        while i != 0 and j != 0:
            if 1 in D[i,:,j][1:]:
                if self.source[i-1] != self.target[j-1]:
                    operations.append(('substitute',self.source[i-1],'by',self.target[j-1]))
                    i,j = i-1, j-1
                else: i,j = i-1, j-1           
            elif 2 in D[i,:,j][1:]:
                operations.append(('delete',self.source[i-1]))
                i = i-1
            elif 3 in D[i,:,j][1:]:
                operations.append(('insert',self.target[j-1]))
                j = j-1
        while i != 0:
                operations.append(('delete',self.source[i-1]))
                i = i-1
        while j != 0:
                operations.append(('insert',self.target[j-1]))
                j = j-1
                
        result = ''
        for operation in reversed(operations):
            result += ' '.join(operation) + '\n'
        
        return result
