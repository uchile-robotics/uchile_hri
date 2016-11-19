#!/bin/sh


# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_nlp";
install_path=$(rospack find "$pkg_name")/install;
install_files="$install_path"/files;


# - - - - - - I N S T A L L - - - - - -
# # # # # # # # # # # # # # # # # # # #






# Installing the speech recognition system
# ==========================================
cd;
cd "$install_files";
cd MBSP/;
sudo python setup.py install;
cd;




echo ""
echo "Done. ;)"
echo ""
# :)
