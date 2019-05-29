import numpy as np
import ROOT
import math as mt
import matplotlib.pyplot as plt
from tqdm import tqdm

def Line_rotation(m_lor, q_lor, r, angles = None):
    
    coeff = []
    #rotated line from ste formula
    for ang in angles:
        
        m_rot = (m_lor*mt.cos(ang)-mt.sin(ang))/(mt.cos(ang)+m_lor*mt.sin(ang))
        q_rot = (m_lor*r)/(mt.cos(ang)+m_lor*mt.sin(ang))
        coeff.append([m_rot,q_rot])
    
    return coeff[0], coeff[1]

#computing lor #MAIN
x_true = 1.16
y_true = -13.25
psi_original = np.radians([157.5, 142.5, 187.5, 210.0, 165.0])
alphas_original = np.radians([46.78, 304.0, 100.1, 138.6, 59.87])
betas_original = np.radians([284.9, 12.6, 263.6, 240.6, 278.4])
averages = []
averages_all = []
distances = []

h2 = ROOT.TH2D("h2", "h2", 200, -1,1 , 200, -1,1)
h21 = ROOT.TH2D("h21", "h21", 200, -1,1 , 200, -1,1)
h3 = ROOT.TH3D("h3", "h3", 200, -1,1 , 200, -1,1, 100, -30, 30)

h3.GetXaxis().SetTitle("Theta Error [#circ]")
h3.GetXaxis().SetTitleOffset(2.2)
h3.GetYaxis().SetTitle("#alpha and #beta errors [#circ]")
h3.GetYaxis().SetTitleOffset(2.2)
h3.GetZaxis().SetTitle("Euclidean Distance [cm]")
#computing cycle itering over a range of +-1 degree, uncertainty on the detectors angle

bin_count = 0

for error_theta in tqdm(np.arange(-.1,.1,0.001)):

    for error_alpha in np.arange(-.1,.1,0.001):
        
        psi_vec = [j-error_theta for j in psi_original]
        alphas = [j-error_alpha for j in alphas_original]
        betas = [j-error_alpha for j in betas_original]


        rotated_lines = []

        for al,be, ps in zip(alphas, betas, psi_vec):
            
            r = 0.32645
            cotan = 1 / mt.tan(ps/2)
            q = -r**cotan
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

        x_avg = np.mean(x)
        y_avg = np.mean(y)

        x_std = np.std(x)
        y_std = np.std(y)
        
        
        """
        if x_std > 1 or y_std > 1:
            #h3.Fill(error_alpha, error_beta, error_theta, 0)
            continue
        
        else:
        """

        #print(x_avg, '+-', np.std(x), y_avg, '+-', np.std(y))
        dist = np.sqrt((x_avg-x_true)**2 + (y_avg-y_true)**2)
        sum_var = np.sqrt((x_std**2+y_std**2))
        #print(dist)
        h2.Fill(error_theta, error_alpha, x_avg)
        h21.Fill(error_theta, error_alpha, sum_var)
        h3.Fill(error_theta, error_alpha, x_avg, x_std)
        bin_count += 1
        averages_all.append([x_avg, x_std,y_avg, y_std, error_theta, error_alpha])
        averages.append([abs(x_avg-x_true), abs(y_avg-y_true)])
        distances.append(np.sqrt((x_avg-x_true)**2 + (y_avg-y_true)**2))


print(min(distances))
point = distances.index(min(distances))
print(averages_all[point])

c = ROOT.TCanvas("c", "c", 1000,1000,1000,1000)
h2.Draw("SURF2Z")
c.Draw()
c.SaveAs("./canvas.png", "png")

c2 = ROOT.TCanvas("c", "c", 1000,1000,1000,1000)
h21.Draw("SURF2Z")
c2.Draw()
c2.SaveAs("./canvas3.png", "png")

c1 = ROOT.TCanvas("c", "c", 1000,1000,1000,1000)
h3.Draw("BOX2Z")
c1.Draw()
c1.SaveAs("./canvas2.png", "png")

