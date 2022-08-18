# Steps to follow

1. Open Google Cloud Shell

	In your home directory create a virtual environment using the command below

	python3 -m venv myenv

2. Activate the environment:

	source myenv/bin/activate

3. In the home directory clone this project. This creates a directory called GC-March-2022

4. From the home directory run the below command

	pip install -r ./GC-March-2022/requirements.txt

5. After all the packages are downloaded, start the app by navigating into GC-March-2022 folder and using the command below:

	python3 main.py


6. To deploy to GCP, select the project to which you want to deploy through the dropdown box in the terminal and then run the below command:

	gcloud app deploy

