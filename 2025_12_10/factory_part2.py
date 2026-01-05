import sys
import numpy as np
import sympy as sp

#linear algebra practice. 

if __name__=="__main__":
	fname=sys.argv[1]

	LIGHTS=[]
	BUTTONS=[]
	JOLTAGES=[]
	with open(fname) as file:
		for line in file:
			l=line.strip().split()
			lights=l[0][1:-1] #first item, get rid of bracket characters
			joltages=l[-1][1:-1] #last item, get rid of curly brackets
			buttons=l[1:-1] #items in between

			#get switches in binary-ready.
			binary=''
			for c in lights:
				if c=='#':
					binary+='1'
				else:
					binary+='0'
			LIGHTS.append(binary)

			#get joltages as integers.
			JOLTAGES.append([int(j) for j in joltages.split(',')])

			butts=[]
			for butt in buttons:
				butt=butt[1:-1].split(',')
				butt=[int(b) for b in butt]
				butts.append(butt)
			BUTTONS.append(butts)

	INF=float('inf')

	IDX=2
	joltages=JOLTAGES[IDX]
	button_list=BUTTONS[IDX]

	M=len(button_list)
	N=len(joltages)

	X=np.zeros((N,M))
	y=np.zeros((N,1))
	for i in range(M):
		button=button_list[i]
		for b in button:
			X[b,i]+=1

	for i,j in enumerate(joltages):
		y[i]=j

	print(button_list)
	print(X)
	print(y)
	# A=sp.Matrix(A)
	# # R=A.rref()	
	# b, residuals, rank, s = np.linalg.lstsq(X, y, rcond=None)
	# print(b)
	# print(residuals)
	# print(rank)
	# print(s)
	# print(R)

	#this darn stupid approach works.
	#it's just linear fitting with regularization
	#it gets things wrong all the time, but the sum
	#of the b is approximately the same. 
	#I am curious how close I can get with this.
	#I got too high
	# That's not the right answer; your answer is too high.
	from sklearn.linear_model import Lasso
	lam=0.005
	model = Lasso(
    	alpha=lam,
    	positive=True,
    	fit_intercept=False,
    	max_iter=40000
	)

	model.fit(X, y)
	w = model.coef_

	totals=[]
	for idx in range(len(JOLTAGES)):
		joltages=JOLTAGES[idx]
		button_list=BUTTONS[idx]

		M=len(button_list)
		N=len(joltages)

		X=np.zeros((N,M))
		y=np.zeros((N,1))
		for i in range(M):
			button=button_list[i]
			for b in button:
				X[b,i]+=1

		for i,j in enumerate(joltages):
			y[i]=j

		model.fit(X, y)
		w=model.coef_
		totals.append(np.sum(np.round(w)))

	total=np.sum(totals)
	print('-'*30)
	print(total)

	# import numpy as np
	# from scipy.optimize import minimize

	# def objective(w, X, y, lam):
	#     return np.sum((X @ w - y)**2) + lam * np.sum(w**2)

	# N = X.shape[1]
	# w0 = np.zeros(N)
	# lam=0.01
	# bounds = [(0, None)] * N  # w >= 0

	# res = minimize(
	#     objective,
	#     w0,
	#     args=(X, y, lam),
	#     bounds=bounds,
	#     method='L-BFGS-B'
	# )

	# w = res.x
	# print(w)
	# print(np.round(w))
	# print(np.sum(np.round(w)))
	# print(np.sum(w))
