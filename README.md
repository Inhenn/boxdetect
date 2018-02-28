# boxdetect
Using OpenCV to detect a box/frame/rectangle contour in an image

This package contains 3 main functions:

box_vertex(img, left_x1, left_x2, left_y1, left_y2, top_x1, top_x2, top_y1, top_y2, right_x1, right_x2, right_y1,
             right_y2, bot_x1,
             bot_x2, bot_y1, bot_y2, line_num, left_length, right_length, top_length,
             bot_length, accuracy)
             
This function returns 4 vertices of the detected box, in the following order upper left vertex, upper right vertex, lower right vertex, lower left vertex.

box_draw(img, left_x1, left_x2, left_y1, left_y2, top_x1, top_x2, top_y1, top_y2, right_x1, right_x2, right_y1,
             right_y2, bot_x1,
             bot_x2, bot_y1, bot_y2, line_num, left_length, right_length, top_length,
             bot_length, accuracy)
This function draws the outline of the detected box.

box_crop(img, left_x1, left_x2, left_y1, left_y2, top_x1, top_x2, top_y1, top_y2, right_x1, right_x2, right_y1,
             right_y2, bot_x1,
             bot_x2, bot_y1, bot_y2, line_num, left_length, right_length, top_length,
             bot_length, accuracy)
This function returns the img which only contains the box area.

left_x1,left_x2,left_y1,left_y2 are used to select the possible area that the left edge lies in, the more accurate the area is, the better the edge detection works. As is shown in this picture, all left_x's and y's take percentage value(relative location of the image), which makes it easier for users to estimate. 
             
![](https://github.com/Inhenn/boxdetect/blob/master/sample.png)

All top_'s, bot_'s and right_'s work the same as left_'s.

line_num: how many attempts do we want to make for a single edge recognization, it is equal to 5 by default.

left_length, right_length, top_length, bot_length: the estimated length of each edge, the more accurate it is, the better the edge detection works, it is equal to 2 by default.

accuracy: the sensitivity of angle, the more sensitive of angle, the more accurate of the edge angle, it is equal to 4 by default.

Consider the picture above, detecting the edge of the top box helps we extract information from the area we wanted. In this case, selecting the top box area and using pytesseract to analyze the text work more efficiently than putting the entire image into pytesseract.

This detection also works when the box is a little bit oblique, as long as 4 edges form a rectangle, and the precise edge areas are provided.
