# Foodgram  
Simple web-app to exchange cooking recipes with your friends. Find, like and create shopping list for your lunch just in few clicks.  
  
  
### Stack:  
Backend based mostly on next technologies:  
- Python  
- Django  
- DRF  
- Djoser  
- Docker  
- PostgreSQL  
- nginx  
- gunicorn  

Front-end based on React and made by Ya.Practicum team.  



### How-to:  
Download ```infra``` folder from repo and run ```$ docker-compose up``` in ```infra``` folder.   
Don't forget to create ```.env``` file and populate it with Django Database settings.  
Run ```docker-compose exec backend bash``` and then   
```
python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py collectstatic && python3 manage.py load_json ingredients.json && python3 manage.py createsuperuser  
```  

### API
Documentations with example requests and responses availiable at   
51.250.69.189/api/docs/redoc  

### Examples

[GET] /api/users/ 
[POST] /api/users/ 
[GET] /api/tags/ 
[POST] /api/recipes/ 
[GET] /api/recipes/download_shopping_cart/
[POST] /api/recipes/{id}/favorite/ 
[DEL] /api/users/{id}/subscribe/
[GET] /api/ingredients/ 
  
### Author:
Dmitriy Belikov

### Check it out at...  
51.250.69.189/

Admin: dmtrybelickov@gmail.com
Password: 123
