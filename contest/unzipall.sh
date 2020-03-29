for i in `ls $1`; do
  fname=${i%-*}
  cmd="unzip '${1}${i}' -d $1${fname}"
  echo $cmd
  eval $cmd
done
