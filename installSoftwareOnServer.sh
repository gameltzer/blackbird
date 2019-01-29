#!/bin/bash
# This installs additional linux software packages necessary for our application.
cd /opt/python/current/app
cd bcftools-1.9
sudo ./configure prefix=/usr/local
sudo make
sudo make install
cd ../samtools-1.9
sudo ./configure prefix=/usr/local
sudo make
sudo make install
cd ../bowtie2-2.3.4.3
sudo make static-lib
sudo make STATIC_BUILD=1
sudo make sudo make install
