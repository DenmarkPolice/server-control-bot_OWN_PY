#!/bin/bash

declare -a ARRAY=()

while read symbol ; do

  ARRAY+=($symbol)
  
done < azure.txt

az login --service-principal --username ${ARRAY[0]} --tenant ${ARRAY[1]} --password ${ARRAY[2]}


sleep 10s
az vm start -g ${ARRAY[3]} -n ${ARRAY[4]}
