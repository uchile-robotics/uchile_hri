#!/bin/sh


# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_speech";
install_path=$(rospack find "$pkg_name")/install;

# - - - - - - I N S T A L L - - - - - -
# # # # # # # # # # # # # # # # # # # #

# install recognizer
bash "$install_path"/install_recognizer.sh

# install synthesizer
bash "$install_path"/install_synthesizer.sh

echo ""
echo "Done. ;)"
echo ""
# :)
