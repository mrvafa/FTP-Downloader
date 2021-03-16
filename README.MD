# FTP Downloader

> This app will get all links from ftp.
> With Downloader we can download all the links
> stored in links.txt and store them to output folder.

## Installation

- Clone the repository
- Create virtual environment using `python -m virtualenv --python=python3 env`
- Activate env (in linux use `. env/bin/activate`)
- Install requirements.txt using `pip install -r requirements.txt`

## Usage

Crawling FTP

```
python main.py -u <ftp-url>
```

Downloading links.txt

```
python downloader.py
```

## Example

Crawling FTP

```
python main.py -u https://dl.songsara.net/FRE/
```
