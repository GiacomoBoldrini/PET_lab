import numpy as np
import ROOT
import math as mt
import matplotlib.pyplot as plt

def Line_rotation(m_lor, q_lor, angles = None):
    
    if angles != None:
        slopes = []
        inter = []
        for ang in angles:
            x1 = 5 #sampling a random point on lor
            x2 = 10
            y1 = m_lor*x1+q_lor
            y2 = m_lor*x2+q_lor

            #rotating
            x1_1 = mt.cos(ang)*x1-mt.sin(ang)*y1
            y1_1 = mt.sin(ang)*x1+mt.cos(ang)*y1
            x2_2 = mt.cos(ang)*x2-mt.sin(ang)*y2
            y2_2 = mt.sin(ang)*x2+mt.cos(ang)*y2

            m = (y1_1-y2_2)/(x1_1-x2_2)
            q = y1_1-m*x1_1

            slopes.append(m)
            inter.append(q)

    return slopes, inter


#computing lor #MAIN
alphas = np.radians([46.78, 304.0, 100.1, 138.6, 59.87])
betas = np.radians([284.9, 12.6, 263.6, 240.6, 278.4])
psi_vec = np.radians([157.5, 142.5, 187.5, 210.0, 165.0])


slopes = []
inter = []

for i,j,z in zip(alphas, betas, psi_vec):
    psi = z

    r = 0.3
    cotan = 1 / mt.tan(z/2)

    q = -0.3*cotan
    m = mt.sin(z)/(mt.cos(z)-1)
    
    s, l = Line_rotation(m, q, angles = [i, j])
    slopes.append(s)
    inter.append(l)

lines_coeff = []

for i,j in zip(slopes, inter):
    m1 = i[0]
    q1 = j[0]
    m2 = i[1]
    q2 = j[1]
    lines_coeff.append([m1,q1])
    lines_coeff.append([m2,q2])

draw_points = []
int_already_done = []
for co in lines_coeff:
    int_already_done.append(co)
    m = co[0]
    q = co[1]
    other_lines = [x for x in lines_coeff if x != co and x not in int_already_done]
    
    for ot_co in other_lines:
        m1 = ot_co[0]
        q1 = ot_co[1]

        x_int = (q1-q)/(m-m1)
        y_int = m*x_int+q
        draw_points.append([x_int*100, y_int*100])

xs = [i[0] for i in draw_points]
ys = [i[1] for i in draw_points]

x_avg = np.mean(xs)
y_avg = np.mean(ys)
print(x_avg, y_avg)
print(np.std(xs), np.std(ys))
#Creating the circle centered in (0,0)

circ = ROOT.TEllipse(0,0,17.5,17.5)
circ.SetLineColor(1)
circ.SetLineWidth(3)
circ.SetFillColor(0)

m = ROOT.TMarker(x_avg, y_avg, 20)
m.SetMarkerSize(1)
m.SetMarkerColor(ROOT.kRed)

g = ROOT.TGraph(len(xs), np.array(xs*100), np.array(ys*100))
g.SetTitle('Geometrical Reconstruction')
g.GetXaxis().SetLimits(-50,50)
g.GetYaxis().SetRangeUser(-50,50)
g.SetMarkerSize(5)
g.SetMarkerStyle(ROOT.kStar)

c = ROOT.TCanvas("c","c",0,0,1000,1000)
c.SetTickx()
c.SetTicky()

#m.Draw('AP')
#c.Draw()
#c.SaveAs('./prova3.png', 'png')

fig = plt.figure(figsize=(20,10))
plt.scatter(xs, ys, c = 'blue', s= 5)
plt.scatter(x_avg, y_avg, c = 'red', s = 20)
fig.savefig("./prova5.png")








