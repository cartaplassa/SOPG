# Secure-Obscure Password Generator

  

The idea behind SOPG is quite simple: to combine the readability of random words combination with resistance towards dictionary attacks that of random char string.

It picks random words from english dictionary divided into four parts of speech to generate structured sentences, replaces some symbols with numbers to make it fit for most of web services' requirements.

## Prerequisites
- **Python >=3.10**, not tested on older versions.

https://www.python.org/downloads/

- **TKinter**, required for GUI

TKinter should come preinstalled with python.
To test whether TKinter is present on system, launch python interpreter (`python` in terminal emulator or command prompt) and enter these lines:

	import tkinter
	tkinter._test()

A window like this should appear:

![Pasted image 20220831131607](https://user-images.githubusercontent.com/99555654/187687507-2dae53ad-5780-4641-8f62-b1c91959a915.png)


If it wasn't the case, try following options:

- For Windows OS: `pip install tk`
- For Ubuntu/Debian-based distribution: `sudo apt-get install python-tk`
- For Arch-based distribution: `sudo pacman -S tk`
- For Fedora-based distribution: `sudo dnf install python3-tkinter`
- For RHEL, CentOS, Oracle Linux: `sudo yum install -y tkinter tk-devel`

## Launch

#### Using git:
1) Navigate to the folder you want the project to be stored
2) `git clone https://github.com/zarni-ein/SOPG`
3) `cd SOPG`
4) Input `python core.py` in terminal emulator or command prompt for CLI version, `python main.py` for GUI

#### Using browser:
1) Download .zip archive
2) Extract the contents to the destination folder of your liking
3) Open folder in terminal emulator or command prompt
4) Input `python core.py` in terminal emulator or command prompt for CLI version, `python main.py` for GUI

## Usage

CLI version: just follow the tooltips. Help message pops up each time an unknown input is registered. So, pressing eg. `q` or `help` will call it.

GUI version: push buttons to do what's written on them, idk. `random` option on headers, dividers and tails will pick random symbol from `Char pool` field.

If you want to go above and beyond, you can add custom wordlists:

1) Create a text file in `./wordlists`, add a word for each line 

![Pasted image 20220831155727](https://user-images.githubusercontent.com/99555654/187687614-2f157ad3-b1eb-40aa-91c1-6badf4cdcb2c.png)

2) Reload the app

3) Add the filename without extension in `Sequence` field

![Pasted image 20220831160118](https://user-images.githubusercontent.com/99555654/187687674-f38f8462-1796-4faa-b987-9c82d82e4f55.png)


## Sources:
- Made possible *with* **Word Lists For Writers - Parts of Speech**

http://ashley-bovan.co.uk/words/partsofspeech.html

- Improved *with* **Actionable Password Advice Based on the Probable Wordlists**

https://github.com/berzerk0/GitPage/wiki/Actionable-Password-Advice-Based-on-the-Probable-Wordlists

- Inspired *by* and surpassed *the* **XKCD password generator**

https://github.com/redacted/XKCD-password-generator
