# Subway-Art-Finder
Subway Art Finder

Take a photo of art you see in the subway and identify what art you are looking at!

Example:
<img width="1115" alt="test4" src="https://github.com/user-attachments/assets/2aaf2954-82ff-49c2-a5b8-82c9c6d7a71a">

Result:
![Screenshot 2024-10-25 at 11 57 24 PM](https://github.com/user-attachments/assets/0a412ff8-1426-4aa8-9c6c-96713e610391)

In terminal:


<img width="922" alt="Screenshot 2024-10-25 at 11 57 37 PM" src="https://github.com/user-attachments/assets/d58f1eae-9e76-4c6b-81e3-b25834a5fadc">


Run the command in the terminal with a photo you took and it will show 5 potential matches for 20 seconds while printing out information about the art you saw in the terminal

Live Demo (in progress): https://mta.darefail.com

## Overview

Every day you take the subway, take a photo and find all the art (nearly 400 pieces) found in the stations around you.

## How to Run

Install Libraries
```
pip install numpy tensorflow opencv-python annoy
```

Search by photo
Add your photo to the directory and run this line (replacing YOUR_IMAGE.png)
```
python searchart.py allimages/ YOUR_IMAGE.png 
```


## Download MTA Images (Already Done)

All MTA art photos are included in this directory. But you can download them all with the download.py script

Install Libraries
```
pip install beautifulsoup4

```

Run photo downloader
```
python download.py
```


## License
This project is licensed under the APACHE 2.0 License - see the LICENSE file for details.

## Acknowledgments
NY MTA OpenData
- https://data.ny.gov/Transportation/MTA-Permanent-Art-Catalog-Beginning-1980/4y8j-9pkd/data 
- https://data.ny.gov/resource/4y8j-9pkd.json
