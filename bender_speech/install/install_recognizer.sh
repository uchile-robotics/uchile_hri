#!/bin/sh


# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_speech";
install_path=$(rospack find "$pkg_name")/install;
install_files="$install_path"/files;


# - - - - - - I N S T A L L - - - - - -
# # # # # # # # # # # # # # # # # # # #






# Installing the speech recognition system
# ==========================================
cd;
cd "$install_files";
cd sphinxbase/;
./autogen.sh;
./configure;
make;
sudo make install;

export LD_LIBRARY_PATH=/usr/local/lib;
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig;

cd ../pocketsphinx
./autogen.sh;
./configure;
make;
sudo make install;





echo ""
echo "Done. ;)"
echo ""
# :)
