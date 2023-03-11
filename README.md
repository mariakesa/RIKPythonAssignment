# RIKPythonAssignment

This is assignment for a job application at Registrite ja Infosüsteemide Keskus. I made a solution in Flask, SQLAlchemy and vanilla JavaScript. The aim of the application is to search and add companies to a registry. The application comes with scripts to automatically generate test data. 

To run the application first install Poetry for Python dependency management https://python-poetry.org/docs/

Clone the repository, cd to the project folder and run 'poetry install'.

Next, run 'poetry run python app.py' in the top-level directory. The application is now running on localhost. 

When first initializing the project the application will automatically check if the test.db exists in the folder and generate test data if it doesn't exist. If you would like to regenerate the test data at some point, you can delete test.db (it's initialized in the top-level folder) and re-run app.py as above. 

![alt text](https://github.com/mariakesa/RIKPythonAssignment/blob/main/doc_images/Screenshot%20from%202023-03-10%2002-37-18.png)
