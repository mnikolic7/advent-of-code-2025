import numpy as np
import pandas as pd
import sys

#simple solution to part 1 of puzzle from Dec 1, 2024
#This is just a test as a preparation for December 1. Happy Thanksgiving everyone. 
if __name__ == "__main__":
	fname=sys.argv[1]

	df=pd.read_csv(fname, sep=r"\s+", header=None, names=["list1", "list2"])

	list1=df['list1'].to_numpy()
	list2=df['list2'].to_numpy()

	list1.sort()
	list2.sort()

	d=np.sum(np.abs(list2-list1))


	print(d)