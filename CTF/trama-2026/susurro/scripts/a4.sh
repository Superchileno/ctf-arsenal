#!/bin/bash
cd /mnt/c/Users/shapl/AppData/Local/Temp/opencode/susurro/out || exit 1
command -v convert magick
convert spec_full.png -crop 1200x190+120+770 +repage -resize 400% crop_text.png
identify crop_text.png
