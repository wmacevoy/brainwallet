common_words.txt :
	curl -o common_words.txt https://norvig.com/ngrams/count_1w.txt
defined_words.txt :
	...
words1.txt : words0.txt:
	cat words0.txt | egrep '[A-Za-z][A-Za-z][A-Za-z]+' | egrep -v '(ed|ly|ing)\t'
