#!/bin/bash

# Desde un .txt genera un 'language model' para ser utilizado en
# el reconocimiento de voces de pocketsphinx

# prepare
cd "$(rospack find bender_speech)"/Grammar
#this_folder=$(rospack find bender_speech)/utils/

text2wfreq < "$1".txt | wfreq2vocab > "$1".vocab
text2idngram -vocab "$1".vocab -idngram "$1".idngram < "$1".txt
idngram2lm -vocab_type 0 -idngram "$1".idngram -vocab "$1".vocab -arpa "$1".arpa
sphinx_lm_convert -i "$1".arpa -o "$1".dmp
sphinx_lm_convert -i "$1".dmp -ifmt dmp -o "$1".lm -ofmt arpa
#pocketsphinx_continuous -lm 1.lm -dict 1.dic