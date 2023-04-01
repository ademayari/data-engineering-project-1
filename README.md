# Data Engineering Project 1

This project aims to scrape flight information from TUI, Ryanair, Transavia, and Brussels Airlines. The project is implemented entirely in Python and is designed to run standalone on an Almalinux 9 server.

## Project Structure

The repository is organized into the following main folders:

- `dependencies`: Contains scripts and files for installing dependencies required by the project.
- `scrape`: Contains the main Python script `scrape.py` which is responsible for scraping flight information from the targeted airlines' websites.
- `service`: Contains the Python script `date_generator.py` which generates dates to be used by `scrape.py`.
- `tijdelijke_data`: Contains temporary data generated during the scraping process.

In addition to these folders, the repository also contains the following files:

- `.gitignore`: Specifies files and directories that should be ignored by Git.
- `ERD.dbfile_idk_extension`: The ERD database file used by the project.
- `Pipfile` and `Pipfile.lock`: The files that specify the dependencies required by the project.
- `README.md`: The file you are currently reading.
- `__init__.py`: An empty file that indicates to Python that the directory containing it should be considered a Python package.
