# load line numbers

xml_file=$1
close_tag=$2
start=$3

path=/tmp/mesh_xml

if [ ! -z "$4" ]
   path=$4
fi

mkdir -p $path

num1=$start

for number in $(cat $xml_file | grep -n $close_tag | cut -d: -f1)
do
    num1=$(($num1 + 1))
    num2=$number
    printf -v sed_string "%s,%sp" $num1 $num2
    sed $sed_string $xml_file > touch $(printf "%s/%s.xml" $path $sed_string)
    num1=$num2
done

rm -rf $path
