# Data Engineering Project 1

This project aims to scrape flight information from TUI, Ryanair, Transavia, and Brussels Airlines. The project is implemented entirely in Python and is designed to run standalone on an Almalinux 9 server. The collected data will be cleaned and loaded into a MySQL database as the OLTP database. A Datawarehouse will be setup in the same MySQL environment. Creating a connection betwween PowerBI and MySQL will allow us to make multiple analysis reports on the collected data.

## Project Structure

The repository is organized into the following main folders:

- `dependencies`: Contains scripts and files for installing dependencies required by the project.
- `scrape`: Contains the main Python script `scrape.py` which is responsible for scraping flight information from the targeted airlines' websites.
- `services`: Contains the Python scripts `driver.py`, `selenium_helpers.py`, `utils.py` which initialize the drivers and additional utils for the scripts that are using selenium.
- `data_collection`: Contains temporary data generated during the scraping process.
- `clean_data_all`: Contains the cleaned data that was collected.
- `local_database_files`: Contains all needed **SQL** files to set up the OLTP database and the Datawarehouse.
- `DWH_sterschema`: Contains the **sterrenschema** for the Datawarehouse.

In addition to these folders, the repository also contains the following files:

- `.gitignore`: Specifies files and directories that should be ignored by Git.
- `ERD.dbfile_idk_extension`: The ERD database file used by the project.
- `Pipfile` and `Pipfile.lock`: The files that specify the dependencies required by the project.
- `README.md`: The file you are currently reading.
- `__init__.py`: An empty file that indicates to Python that the directory containing it should be considered a Python package.
- `cleaning_duplicates.py`: Python file that will clean a .csv file by getting rid of all the duplicates and output a new cleaned .csv file.
- `date_generator.py`: File that generates a list of all the dates starting from current up to a set end date.
- `scrape.py`: Main scraping script. It takes several arguments to scrape the desired airline. To be used within a pip virtual environment.

## Workflow MySQL and PowerBI

- `local_database_files`: Contains all SQL files needed to set up the OLTP database and Datawarehouse.

1. Use `airlines_OLTP_database.sql` to create the needed database structure for the OLTP database.
2. Use `airlines_DWH_database.sql` to create the needed database structure for the Datawarehouse.
3. Load in the data from `clean_data_all` by using the `OLTP_data_fill_tables.sql` script if you're running a Windows machine, in case of using a MACOS based system, use the `OLTP_data_fill_tables_MACOS.sql` script instead.
4. Call, after creating, the stored procedure in `fill_dimdate.sql` to fill the **DimDate** table in the Datawarehouse.
5. Use `fill_dimairport_dimairline.sql` to fill the **DimAirport** and **DimAirline** tables in the Datawarehouse.
