from npnlp import minimize
import numpy as np

def J(x):
    return np.array([x[0]**4 + x[1]**2 - x[0]**2*x[1]])

def eq_con(x,l):
    return np.array([1 - 2*x[0]*x[1]/3, (3*x[0]**2 - 4*x[1])/3 + 1])

x0 = np.array([0.5, 3.0])

out = minimize(J, x0, A=np.array([[1,0]]), b=np.array([-1]), nonlconeq=None, method='SQP')
# out = minimize(J, x0, nonlconineq=eq_con, method='SQP')

print(out)
