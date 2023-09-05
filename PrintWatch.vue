<style scoped>
.content {
	position: relative;
	min-height: 480px;
}

.content canvas {
	position: absolute;
}

th {
	white-space: nowrap;
}

iframe {
	width: 100%;
	height: 100%;
	border: 0px;
	overflow: hidden;
}

img {
	max-width: 100%;
	max-height: 100%;
	border: 0px;
	overflow: hidden;
}

.img-container {
	overflow: hidden;
}
</style>

<template>
	<v-row>
		<v-col>
			<v-card>
				<v-tabs v-model="tab">
					<!-- Tabs -->
					<v-tab href="#current">
						<v-icon class="mr-1">mdi-information</v-icon>
						Preview
					</v-tab>
					<v-tab href="#settings">
						<v-icon class="mr-1">mdi-cog</v-icon>
						Settings
					</v-tab>
					<v-btn v-if="enableMonitoring && !testMode" color="success" class="align-self-center ml-auto mr-2 hidden-sm-and-down" :disabled="!enableMonitoring" @click="testMode = !testMode">
						<v-icon class="mr-1">mdi-test-tube</v-icon>
						Enable Test Mode
					</v-btn>
					<v-btn v-if="!enableMonitoring || (enableMonitoring && testMode)" color="gray" class="align-self-center ml-auto mr-2 hidden-sm-and-down" :disabled="!enableMonitoring" @click="testMode = !testMode">
						<v-icon class="mr-1">mdi-test-tube</v-icon>
						Disable Test Mode
					</v-btn>
					<v-btn v-if="!enableMonitoring" color="success" class="align-self-center ml-2 mr-2 hidden-sm-and-down" :disabled="false" @click="enableMonitoring = !enableMonitoring">
						<v-icon class="mr-1">mdi-power</v-icon>
						Enable Monitoring
					</v-btn>
					<v-btn v-if="enableMonitoring" color="warning" class="align-self-center ml-2 mr-2 hidden-sm-and-down" :disabled="false" @click="enableMonitoring = !enableMonitoring">
						<v-icon class="mr-1">mdi-power</v-icon>
						Disable Monitoring
					</v-btn>
				</v-tabs>

				<v-tabs-items v-model="tab">
					<!-- Current Preview -->
					<v-tab-item value="current">
						<div class="d-flex flex-column">
							<v-alert :value="!enableMonitoring" type="info" class="mb-0">
								AI Monitoring is not enabled. Please enable it with the "Enable Monitoring" button
							</v-alert>
							<div v-show="enableMonitoring" class="content flex-grow-1 pa-2">
								<div class="row">
									<div class="col-md-6 col-lg-6 col-12">
										<div class="v-card v-sheet v-sheet--outlined theme--light">
											<v-card-text class="pa-0 img-container">
												<v-responsive v-if="enableMonitoring" :aspect-ratio="16/9">
													<img :src="imageDetectionPreview"  class="previewIFrame" style="width:100%;height:100%">
												</v-responsive>
											</v-card-text>
										</div>
									</div>
									<div class="col-md-2 col-lg-2 col-12">
										<div class="v-card v-sheet v-sheet--outlined theme--light">
											<div class="v-card__title pb-0">
												Defectiveness Level
											</div>
												<div class="text-center mb-4 mt-4">
													<v-progress-circular
														v-model="defectLevel"
														:rotate="180"
														:size="100"
														:width="15"
														:color="gaugeColor"
													>
														<strong style="color:black">{{ defectLevel }}</strong>
													</v-progress-circular>
												</div>
											</div>
									</div>
								</div>
							</div>
						</div>
					</v-tab-item>

					<!-- Settings -->
					<v-tab-item value="settings">
						<div class="d-flex flex-column">
							<v-alert :value="!enableMonitoring" type="info" class="mb-0">
								AI Monitoring is not enabled. Please enable it with the "Enable Monitoring" button
							</v-alert>
							<div class="content flex-grow-1 pa-2">

							<v-card-text>
										<v-row :dense="$vuetify.breakpoint.mobile">
											<div class="row pa-3"  v-show="enableMonitoring">
												<div class="col-md-4 col-lg-4 col-12">
													<div class="v-card v-sheet v-sheet--outlined theme--light">
														<div class="v-card__title pb-0">
															General
														</div>
														<div class="col-md-12 col-12">
															<v-col cols="12" md="8">
																<v-text-field v-model="apiKey" label="API key" hide-details></v-text-field>
															</v-col>
															<v-col cols="12" md="8">
																<v-text-field v-model="snapshotUrl" label="Webcam URL" hide-details></v-text-field>
															</v-col>
															<v-col cols="12" md="8">
																<v-text-field v-model="emailAddr" label="Email address" hide-details></v-text-field>
															</v-col>
															<div class="pt-8">
																<div class="text-caption">
													        Notification Threshold
													      </div>
																<v-slider
															    v-model="notificationThreshold"
															    :max="100"
															    :min="0"
															    hide-details
																	thumb-label="always"
																	class="pt-8"
															  >
															  </v-slider>
															</div>

															<div class="pt-2">
																<div class="text-caption">
													        Action Threshold
													      </div>
																<v-slider
															    v-model="actionThreshold"
															    :max="100"
															    :min="0"
															    hide-details
																	thumb-label="always"
																	class="pt-8"
															  >
															  </v-slider>
															</div>

														</div>
													</div>
												</div>
												<div class="col-md-4 col-12">
													<div class="v-card v-sheet v-sheet--outlined theme--light">
														<div class="v-card__title pb-0">
															Action
														</div>
														<div class="col-md-12 col-12">
															<v-col cols="12" md="12">
																<v-switch v-model="enableNotify" label="Enable Email Notification" hide-details></v-switch>
															</v-col>
															<v-col cols="12" md="12">
																<v-switch v-model="pausePrint" label="Pause Print" hide-details></v-switch>
															</v-col>
														</div>
													</div>
												</div>

											</div>
										</v-row>
							</v-card-text>
							</div>
						</div>
					</v-tab-item>
				</v-tabs-items>
			</v-card>
		</v-col>
	</v-row>
</template>

<script>
'use strict'
import { mapState, mapGetters } from 'vuex'

export default {
	components: {
	},
	computed: {
		...mapState(['selectedMachine']),
		...mapGetters(['isConnected', 'uiFrozen'])
	},
	data() {
		return {
			tab : null,
			imageDetectionPreview : null,
			enableMonitoring : true,
			trackingInfo : {},
			intervalId : null,
			streamIntervalId : null,
			notificationThreshold : null,
			actionThreshold : null,
			pausePrint : false,
			emailAddr : '',
			enableNotify : false,
			snapshotUrl : '',
			apiKey : '',
			testMode : false,
			defectLevel : 0,
			gaugeColor : 'primary'
		}
	},

	methods: {
		setGaugeColor() {
			if(this.defectLevel < 20) {
				this.gaugeColor = "success";
			} else if (this.defectLevel >= 20 && this.defectLevel < 40.0) {
				this.gaugeColor = "amber";
			} else if (this.defectLevel >= 40 && this.defectLevel < 60.0) {
				this.gaugeColor = "warning";
			} else {
				this.gaugeColor = "error";
			}
		},
		fetchSettings() {
			// API call to backend
			fetch('/machine/printwatch/get_settings')
				.then((response) => response.json())
				.then((data) => {
					this.notificationThreshold = Math.round(data.settings.thresholds.notification * 100.0);
					this.actionThreshold = Math.round(data.settings.thresholds.action * 100.0);
					this.pausePrint = data.settings.actions.pause;
					this.emailAddr = data.settings.email_addr;
					this.enableNotify = data.settings.actions.notify;
					this.snapshotUrl = data.settings.camera_ip;
					this.apiKey = data.settings.api_key;
					this.testMode = data.settings.test_mode;
					this.enableMonitoring = data.settings.monitoring_on;
				})
				.catch(error => {
					console.log('There was a problem with the fetch operation:', error);
				});
		},
    fetchData() {
      // API call to backend
      fetch('/machine/printwatch/monitor')
        .then((response) => response.json())
        .then((data) => {
					if (data.status == 8000) {
						this.trackingInfo = data.items.status;
						this.defectLevel = parseInt(parseFloat(data.items.status.buffer.slice(-1)[0][0]) * 100)
						console.log(data.items.status.buffer.slice(-1)[0][0]);
					}
        })
        .catch(error => {
          console.log('There was a problem with the fetch operation:', error);
        });
    },
		fetchPreview() {
      // API call to backend
      fetch('/machine/printwatch/preview')
        .then((response) => response.json())
        .then((data) => {
					if (data.status == 8000) {
						this.imageDetectionPreview = data.items.status.preview;
					}
        })
        .catch(error => {
          console.log('There was a problem with the fetch operation:', error);
        });
    },
		initMonitor() {
      // API call to backend
      fetch('/machine/printwatch/monitor_init')
        .then((response) => response.json())
        .then((data) => {
					console.log(data);
        })
        .catch(error => {
          console.log('There was a problem with the fetch operation:', error);
        });
    },
		setIFrame() {
      // API call to backend
			console.log('LOL?');
			console.log(document.getElementsByClassName("previewIFrame"));
			let width = document.getElementsByClassName("previewIFrame")[0].clientWidth;
			let height = document.getElementsByClassName("previewIFrame")[0].clientHeight;
			console.log(width);
			console.log(height);
      fetch('http://localhost:8989/iframe/set?width=${width}&height=${height}')
        .then((response) => response.json())
        .then((data) => {
					console.log(data);
        })
        .catch(error => {
          console.log('There was a problem with the fetch operation:', error);
        });
    },
		stopMonitor() {
      // API call to backend
      fetch('/machine/printwatch/monitor_off')
        .then((response) => response.json())
        .then((data) => {
					console.log(data);
        })
        .catch(error => {
          console.log('There was a problem with the fetch operation:', error);
        });
    },
		setSettings(keyName, value) {
      // API call to backend
			var ss = {};
			ss[keyName] = value;
      fetch('/machine/printwatch/set_settings', {
				method: 'POST',
				headers: {
		      'Accept': 'application/json',
		      'Content-Type': 'application/json'
	    	},
	    	body: JSON.stringify(ss),
			})
      .then(response => response.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.log('There was a problem with the fetch operation:', error);
      });
    },
    checkAndStartInterval() {
      if (this.enableMonitoring) {
        this.fetchData(); // Initial API call
				this.fetchPreview();
				console.log(this.settings);
        this.intervalId = setInterval(() => {
          this.fetchData();
        }, 1000); // Every 1 seconds
				this.streamIntervalId = setInterval(() => {
          this.fetchPreview();
        }, 5000); // Every 5 seconds
      }
    },
    stopInterval() {
      clearInterval(this.intervalId);
			clearInterval(this.streamIntervalId);
    }
  },

	mounted() {
		// Reload the file list
		this.fetchSettings();
    this.checkAndStartInterval();
		this.setGaugeColor();
	},
	beforeDestroy() {
		this.stopInterval();
	},
	watch: {
		enableMonitoring : function(){
			if (this.enableMonitoring) {
				this.initMonitor();
				this.checkAndStartInterval();
			} else {
				this.stopMonitor();
				this.stopInterval();
			}
		},
		apiKey : function(){
			this.setSettings("api_key", this.apiKey);
		},
		snapshotUrl : function(){
			this.setSettings("camera_ip", this.snapshotUrl);
		},
		emailAddr : function(){
			this.setSettings("email_addr", this.emailAddr);
		},
		notificationThreshold : function(){
			this.setSettings("notification_threshold", this.notificationThreshold);
		},
		actionThreshold : function(){
			this.setSettings("action_threshold", this.actionThreshold);
		},
		enableNotify : function(){
			this.setSettings("notify_action", this.enableNotify);
		},
		pausePrint : function(){
			this.setSettings("pause_action", this.pausePrint);
		},
		testMode : function(){
			this.setSettings("test_mode", this.testMode);
		},
		defectLevel : function(){
			this.setGaugeColor();
		}
	}
}
</script>
