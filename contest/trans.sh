#!/bin/bash
for i in `find $1 -not -name "*.a" -type f`; do
  cmd="mv $i $i.in"
  echo $cmd
  eval $cmd
done

for i in `find $1 -name "*.a" -type f`; do
  f="${i%.a}"
  cmd="mv $f.a $f.ans"
  echo $cmd
  eval $cmd
done
