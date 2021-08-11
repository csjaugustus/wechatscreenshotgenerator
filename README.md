# WeChat Screenshot Generator
A Tkinter GUI program written to generate WeChat screenshots. Offers support for Chinese characters, custom avatars and dark mode.

## Table of Contents
* [Installation](#installation)
* [Main Interface](#main-interface)
* [Adding an Entry](#adding-an-entry)
* [Saving Images](#saving-images)
* [Dark Mode Support](#dark-mode-support)

## Installation
```
$ git clone https://github.com/csjaugustus/wechatscreenshotgenerator.git
```
```
$ pip install -r requirements.txt
```
```
$ main.py
```

## Main Interface
<img src="https://user-images.githubusercontent.com/61149391/128868735-996bd8fb-5799-4edf-8180-9c9a4ce24666.png" width=50% height=50%>
On the right you can set the chat title and add new speech bubbles, and on the left the changes are reflected in the preview image area.

## Adding an Entry
<img src="https://user-images.githubusercontent.com/61149391/128868975-d398fab7-2c2e-44f1-9f06-90dbadee1c19.png" width=50% height=50%>
Save your square avatars under files\avatars in either .png or .jpg format. They do not need to be manually resized. You do not need to select an avatar or side if you are adding a time marker.

## Saving Images
<img src="https://user-images.githubusercontent.com/61149391/128869574-539a09ea-02da-44a1-8b9e-3c4ebb2a9a52.png" width=50% height=50%>
You can choose to either save the entire screenshot or only the selected speech bubble (or time marker). Outputs will be saved under the "output" folder, which will be automatically created.

## Dark Mode Support
<img src="https://user-images.githubusercontent.com/61149391/128869640-c7efdaec-4ac9-4ccd-a6de-721c993d298f.png" width=50% height=50%>
You can toggle between dark & light mode at any time.
