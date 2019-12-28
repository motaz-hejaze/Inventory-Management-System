# Inventory-Managment-System

A Managment System with concept applicable for Inventories , stores any thing regarding keeping and storing items

The system characterstics are:

- Two Generators function to generate dummy data ( 1000 user and 10000 items )
- Using python asyncio with generator function to keep the generation in background and not block request/response cycle
- Multiuser system ( Three user types )
- Using Datatables for more efficient data representation
- Beautifull admin interface built on top of bootstrap
- Modern notification cards that enhance the UX
- Profile page for each user
- Authorization System to permit only allowed user type to view the content of the page

Requirements:

1 - python >= 3.4
2 - virtualenv or pipenv

Installation: 

1 - git init 

2 - git remote add origin https://github.com/motaz-hejaze/Inventory-Managment-System.git

3 - git pull origin master

4 - virtualenv myenv -p python3

5 - source myenv/bin/activate

6 - pip install -r requirements.txt

7 - python manage.py makemigrations

8 - python manage.py migrate

9 - python manage.py createsuperuser
  
  - username : admin
  - email : admin@admin.com
  - password : whateveryouwant
  - Role : Administrator
  
10 - python manage.py runserver

11 - open 127.0.0.1:8000 in your browser
