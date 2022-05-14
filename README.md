<!-- GETTING STARTED -->
## Web scaping tool

This is a sperimental web scraping tool which allows the scaping of images and related text contained in the media tags of HTML in order to make analysis on the output.The tool creates for each page scraped a folder with all the website's images found in css an html, a BigFile.csv in order to make allow possible AI analyisis on them,a more detailed CSV with the resources found and optionally a .docx report with the statistics.The tool is made with Python, beautifulsoup and Selenium framework the scrape all tags and make automatic scraping like going through pages and manage infinite scroll pagination.

*The tool needs a lot of improvements and bugfix.

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Clone the repo
   ```sh
   git clone https://github.com/MarioTesoro/Web_scraping.git
   ```
2. Install requirements
    ```sh
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

usage: main.py [-h] (-f [file_name] | -u [path]) [-o] [-s [SCROLLTIME]] [-l [LOADINGTIME]] [-mp [MAXPAGES]]

Useful tags:

Flag  | Usage
------------- | -------------
-f, --file  | Opens and reads the specified text file.
-u, --url  | Starts the scraping of the url.
-o, --output  | Can be printed and output in a .docx file with the scaping statistics.
-s, --scrolltime  | Defines a maximum time to scroll page with infinite scroll pagination.Default is 60 seconds.
-l, --loadingtime  | Defines a time t in order to make the scraper wait the full loading of a webpage.Default is 7 seconds.
-mp, --maxpages  | Defines a number n of pages to be scraped. Default is 100.
   
## Examples
```sh
  python3 main.py -u https://www.website.it/ -s 20 -l 8 -mp 90 
  ```

```sh
  python3 main.py -f file.txt -o
  ```
  

<p align="right">(<a href="#top">back to top</a>)</p>