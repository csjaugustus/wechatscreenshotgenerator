# WeChat Screenshot Generator
A Tkinter GUI program written to generate WeChat screenshots. One of the main differences between this program and other WeChat generator programs is that this supports the input of Chinese characters. 

## Main Interface
<img src="https://user-images.githubusercontent.com/61149391/124909696-58989480-e01d-11eb-994e-c09857bba2f1.png" width=50% height=50%>
On the right you can set the chat title and add new speech bubbles, and on the left the changes are reflected in the preview image area.

## Adding an entry
<img src="https://user-images.githubusercontent.com/61149391/124594773-c8c6df00-de92-11eb-8d9e-b478b02391c3.png" width=50% height=50%>
The program automatically searches through the files\avatars folder, and allows you to select either of them as the avatar of a speech bubble. The icons saved under the avatars folder do not need to be scaled to the correct size, as the resizing will be done by the program, but preferably, please only use square photos that are .JPG or .PNG. You will also be required to choose "left" or "right", meaning which side you want the speech bubble to be. "Right" will generate a green bubble instead of white.

## Saving images
<img src="https://user-images.githubusercontent.com/61149391/124594655-a634c600-de92-11eb-8be7-98e7c9586baa.png" width=50% height=50%>
Once you are finished, you can either choose to save the speech bubbles individually using the save button on the bottom right corner, or save the whole screenshot using the button on the bottom left. Images will be saved under the output folder, and the name of each image file will be given a unique timestamp, so in most situations, the images will not be replaced by each other (unless you quickly save twice within 1 second). 
