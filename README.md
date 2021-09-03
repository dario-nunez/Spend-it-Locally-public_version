# Spend-it-Locally
#### By Dario Nunez

A Data Science system to analyse the socio-economic state of The City of Westminster in London, United Kingdom. Consists of a data processing pipeline written in Python and a user interface and data visualization system written in Javascript. The system deals with resident census data, a places catalogue, population demographic distribution estimate models and supply & demand metrics. 

## Running instructions

In the delivered version of the project, the datasets in the data processing project are not present due to legal reasons. The user interface does have the datasets it requires to run, so the running instructions can be followed starting at step 6. 

### Steps

**(Data processing pipeline)**

1. Ensure all the required raw data files are found in the appropriate subdirectories under `data_processing/raw_data`.
2. Execute the `run_scrape_places.py` script.
3. Execute the `run_focused.py` script.
4. Execute the `run_processed.py` script.
5. Execute the `copy_dataset_files.py` script.

**(User interface and visualization web application)**

6. Ensure all the required data files are found in the `user_interface/website_ui/data` directory.
7. Launch the web application project. 

### Web application launching

For development, testing and demonstrations, it is sufficient to launch the app in a local development server. Many alternatives exist but a working procedure is detailed below:

1. Download and install the Visual Studio Code (VSCode) code editor at https://code.visualstudio.com/.
2. In the Extensions pane on the left hand side tool bar, install the Live Server extension. Can also be found at https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer.
3. Open the project root `Spend-it-Locally` with VSCode.
4. Open the `index.html` file in the main code editing window.
5. Click on the *Go Live* button in the bottom right of the editor window.
