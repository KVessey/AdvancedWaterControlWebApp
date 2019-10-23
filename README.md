## Advanced Water Control Web Application

The Advanced Water Control Web Application (AWCWA) is an admin dashboard which leverages Raspberry Pi devices to manage water across multiple properties via a single web app

## Download and Installation

To begin using the Advanced Water Control Web App, use the following steps to get started:
* [Fork, Clone, or Download on GitHub](https://github.com/KVessey/AdvancedWaterControlWebApp) Advance Water Control Web App

## Setup
### Python Packages
1)First we need to make sure Python is installed and up to date. On windows, open the command prompt and enter:
>> python -V

User should see a python version. If your version is less than 3, it is best to update to the latest version of python

2)Check the version of pip
On windows, open the command prompt and enter:
>> pip -V

Pip should come with Python version 3+. If pip is not installed, recheck the version of Python which is installed

To setup the application on the Raspberry Pi, we must run the following commands to include the python packages:
* pip install RPi.GPIO
* pip install flask
* pip install flask-sqlalchemy
* pip install psutil

## Usage

### Basic Usage

After downloading, simply edit the HTML and CSS files included with the template in your favorite text editor to make changes. These are the only files you need to worry about, you can ignore everything else! To preview the changes you make to the code, you can open the `index.html` file in your web browser.

### Advanced Usage

After installation, run `npm install` and then run `npm start` which will open up a preview of the template in your default browser, watch for changes to core template files, and live reload the browser when changes are saved. You can view the `gulpfile.js` to see which tasks are included with the dev environment.


## Bugs and Issues

Have a bug or an issue with this template? [Open a new issue](https://github.com/BlackrockDigital/startbootstrap-sb-admin/issues) here on GitHub or leave a comment on the [template overview page at Start Bootstrap](http://startbootstrap.com/template-overviews/sb-admin/).


## About

Start Bootstrap is an open source library of free Bootstrap templates and themes. All of the free templates and themes on Start Bootstrap are released under the MIT license, which means you can use them for any purpose, even for commercial projects.

