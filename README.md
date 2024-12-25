# netbox_nmap

The script selects data about subnets from the networks.txt file, parses the nmap output, extracts the address and description values ​​into XML, and then converts them into JSON format.
Then, two methods, Patch and Posy, are implemented via the API. Patch checks the changes, Post creates hosts from the received data output.

For the plugin to work correctly, it is necessary:

1. First, you need to copy the repository and install the necessary packages:

  $ git clone https://github.com/DarkFan911/netbox_nmap.git
  $ python3 -m venv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt

2. In the networks.txt file in the root of the project, specify the necessary subnets.
3. In the netbox-scanner.conf file, specify the address in the '10.x.x.x' format and the API authorization token in the 'token' format
4. In the __init__.py file in the nbc folder, at the end of the year, add the token and the netbox address in the 'https://x.x.x.x' format

The script is launched from the root folder with the nmap-scan.sh shell file

More detailed nmap scanning results will be implemented in the future.
I will also optimize the code in the near future and make dynamic values ​​in point 3 that will be automatically substituted from the conf file in the root directory.

=========================================================================================

Скрипт выбирает из файла networks.txt данные о подсетях парсит вывод нмап, извлекает значения адресс и дескрипшен в XML, а затем конвертировать в формат в JSON.
Далее по АПИ реализованы два метода Patch и Posy. Patch сверяет изменения, Post создает хосты с полученных вывода данных.

Для корректной работы плагина,необходимо:

1. Для начала необходимо скопировать репозиторий и поставить необходимые пакеты:

  $ git clone https://github.com/DarkFan911/netbox_nmap.git
  $ python3 -m venv venv
  $ source venv/bin/activate
  $ pip install -r requirements.txt 

2. В файле networks.txt в корне проекта прописать необходимые подсети.
3. В файле netbox-scanner.conf прописать адрес в формате '10.x.x.x' и токен авторизации по API в формате 'token'
4. В файле __init__.py  в папке nbc, в конце года дописать token и адрес netbox в формате 'https://x.x.x.x'

Скрипт запускается с корневой папки с shell файла nmap-scan.sh

В дальнейшем будет реализованы более подробные результаты сканирования nmap.
Так же в ближайшее время оптимизирую код и и сделаю в пункте 3 динамические значения которые будут автоматически подставляться с конф файла в корневой директории.
