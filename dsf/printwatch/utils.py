from .client import PrintWatchClient
from .interface import MJPEG
from time import time
from base64 import b64encode
from uuid import uuid4
import asyncio
import aiohttp
import requests
from PIL import ImageDraw
import PIL.Image as Image
from io import BytesIO
from dsf.connections import SubscribeConnection, SubscriptionMode

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



DUET_STATES = {
    "C" : "Configuration",
    "I" : "Idle",
    "B" : "Busy",
    "P" : "Printing",
    "D" : "Decelerating",
    "S" : "Stopped",
    "R" : "Resuming", #Resuming a paused print
    "H" : "Halt", # Halt after E-Stop
    "F" : "Flashing", # Flashing new firmware
    "T" : "Toolchange"
}

def get_camera_struct(request) -> list:
    '''
    Returns the cameraStructure from a request

    Inputs:
    - request : flask.request - the request associated with an endpoint call

    Returns:
    - cameraStruct | list : list
    '''
    try:
        data = request.get_json()
        cameraStruct = data.get('cameras', None)
        return cameraStruct
    except Exception as e:
        print("Error get camera struct: {}".format(str(e)))
        return [False, e]

def get_setting_struct(request):
    '''
    Returns the settings structure from a request

    Inputs:
    - request : flask.request - the request associated with an endpoint call

    Returns:
    - settingStruct | dict : dict
    '''
    try:
        data = request.get_json()
        return data
    except Exception as e:
        print("Error get settings struct: {}".format(str(e)))
        return {}

def xywh2xyxy(region : list) -> list:
    '''
    Converts coordinates from xywh to xyxy

    Inputs:
    - region : list - xywh format of coordinates

    Returns:
    - xyxy : list - xyxy format of coordinates
    '''
    x1 = region[0]
    y1 = region[1]
    x2 = x1 + region[2]
    y2 = y1 + region[3]
    return [x1, y1, x2, y2]

def scale_xy(region : list, width : int, height : int) -> list:
    '''
    Scales coordinates down to relative percent of frame

    Inputs:
    - region : list - coordinates of the region
    - width : int - width of the master frame
    - height : int - height of the master frme

    Returns:
    - coordinates : list - scaled coordinates. Each element is in the range of 0.0 - 1.0
    '''
    return [region[0]/width, region[1]/height, region[2]/width, region[3]/height]

class EndpointAction(object):
    '''
    Used to add endpoint rule to object in API class
    '''

    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        return self.action()


class RepRapAPI:
    '''
    Handling of all API requests to the DUET RepRap firmware
    If using docker, this only works with the re-written firmware
    that includes logic for proxied requests
    '''

    def __init__(self, url : str = 'localhost'):
        self.url = url
        self.uniqueId = ''
        self.uniqueIdFromRR = False
        self._get_uid()

    def set_url(self, url):
        if self.url != url:
            self.url = url
            return True
        return False

    def _get_uid(self):
        if self.url != '':
            try:
                response = requests.get("http://{}/machine/model".format(self.url), timeout=5.0)
                response = response.json()
                uniqueId = response.get("boards")[0].get("uniqueId")
                self.uniqueId = uniqueId
                if uniqueId.strip() in [None, ""] or len(uniqueId) < 4:
                    if len(self.uniqueId) > 10 and not self.uniqueIdFromRR:
                        uniqueId = uuid4().hex
                        self.uniqueId = uniqueId
                        self.uniqueIdFromRR = False
                else:
                    self.uniqueIdFromRR = True
            except:
                if len(self.uniqueId) > 10 and not self.uniqueIdFromRR:
                    uniqueId = uuid4().hex
                    self.uniqueIdFromRR = False
                    self.uniqueId = uniqueId
        else:
            if len(self.uniqueId) > 10 and not self.uniqueIdFromRR:
                uniqueId = uuid4().hex
                self.uniqueIdFromRR = False
                self.uniqueId = uniqueId


    async def _get_state(
                self,
                endpoint : str = '',
                status_type : int = 3
            ) -> dict:
            '''
            Gets the state of the printer from the RepRap firmware

            Inputs:
            - endpoint : str - the endpoint to check the state with.
            - status_type : int - the stype of status response to get. Used with the endpoint /rr_status

            Returns:
            - response : dict - RepRap firmware status response
            '''
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                                    'http://{}{}?type={}'.format(
                                                            self.url,
                                                            endpoint,
                                                            status_type
                                    ),
                                    timeout=aiohttp.ClientTimeout(total=1.0)
                                ) as response:
                                r = await response.json()
                return r
            except:
                return False

    async def _pause_print(
                    self,
                    gcode : str = 'm25'
                ):
                '''
                Send a G-code command to the RepRap firmware to pause the print

                Inputs:
                - g-code : str - the G-code command that corresponds to a pause print command

                Returns:
                - response : dict - RepRap firmware pause print command response
                '''
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                                    'http://{}/machine/code?async=false'.format(
                                                            self.url
                                    ),
                                    data=f'{gcode}',
                                    timeout=aiohttp.ClientTimeout(total=10.0)
                                ) as response:
                                r = await response.text()
                return r

    def parse_state_response(self, response):
        if not isinstance(response , bool):
            state_response = response.get("boards", [{}])[0].get("state", None)
            return state_response
        return False


async def _async_infer(
        image,
        scores : list,
        print_stats : dict,
        api_client : PrintWatchClient
    ):
    '''
    Returns the inference response in an asynchrnous function call

    Inputs:
    - image : base64 encoded string - image to send for inference
    - printer_info : PrinterInfo - payload information for API call
    - api_client : PrintWatchClient - the client object to us for the API call

    Returns:
    - response : Flask.Response - inference response
    '''
    payload = api_client._create_payload(
                            encoded_image=image,
                            scores=scores,
                            print_stats=print_stats
                        )

    response = await api_client._send_async('api/v2/infer', payload)
    return response

async def _async_notify(
        api_client : PrintWatchClient,
        notification_level : str = 'warning'
    ):
    '''
    Returns the notification endpoint response in an asynchrnous function call

    Inputs:
    - printer_info : PrinterInfo - payload information for API call
    - api_client : PrintWatchClient - the client object to us for the API call
    - notification_level : str - the notification level to report to the API

    Returns:
    - response : Flask.Response - inference response
    '''
    payload = api_client._create_payload(
                            None,
                            notify=True,
                            notification_level=notification_level
                        )

    response = await api_client._send_async('api/v2/notify', payload)
    return response



class LoopHandler:
    '''
    Controls the general loop logic for making API requests to the
    PrintWatch API, handles the buffers, and action taking.
    '''
    def __init__(
            self,
            settings : dict,
            api_client : PrintWatchClient,
            rep_rap_api : RepRapAPI,
            camera : MJPEG,
            MULTIPLIER : float = 4.0,
            duet_states = DUET_STATES
        ):
        self.settings = settings
        self._api_client = api_client
        self.camera = camera
        self.MULTIPLIER = MULTIPLIER
        self._buffer = [[0, 0, 0]] * settings.get("buffer_length")
        self._scores = [0] * int(settings.get("buffer_length") * self.MULTIPLIER)
        self._levels = [False, False] # Corresponds to [Notify, Action]
        self._actionsSent = 0
        self._lastAction = 0
        self._notificationsSent = []
        self._lastNotification = 0
        self.retrigger_valid = False
        self.notifyTimer = 10.0 * 60.0 # 10 minutes between notifications minimum
        self.duet_states = duet_states
        self.rep_rap_api = rep_rap_api
        self.currentPreview = None

    def resize_buffers(self):
        if len(self._buffer) > self.settings.get("buffer_length"):
            while len(self._buffer) > self.settings.get("buffer_length"):
                self._buffer.pop(0)
            while len(self._scores) > int(self.settings.get("buffer_length") * self.MULTIPLIER):
                self._scores.pop(0)
        else:
            self._buffer.extend([[0, 0, 0]] * (self.settings.get("buffer_length") - len(self._buffer)))
            self._scores.extend([0] * (int(self.settings.get("buffer_length") * self.MULTIPLIER) - len(self._scores)))

    def _draw_boxes(self, image, boxes : list) -> str:
        pil_img = Image.open(BytesIO(image))
        #if self._iframe_width is not None and self._iframe_height is not None:
        #pil_img = pil_img.resize((self._iframe_width, self._iframe_height))
        process_image = ImageDraw.Draw(pil_img)
        width, height = pil_img.size

        for i, det in enumerate(boxes):
            det = [j / 640 for j in det]
            x1 = det[0] * width
            y1 = det[1] * height
            x2 = det[2] * width
            y2 = det[3] * height
            process_image.rectangle([(x1, y1), (x2, y2)], fill=None, outline="red", width=4)

        out_img = BytesIO()
        pil_img.save(out_img, format='PNG')
        contents = b64encode(out_img.getvalue()).decode('utf8')
        self.currentPreview = 'data:image/png;charset=utf-8;base64,' + contents.split('\n')[0]

    def _handle_buffer(
                self,
                score : float,
                smas : list,
                levels : list
        ):
        '''
        Manages the buffer, scores, and levels.

        '''

        self._buffer.append(smas)
        self._scores.append(score)
        self._levels = levels

        while len(self._buffer) > self.settings.get("buffer_length"):
            self._buffer.pop(0)

        while len(self._scores) > self.settings.get("buffer_length") * self.MULTIPLIER:
            self._scores.pop(0)



    def _allow_trigger(
            self,
            type : str = 'notify'
        ):
        '''
        CHecks if a trigger action should be permitted

        Inputs:
        - type : str - the type of trigger to check for

        Returns:
        - valid : Boolean - whether a certain trigger should be allowed
        '''
        if self._actionsSent > 10: # May want to change this for the show
            return False
        if type == 'notify':
            if self.last_n_notifications_interval() < 100: #and self.retrigger_check():
                return True if len(self._notificationsSent) < 1000 and time() - self._lastNotification > self.notifyTimer else False
            return False
        elif type == 'action':
            return True if self._actionsSent < 100 and time() - self._lastAction > self.notifyTimer else False

    def last_n_notifications_interval(self, interval : int = 4 * 60 * 60) -> int:
        '''
        Checks how many notifications have been sent in the last N hours

        Inputs:
        - interval : int - the interval to check occurences of notifications

        Returns:
        - running_total : int - number of notifications in the last N hours
        '''
        # 4 hour default interval
        current_time = time()
        running_total = 0

        # reverse-order because self._notificationsSent values get appended
        for idx in reversed(range(len(self._notificationsSent))):
            if time() - self._notificationsSent[idx] > interval:
                break
            running_total += 1
        return running_total

    def retrigger_check(self) -> bool:
        '''
        Checks whether a previous detection has reset. The criteria for resetting
        are as follow:
            - AI Level has been prior above the notification threshold and a
            notification has been sent
            - The AI Level has decreased below the notification threshold and
            remained there for N = bufer_length * buffer_percent cycles


        Inputs:

        Returns:
        - Boolean - Whether retrigger has latched
        '''
        if not self.retrigger_valid:
            num_below_threshold = [True if ele < self.settings.get("thresholds", {}).get("notification", 0.3) else False for ele in self._buffer].count(True)
            if num_below_threshold >= int(self.settings.get("buffer_length") * self.settings.get("buffer_percent")):
                self.retrigger_valid = True
                return True
            return False
        return True



    async def _handle_action(
            self
        ):
        '''
        Checks if any actions should be taken.
        Notifications and Pauses will be triggered from inside this method.
        '''
        if self._levels[1] and self._allow_trigger('action') and self.settings.get("actions", {}).get("pause", False):
            # Currently no way of supporting actions via serial.
            # Only supported over ethernet/IP
            notification_level = 'action'
            if self.settings.get("actions", {}).get("pause", False) or self.settings.get("actions", {}).get("cancel", False):
                print("SENDING ACTION")
                # Take the pause action if enabled
                r = await self.rep_rap_api._pause_print(gcode = 'm25')

                response = await _async_notify(
                                        api_client=self._api_client,
                                        notification_level=notification_level
                                    )

                if response.get('statusCode') == 200:
                    self._buffer = [0] * self.settings.get("buffer_length")
                    self._scores = [0] * int(self.settings.get("buffer_length") * self.MULTIPLIER)
                    self._levels = [False, False]
                    self._actionsSent += 1
                    self._lastAction = time()
                else:
                    # Retry logic
                    pass
        elif self._levels[0] and self._allow_trigger('notify'):
            print("Sending Warning via Email")
            notification_level = 'warning'

            response = await _async_notify(
                                    api_client=self._api_client,
                                    notification_level=notification_level
                                )
            self._lastNotification = time()
            self.retrigger_valid = False
            self._notificationsSent.append(time())



    async def _run_once(self):
        '''
        Runs one loop of the cycle. This method is a callback for the asynchronous loop
        '''

        try:
            # Add conditional for checking whether print state
            duet_state = await self.rep_rap_api._get_state('/machine/status')
            if self.rep_rap_api.parse_state_response(duet_state) == 'P' or self.settings.get("test_mode"):
                frame = self.camera.snap_sync()
                if not isinstance(frame, bool):


                    # Get the DUET print state here
                    print_stats = {}
                    if self.settings.get("test_mode") and not self.rep_rap_api.parse_state_response(duet_state) == 'P':
                        print_stats = {
                            "state" : 0,
                            "printTime" : 550,
                            "printTimeLeft" : 1,
                            "progress" : 99.9,
                            "job_name" : "temp-job-name.stl"
                        }

                    response = await _async_infer(
                                        image=b64encode(frame).decode('utf8'),
                                        scores=self._scores,
                                        print_stats=print_stats,
                                        api_client=self._api_client
                                    )
                    if response.get('statusCode') == 200:
                        self._draw_boxes(frame, response.get('boxes'))
                        self._handle_buffer(
                                    score=response.get("score"),
                                    smas=response.get("smas")[0],
                                    levels=response.get("levels")
                            )
                        await self._handle_action()
                else:
                    print("Issue with camera")
        except Exception as e:
            print("Exception as e: {}".format(str(e)))
        except Exception as e:
            print("Error running once: {}".format(str(e)))




class Scheduler:
    def __init__(
            self,
            interval : float = 10.0,
            callback = None,
            loop_handler : LoopHandler = None
        ):
        '''
        Handles the scheduling of the loop.
        Controls the asynchronous callback in the LoopHandler object
        '''

        self._interval = interval
        self.task = asyncio.ensure_future(self._run_loop())
        self._run = True
        self._callback = None
        if loop_handler is not None:
            self._callback = loop_handler._run_once
        else:
            self._callback = callback
        self._loop_handler = loop_handler

    async def _run_loop(self):
        '''
        Runs the loop.
        Basic sleep function for the inference call interval (default 10.0s), then
        the Inference and handing
        '''
        try:
            print('Starting loop')
            while self._run:
                await asyncio.sleep(self._interval)
                await self._callback()
        except asyncio.CancelledError:
            print("Cancelled")
            raise
        except Exception as e:
            # Add logic to re-start loop if it fails.

            print('Scheduler = {}'.format(str(e)))

            self._restart_loop()

    def set_interval(self, value : float = 10.0):
        self._interval = value

    def _restart_loop(self):
        # Cleanup first
        self._run = False
        self.cancel()
        self.task = None

        # Re-start the task
        self._run = True
        self.task = asyncio.ensure_future(self._run_loop())

    def cancel(self):
        self._run = False
        self.task.cancel()
