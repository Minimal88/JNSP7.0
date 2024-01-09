#!/bin/bash

gawk  ' BEGIN {printf "#SOD    DOY YEAR  NSATS   RX-LAT[DEG]     RX-LON[DEG]   RX-ALT[m]\
       EPE[m]   NPE[m]   UPE[m]  SIG-EPE  SIG-NPE  SIG-UPE\
   GDOP      PDOP     TDOP     HDOP     VDOP\n"}

{
	
	sod=$4;doy=$3;year=$2
	rx=$6;ry=$7;rz=$8;
	xpe=$9;ype=$10;zpe=$11;
	
	rlat=$15;rlon=$16;ralt=$17;
	epe=$19;npe=$18;upe=$20;
	sigma_east=$22;
	sigma_north=$21;
	sigma_up=$23;
	
	gdop=$24;
	pdop=$25;
	tdop=$26;
	hdop=$27;
	vdop=$28;
	
	nsats=$32;

	
	printf "%6.1f %3d %4d %4d %15.9f %15.9f %15.9f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n",sod,doy,year,nsats,rlat,rlon,ralt,epe,npe,upe,sigma_east,sigma_north,sigma_up,gdop,pdop,tdop,hdop,vdop
	
	
	}' "$1"
