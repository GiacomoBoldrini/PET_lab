import numpy as np
import ROOT
import math as mt
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.stats import f

def Line_rotation(m_lor, q_lor, r, angles = None):
    
    coeff = []
    #rotated line from ste formula
    for ang in angles:
        
        m_rot = (m_lor*mt.cos(ang)-mt.sin(ang))/(mt.cos(ang)+m_lor*mt.sin(ang))
        q_rot = (m_lor*r)/(mt.cos(ang)+m_lor*mt.sin(ang))
        coeff.append([m_rot,q_rot])
    
    return coeff[0], coeff[1]

#computing lor #MAIN
alphas = np.radians([46.78, 304.0, 100.1, 138.6, 59.87])
betas = np.radians([284.9, 12.6, 263.6, 240.6, 278.4])
psi_vec = np.radians([157.5, 142.5, 187.5, 210.0, 165.0])
x_true = 1.16
y_true = -13.25
rotated_lines = []

for al,be, ps in zip(alphas, betas, psi_vec):
    
    r = 0.32645
    cotan = 1 / mt.tan(ps/2)
    q = -0.32645*cotan
    m = mt.sin(ps)/(mt.cos(ps)-1)
    coeff1, coeff2 = Line_rotation(m, q,r, angles = [al, be])
    rotated_lines.append(coeff1)
    rotated_lines.append(coeff2)

draw_points = []
already_done = []
for co in rotated_lines:
    already_done.append(co)
    m = co[0]
    q = co[1]
    other_lines = [x for x in rotated_lines if x != co and x not in already_done]
    
    for ot_co in other_lines:
        m1 = ot_co[0]
        q1 = ot_co[1]
        
        x_int = (q1-q)/(m-m1)
        y_int = m*x_int+q
        draw_points.append([x_int*100, y_int*100])

x = [i[0] for i in draw_points]
y = [i[1] for i in draw_points]

x_cov = np.array([[i[0], i[1]] for i in draw_points]).T

x_avg = np.mean(x)
y_avg = np.mean(y)

x_std = np.std(x)
y_std = np.std(y)

print(x_avg, '+-', np.std(x)/mt.sqrt(45), y_avg, '+-', np.std(y)/mt.sqrt(45))

x1 = np.array([x_avg, y_avg])
x_real = np.array([x_true, y_true])

x_t = x1-x_real
cov1 = np.cov(x_cov)[0,1]
cov = [[np.var(x), cov1],[cov1, np.var(y)]]
Sinv = inv(cov)
#b = x_t.T
b = np.array([-0.05,.05]).T
T2 = len(x)*b.dot(Sinv.dot(x_t))
print(b, Sinv, cov, x_t)
#hypothesis H0: x-x_real = 0, H1: x-x_real =! 0. reject
#H0 at a level a if T2 >(p(n-1))/(n-p)F_{p,n-p}(a) where
#F is the F distribution.
num_dof = 2
den_dof = len(x)-2
a = .95
#rv =  f.pdf(dfn=num_dof, dfd=den_dof, a, loc=0, scale=1)
rv =  ((2*(44))/(43))*f.ppf(a, num_dof, den_dof)

print(rv, T2)

