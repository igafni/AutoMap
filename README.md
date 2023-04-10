Network Graph Mapper Visualization
=================================

The purpose of this tool is to produce a network diagram by collating network information gathered on remote hosts.
Based on lorenzog/NetworkMap

Example:

* Log on host A as any user
* Dump some network information e.g. routing table, ARP table, traceroute
* Feed the dumps to this tool
* Go to another host
* Dump network information

...rinse, repeat

* Ultimately, this tool produces a network diagram showing all hosts reachable
  from your compromised nodes.

![Sample screenshot](example.png?raw=true "Simple Network Example")


Installation
------------

You'll need a fairly recent Python version with setuptools.

1. Set up a virtualenv:

       virtualenv venv
       source venv/bin/activate

2. Install the required libraries:

       pip install -r requirements.txt

Usage
-----

#### Run Streamlit to host your website

Run the tool on the command line:

    streamlit run app.py

You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8502


### Installing GraphViz (Optional)

If you want to automatically generate graphs (by default: yes) then you'll need
pygraphviz installed.

For windows systems:

    pip install graphviz

For debian-based systems:

    apt-get install pkg-config libgraphviz-dev graphviz-dev graphviz libgraphviz

For RPM based systems:

    yum install graphviz graphviz-devel

#### Weird errors when installing pygraphviz

##### Undefined symbol: Agundirected

If you get a similar error to this one on a Debian-based system:

File "/home/user/dev/NetworkMap/venv/local/lib/python2.7/site-packages/pygraphviz/graphviz.py", line 24, in
swig_import_helper
_mod = imp.load_module('_graphviz', fp, pathname, description)
ImportError: /home/user/dev/NetworkMap/venv/local/lib/python2.7/site-packages/pygraphviz/_graphviz.so: undefined symbol:
Agundirected

Then fix it like that:

    pip uninstall graphviz
    pip install pygraphviz --install-option="--include-path=/usr/include/graphviz" --install-option="--library-path=/usr/lib/graphviz/"

Source: http://stackoverflow.com/questions/32885486/pygraphviz-importerror-undefined-symbol-agundirected

##### redhat-hardened-cc1 missing

If you get this error on a Fedora-based system:

    gcc: error: /usr/lib/rpm/redhat/redhat-hardened-cc1: No such file or directory

You need to install redhat-rpm-config. Source: http://stackoverflow.com/a/34641068/204634

##### fatal error C1083

installed the latest graphviz using the latest win64 executable from graphviz.org

then installation using the following command

    pip install --global-option=build_ext --global-option="-IC:\Program Files\Graphviz\include" --global-option="-LC:\Program Files\Graphviz\lib" pygraphviz

Possible alternatives
---------------------

P2NMAP https://github.com/codemedici/P2NMAP


albert https://github.com/haymovich/albert

Pcap alternatives
---------------------

pcap-analyser https://github.com/pkpraveen895/pcap-analyser

flowmeter https://github.com/alekzandr/flowmeter

CapCSV-meter https://github.com/maliksh7/CapCSV-meter

#### Future:

* Dump into Excel spreadsheet or SQL database?
* Import into Microsoft
  Visio? https://support.office.com/en-gb/article/Create-a-detailed-network-diagram-by-using-external-data-in-Visio-Professional-1d43d1a0-e1ac-42bf-ad32-be436411dc08#bm2

Misc notes
----------

* Graphviz can also do clustering? http://www.graphviz.org/Gallery/undirected/gd_1994_2007.html
* Graphviz and network maps (icons are a bit ugly tho): http://www.graphviz.org/Gallery/undirected/networkmap_twopi.html
* For manual graphs (meh) - requires probably generating an output properly formatted like XML. Pain to
  maintain: https://community.spiceworks.com/topic/521280-i-need-software-that-make-my-whole-network-diagram-automatically
