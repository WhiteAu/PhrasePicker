# PhrasePicker
A python3 based sentence parsing toy project

## Usage
> import PhrasePicker.utils.stringparser as sp

> my_phrase = "But soft, what light through yonder window breaks?"

> print(get_top_count_of_phrases_from_passage(my_phrase))

##Dependencies
This assumes access to the NTLK package. Learn more about this package here: http://www.nltk.org/
 

## Installation
A Python 3.6 virtual environment has been created under venv.
This can be invoked by: 

> source <project root dir>/venv/bin/activate

You can always turn off a virtual environment like:
> deactivate

Then, the python module can be installed via:
> python setup.py install

or an egg built by :
> python setup.py bdist_egg


## Testing
Tests were written in place with DocTests. Individual modules can be tested by invoking them as 
the main entry point via the command line like:
> python stringparser.py


