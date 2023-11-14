#!/bin/bash

gawk  ' BEGIN {printf "#SOD    DOY YEAR  PRN   ELEV    AZIM   TOF[ms]   MEAS[m] \
SNR[db-Hz]    SAT-X[m]       SAT-Y[m]       SAT-Z[m]     VEL-X[m/s] VEL-Y[m/s]\
 VEL-Z[m/s] RANGE[m]     SV-CLK[m]    DTR[m]    TGD[m] TROPO[m]   STEC[m]  VTEC[m] MPP[elev]\n"}


$7=="L1P"{cn0=$31}

$7=="C1C"{
	
	E=$29;
	R=6378.1363
	h=350;
	#mp=1.001/sqrt(0.002001+sin(E*3.14159/180)*sin(E*3.14159/180))
	mp=1/sqrt(1-((R/(R+h))*cos(E*3.14159/180))*((R/(R+h))*cos(E*3.14159/180)))
	Clk=-$18
	Dtr=-$22
	TGD=$27
	
	printf "%6.1f %3d %4d %4d %8.3f %8.3f %5.1f %5.2f %7.1f %15.3f %15.3f %15.3f %9.3f %9.3f %9.3f %13.3f %13.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n",$4,$3,$2,$6,$29,$30,$8*1E3,$9,cn0,$11,$12,$13,$14,$15,$16,$17,Clk,Dtr,TGD,$24,$25,$25/mp,mp
	
	
	}' "$1"
