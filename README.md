# netbox_nmap

The script reads subnet data from the networks.txt file and parses the Nmap output, extracts the address and description values ​​into XML. Then it converts the data received in XML format into JSON.
Then the API implements two methods Patch and Post. Patch checks the changes, Post creates hosts from the received data output.

For the plugin to work correctly, it is necessary:

1. First, you need to copy the repository and install the necessary packages:
```  
  $ git clone https://github.com/DarkFan911/netbox_nmap.git
  $ python3 -m venv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt
```

3. In the networks.txt file in the root of the project, specify the necessary subnets.
4. In the netbox-scanner.conf file, specify the address in the '10.x.x.x' format and the API authorization token in the 'token' format
5. In the __init__.py file in the nbc folder, at the end of the code, add the token and the netbox address in the 'https://x.x.x.x' format

The script is launched from the root folder with the nmap-scan.sh shell file

More detailed nmap scanning results will be implemented in the future.
I will also optimize the code in the near future and make dynamic values ​​in point 4 that will be automatically substituted from the conf file in the root directory.

===========================================================================

Скрипт считывает из файла networks.txt данные о подсетях и парсит вывод Nmap, извлекает значения address и description в XML. Затем конвертирует данные полученные в формате XML в JSON.
Далее по API реализованы два метода Patch и Post. Patch сверяет изменения, Post создает хосты с полученных вывода данных.

Для корректной работы плагина,необходимо:

1. Для начала необходимо скопировать репозиторий и поставить необходимые пакеты:
```
  $ git clone https://github.com/DarkFan911/netbox_nmap.git
  $ python3 -m venv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt 
```

2. В файле networks.txt в корне проекта прописать необходимые подсети.
3. В файле netbox-scanner.conf прописать адрес в формате '10.x.x.x' и токен авторизации по API в формате 'token'
4. В файле __init__.py  в папке nbc, в конце года дописать token и адрес netbox в формате 'https://x.x.x.x'

Скрипт запускается с корневой папки с shell файла nmap-scan.sh

В дальнейшем будет реализованы более подробные результаты сканирования nmap.
Так же в ближайшее время оптимизирую код и и сделаю в пункте 4 динамические значения которые будут автоматически подставляться с конф файла в корневой директории.
