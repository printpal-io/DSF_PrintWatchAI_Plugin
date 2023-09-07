# PrintWatch AI Plugin for Duet

This plugin monitors the webcam stream on any RepRapFirmware printer for spaghetti type defects. It can work with any camera that is accessible via an IP address/HTTP endpoint. 
It can only be used in SBC mode currently.

![alt text](https://forum.duet3d.com/assets/uploads/files/1693886852613-665bd7f4-af57-4130-a03a-eadb9dd80558-image.png)
## Installation

To install this plugin, open DWC, go to `Settings -> Plugins -> External Plugins` and click on "Install Plugin".
Then select the plugin ZIP file and confirm the following steps. 

The plugin ZIP can be found on this GitHub repository's **Releases -> Version X.X.X -> PrintWatch-X.X.X.zip**. 

Alternatively, click [here](https://github.com/printpal-io/DSF_PrintWatchAI_Plugin/releases) to be taken to the release page.

**Notice:**

As of September 7th, 2023, there is a bug with this plugin using DSF 3.5.0-rc that will cause the HTTP endpoints created for this plugin to be unreachable.
To fix this:

- Make sure the plugin is installed and started
- SSH into the SBC
- Enter the following command: `sudo systemctl restart duetwebserver`

This will restart the webserver and register the endpoints correctly. This must be done every time the SBC is started up. This should be fixed in the next release.


## Usage
**Getting started with the plugin.**
  1. Go to the plugin tab by navigating the side panel **Plugins -> PrintWatch AI**
  2. Enable the plugin by clicking the **Enable Monitoring** button
  3. In the PrintWatch AI plugin page, navigate to the **Settings** tab.
  4. Obtain your API key and enter it into the **API key** field. Navigate to the [WebApp](https://app.printpal.io) and create a Free account:
      1. Click 'Sign Up'
      2. Enter desired credentials
      3. Verify account with code sent via email
      4. Log into the WebApp and navigate to **Account -> Settings** and copy the **API key** value. Paste this value into the **API key** field in the Duet plugin
  6. For the Webcam URL input, enter the HTTP url at which the static image of the IP camera can be found. If using [Motion](https://plugins.duet3d.com/plugins/MotionWebcamServerPlugin.html) to handle the webcam streaming,       this value will be: "http://<ip_address>:<port>/<camera_number>/current". If configured using default settings with the Motion Plugin, this will be:  "http://localhost:8081/0/current"


**Thresholds**
   
   There are two threshold setting values:
   - _Notification Threshold:_ this is the defectiveness value at which a notification will be sent to the user. The defectiveness value 
   - _Action Threshold:_ this is the defectiveness value at which an action (pause with m25) will be taken on behalf of the printer.


**Enabling Monitoring**

The plugin will begin actively monitoring the printer if:
- A print job is currently active
  
OR
- Test mode is enable. (Enable this by clicking the **Enable Test Mode** button in the top right corner or the Plugin page)


**Interpreting Results**

Navigate to the **Preview** tab on the PrintWatch AI plugin page to view the AI's bounding boxes overlayed on the webcam preview. Detections with a certain score value will be drawn boxed in _red_.

The **Defectiveness Level** is shown on a circular Gauge to the right of the camera preview. The Guage displays the level on a scale of 0 - 100. A score close to zero indicates that there are no defects detected in the current frame, where a larger value indicates that defects have been detected.

Each printer and configuration will have a different value at which defects are detected well at. Please refer [section 1.3.1 of the Configuration Guide](https://printpal.io/documentation/tuning-your-setup/#articleTOC_3) to properly setup the printer's AI.


