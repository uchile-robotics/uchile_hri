#!/bin/sh


# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_nlp";
install_path=$(rospack find "$pkg_name")/install;
install_files="$install_path"/files;
DIRECTORY="files"; 

# - - - - - - I N S T A L L - - - - - -
## Download and install dependences

cd;
cd "$install_path";
if [ ! -d "$DIRECTORY" ]; then
  mkdir "$DIRECTORY";
fi
cd "$install_files";
git clone https://github.com/clips/MBSP.git;

