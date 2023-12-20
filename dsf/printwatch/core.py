from .client import *
from .utils import LoopHandler, Scheduler, _async_heartbeat, RepRapAPI
from .interface import *
import asyncio
import ujson
import os
from dsf.connections import CommandConnection
from dsf.http import HttpEndpointConnection, HttpEndpointType, HttpResponseType

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()

class PrintFarmPro:
    '''
    This is the main object that controls all of the other objects and functions

    '''
    def __init__(
            self
        ):
        '''
        Load settings, create API endpoints, and begin the program.

        '''
        self.runner = None
        self.printwatch = None
        self.rep_rap_api = None
        self._load_settings()
        self.aio = get_or_create_eventloop()
        if self.settings.get("monitoring_on"):
            self._init_monitor()
        self._init_api()
        self.aio.run_forever()

    def _init_api(self):
        self.endpoints = []
        self.cmd_conns = []

        self.cmd_conns.append(CommandConnection(debug=False))
        self.cmd_conns[0].connect()

        self.endpoints.append(self.cmd_conns[0].add_http_endpoint(HttpEndpointType.POST, "printwatch", "set_settings"))
        self.endpoints[0].set_endpoint_handler(self._change_settings)

        self.cmd_conns.append(CommandConnection(debug=False))
        self.cmd_conns[1].connect()

        self.endpoints.append(self.cmd_conns[1].add_http_endpoint(HttpEndpointType.GET, "printwatch", "get_settings"))
        self.endpoints[1].set_endpoint_handler(self._get_settings)

        self.cmd_conns.append(CommandConnection(debug=False))
        self.cmd_conns[2].connect()

        self.endpoints.append(self.cmd_conns[2].add_http_endpoint(HttpEndpointType.GET, "printwatch", "monitor"))
        self.endpoints[2].set_endpoint_handler(self._get_monitor)

        self.cmd_conns.append(CommandConnection(debug=False))
        self.cmd_conns[3].connect()

        self.endpoints.append(self.cmd_conns[3].add_http_endpoint(HttpEndpointType.GET, "printwatch", "preview"))
        self.endpoints[3].set_endpoint_handler(self._get_preview)

        self.cmd_conns.append(CommandConnection(debug=False))
        self.cmd_conns[4].connect()

        self.endpoints.append(self.cmd_conns[4].add_http_endpoint(HttpEndpointType.GET, "printwatch", "monitor_init"))
        self.endpoints[4].set_endpoint_handler(self._add_monitor)

        self.cmd_conns.append(CommandConnection(debug=False))
        self.cmd_conns[5].connect()

        self.endpoints.append(self.cmd_conns[5].add_http_endpoint(HttpEndpointType.GET, "printwatch", "monitor_off"))
        self.endpoints[5].set_endpoint_handler(self._kill_monitor)




    def _on_settings_change(self):
        if self.printwatch is None:
            self.printwatch = PrintWatchClient(settings=self.settings)

        if self.settings.get("printer_id", "") == "" or ('-' not in self.rep_rap_api.uniqueId):
            self.rep_rap_api._get_uid()
            self.settings["printer_id"] = self.rep_rap_api.uniqueId
        if self.runner is not None:
            self.runner._loop_handler.resize_buffers()
            self.runner._loop_handler.camera.ip = self.settings.get("camera_ip")

        settings_ = {
                    'detection_threshold' : int(self.settings.get("thresholds", {}).get("display", 0.6) * 100),
                    'buffer_length' : int(self.settings.get("buffer_length")),
                    'notification_threshold' : int(self.settings.get("thresholds", {}).get("notification", .30) * 100),
                    'action_threshold' : int(self.settings.get("thresholds", {}).get("action", .60) * 100),
                    'enable_notification' : self.settings.get("actions", {}).get("notify", False),
                    'email_address' : self.settings.get("email_addr"),
                    'pause_print' : self.settings.get("actions", {}).get("pause", False),
                    'cancel_print' : self.settings.get("actions", {}).get("cancel", False),
                    'extruder_heat_off' : self.settings.get("actions", {}).get("extruder_off", False),
                    'enable_feedback_images' : True
                }
        _async_heartbeat(api_client=self.printwatch, settings=settings_)

    def _save_settings(self):
        with open("settings.json", "w") as f:
            ujson.dump(self.settings, f, indent=4)

    def _load_settings(self):
        if not os.path.exists("settings.json"):
            self.settings = {
                "api_key" : "",
                "printer_id" : "",
                "duet_ip" : "",
                "camera_ip" : "",
                "email_addr" : "",
                "test_mode" : False,
                "monitoring_on" : False,
                "thresholds" : {
                    "notification" : 0.3,
                    "action" : 0.6,
                    "display" : 0.6
                },
                "buffer_length" : 16,
                "buffer_percent" : 60,
                "actions": {
                    "pause" : False,
                    "cancel" : False,
                    "notify" : False,
                    "extruder_off" : False,
                    "macro" : False
                },
                "current_sma" : 0.0,
                "require_sync" : 0, # Enum value, {0 : no sync required, 1 : backend has correct value, 2: frontend has correct}
                "pause_gcode" : "",
                "cancel_gcode" : "",
                "resume_gcode" : "",
                "rotation" : 0
            }
            self.rep_rap_api = RepRapAPI()
            self._on_settings_change()
            self._save_settings()
        else:
            with open("settings.json", "r") as f:
                self.settings = ujson.load(f)
            self.rep_rap_api = RepRapAPI()
            self._on_settings_change()

    def _init_monitor(self, ticket_id : str = ''):
        if self.runner is not None:
            return False
        loop = LoopHandler(
                        settings=self.settings,
                        api_client=self.printwatch,
                        rep_rap_api=self.rep_rap_api,
                        camera=MJPEG(ip=self.settings.get("camera_ip"))
                    )
        self.runner = Scheduler(interval=10.0, loop_handler=loop)
        self.settings["monitoring_on"] = True
        self._save_settings()
        self._on_settings_change()
        return True

    async def _get_monitor(self, http_endpoint_connection: HttpEndpointConnection):
        await http_endpoint_connection.read_request()
        if self.runner is None:
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8001, 'response' : 'No monitor active'}), response_type=HttpResponseType.JSON)
        else:
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8000,
                    'items' :
                        {'status' :
                            {'scores' : self.runner._loop_handler._scores,
                            'levels' : self.runner._loop_handler._levels,
                            'buffer' : self.runner._loop_handler._buffer
                            }
                        }
                    }), response_type=HttpResponseType.JSON)
        http_endpoint_connection.close()

    async def _get_preview(self, http_endpoint_connection: HttpEndpointConnection):
        await http_endpoint_connection.read_request()
        if self.runner is None:
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8001, 'response' : 'No monitor active'}), response_type=HttpResponseType.JSON)
        else:
            if self.runner._loop_handler.active:
                if self.runner._loop_handler.settingsIssue:
                    preview_ = 'settingsIssue'
                else:
                    preview_ = 'loading' if self.runner._loop_handler.currentPreview is None else self.runner._loop_handler.currentPreview
            else:
                preview_ = None
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8000,
                    'items' :
                        {'status' :
                            {'preview' : preview_,
                            'message' : self.runner._loop_handler.errorMsg
                            }
                        }
                    }), response_type=HttpResponseType.JSON)
        http_endpoint_connection.close()

    async def _change_settings(self, http_endpoint_connection: HttpEndpointConnection):
        try:
            settings = await http_endpoint_connection.receive_json()
            settings = ujson.loads(ujson.loads(settings).get("body"))
            for key, value in settings.items():
                value = value.replace('\\', '').replace('\n^', '').replace('\/', '/') if isinstance(value, str) else value
                if value is not None:
                    if key == 'notification_threshold':
                        self.settings['thresholds']['notification'] = value if value < 1.0 else value / 100.
                    elif key == 'action_threshold':
                        self.settings['thresholds']['action'] = value if value < 1.0 else value / 100.
                    elif key == 'notify_action':
                        self.settings['actions']['notify'] = value
                    elif key == 'pause_action':
                        self.settings['actions']['pause'] = value
                    elif key == 'rotation':
                        self.settings["rotation"] = int(value)
                    else:
                        self.settings[key] = value
            self._save_settings()
            self._on_settings_change()

            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8000}), response_type=HttpResponseType.JSON)
        except Exception as e:
            await http_endpoint_connection.send_response(200, ujson.dumps({'e' : str(e)}), response_type=HttpResponseType.JSON)
        http_endpoint_connection.close()

    async def _get_settings(self, http_endpoint_connection: HttpEndpointConnection):
        await http_endpoint_connection.read_request()
        await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8000, 'settings' : self.settings}), response_type=HttpResponseType.JSON)
        http_endpoint_connection.close()

    async def _add_monitor(self, http_endpoint_connection: HttpEndpointConnection):
        await http_endpoint_connection.read_request()
        result = self._init_monitor()
        if result:
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8000}), response_type=HttpResponseType.JSON)
        else:
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8001, 'response' : 'Monitor loop already exists'}), response_type=HttpResponseType.JSON)
        http_endpoint_connection.close()

    async def _kill_monitor(self, http_endpoint_connection: HttpEndpointConnection):
        await http_endpoint_connection.read_request()
        try:
            self.runner.cancel()
            self.runner = None
            self.settings["monitoring_on"] = False
            self._save_settings()
            self._on_settings_change()
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8000}), response_type=HttpResponseType.JSON)
        except Exception as e:
            await http_endpoint_connection.send_response(200, ujson.dumps({'status' : 8001, 'response' : str(e)}), response_type=HttpResponseType.JSON)
        http_endpoint_connection.close()
