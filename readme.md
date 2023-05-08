# API for data Processing and Modelling hate speech and abusive language detection in the Indonesian Twitter


## Data Collection =  dbtable.py
 **Create Database** : Create database in SQLite for data reference with table ABUSIVE and table ALAYSET. Database for documentation process API Text Processing in table TEXT_OUTPUT and API File Processing in table FILE_OUTPUT


## Cleansing Data = Cleansing.py
in this file is a function for cleansing punctuation, change data alay to normal, and remove abusive word:
 * **Cleansing Data Punctuation** : in this function is define for cleansing text from punctuation, web url, word 'user', word 'url', unidecode, and other.

 * **Change alay** : in this function is define for change word alay to normal in dataset
 example change word is :
    * *beud --> banget*
    * *jgn --> jangan*
    * *loe --> kamu*

 * **Remove Abusive** : in this function is define for remove abusive word form text based on file abusive word

## API File = main.py
In this API there are 2 API:
* **API Text Processing** : this end point can process input **text** on API to cleansing with function Cleansing and the outpun can show on API and recorded on tha database in table TEXT_OUTPUT
* **API File Processing** :this end point can process input **File.CSV** on API to cleansing with function Cleansing the output can show on API
The output recorded on tha database in table FILE_OUTPUT and **File.CSV** after process can show on local folder in **OUTPUT**


## API Visualatation with Flask Swagger and Gradio


# Citation
**Muhammad Okky Ibrohim and Indra Budi. 2019. Multi-label Hate Speech and Abusive Language Detection in Indonesian Twitter. In *ALW3: 3rd Workshop on Abusive Language Online, 46-57*.** (Every paper template may have different citation writting. For LaTex user, you can see **citation.bib**).

## License
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
"# Indonesian-Hate-Speech-Twitter-Text" 
