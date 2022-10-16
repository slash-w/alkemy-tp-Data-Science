 Para crear el entorno virtual se debera abrir CMD en la carpeta donde se quiere crear
y se introducira este comando:
python -m venv myvenv

 Una vez creado, vamos a movernos dentro de el
cd myvenv

 Ahora hay que activarlo para instalar las librerias necesarias
./Scripts/activate.bat

 Ya habiendo activado nuestro venv instalamos las librerias
python -m pip install pandas
python -m pip install sqlalchemy
python -m pip install psycopg2
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

 No llegue a crear la BDD desde sqlalchemy, asi que voy a dejar el archivo .sql para 
que se haga de forma manual
