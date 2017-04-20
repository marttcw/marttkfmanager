#!/bin/sh

echo "marttkfmanager cython3 Linux installation"
echo "cython3: Converting to C..."
cython3 --embed marttkfmanager.py -o marttkfmanager.c
echo "gcc: Compiling to executable..."
gcc $(pkg-config --libs --cflags python3) marttkfmanager.c -o marttkfmanager
echo "Making /usr/share/marttkfmanager directory..."
mkdir /usr/share/marttkfmanager
echo "Copying executable to /usr/bin..."
cp marttkfmanager /usr/bin/.
echo "Copying logo and default configuration to /usr/share/marttkfmanager..."
cp logo.png marttkfmanagerrc_DEFAULT /usr/share/marttkfmanager/.
echo "Done!"

