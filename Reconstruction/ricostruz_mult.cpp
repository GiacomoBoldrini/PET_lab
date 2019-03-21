//c++ -o ricostruz_mult ricostruz_mult.cpp `root-config --glibs --cflags`

#include <iostream>
#include <stdio.h>

#include "TGraph.h"
#include "TCanvas.h"
#include "TApplication.h"
#include "TH1F.h"
#include "TF1.h"
#include "TAxis.h"
#include <cmath>
#include "TLine.h"
#include "TVector3.h"
#include "TEllipse.h"

#define radius 30       //in centimetri
#define pi 3.1415926535
using namespace std;

int main(){ 

//Definisco una struct che contiene tutte le informazioni derivanti da una presa dati e da cui si otterranno due rette
    struct misura{
        double theta;       //angolo tra i due scintillatori  
        double alpha;       //angol01 picco rate
        double beta;        //angolo2 picco rate
        TVector3 v1;
        TVector3 v1_a;      //v1 e v2 sono i vettori che puntano ai due
        TVector3 v1_b;      //scintillatori, il pedice a o b intende una 
        TVector3 v2;        //rotazione effettuata di alpha o beta
        TVector3 v2_a;
        TVector3 v2_b;
        TLine linea1;
        TLine linea2;
    };
    
//Definizioni preliminari    
    TApplication * app = new TApplication("app",0,NULL);
    TCanvas * c = new TCanvas("c", "c", 0,0, 700, 700);
    //c->SetGrid();
    c->SetTickx();
    c->SetTicky();
    
    
//Preparo un graph con coordinata (0,0) al centro e di semiampiezza n/2
    int n=40;
    double x[n], y[n];
    for(int i=0; i<n; i++){
        x[i]=i-n/2;
        y[i]=i-n/2;
    }
    TGraph * gr = new TGraph(n,x,y);
    gr->SetTitle("Geometric Reconstruction");
    gr->GetXaxis()->SetTitle("x coordinate (cm)");
    gr->GetYaxis()->SetTitle("y coordinate (cm)");
    gr->GetYaxis()->SetTitleOffset(1.2);
    
    gr->SetMarkerColor(0);
    
 //Si inserisce il numero di misure fatte e i dati necessari e calcolo tutto il necessario pèr arrivare alle rette
    int N_misure;
    cout << "Quante misure includi nella ricostruzione?" << endl;
    cin >> N_misure;
    
    misura array[N_misure];     //definisco un array di struct
    
    for(int i=0; i<N_misure; i++){
        cout << "Inserire theta misura" << i+1 << ":" << endl;
        cin >> array[i].theta;
        cout << "Inserire alpha misura" << i+1 << ":" << endl;
        cin >> array[i].alpha;
        cout << "Inserire beta misura" << i+1 << ":" << endl;
        cin >> array[i].beta;
        
        array[i].v1 = TVector3(-radius, 0, 0);
        
        array[i].v2 = TVector3(radius*cos(pi - array[i].theta*pi/180.),-radius*sin(pi - array[i].theta*pi/180.), 0);
        array[i].v1_a = array[i].v1;
        array[i].v1_a.RotateZ(-array[i].alpha*pi/180);
        array[i].v1_b = array[i].v1;
        array[i].v1_b.RotateZ(-array[i].beta*pi/180);
        array[i].v2_a = array[i].v2;
        array[i].v2_a.RotateZ(-array[i].alpha*pi/180);
        array[i].v2_b = array[i].v2;
        array[i].v2_b.RotateZ(-array[i].beta*pi/180);
        array[i].linea1.SetX1(array[i].v1_a.X());
        array[i].linea1.SetY1(array[i].v1_a.Y());
        array[i].linea1.SetX2(array[i].v2_a.X());
        array[i].linea1.SetY2(array[i].v2_a.Y());
        array[i].linea2.SetX1(array[i].v1_b.X());
        array[i].linea2.SetY1(array[i].v1_b.Y());
        array[i].linea2.SetX2(array[i].v2_b.X());
        array[i].linea2.SetY2(array[i].v2_b.Y());
    }
    
//Definisco la circonferenza che rappresenta la plate     
    TEllipse * circle = new TEllipse(0,0,15,15);
    circle->SetLineColor(1);
    circle->SetLineWidth(3);
    circle->SetFillColor(0);
//Plotto grafico con assi, le rette e la circonferenza
    c->cd();
    gr->Draw("AP");
    circle->Draw();
    for(int j=0; j<N_misure; j++){
        array[j].linea1.SetLineWidth(2);
        array[j].linea1.SetLineStyle(9);
        array[j].linea2.SetLineWidth(2);                array[j].linea2.SetLineStyle(9);
        if(j>4){
            if(j==5){
                array[j].linea1.SetLineColor(9);
                array[j].linea2.SetLineColor(13); 
            }
            else if(j==6){
                array[j].linea1.SetLineColor(30);
                array[j].linea2.SetLineColor(28);                
            }
            else if(j==7){
                array[j].linea1.SetLineColor(46);
                array[j].linea2.SetLineColor(49);                
            }
            else{
                cout << "TROPPE MISURE E POCHI COLORI!!" << endl;
            }
        }
        else{
            array[j].linea1.SetLineColor(1+2*j);
            array[j].linea2.SetLineColor(2+2*j);

        }
        array[j].linea1.Draw();
        array[j].linea2.Draw();
    }
    
//Salvo il canvas!!!!!    
    c->SaveAs("/home/stefano/Scrivania/uni/Magistrale/Lab/Ricostruzione_grafica/image.pdf");
    
    
    app->Run("");
    return 0;
    }
