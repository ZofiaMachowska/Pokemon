# Pokmon
W ramach zajęć stworzyliśmy symulator walki pomiędzy Pokmonami inspirując się grą Pokemony i jej mechanizmami
walki. Gra dla dwóch graczy. Serwer pozwala klientom włączyć się do gry, tworzy osobny wątek dla 
każdej pary i pozwala im grać. 



## Specyfikacja

* Język implementacji: Python
* Framework do GUI: Tkinter
* Mechanizm komunikacji: XML-RPC
* Środowisko: PyCharm 

## Przebieg rozgrywki 

* Po uruchomieniu serwera jeden z graczy tworzy nową grę podając jej nazwę i hasło
* Drugi gracz dołącza się do istniejącej gry podając jej nazwę i hasło  
* Każdy z graczy wybiera 3 Pokmony z podanej listy i zatwierdza swój wybór
* Gracze wykonują ruchy naprzemiennie. Możliwe ruchy: 
– Wykonanie ataku. Aktywny gracz wybiera jeden atak z listy. Po zaznaczeniu ataku 
pojawią się jego szczegóły (typ, celność, moc). Niektóre typy ataków mogą być bardzo 
efektywne lub nieefektywne przeciwko konkretnym Pokmonom. Po podjęciu decyzji 
należy zatwierdzić wybrany atak. 
– Zmiana Pokmona. Aktywny gracz wybiera nowego Pokmona z listy Pokmonów, 
które wybrał przed bitwą. Po zaznaczeniu nowego Pokmona należy zatwierdzić 
wybór. 
* Jeżeli dowolny Pokmon omdleje, jego właściciel musi wybrać nowego Pokmona z listy 
Pokmonów, które wybrał przed bitwą. Po zaznaczeniu nowego Pokmona należy 
zatwierdzić wybór. Nie jest to uznawane za wykonanie ruchu. 
* Gracz wygrywa jeśli po pokonaniu Pokmona przeciwnika, ten nie będzie miał innych 
Pokmonów do wykorzystania.

## Zrzuty z gry

<h4>Ekran powitalny:</h4>
<p>
  <img src="/1.png ">
</p>

<h4>Wybór Pokmonow:</h4>
<p>
  <img src="/2.png ">
</p>

<h4>Rozgrywa:</h4>
<p>
  <img src="/3.png ">
  <img src="/4.png ">
</p>


## Uruchomienie
* Sklonuj repozytorium:
```sh
git clone https://github.com/ZofiaMachowska/Pokemon.git
```
* Zainstaluj wymagane pakiety:
```sh
pip install pillow
```
* Uruchom projekt:
```sh
python Server.py
```


 
