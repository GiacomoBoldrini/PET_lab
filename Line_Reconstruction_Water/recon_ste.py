import numpy as np
import ROOT
import math as mt
import matplotlib.pyplot as plt

def Line_rotation(m_lor, q_lor, r, angles = None):
    
    coeff = []
    #rotated line from ste formula
    for ang in angles:
        
        m_rot = (m_lor*mt.cos(ang)-mt.sin(ang))/(mt.cos(ang)+m_lor*mt.sin(ang))
        q_rot = (m_lor*r)/(mt.cos(ang)+m_lor*mt.sin(ang))
        coeff.append([m_rot,q_rot])

    return coeff[0], coeff[1]

def ellipse_confidence(x,y, t):
    
    #http://www.visiondummy.com/2014/04/draw-error-ellipse-representing-covariance-matrix/
    
    #calcola la media
    center_x = x.mean()
    center_y = y.mean()
    #calcolo deviazioni
    s_x = np.std(x)
    s_y = np.std(y)
    #covariance matrix
    cov = np.cov(x,y)
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
        print(x_int*100, y_int*100)
        draw_points.append([x_int*100, y_int*100])

x = [i[0] for i in draw_points]
y = [i[1] for i in draw_points]

x_avg = np.mean(x)
y_avg = np.mean(y)

x_std = np.std(x)
y_std = np.std(y)

print(x_avg, '+-', np.std(x), y_avg, '+-', np.std(y))


"""
fig = plt.figure(figsize=(20,10))
plt.scatter(xs, ys, c = 'blue', s= 5)
plt.scatter(x_avg, y_avg, c = 'red', s = 20)
fig.savefig("./prova4.png")
"""

c = ROOT.TCanvas("c", "c", 1000,1000,2000,1500)
legend = ROOT.TLegend(0.15,0.71,0.35,0.89)
legend.SetHeader("", "C")
legend.SetLineWidth(0)

g = ROOT.TGraph(len(x), np.array(x), np.array(y))
g.SetTitle('')
g.GetXaxis().SetLimits(-50,18)
g.GetYaxis().SetRangeUser(-20,20)
g.SetMarkerSize(1)
g.SetMarkerStyle(ROOT.kStar)

g_sub = ROOT.TGraph(len(x), np.array(x), np.array(y))
g_sub.SetTitle('')
g_sub.GetXaxis().SetLimits(-1.9,2.9)
g_sub.GetYaxis().SetRangeUser(-17,-8)
g_sub.SetMarkerSize(1)
g_sub.SetMarkerStyle(ROOT.kStar)


l1 = ROOT.TLine(-17.5,0,17.5,0)
l2 = ROOT.TLine(0,-17.5,0,17.5)


circle = ROOT.TEllipse(0,0,17.5,17.5)
circle.SetLineColor(1)
circle.SetLineWidth(3)
circle.SetFillStyle(0)

sub_circle = ROOT.TEllipse(0,0,17.5,17.5)
sub_circle.SetLineColor(1)
sub_circle.SetLineWidth(3)
sub_circle.SetFillStyle(0)

real_slit = ROOT.TEllipse(0,0,13.3,13.3)
real_slit.SetLineColor(1)
real_slit.SetLineWidth(1)
real_slit.SetFillStyle(0)
real_slit.SetLineStyle(9)

#confidence levels 68
[center_x, center_y], maj_axis, min_axis, theta = ellipse_confidence(np.array(x), np.array(y), 2.35)

cl = ROOT.TEllipse(center_x,center_y,min_axis,maj_axis,0,360, theta)
cl.SetLineColor(0)
cl.SetFillColorAlpha(ROOT.kBlue, 0.2)
cl.SetFillStyle(1100)
legend.AddEntry(cl,"68% cl","f")

#confidence levels 95
[center_x, center_y], maj_axis1, min_axis1, theta1 = ellipse_confidence(np.array(x), np.array(y), 5.991)

cl1 = ROOT.TEllipse(center_x,center_y,min_axis1,maj_axis1,0,360, theta1)
cl1.SetLineColor(0)
cl1.SetFillColorAlpha(ROOT.kGreen, 0.2)
cl1.SetFillStyle(1100)
legend.AddEntry(cl1,"95% cl","f")

t1 = ROOT.TLatex(.8,-10.3,"68% ellipse")
t1.SetTextAngle(-45)
t1.SetTextSize(.035)

t2 = ROOT.TLatex(1,-9.5,"95% ellipse")
t2.SetTextAngle(-45)
t2.SetTextSize(.035)

t3 = ROOT.TLatex(-8.6,11,"4th slit")
t3.SetTextSize(.025)
t3.SetTextAngle(28)

zoom_box = ROOT.TBox(-1.9,-17,2.9,-8)
zoom_box.SetLineColor(1)
zoom_box.SetLineWidth(1)
zoom_box.SetFillStyle(0)
zoom_box.SetLineStyle(1)

zoom_sigma = ROOT.TBox(x_avg-x_std,y_avg-y_std,x_avg+x_std,y_avg+y_std)
zoom_sigma.SetLineColor(0)
zoom_sigma.SetFillColorAlpha(ROOT.kBlue, 0.2)
zoom_sigma.SetFillStyle(1100)
#legend.AddEntry(zoom_sigma,"1#sigma region","f")

zoom_2sigma = ROOT.TBox(x_avg-2*x_std,y_avg-2*y_std,x_avg+2*x_std,y_avg+2*y_std)
zoom_2sigma.SetLineColor(0)
zoom_2sigma.SetFillColorAlpha(ROOT.kGreen, 0.2)
zoom_2sigma.SetFillStyle(1100)
#legend.AddEntry(zoom_2sigma,"2#sigma region","f")




legend.AddEntry(g,"Measure","P");


m = ROOT.TMarker(x_avg, y_avg, 20)
m.SetMarkerSize(1)
m.SetMarkerColor(ROOT.kRed)
legend.AddEntry(m,"Averaged Position","P")

#drawing
g.Draw('AP')
l1.Draw()
l2.Draw()
circle.Draw()
real_slit.Draw()
m.Draw()
zoom_box.Draw()
t3.Draw()
legend.Draw()


subpad = ROOT.TPad("subpad","",0.12,0.12,0.425,0.7)
subpad.Draw()
subpad.cd()
g_sub.Draw('AP')
real_slit.Draw()
#sub_circle.Draw()
cl.Draw()
cl1.Draw()
#zoom_sigma.Draw()
#zoom_2sigma.Draw()
m.Draw()
#t1.Draw()
#t2.Draw()



c.cd()
c.Draw()
c.SaveAs('./allinter_326_cl.png', 'png')
c.SaveAs('./allinter_326_cl.root', 'root')



