# self-Grading Quiz

Python script for use as a webhook with Survey123 - to create a self-grading quiz. The python script can be loaded
into Amazon Lambda or Google Cloud Front and triggered upon quiz (Survey 123) submission.  The following fields will need to be
added to your survey's table for the script to work as-is.


An example of the <a href="https://education.maps.arcgis.com/home/item.html?id=64a66c7396f143228fa524d7733b588f" target="new">quiz can be found here</a>
- Processed [integer]
- total_correct [integer]
- percent_correct [string]

Survey must have eight questions, the labels must be Q1 - Q8.

