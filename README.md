# WeChat Screenshot Generator
A Tkinter GUI program written to generate WeChat screenshots. One of the main differences between this program and other WeChat generator programs is that this supports the input of Chinese characters. 

## Main Interface
<img src="https://user-images.githubusercontent.com/61149391/124533276-9c847180-de44-11eb-842e-e2b3c909dbbe.png" width=50% height=50%>
On the right you can set the chat title and add new speech bubbles, and on the left the changes are reflected in the preview image area.

## Adding an entry
<img src="https://user-images.githubusercontent.com/61149391/124533398-d5bce180-de44-11eb-989d-011692ee2dae.png" width=50% height=50%>
The program automatically searches through the files\avatars folder, and allows you to select either of them as the avatar of a speech bubble. The icons saved under the avatars folder do not need to be scaled to the correct size, as the resizing will be done by the program, but preferably, please only use square photos that are .JPG or .PNG. You will also be required to choose "left" or "right", meaning which side you want the speech bubble to be. "Right" will generate a green bubble instead of white.

## Saving images
<img src="https://user-images.githubusercontent.com/61149391/124533719-727f7f00-de45-11eb-8cf8-aeee752d32f4.png" width=50% height=50%>
Once you are finished, you can either choose to save the speech bubbles individually using the save button on the bottom right corner, or save the whole screenshot using the button on the bottom left. Images will be saved under the output folder, and the name of each image file will be given a unique timestamp, so in most situations, the images will not be replaced by each other (unless you quickly save twice within 1 second). 

## Limits
<img src="https://user-images.githubusercontent.com/61149391/124533937-d609ac80-de45-11eb-937e-f4edc0349fb6.png" width=50% height=50%>
The program currently does not support longer screenshots than the given preview image.
