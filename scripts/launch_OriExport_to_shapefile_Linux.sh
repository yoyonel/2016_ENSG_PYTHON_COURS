#!/bin/bash
mkdir -p export/

python app/OriExport_to_shapefile.py \
    ../2016-07-18_LI3DS_Nexus5_Synch_BatU/micmac/OriExport_Ori-RTL-Init.txt \
    -v \
    -s export/OriExport_Ori-RTL-Init \
    $@
