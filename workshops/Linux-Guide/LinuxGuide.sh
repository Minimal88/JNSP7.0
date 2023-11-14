#!/bin/bash

################################################################################
# LinuxGuide.sh:
# An introduction to Linux by GNSS Academy
#
#  Project:        LINUX-GUIDE
#  File:           LinuxGuide.sh
#  Date(YY/MM/DD): 11/08/21
#
#   Author: GNSS Academy
#   Copyright 2021 GNSS Academy
#
# -----------------------------------------------------------------
# Date       | Author             | Action
# -----------------------------------------------------------------
# 15/07/21     tapiasa              Creation
################################################################################


#*******************************************************************************
#*******************************************************************************
#                           LINUX GUIDE JSNP
#*******************************************************************************
#*******************************************************************************

# Remove previous filesystem and create a new one
rm -rf filesystem
mkdir filesystem
cd filesystem

set -x

# cat << EOC
# Directories
#-------------------------------------------------------------------------------
pwd
# Directory creation
mkdir DIR1 DIR2 DIR3 DIRN DIRN/DIRN1 DIRN/DIRN2 DIRN/DIRNN
cd DIR1
pwd
cd ..
pwd
cd DIRN/DIRN1
pwd
cd ../..

# Files
#-------------------------------------------------------------------------------
# Empty files creation
touch file1.txt .file2 DIR1/file11.txt DIR3/file31.dat

# List files and directories in working directory
ls
# List files and directories recursively from working directory
ls -R
# with expanded information:
ls -Rlrt
# including hidden
ls -Rlrta

# stdout
echo This is a string
echo This is a string > newfile.txt
cat newfile.txt
echo This is a string >> newfile.txt
echo This is a string > newfile.txt
echo This is a string | tee newfile.txt
cat newfile.txt

# stdin
cat newfile.txt | wc -l

# stderr
ls file.txt > ls.out 2> ls.err
cat ls.out 
cat ls.err

# Show default permissions
umask

# Change default permissions
umask 111
umask 22

# Changing permissions
ls -lrt newfile.txt

chmod -r newfile.txt
ls -lrt newfile.txt

chmod +w newfile.txt
ls -lrt newfile.txt

chmod +x newfile.txt
ls -lrt newfile.txt

chmod 777 newfile.txt
ls -lrt newfile.txt


# Symbolic links
#-------------------------------------------------------------------------------
cd DIR2

# Create symbolic link
ln -s ../DIR1/file11.txt file21.txt
cd -

# Check the link
ls -Rlrt

# Filesystem commands
#-------------------------------------------------------------------------------
# Fancy representation of the filesystem
tree

# Check total size
du
du -sh .

# Check available space in disk
df
df -h .

# Get filename and directory from path
pwd
basename $(pwd)
dirname $(pwd)

# Copy files
cp -v newfile.txt file1.txt
cp -v newfile.txt file2.txt
cp -v newfile.txt DIR2
ls -lrt . DIR2

# Move files
mv -v DIR2/newfile.txt DIR1
mv -v DIR1/newfile.txt DIR1/file12.txt
ls -lrt . DIR1 DIR2

# Remove files
rm newfile.txt

# Manipulating directories
cp -v -r DIR1 DIR4
mv DIR4 DIRN/DIRN3
rm -rf DIR3
rmdir DIR1
rmdir DIRN/DIRN1
ls -lrt . DIRN

# Wildcards
ls -lrt file*
ls -lrt *.out
ls -lrt ???[1N]
mv ???[1N] /tmp
rm *.err
rm -rf /tmp/???[1N]

# Skipping special characters
echo *
echo \*

# find
find . -type f
find . -type d
find . -type f -name "file*"
find . -type d -name "file*"
find / -maxdepth 3 -type d -name "*lib*"
find / -maxdepth 3 -type d -name "*lib*" 2> /dev/null

# Create a longer file
python -m this > file3.txt

# Looking inside files
# Paginated more
# more file3.txt
cat file3.txt
ghead file3.txt
ghead -3 file3.txt
gtail -1 file3.txt
gtail file3.txt

gtail -n +3 file3.txt > file4.txt
cat file4.txt

wc file3.txt file4.txt

# Check contents differences
cmp file3.txt file4.txt
diff file3.txt file4.txt
sdiff file3.txt file4.txt

cp file4.txt file5.txt
cmp file5.txt file4.txt
diff file5.txt file4.txt

# Create tarball
tar cvf filesystem.tar *
gzip filesystem.tar
tar cvfz filesystem.tar.gz $(ls | grep -v tar)


# Variables
#-------------------------------------------------------------------------------
var=10
var2="Hello, world"
var3=$(ls)

# Global variables
export MY_VAR=5

# Check their contents
echo $var
echo ${var}0
echo $var2

# Variable substitution
echo ${var2/, world} 
echo ${var2//world/friend}
echo ${var2:2} 
echo ${var2:2:7}

# Built-in variables
echo $PWD
echo $HOME


# Control statements
#-------------------------------------------------------------------------------
list=$(ls file*)

# for element in list
for f in $list
do
    echo $f

done

# for element in list (compact)
for f in $list; do echo $f; done

# classic for
for((i=0; i<5; i++)); do echo $i $((i*i)); done

# if
if [ $i -gt 4 ]
then
    echo i = $i \> 4

else echo i = $i \<= 4
fi

# compact if
[ $i -le 4 ] && echo Condition checked && echo i is lower or equal to 4
[ $i -gt 4 ] && echo i is greater than 4

# Other examples of for loop
for f in $(ls *.txt); do mv $f ${f/.txt/.dat}; done
for ((i=1; i<=9; i++)); do mkdir -p DIR$i/DIR${i}1; done
ls -lrt


# Text manipulation
#-------------------------------------------------------------------------------
# echo prints its arguments to stdout
echo Hello, world

# printf is also available in the command line
string="This is a string"
pi=3.1416
printf "%-20s: %d %02d %8d %f %15.3f %e\n" "$string" 2 2 2 $pi $pi $pi
printf "%-20s: %d %02d %8d %f %15.3f %e\n" $string 2 2 2 $pi $pi $pi

# Create shortcut to OBSZ file
ln -s ../OBS_TLSZ_Y19D014.dat

# more to read files in paginated form
# more OBS_TLSZ_Y19D014.dat

# cat concatenates files
ls file?.dat
cat file?.dat

# Find patterns in your file
# Find lines containing the word if (case sensitive)
grep if file?.dat

# Find lines containing the word if (case insensitive)
grep -i if file?.dat

# Find lines beginnning with the word if (case insensitive)
grep -E -i '^if' file?.dat

# Find lines ending with the word if (case insensitive)
grep -E -i '!$' file?.dat

# Find lines beginnning with the word "if" and ending with "good idea" (case insensitive)
grep -E -i '^if.*good idea.$' file?.dat

# Inverse grep
grep -E -i -v '\.$' file?.dat

# cut your file to select some columns
cut -c1-6 OBS_TLSZ_Y19D014.dat > OBS_TLSZ_Y19D014_SOD.dat
ghead OBS_TLSZ_Y19D014_SOD.dat

cut -c25-28 OBS_TLSZ_Y19D014.dat > OBS_TLSZ_Y19D014_PRN.dat
ghead OBS_TLSZ_Y19D014_PRN.dat

# File sorting
sort OBS_TLSZ_Y19D014_PRN.dat | ghead -100

# File sorting + duplicates supression
sort OBS_TLSZ_Y19D014_PRN.dat | uniq
cat OBS_TLSZ_Y19D014_SOD.dat  | sort | uniq | ghead -100 > OBS_TLSZ_Y19D014_SOD_sorted.dat

# Character translation with sed
sed 's/e/E/g' file3.dat
sed 's/\./,/g' file3.dat
# in-place
sed -i .bk 's/e/E/g' file3.dat

# Character deletion with sed
sed 's/\.//g' file3.dat

# Change only some of the occurences
echo "My string my string" | sed 's/str/Str/1'
echo "My string my string" | sed 's/str/Str/2'

# paste files horizontally
paste OBS_TLSZ_Y19D014_SOD.dat OBS_TLSZ_Y19D014_DOY.dat | ghead -100
nlines=$(wc -l file4.dat | gawk '{print $1}')
paste <(ghead -${nlines} OBS_TLSZ_Y19D014_SOD_sorted.dat) file4.dat <(sed 's/e/E/g' file4.dat)

# EOC

# gawk
#-------------------------------------------------------------------------------
# Display only some lines
gawk '$1 < 5' OBS_TLSZ_Y19D014.dat
gawk '$4 == "E"' OBS_TLSZ_Y19D014.dat | ghead
gawk '$5 == 10' OBS_TLSZ_Y19D014.dat | ghead

# Display only some columns
gawk '{print $6}' OBS_TLSZ_Y19D014.dat | ghead
gawk 'NR==1 {print $7} NR!=1 {print $6}' OBS_TLSZ_Y19D014.dat | ghead

gawk '{print $6, $7}' OBS_TLSZ_Y19D014.dat | ghead
gawk '{printf("%8.3f %8.3f\n", $6, $7)}' OBS_TLSZ_Y19D014.dat | ghead

# Display only some columns but skip header this time
# NR (Number of Records)
gawk 'NR>1 {printf("%8.3f %8.3f\n", $6, $7)}' OBS_TLSZ_Y19D014.dat | ghead

# Number of fields (NF)
gawk 'NR>1 {print NF}' OBS_TLSZ_Y19D014.dat | ghead

# Output Record Separator (ORS)
gawk 'BEGIN {ORS=" "} {print}' file3.dat

# Output Field Separator (OFS)
gawk 'BEGIN {OFS=";"} {$1=$1; print}' OBS_TLSZ_Y19D014.dat | ghead

# Pass variables and use logical expressions in condition
elev=6; azim=7;
gawk -v elev=$elev -v azim=$azim 'NR>1 && $5==5 {printf("%8.3f %8.3f\n", $elev, $azim)}' OBS_TLSZ_Y19D014.dat | ghead

# Print line numbers
gawk '{printf("%5d| %s\n", NR, $0)}' OBS_TLSZ_Y19D014.dat | ghead

# Skip comments
gawk '/#/ {next} {printf("%5d| %s\n", NR, $0)}' OBS_TLSZ_Y19D014.dat | ghead

# Arrays
gawk '
BEGIN {
    sod=1
    doy=2
    year=3
    const=4
    prn=5
    elev=6
    azim=7
    c1=8
    l1=9
    p2=10
    l2=11
    s1=12
    s2=13
}
/#/ {next} 
{
    sat = sprintf("%s%02d", $const, $prn)
    sum[sat] += $s1
    n[sat] += 1
}
END {
    for (sat in sum) {
    printf("%s: %f\n", sat, sum[sat]/n[sat])
    }
}
' OBS_TLSZ_Y19D014.dat | sort

# Numeric functions
gawk 'BEGIN {print cos(0)}'
gawk 'BEGIN {print rand()}'
gawk 'BEGIN {print sqrt(2)}'
sqrt2=$(gawk 'BEGIN {print sqrt(2)}')
echo $sqrt2 | gawk '{print $1*$1}'
echo 2 $sqrt2 | gawk '{print $1*$2}'

# gnuplot
#-------------------------------------------------------------------------------
cat << EOF | gnuplot --persist
plot "OBS_TLSZ_Y19D014.dat" u 1:6 w p
plot "<gawk '\$5==5' OBS_TLSZ_Y19D014.dat" u 1:6 w p pt 2 ps .5 lc "orange" t "Elevation [deg]"
set title 'Elevation PRN05'
plot "<gawk '\$5==5' OBS_TLSZ_Y19D014.dat" u 1:6 w p pt 2 ps .5 lc "orange" t "Elevation [deg]"
plot "<gawk 'NR>1 && \$5==5' OBS_TLSZ_Y19D014.dat" u (\$1/3600):6 w p pt 2 ps .5 lc "orange" t "Elevation [deg]"
set xtics 1
plot "<gawk 'NR>1 && \$5==5' OBS_TLSZ_Y19D014.dat" u (\$1/3600):6 w p pt 2 ps .5 lc "orange" t "Elevation [deg]"
plot [0:24] "<gawk 'NR>1 && \$5==5' OBS_TLSZ_Y19D014.dat" u (\$1/3600):6 w p pt 2 ps .5 lc "orange" t "Elevation [deg]"
plot [0:24] "<gawk 'NR>1 && \$5==5' OBS_TLSZ_Y19D014.dat" u (\$1/3600):6 w p pt 2 ps .5 lc "orange" t "PRN05 Elevation [deg]", "<gawk 'NR>1 && \$5==6' OBS_TLSZ_Y19D014.dat" u (\$1/3600):6 w p pt 2 ps .5 lc "green" t "PRN06 Elevation [deg]"
EOF


# Miscellaneous commands
#-------------------------------------------------------------------------------
gawk --help
gawk -h
gawk --version

which ls

# history

# man

# top

# htop

# sleep

# Sourcing a file
. ../GnssConstants.sh

# Access a variable from the sourced file
echo $FLATTENING



