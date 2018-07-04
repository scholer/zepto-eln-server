REM Use this script as a template;
REM Copy the script to a location of your choice (e.g. your desktop), configure the app by modifying the values,
REM and then execute the script to run the Zepto-ELN webserver app.
call activate zepto-eln
set FLASK_ENV=development
set ZEPTO_ELN_DOCUMENT_ROOT=D:/path/to/your/documents
set ZEPTO_ELN_TEMPLATE_DIR=D:/path/to/your/documents/templates
set FLASK_APP=zepto_eln.eln_server.eln_server_app
flask run

