#!/bin/sh


# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_speech";
install_path=$(rospack find "$pkg_name")/install;
install_files="$install_path"/files;


# - - - - - - I N S T A L L - - - - - -
# # # # # # # # # # # # # # # # # # # #

roscd;


## Download and install dependences

# speech recognizer (pocketsphinxs)
sudo apt-get install gstreamer0.10-plugins-base;
sudo apt-get install gstreamer0.10-pocketsphinx;
sudo apt-get install bison;
sudo apt-get install sphinxbase-utils;

# other tools
sudo apt-get install unzip;
sudo apt-get install autoconf automake


# Installing the speech recognition system
# ==========================================

# Untar pocketsphinx
cd "$install_files"/pocketsphinx/;
tar xvf pocketsphinx-0.8.tar.gz;
tar xvf sphinxbase-0.8.tar.gz;

# Configure sphinxbase
cd sphinxbase-0.8/;
./autogen.sh;
./configure;
make;
sudo make install;

# Configure pocketphinx
cd ../pocketsphinx-0.8;
./configure;
make;
sudo make install;

# Delete unnecessary folders
cd ..;
sudo rm -rf sphinxbase-0.8/;
sudo rm -rf pocketsphinx-0.8/;


# ------------------------------------------

# LOGIOS & CMUCLMTK tools (for offline compiling of dictionaries

# requerido
sudo apt-get install subversion ;

# download source
# TODO: fix this. when trying to install this from command line (using this install.sh script)
# some svn refs are not properly downloaded.
cd ;
svn checkout --non-recursive http://svn.code.sf.net/p/cmusphinx/code/trunk cmusphinx-code ;
svn update --set-depth infinity cmusphinx-code/logios ;
svn update --set-depth infinity cmusphinx-code/cmuclmtk ;

# make
cd ~/cmusphinx-code/cmuclmtk/ ;
./autogen.sh ;
./configure ;
sudo make install ;

# OBS: Si se encuentran problemas de compilación revisar paquetes de PERL faltantes

echo ""
echo "Done. ;)"
echo ""
# :)
