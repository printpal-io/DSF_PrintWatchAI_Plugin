# Tuning the AI model

## Resolution
One of the first items we are able to tune with the AI model is the input resolution. A higher input resolution will typically be able to detect more accurately, however it will require more resources and time to run. The current resolution that the AI model is run with is `640 x 640 pixels`. This means that the image is resized to `640x640` from the native resolution.

## Slicing 
One option to provide better analysis on the entire camera frame that is running with a large resolution is to "slice" the camera frame into multiple smaller images and then run those individual images through the AI model. This is beneficial when the camera reolution is very large and a larger format printer is being monitored.

This method will take longer to run the AI model. The total additional time it takes to run the AI model can be calculated as: `Total additional time = (# slices - 1) * BASE_MODEL_TIME`.

**Example:** this 1920 x 1080 frame (shown below) is sliced vertically down the middle to produce two smaller images both of resolution `960 x 1080` pixels. The software will resize both of these images to `640 x 640` and then run them through the AI model and treat the results as if they were from a single image.

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/e301123d-ddcd-4568-af23-8e3eab7e6f50)

## Non-max suppression
We are able to have a minimum and maximum defect-size requirement. One reason may be that we do not want small little strings or objects to be identified as defects when the software runs.

**Example:** let's say this small intricate detail (pictured below) is causing the AI to detect a defect, and we know that this is not a defect. Let's say we need the defect to be at least 1 cm large in order for us to care, then we can set the setting to require it to be at least `12 x 12` pixels, otherwise we do not consider it.

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/dbc8962b-70f8-4f21-b309-6f8d6dfeebb2)
