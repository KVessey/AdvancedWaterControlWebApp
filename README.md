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
* `pip install -r requiremnts/base.txt`

This will import all of the dependencies needed for this project, including:

* `RPi.GPIO`
* `flask`
* `flask-sqlalchemy`
* `psutil`
* `Flask-WTF`

## Usage

### Basic Usage

NOTES TO ADD TO README:
* DB will be automatically configured when app is started with db_init() script
* cron job will automatically start web application


After downloading, simply edit the HTML and CSS files included with the template in your favorite text editor to make changes. These are the only files you need to worry about, you can ignore everything else! To preview the changes you make to the code, you can open the `index.html` file in your web browser.

### Advanced Usage

NOTES TO ADD TO README:
* Advanced setup of cron job (how to configure)
* 


## Bugs and Issues

Have a bug or an issue with this template? [Open a new issue](https://github.com/KVessey/AdvancedWaterControlWebApp/issues) here on GitHub


## About

Start Bootstrap is an open source library of free Bootstrap templates and themes. All of the free templates and themes on Start Bootstrap are released under the MIT license, which means you can use them for any purpose, even for commercial projects.

## Future Work For AWCWA
- [ ] Create User Login page
- [ ] Add multiple plants to single Pi device

## References
* https://dzone.com/articles/flask-101-adding-a-database
* https://dzone.com/articles/flask-101-adding-editing-and-displaying-data
* https://gist.github.com/taniarascia/cb7d10cc3dbb5bcfaf974b2279cc5e37
* https://dzone.com/articles/flask-101-how-to-add-a-search-form
* https://dzone.com/articles/using-docker-for-python-flask-development
