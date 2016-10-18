#!/bin/bash
mkdir -p export/

ORIEXPORT=datas/2016-10-11_ProtoLI3DS_BatU/2016-10-11_OriExport_Ori-RTL-Init.txt

python app/OriExport_to_shapefile.py \
    $ORIEXPORT \
    -v \
    -s export/ProtoLI3DS/OriExport_Ori-RTL-Init \
    $@
