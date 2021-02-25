#!/bin/bash

declare -a ARRAY=()

while read symbol ; do

  ARRAY+=($symbol)
  
done < azure.txt

az login --service-principal --username ${ARRAY[0]} --tenant ${ARRAY[1]} --password ${ARRAY[2]}


sleep 10s
az vm start --resource-group ${ARRAY[3]} --name ${ARRAY[4]}
