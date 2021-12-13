#Get INN of people according to their data

### How to install
Alert!! Work on Python 3.9<br/>
Open the folder in the cmd, write this in it:<br/>
`pip install -r requirements.txt`

### How to start
Open the folder in the console, write this in it:<br/>
`py main.py`

Select document with peoples data what looks like <br/>
`surname|name|patronymic(Optional)|year-month-day|passport`<br/>
and pick output folder. After that press "Начать". Code will send requests
to server and show you answers on it, in parallel, it creates a file
"completed.txt" in directory what you pick (or supplement it if it already exists)
file will be created and data will be written to this file.

### Description of files
Config.py - config class, that have many methods that manipulate with config<br/>
Controller.py - two classes with all logic, that touches the layer between requests and the interface<br/>
inn_requests.py - two function with requests to server<br/>
Interface.py - class with all logic that manipulate interface.<br/>
main.py - starter<br/>
window.ui - application visual<br/>