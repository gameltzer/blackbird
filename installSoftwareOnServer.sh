cd /opt/python/current/app
cd bcftools-1.9
sudo ./configure /usr/local
sudo make
sudo make install

cd ../samtools-1.9
sudo ./configure /usr/locals
sudo make
sudo make install

cd ../bowtie2-2.3.4.3
sudo make static-lib
sudo make STATIC_BUILD=1
sudo make sudo make install