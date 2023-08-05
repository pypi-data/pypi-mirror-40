# Emuparadise-dl

emuparadise-dl is a (maybe) helpful script to search and retrieve roms from the top rom-hosting websites out there.

It was originally built because I wanted to access the Emuparadise's site huge database in a faster (and less javascriptish) way, but then I decided to extend the support to more sites. 

## Installation

pip3 install emuparadise-dl

## Usage

Basic Usage

```bash
emuparadise-dl search "Metal Gear Solid"
```

![](screenshots/simple_search.png)

It will search using the search function provided by the site and It will report back the found results in a tabular format. You will be prompted to insert the ID (first column) of the rom to retrieve (or just type N to abort).

![](screenshots/simple_search_with_retrieve.png)

To known the list of supported backend just type

```bash
emuparadise-dl list
```

By default it uses emuparadise.me as backend, it is possible to use a different one or to search on all the avaliable backend at once, but I suggest of doing so only for very rare titles since the output could be very long for common roms 

![](screenshots/all_search.png)

The program is equipped with a well functioning help manual (provided by the godly argparse python library).
For the general help type ```emuparadise-dl -h```. 
For every subcommand is available the related help section (i.e. ```emuparadise-dl search -h```

## FAQ

Q: I'm the owner of one of those backend you are supporting and I want you to stop targeting my site.

A: Ok, so when I sent you an email asking for permission why didn't you reply? However, send me an email and I'll remove support from future releases

Q: Is this a scraper?

A: NO, it is a TUI search engine for roms, all the content is hosted on the sites, so you sould support the backend you are using

Q: The name sounds familiar...

A: Yeah, I took inspiration from youtube-dl

Q: OMG, your parsing-fu skills sucks, I bet it's possible to rewrite all those parsing in 2 lines

A: Pull request or GTFO
