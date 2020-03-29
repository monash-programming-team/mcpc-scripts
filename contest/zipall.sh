#!/bin/bash

for i in `ls $1`; do
  pname=`basename $i`
  zname="${pname}.zip"
  cmd="cd ${1}${pname}"
  echo $cmd
  eval $cmd

  cmd="zip -r ${zname} *"
  echo $cmd
  eval $cmd
  
  cmd="cd -"
  echo $cmd
  eval $cmd
  
  cmd="mv ${1}${pname}/${zname} $1${zname}"
  echo $cmd
  eval $cmd
done
