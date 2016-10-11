#!/bin/bash
mkdir -p export/

ORIEXPORT=datas/2016-10-11_ProtoLI3DS_BatU/2016-10-11_OriExport_Ori-RTL-Init.txt
#ORIEXPORT=datas/2016-07-18_LI3DS_Nexus5_Synch_BatU/micmac/OriExport_Ori-RTL-Init.txt

python app/OriExport_to_shapefile.py \
    $ORIEXPORT \
    -v \
    -s export/OriExport_Ori-RTL-Init \
    $@
