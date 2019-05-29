import numpy as np
import ROOT
import math as mt
import matplotlib.pyplot as plt
from numpy.linalg import inv
from scipy.stats import f
import scipy


def Line_rotation(m_lor, q_lor, r, angles = None):
    
    coeff = []
    #rotated line from ste formula
    for ang in angles:
        
        m_rot = (m_lor*mt.cos(ang)-mt.sin(ang))/(mt.cos(ang)+m_lor*mt.sin(ang))
        q_rot = (m_lor*r)/(mt.cos(ang)+m_lor*mt.sin(ang))
        coeff.append([m_rot,q_rot])
    
    return coeff[0], coeff[1]


def ellipse_confidence(x, t):
    
    #http://www.visiondummy.com/2014/04/draw-error-ellipse-representing-covariance-matrix/
    
    #calcola la media
    center_x = x[0].mean()
    center_y = x[1].mean()
    #calcolo deviazioni
    s_x = np.std(x[0])
    s_y = np.std(x[1])
    #covariance matrix
    cov = np.cov(x)
    eigenvalues, eigv = np.linalg.eig(cov)
    
    #maj_axis = 2*np.sqrt(2.35*max(eigenvalues))
    #min_axis = 2*np.sqrt(2.35*min(eigenvalues))
    maj_axis = np.sqrt(t*max(eigenvalues))
    min_axis = np.sqrt(t*min(eigenvalues))
    
    i = np.where(eigenvalues==max(eigenvalues))
    max_eigenvector = eigv[:,i]
    
    theta = mt.atan(max_eigenvector[1][0][0]/max_eigenvector[0][0][0])
    
    return [center_x, center_y], maj_axis, min_axis, theta

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

x1 = np.array([x_avg, y_avg])
x_real = np.array([x_true, y_true])

x_t = x1-x_real

#now we implement hotelling for two sample statistics:
#POOLED COVARIANCE MATRIX
n1 = len(x)
n2 = 1
cov_1 = np.cov(x_cov, rowvar = True)
cov_2 = np.array([[.04,0],[0,.04]])

b = x_t.T
cov_pooling = ((n1-1)*cov_1+(n2-1)*cov_2)/(n1+n2-2)
#cov_pooling = ((n1-1)*cov_1+[[0,0],[0,0]])/(n1+n2-2)
Sinv = inv(cov_pooling)
#print(cov_pooling)

t = ((n1*n2)/(n1+n2))*(b.dot(Sinv.dot(x_t)))

#hypothesis H0: x-x_real = 0, H1: x-x_real =! 0. reject
#H0 at a level a if T2 >(p(n-1))/(n-p)F_{p,n-p}(a) where
#F is the F distribution.
num_dof = 2
den_dof = 45-2
a = .43
#rv =  f.pdf(dfn=num_dof, dfd=den_dof, a, loc=0, scale=1)
#central F suppositions
rv =  (2*(45+1-2)/(45+1-2-1))*f.ppf(a, num_dof, den_dof)
#rm =  (2*(45+1-2)/(45+1-2-1))*f.cdf(a, num_dof, den_dof)

fig = plt.figure(figsize=(13,8))
x = np.linspace(f.ppf(0.01, num_dof, den_dof), f.ppf(0.99, num_dof, den_dof), 100)
x_alpha = np.linspace(f.ppf(0.95, num_dof, den_dof), f.ppf(0.99, num_dof, den_dof), 100)
plt.plot(x, f.pdf(x, num_dof, den_dof), 'b-', lw=3, label='f pdf')
plt.title('Fischer PDF for dfn = {}, dfd = {}'.format(num_dof, den_dof))
plt.fill_between(x_alpha, f.pdf(x_alpha, num_dof, den_dof), color = 'r', label = r'$\alpha$ = 0.05%')
plt.legend(loc = 'upper right')
plt.savefig('./fischer.pdf')


print( t, rv)


#NOW WE DO THE SAME WITH THE VALUES FROM THE PAIRED LINES METHOD:
x_paired = [0.6647315155340111, 0.6528186562246899, 0.4926493627791132, 1.2617404216106476, 0.7570001093882107]
y_paired = [-13.076823521140671, -12.668032654288993, -14.850727275337231, -13.34781942915438, -12.874600849995796]

x_paired_joined = []
for i, j in zip(x_paired, y_paired):
    x_paired_joined.append([i,j])

x2 = np.array([np.mean(x_paired), np.mean(y_paired)])

x_t = x2-x_real

#now we implement hotelling for two sample statistics:
#POOLED COVARIANCE MATRIX
n1 = len(x_paired)
n2 = 1
cov_1 = np.cov(np.array(x_paired_joined).T, rowvar = True)
cov_2 = np.array([[.04,0],[0,.04]])

b = x_t.T
cov_pooling = ((n1-1)*cov_1+(n2-1)*cov_2)/(n1+n2-2)
#cov_pooling = ((n1-1)*cov_1+[[0,0],[0,0]])/(n1+n2-2)
Sinv = inv(cov_pooling)
#print(cov_pooling)

t = ((n1*n2)/(n1+n2))*(b.dot(Sinv.dot(x_t)))

#hypothesis H0: x-x_real = 0, H1: x-x_real =! 0. reject
#H0 at a level a if T2 >(p(n-1))/(n-p)F_{p,n-p}(a) where
#F is the F distribution.

#rv =  f.pdf(dfn=num_dof, dfd=den_dof, a, loc=0, scale=1)
#central F suppositions
rv2 =  (2*(45+1-2)/(45+1-2-1))*f.ppf(a, num_dof, den_dof)

print( t, rv)



#PLOTTING

c = ROOT.TCanvas("c", "c", 1000,1000,2000,1500)
legend = ROOT.TLegend(0.15,0.71,0.35,0.89)
legend.SetHeader("", "C")
legend.SetLineWidth(0)


#confidence levels 68
[center_x, center_y], maj_axis, min_axis, theta = ellipse_confidence(x_cov, 2.35)

cl = ROOT.TEllipse(center_x,center_y,min_axis,maj_axis,0,360, theta)
cl.SetLineColor(0)
cl.SetFillColorAlpha(ROOT.kGreen, 0.2)
cl.SetFillStyle(1100)
legend.AddEntry(cl,"68% cl all intercepts","f")

#confidence levels 95
[center_x, center_y], maj_axis1, min_axis1, theta1 = ellipse_confidence(x_cov, 5.991)

cl1 = ROOT.TEllipse(center_x,center_y,min_axis1,maj_axis1,0,360, theta1)
cl1.SetLineColor(0)
cl1.SetFillColorAlpha(ROOT.kGreen, 0.2)
cl1.SetFillStyle(1100)
#legend.AddEntry(cl1,"95% cl measured","f")


#confidence level paired
[center_x, center_y], maj_axis1, min_axis1, theta1 = ellipse_confidence(np.array(x_paired_joined).T, 2.35)

cl1 = ROOT.TEllipse(center_x,center_y,min_axis1,maj_axis1,0,360, theta1)
cl1.SetLineColor(0)
cl1.SetFillColorAlpha(ROOT.kBlue, 0.2)
cl1.SetFillStyle(1100)
legend.AddEntry(cl1,"68% cl paired","f")


"""
sigma = ROOT.TBox(x_true-0.2,y_true-0.2,x_true+0.2,y_true+0.2)
sigma.SetLineColor(0)
sigma.SetFillColorAlpha(ROOT.kRed, 0.2)
sigma.SetFillStyle(1100)
legend.AddEntry(sigma,"1#sigma region real", "f")
"""

sigma = ROOT.TEllipse(x_true,y_true,0.2,0.2,0,360, theta1)
sigma.SetLineColor(0)
sigma.SetFillColorAlpha(ROOT.kRed, 0.2)
sigma.SetFillStyle(1100)
legend.AddEntry(sigma,"1#sigma region real","f")


g = ROOT.TGraph(1, np.array(x_avg), np.array(y_avg))
g.SetTitle('')
g.GetXaxis().SetLimits(-1,2)
g.GetXaxis().SetTitle('X[cm]')
g.GetYaxis().SetRangeUser(-16,-10)
g.GetYaxis().SetTitle('Y[cm]')
g.SetMarkerSize(1.5)
g.SetMarkerStyle(20)
legend.AddEntry(g,"Measured, all interception", "p")

g1 = ROOT.TGraph(1, np.array(np.mean(x_paired)), np.array(np.mean(y_paired)))
g1.SetTitle('')
g1.GetXaxis().SetLimits(-1,2)
g1.GetXaxis().SetTitle('X[cm]')
g1.GetYaxis().SetRangeUser(-17,-9)
g1.GetYaxis().SetTitle('Y[cm]')
g1.SetMarkerSize(1.5)
g1.SetMarkerStyle(21)
legend.AddEntry(g1,"Measured, paired lines", "p")

g2 = ROOT.TGraph(1, np.array(x_true), np.array(y_true))
g2.SetTitle('')
g2.GetXaxis().SetLimits(-2,3)
g2.GetXaxis().SetTitle('X[cm]')
g2.GetYaxis().SetRangeUser(-17,-9)
g2.GetYaxis().SetTitle('Y[cm]')
g2.SetMarkerSize(1.5)
g2.SetMarkerStyle(22)
legend.AddEntry(g2,"True value", "p")

real_slit = ROOT.TEllipse(0,0,13.3,13.3)
real_slit.SetLineColor(1)
real_slit.SetLineWidth(1)
real_slit.SetFillStyle(0)
real_slit.SetLineStyle(9)
legend.AddEntry(real_slit,"4th Slit circumference", "l")



#average
m = ROOT.TMarker(x_avg, y_avg, 20)
m.SetMarkerSize(1)
m.SetMarkerColor(ROOT.kBlack)
#real
m_real = ROOT.TMarker(x_true, y_true, 20)
m_real.SetMarkerSize(1)
m_real.SetMarkerColor(ROOT.kBlack)

g.Draw("AP")
g1.Draw("same P")
g2.Draw("same P")
real_slit.Draw("same")
cl.Draw()
cl1.Draw()
sigma.Draw()
legend.Draw()

c.Draw()
c.SaveAs('./prova.png', 'png')


#NOW PLOTTING WITH RESPECT TO THE CENTER FOR BOTH ESTIMATION. PROPAGATION OF ERROR IS DONE THROUGH
#THE SUM OF THE COVARIANCE MATRICES OF THE MEASURED REAL AND THE RECONSTRUCTED ONE.
#WE KNOW THE REAL VALUE IS IN 0,0 DIFFERENCE.

legend = ROOT.TLegend(0.15,0.71,0.35,0.89)
legend.SetHeader("", "C")
legend.SetLineWidth(0)

x_t1 = x1-x_real
x_t2 = x2-x_real

cov_1 = np.cov(x_cov, rowvar = True)
cov_2 = np.cov(np.array(x_paired_joined).T, rowvar = True)
cov_real = np.array([[0.04,0], [0,0.04]])

#fist ellipse

cov_sum_1 = cov_1 + cov_real
eigenvalues1, eigv1 = np.linalg.eig(cov_sum_1)
maj_axis1 = np.sqrt(2.35*max(eigenvalues1))
min_axis1 = np.sqrt(2.35*min(eigenvalues1))
i1 = np.where(eigenvalues1==max(eigenvalues1))
max_eigenvector1 = eigv1[:,i1]
theta1 = mt.atan(max_eigenvector1[1][0][0]/max_eigenvector1[0][0][0])

el1 = ROOT.TEllipse(x_t1[0],x_t1[1],min_axis1,maj_axis1,0,360, theta1)
el1.SetLineColor(0)
el1.SetFillColorAlpha(ROOT.kGreen, 0.2)
el1.SetFillStyle(1100)
legend.AddEntry(el1, "68% C.L. all intercepts", "f")

#second ellipse

cov_sum_2 = cov_2 + cov_real
eigenvalues2, eigv2 = np.linalg.eig(cov_sum_2)
maj_axis2 = np.sqrt(2.35*max(eigenvalues2))
min_axis2 = np.sqrt(2.35*min(eigenvalues2))
i2 = np.where(eigenvalues2==max(eigenvalues2))
max_eigenvector2 = eigv1[:,i2]
theta2 = mt.atan(max_eigenvector2[1][0][0]/max_eigenvector2[0][0][0])

el2 = ROOT.TEllipse(x_t2[0],x_t2[1],min_axis2,maj_axis2,0,360, theta2)
el2.SetLineColor(0)
el2.SetFillColorAlpha(ROOT.kRed, 0.2)
el2.SetFillStyle(1100)
legend.AddEntry(el2, "68% C.L. paired", "f")

g = ROOT.TGraph(1, np.array(0), np.array(0))
g.SetTitle('')
g.GetXaxis().SetLimits(-2.5,1)
g.GetXaxis().SetTitle('x coordinate [cm]')
g.GetYaxis().SetRangeUser(-2,2.3)
g.GetYaxis().SetTitle('y coordinate [cm]')
g.SetMarkerSize(1.5)
g.SetMarkerStyle(20)
g.GetYaxis().SetLabelOffset(0.02)
legend.AddEntry(g,"Expected value", "p")

g1 = ROOT.TGraph(1, np.array(x_t1[0]), np.array(x_t1[1]))
g1.SetTitle('')
g1.GetXaxis().SetLimits(-2,1)
g1.GetXaxis().SetTitle('X[cm]')
g1.GetYaxis().SetRangeUser(-2,2.3)
g1.GetYaxis().SetTitle('y coordinate [cm]')
g1.SetMarkerSize(1.5)
g1.SetMarkerStyle(21)
legend.AddEntry(g1,"All intercepts", "p")

g2 = ROOT.TGraph(1, np.array(x_t2[0]), np.array(x_t2[1]))
g2.SetTitle('')
g2.GetXaxis().SetLimits(-2,1)
g2.GetXaxis().SetTitle('X[cm]')
g2.GetYaxis().SetRangeUser(-2,2.3)
g2.GetYaxis().SetTitle('Y[cm]')
g2.SetMarkerSize(1.5)
g2.SetMarkerStyle(22)
legend.AddEntry(g2,"Paired", "p")

line1 = ROOT.TLine(0,-2,0,2.3)
line1.SetLineStyle(2)

line2 = ROOT.TLine(-2.5,0,1,0)
line2.SetLineStyle(2)

g.Draw("AP")
g1.Draw("same P")
g2.Draw("same P")
el1.Draw()
el2.Draw()
line1.Draw()
line2.Draw()
legend.Draw()

c.Draw()
c.SaveAs('./prova2.png', 'png')
c.SaveAs('./difference_real.root', 'root')







