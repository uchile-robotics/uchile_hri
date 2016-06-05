#!/bin/bash
#
# run me like this:
# > cdb bender_speech
# > bash install/install.sh
#

# - - - - - - S E T U P - - - - - - - -
# # # # # # # # # # # # # # # # # # # #

# Useful Variables
pkg_name="bender_speech"
pkg_path=$(rospack find "$pkg_name")
install_space="$BENDER_WS"/install/soft/hri/speech
mkdir -p "$install_space" && cd "$install_space"

# - - - - - - I N S T A L L - - - - - -
# # # # # # # # # # # # # # # # # # # #

## ensure we have all required files
# locations
tarfile="$install_space"/speech.tar.gz
tarfolder="$install_space"/files

tarfile_short="\"\$BENDER_WS\"/${tarfile#$BENDER_WS/}"
tarfolder_short="\"\$BENDER_WS\"/${tarfolder#$BENDER_WS/}/"
if [ ! -d "$tarfolder" ] || [ ! $(ls -A "$tarfolder") ]; then
	rm -rf "$tarfolder"
	echo " - speech install files NOT found on path: $tarfolder_short"

	if [ ! -e "$tarfile" ]; then
		echo " - tar file NOT found: $tarfile_short"

		# retrieve install files from mega
		echo " - ... retrieving tarfile from mega"
		"$BENDER_SYSTEM"/bash/megadown/megadown 'https://mega.nz/#!vltxCDoB!ZncFt39E9QMfCNW8-we7O7veBjlmKaAezcqrhbdYUDM'
	else
		echo " - tar file found: $tarfile_short"
	fi
	echo " - ... extracting speech files"
	mkdir -p "$tarfolder"
	tar -xf "$tarfile" -C "$install_space"
	echo " - ... OK"
else
	echo " - speech install files found on path: $tarfolder_short"
fi


# install synthesizer
bash "$pkg_path"/install/install_synthesizer.sh

# install recognizer
bash "$pkg_path"/install/install_recognizer.sh


echo ""
echo "Done. ;)"
echo ""
# :)
