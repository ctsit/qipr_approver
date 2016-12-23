# load line numbers

xml_file=$1
close_tag=$2
start=$3

path=/tmp/mesh_xml

if [ ! -z "$4" ]
   then
   path=$4
fi

rm -rf $path
mkdir -p $path

num1=$start

for number in $(cat $xml_file | grep -n $close_tag | cut -d: -f1)
do
    num1=$(($num1 + 1))
    num2=$number
    printf -v sed_string "%s,%sp" $num1 $num2
    printf "processing lines %s to %s...\n" $num1 $num2
    sed -n $sed_string $xml_file > $(printf "%s/%s_to_%s.xml" $path $num1 $num2)
    num1=$num2
done
