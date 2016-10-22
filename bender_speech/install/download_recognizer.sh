#!/bin/sh


# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_speech";
install_path=$(rospack find "$pkg_name")/install;
install_files="$install_path"/files;


# - - - - - - I N S T A L L - - - - - -
## Download and install dependences

# speech recognizer (pocketsphinx)

sudo apt-get install gcc automake autoconf libtool bison swig; 
sudo apt-get install bison;
cd;
cd "$install_files";
git clone https://github.com/cmusphinx/sphinxbase.git;
git clone https://github.com/cmusphinx/pocketsphinx.git;


# other tools
sudo apt-get install unzip;
sudo apt-get install autoconf automake