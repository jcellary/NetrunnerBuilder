# NetrunnerBuilder
Script for outputing Android Netrunner Card Game deck sorted in a way matching my card collection organisation - that is first by faction and then by card number. This allows for faster physical deck construction when someone stores their card collection in this fashion. Sample output of the script can be seen in the sample_output.csv file.

## Installation

You will need to download and install the following:
- Python (https://www.python.org/downloads/ - tested on 2.x, but 3.x probably should also run)
- OCTGN client (found in http://octgn.net/Home/GetOctgn)
- OCTGN Android Netrunner definition (http://octgngames.com/anr/)

Next step is to clone this repository or download the netrunner.py and start.cmd files directly.

Afterwards you need to adjust the file netrunner.py and set the set_root_dir const to point to your OCTGN Netrunner directory

You can change the ordering of sets by editing the set_groups const. Also you will need to edit this const when new data packs come out. Otherwise cards will be missing part of information and won' be correctly sorted.

## Running

To process your decks you will need to download ocgtn deck definition files (i.e. from netrunnerdb.com), put them to the folder with the script and name as follows:
- current_corp.o8d
- next_corp.o8d
- current_runner.o8d
- next_runner.o8d 

Then simply start the start.cmd file
