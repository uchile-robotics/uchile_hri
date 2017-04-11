#!/bin/sh
# run me like this: bash install/install.sh

# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_nlp"
install_path="$BENDER_WS/install/soft/hri/nlp"

# - - - - - - I N S T A L L - - - - - -


## Download and install dependences
mkdir -p "$install_path"
cd "$install_path"
git clone https://github.com/uchile-robotics-forks/MBSP.git


## Installing the speech recognition system
if [ ! -d "MBSP" ]; then
	echo "It seems the MBSP repository failed to download. Please try again."
	exit 1
fi

cd MBSP
sudo python setup.py install

echo ""
echo "Done. :)"
echo ""