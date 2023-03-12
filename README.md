# RIKPythonAssignment

This is assignment for a job application at Registrite ja Infosüsteemide Keskus. I made a solution in Flask, SQLAlchemy, Bootstrap and vanilla JavaScript. The aim of the application is to search and add companies to a registry. The application comes with scripts to automatically generate test data. 

To run the application first install Poetry for Python dependency management https://python-poetry.org/docs/

Clone the repository, cd to the project folder and run 'poetry install'.

Next, run 'poetry run python app.py' in the top-level directory. When you initialize for the first time,the test data will be automatically generated and it takes a few minutes. Please, be patient and wait for the `* Running on http://127.0.0.1:5000` message to appear. The application is now running on localhost and can be accessed in the web browser by visiting http://127.0.0.1:5000.

When first initializing the project the application will automatically check if the test.db exists in the folder and generate test data if it doesn't exist. If you would like to regenerate the test data at some point, you can delete test.db (it's initialized in the top-level folder) and re-run app.py as above. 

***


Siin on Registrite ja Infosüsteemide keskuse proovitöö lahendus. Ma programmeerisin minimaalse lahenduse Flaskis, SQLAlchemys, Bootstrapis ja JavaScriptis. Rakenduse eesmärgiks on otsida osaühinguid erinevate parameetrite järgi ning uusi osaühinguid lisada. Rakendusega on kaasas skriptid, mis automaatselt genereerivad testandmestiku.

Rakenduse jooksutamiseks installeerige Pythoni pakkide- ja sõltuvushaldur Poetry: https://python-poetry.org/docs/

Siis kloonige käesolev repositoorium, liikuge projekti kausta ning jooksutage 'poetry install'. 

Rakenduse käivitamiseks jooksutage 'poetry run python app.py'. Esmakordsel jooksutamisel toimub testandmete genereerimine, nii et peab ootama kuni paar minutit. Kui ekraanile ilmub `* Running on http://127.0.0.1:5000`, jookseb rakendus localhost'is ja selle saab veebilehitsejas avada aadressil http://127.0.0.1:5000. 

Soovi korral võib andmed uuesti initsialiseerida, kui kustutada projekti kaustast fail test.db ja rakendust uuesti jooksutada. Ma määrasin juhuarvude generaatori *seed'i*, mida saab muuta failis data_generation.py

Ma nägin rakendusega päris palju vaeva, nii palju kui vaba aega oli. Koodis on silumata osasid, aga loodan et üldiselt sai töö üsna hea ja kergesti kasutatav.

![alt text](https://github.com/mariakesa/RIKPythonAssignment/blob/main/doc_images/Screenshot%20from%202023-03-10%2002-37-18.png)
