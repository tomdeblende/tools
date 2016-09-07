#!/bin/bash

sed -e '1,7d' < cf.yml > removehead.txt
head -n -2 < removehead.txt > removetail.txt
sed '/^$/d' removetail.txt > cleared.txt
echo '[' > out.txt
while read line; do
	key=`echo $line | cut -d: -f1`
	value=`echo $line | cut -d: -f2 | sed 's/^ //g'`
	echo '{'
	echo '"ParameterKey": "'$key'",'
	echo '"ParameterValue": "'$value'"'
	echo '},'
done < cleared.txt >> out.txt
echo ']' >> out.txt
sed -n 'x;${s/,$//;p;x}; 2,$ p' < out.txt > params.json
rm -f out.txt cleared.txt removehead.txt removetail.txt
