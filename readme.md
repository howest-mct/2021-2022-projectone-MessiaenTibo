# Project One - Name of the project

**De inhoud van dit document schrijf je volledig in het Engels**

Omschrijf het project. Doe dit in het markdown formaat.
- [Syntax md](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

Hoe kan een externe persoon (die niets weet over de "ProjectOne" opdracht) het project snel runnen op de eigen pc?
Op github vind je verschillende voorbeelden hoe je een readme.md bestand kan structureren.
- [Voorbeeld 1](https://github.com/othneildrew/Best-README-Template)
- [Voorbeeld 2](https://github.com/tsungtwu/flask-example/blob/master/README.md)
- [Voorbeeld 3](https://github.com/twbs/bootstrap/blob/main/README.md)
- [Voorbeeld 4](https://www.makeareadme.com/)

## Inhoud
<!-- GETTING STARTED -->
## Getting Started
This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.
### Installation
_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._
1. Clone the repo
   ```sh
   gitclone https://github.com/howest-mct/2021-2022-projectone-MessiaenTibo.git
   ```
2. Installing python packages
    ```
    - pip install mysql-connector-python
    - pip install flask-socketio
    - pip install flask-cors
    - sudo pip install adafruit-circuitpython-neopixel
    ```
3. Enable
    ```
    sudo raspi config
    ```
    <p>Go to 3 Interfacing Options. (use the arrow keys)</p>
    <p>Enable I2C (For the  LCD)</p>
    <p>Enable Serial Port (for printing)</p>
    <p>Enable One-wire (For the Temperature sensor)</p>
<p align="right">(<a href="#top">back to top</a>)</p>
<!-- USAGE EXAMPLES -->

## Usage

The complete application is easy to use. Place the rubberduck with the magnet on one of the 4 magnet-contacts and that 'person' is ready to shower. The watertemp, waterflow, room temp and humidity will be mesured and saved in the database. These mesurements are also visible on the home page of the website.


  
## Instructables
https://www.instructables.com/Water-shower-monitor/