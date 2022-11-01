import argparse
import os


#utils
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .txt file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."

def check_browser(input) -> str:
    input = str(input).strip().lower()
    browsers=["chrome","firefox"]
    for el in browsers:
        if el == input:
            return el

def check_integer_input(input) -> int:
    if isinstance(input, int): 
        if input>0:
            return input
        else:
            print("The number have to be greater than 0")
    else:
        print("The number is not an integer")

def validate_file(file_name):
    '''
    validate file name and path.
    '''
    if not valid_path(file_name):
        print(INVALID_PATH_MSG%(file_name))
        quit()
    elif not valid_filetype(file_name):
        print(INVALID_FILETYPE_MSG%(file_name))
        quit()
    return
     
def valid_filetype(file_name):
    # validate file type
    return file_name.endswith('.txt')
def valid_path(path):
    # validate file path
    return os.path.exists(path)
 
def read(args) -> list:
    arr=list()
    # get the file name/path
    file_name = args.file
 
    # validate the file name/path
    validate_file(file_name)
 
    # read and print the file content
    with open(file_name, 'r') as my_file:
        for line in my_file:
            arr.append(line)
    return arr

def url(args) -> list:
    print(args)
    url =list()
    url.append(args.url)
    return url
 
def args_parser():
# create parser object
    parser = argparse.ArgumentParser(description = "Web scraping tool")
    exclusive_args=parser.add_argument_group(description="One of these options must be choosen")
    exclusive_args=exclusive_args.add_mutually_exclusive_group(required=True)
    # defining arguments mutially exclusive for parser object
    exclusive_args.add_argument("-f", "--file", type = str, nargs = '?',
                        metavar = "file_name", default = None,
                        help = "Opens and reads the specified text file.")
     
    exclusive_args.add_argument("-u", "--url", type = str, nargs = '?',
                        metavar = "path", default = None,
                        help = "Starts the scraping of the url")
    #defining optional arguments
    parser.add_argument("-o", "--output",default=False, action='store_true',
                    help = "Can be printed and output in a .docx file with the scaping statistics") 
    parser.add_argument("-s","--scrolltime", type = int, nargs = '?',
                        default = 60,
                        help = "Defines a maximum time to scroll page with infinite scroll pagination.Default is 60 seconds")
    parser.add_argument("-l","--loadingtime",type = int, nargs = '?',
                        default = 7,
                        help = "Defines a time t in order to make the scraper wait the full loading of a webpage.Default is 7 seconds")
    parser.add_argument("-mp","--maxpages",type = int, nargs = '?',
                        default = 100,
                        help = "Defines a number n of pages to be scraped. Default is 100") 
    parser.add_argument("-b", "--browser", type = str, nargs = '?',
                        default = "chrome",
                        help = "Select the browser to use for scraping, the default one is Google Chrome. Are supported: chrome, firefox")  #tor
    print("Example: main.py -u https://www.ansa.it/ -s 20 -l 8 -mp 90 \nExample: main.py -f file.txt -o")              
 
    # parse the arguments from standard input
    args = parser.parse_args()
     
    # calling functions depending on type of argument
    #detail=
    out = False
    loadingTime = 7
    scrollTime = 60
    maxPages = 100
    browser = "chrome"
    if args.output!=None:
        print(args.output)
        out=True
    if args.loadingtime!=None:
        loadingTime =check_integer_input(args.loadingtime)
    if args.maxpages!=None:
        maxPages = check_integer_input(args.maxpages)
    if args.scrolltime!=None:
        scrollTime = check_integer_input(args.scrolltime)
    if args.browser!=None:
        browser = check_browser(args.browser)
    #mutually exclusive args
    if args.file != None:
        return read(args),out,scrollTime,loadingTime,maxPages,browser
    elif args.url != None:
        return url(args),out,scrollTime,loadingTime,maxPages,browser
    