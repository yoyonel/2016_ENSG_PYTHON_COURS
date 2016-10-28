#!/bin/bash
mkdir -p export/

ORIEXPORT=datas/2016-07-18_LI3DS_Nexus5_Synch_BatU/micmac/OriExport_Ori-RTL-Init.txt

python app/OriExport_to_shapefile.py \
    $ORIEXPORT \
    -v \
    -s export/Nexus5/OriExport_Ori-RTL-Init \
    $@
