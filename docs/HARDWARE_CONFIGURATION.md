# How to Configure the Hardware for using the AI

## Camera Setup

**Resolution:** The Camera should produce a good quality image of the print bed area. It is reccomended to use a RPi-based camera like the Raspberry Pi Camera Module 3 or the Raspbeerry Pi Camera v2. The camera must run with a minimum resoltuion of 640 x 640 pixels. It is highly recomended to run the camera quality at a higher resolution than this, because the camera may be used for other purposes in addition to AI monitoring. 

As a result, it is reccomended that the camera be run in a resolution of 1920 x 1080 pixels. 

For large-format printers it is recommended to use multiple High-Quality cameras, or to use a single 4K+ camera with multiple monitoring zones. See [AI_MODEL_TUNING.md](https://github.com/printpal-io/DSF_PrintWatchAI_Plugin/blob/main/docs/AI_MODEL_TUNING.md#slicing) to learn what multiple monitoring zones are.

**Quality:** The camera streamer has a quality setting that ranges from 0-100, with 100 being the best quality. It is recomended to run the camera in a quality of 100 or as close to 100 as possible, with the absolute minimum being a quality of 80. 

**Framerate:** The camera framerate (FPS) does not need to be high in order to run the AI. The AI software analyzes the current image every 10 seconds. A frame rate of 1 frame per second is sufficient to run the AI software, however it is reccomended to use a frame rate of 5 frames per second to run the AI software. 


## Position
The camera should be positioned such that the entire print bed and print area is visible in the frame. The print bed and print area should fill up as much of the frame as possible, with the best scenario being that the print bed and print area are edge-to-edge in the camera frame. It is important that the camera is not able to see items in the background or outside of the printer, as these may cause False-Positive detections for items outside of the printer.

The `BambuLabs printers` are a good example of camera placement (model P1S pictured):

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/05363ed4-af23-4046-8c5e-f8cf5af02487)


## Lighting
The print bed and print area should be well-lit and visible with the human eye. The rule of thumb for Computer-Vision based AI is that if a person is unable to see clearly what is in the frame, then neither will the AI. It is also important to not over-expose the print bed and print object with too much light, as this may cause the AI to not detect properly either. A good balance between well-lit and not too bright is required (see examples below).

**Good Example:** Good lighting, object is visible, and not overexposed

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/c62ead1f-0bd7-4d1f-8a07-a4bcb7fb3b68)

**Bad Example:** Not enough lighting, object is not really visible

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/2ffd662b-4be2-424b-bf3c-c009dad286ab)

**Bad Example:** Too much lighting, object is overexposed

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/1000a527-5f47-48fe-937d-6641116eb140)


## Extras
If there are items within the print chamber that are causing issues with the AI software like producing False-Positives, we are able to address this in two ways:

1. Sample images from the camera inside the printer enclosure and train with it to cancel out the False-Potivies
2. Add blockout regions inside the AI software.
   - This replaces the selected camera frame areas with black pixels when being sent to the AI model
   - Essentially removes the item from the frame
   - This does not change the camera stream or stream preview
  
Example of `#2`

The purge shoot on the BambuLabs may get some pieces of spaghetti stuck and visible inside of the frame, and this may cause the AI to unwantingly detect it:

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/d19e3049-35a8-4a3b-b12a-a6faed4c9ee2)

The AI software will draw over the selected area with black pixels so the AI model ignores anything in this region:

![image](https://github.com/printpal-io/MATTERSHAPER_BUILD/assets/95444610/8756587b-5cd8-4498-a173-e24c1319c90a)
