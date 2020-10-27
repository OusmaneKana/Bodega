Mandatory Files:
- Have the initial excel renames "sbler" and formatted .xlsx in the same folder as the executable "run"




Step 1: Donwload Python ( Version )

	https://www.python.org/downloads/

Step 2: Install the dependencies
	- Make sure you are in the Folder Bodega\bodega
	- In the address bar the current folderp type "powershell" to open a terminal
	- in the terminal, copy-paste the following code:
		pip install -r requirements.txt

Step 3: Run the app 
	- After the all the libraries have been installed, run the software wuth the "run.bat"
	- The output is going to be stored in \dataBase




******************************* IMMPORTANT TIPS ********************************

The current the current request delay is set to 0 sec. I order to avoid 
getting kick-out by the server. 

The recommended delay is between 0.5 to 2 seconds

To change these settings, open the file bodega\settings.py and look for the following variables:


		DOWNLOAD_DELAY 
		AUTOTHROTTLE_ENABLED 


You can set the value of download_delay = anytimeyouChoose, or (what I advice) set autothrottle_enabled = true.
 
remove the # to turn to comment into aline of code