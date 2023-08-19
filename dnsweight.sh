#!/bin/bash
for i in {1..1000}
do
#domain=$(dig $1 $2 @RecursiveResolver_IP +short)
domain=$(dig $1 $2 +short)
echo $i"."$domain
echo -e  "$domain" >> RecursiveResolver_results.txt
done

# awk ' " " ' RecursiveResolver_results.txt | sort | uniq -c
