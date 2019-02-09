from __future__ import absolute_import
from __future__ import print_function
import numpy as np

class LevDist(object):
	'''LevDist class'''
	def __init__(self,sstr,dstr, i_score=1, d_score=1, s_score=1, verbose=False):
		self.sstr = '#' + sstr
		self.dstr = '#' + dstr
		self.verbose = verbose
		self.scores = {'insert':i_score,'del': d_score, 'sub': s_score}
		self._find_dist()

	def _find_dist(self):
		N,M = len(self.sstr),len(self.dstr)

		lev = np.zeros(shape=(N,M))
		lev[:,0], lev[0] = np.arange(N),np.arange(M)
		
		for i in range(1,N):
			for j in range(1,M):
				lev[i,j] = min(lev[i-1,j] + self.scores['del'],
						   lev[i,j-1] + self.scores['insert'],
						   lev[i-1,j-1]+(self.scores['sub'] if self.sstr[i] != self.dstr[j] else 0))
		backtrace = []
		while i!=0 and j!=0:
			if lev[i,j] == lev[i-1,j] + self.scores['del']:
				backtrace.append("del " + self.sstr[i])
				i -= 1
			elif lev[i,j] == lev[i,j-1] + self.scores['insert']:
				backtrace.append("insert " + self.dstr[j])
				j -= 1 
			else:
				if self.sstr[i] != self.dstr[j]:
					backtrace.append("sub " + self.sstr[i] + ' ' + self.dstr[j])
				i -= 1
				j -= 1
		
		if self.verbose:     
			print(lev)
		self.lev_dist = lev[N-1,M-1]
		self.backtrace = '\n'.join(backtrace[::-1])
				
	def get_distance(self):
		"Calculate distance"
		return self.lev_dist
	
	def get_backtrace(self):
		"Find sequence of insertion, deletion and substitution"
		return self.backtrace
