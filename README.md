## Advanced Water Control Web Application

The Advanced Water Control Web Application (AWCWA) is an admin dashboard which leverages Raspberry Pi devices to manage water across multiple properties via a single web app

## Download and Installation

To begin using the Advanced Water Control Web App, use the following steps to get started:
* [Fork, Clone, or Download on GitHub](https://github.com/KVessey/AdvancedWaterControlWebApp) Advance Water Control Web App

## Setup
### Python Packages
1. First we need to make sure Python is installed and up to date. On windows, open the command prompt and enter:
 `python -V`

User should see a python version. If your version is less than 3, it is best to update to the latest version of python

2. Check the version of pip
On windows, open the command prompt and enter:
 `pip -V`

Pip should come with Python version 3+. If pip is not installed, recheck the version of Python which is installed

To setup the application on the Raspberry Pi, we must run the following commands to include the python packages:
* `pip install -r requirements/requirements.txt`

This will import all of the dependencies needed for this project, including:

* `RPi.GPIO`
* `flask`
* `flask-sqlalchemy`
* `psutil`
* `Flask-WTF`

## Usage

### Basic Usage
This web application is configured with a cron job which automatically boots when the Raspberry Pi device is switched on. This is done to make the process seemless when adding a new Pi device. Details on configuring the cron job will be listed in the Advanced Usage section below.

To manually boot the web application, simply run the following command in your project directory:
`python main.py`
This will boot the Flask web application, and generate the database with empty tables for the user to later populate.

Currently, the database has two tables (Devices and Plants), which store data related to the device the user is registering as well as the plant information which is configurable. The user should navigate to the Device Configuration page or the Plant Configuration page in the web application to add/edit an entry from the database.

### Advanced Usage

NOTES TO ADD TO README:
* Advanced setup of cron job (how to configure)
* 


## Bugs and Issues

Have a bug or an issue with this template? [Open a new issue](https://github.com/KVessey/AdvancedWaterControlWebApp/issues) here on GitHub


## Future Work For AWCWA
- [ ] Create User Login page
- [x] Add multiple plants to single Pi device
- [ ] Configure cron job to automatically boot web server upon device startup

## References
* https://dzone.com/articles/flask-101-adding-a-database
* https://dzone.com/articles/flask-101-adding-editing-and-displaying-data
* https://gist.github.com/taniarascia/cb7d10cc3dbb5bcfaf974b2279cc5e37
* https://dzone.com/articles/flask-101-how-to-add-a-search-form
* https://dzone.com/articles/using-docker-for-python-flask-development
