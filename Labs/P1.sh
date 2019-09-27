1
a) wc -l alice.txt //  wc -w alice.txt
b) grep just alice.txt
c) grep -c just alice.txt // grep just alice.txt | wc -l
d) grep -e "\s[jJ]ust\s" alice.txt 
e) tr -sc 'A-Za-z' '\n' < alice.txt | sort | uniq -c
f) tr -sc 'A-Za-z' '\n' < alice.txt | sort | uniq -c -i |sort -n | tail -n 20
2
a) tr -sc 'A-Za-z' '\n' < perguntasPT.txt | sort | uniq -c -i | wc -l
b) tr -sc 'A-Za-z' '\n' < alice.txt | sort | uniq -c
c) cat perguntasPT.txt |uniq -i | wc -l
d) cat perguntasPT.txt | sort | uniq -c -i |sort -nr
