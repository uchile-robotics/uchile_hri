#!/bin/sh

sudo apt-get install portaudio19-dev
sudo pip install pyaudio
curl -O -J -L "https://drive.google.com/uc?export=download&id=1PSKIwIaAzPoSJNEYR27kjeQs5jdF5Vcg"
sudo pip install deepspeech-0.8.2-cp27-cp27mu-manylinux1_x86_64.whl
rm deepspeech-0.8.2-cp27-cp27mu-manylinux1_x86_64.whl
# get models
model_dir="$(dirname $(dirname $(realpath $0)) )/model"
if [ -d $model_dir ] 
then
    echo "Directory /model/ exists." 
else
    mkdir $model_dir
fi

if [ -f "$model_dir/deepspeech-0.8.2-models.pbmm" ]; 
then
    echo "model exists."
else
    echo "Downloading model"
    ggID='1RA3FXlBqZetmmrKUkweZmZlOBJSviBg-'  
    ggURL='https://drive.google.com/uc?export=download'  
    curl -sc /tmp/gcokie "${ggURL}&id=${ggID}" >/dev/null  
    getcode="$(awk '/_warning_/ {print $NF}' /tmp/gcokie)"  
    curl -Lb /tmp/gcokie "${ggURL}&confirm=${getcode}&id=${ggID}" -o "$model_dir/deepspeech-0.8.2-models.pbmm"  
    #curl -L "https://drive.google.com/uc?export=download&id=1RA3FXlBqZetmmrKUkweZmZlOBJSviBg-" -o "$model_dir/gpsr.scorer"
fi

if [ -f "$model_dir/gpsr.scorer" ]; 
then
    echo "scorer exists."
else
    echo "Downloading scorer"
    curl -L "https://drive.google.com/uc?export=download&id=1bo1XUXfO83-kstjZIJgZFrycLdQLKbOr" -o "$model_dir/gpsr.scorer"
fi