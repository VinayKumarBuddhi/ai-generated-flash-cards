# ai-generated-flash-cards



at the "text_extractor\extractor\views.py" file under the upload_file :-replace api_key with your own api key
requirements:
1.install django-----pip install django

2.install extraction tools-------pip install PyPDF2 python-docx requests

3.create a django project-------django-admin startproject text_extractor

4.go to text_extractor folder create django app----------python manage.py startapp extractor

5.Open text_extractor/settings.py and add 'extractor' to the INSTALLED_APPS list

6.run migrations------python manage.py makemigrations
                      python manage.py migrate
                      
7.after all set up,start server--------python manage.py runserver
