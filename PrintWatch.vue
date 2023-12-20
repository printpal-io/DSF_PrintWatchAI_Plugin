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
											<v-card-text class="pa-0 img-container" style="background-color:black;width:100%;aspect-ratio:16/9;text-align:center;color:white">
												<v-responsive v-if="enableMonitoring" :aspect-ratio="16/9">
													<img :src="imageDetectionPreview"  class="previewIFrame" style="height:100%">
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
																<v-select v-model="rotation"
																  label="Counter-Clockwise Rotation"
																  :items="['0', '90', '180', '270']"
																></v-select>
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
															<v-col cols="4" md="4">
																<v-switch v-model="pausePrint" label="Pause Print" hide-details></v-switch>
															</v-col>
															<v-col cols="12" md="8">
																<v-text-field v-model="pauseGCode" label="Pause G/M-Code command" :disabled="!pausePrint" hide-details></v-text-field>
															</v-col>
															<v-col cols="12" md="8">
																<v-text-field v-model="resumeGCode" label="Resume G/M-Code command" hide-details></v-text-field>
															</v-col>
															<v-col cols="12" md="8">
																<v-text-field v-model="cancelGCode" label="Cancel G/M-Code command" hide-details></v-text-field>
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
			gaugeColor : 'primary',
			pauseGCode : '',
			cancelGCode : '',
			resumeGCode : '',
			cameraIPValid : false,
			validateCamIntervalId : undefined,
			webcamController : undefined,
			rotation : '0',
			previewRefreshController : null,
			previewRefreshId : undefined,
			noPreview : 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QBoRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAExAAIAAAARAAAATgAAAAAAAABgAAAAAQAAAGAAAAABcGFpbnQubmV0IDUuMC4xMgAA/9sAQwAGBAUGBQQGBgUGBwcGCAoQCgoJCQoUDg8MEBcUGBgXFBYWGh0lHxobIxwWFiAsICMmJykqKRkfLTAtKDAlKCko/9sAQwEHBwcKCAoTCgoTKBoWGigoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgo/8AAEQgB4AKAAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A6uiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoqVbW4ZQywSlTyCEJBqIggkEYI4INABRRUsdtPIm+OGV1/vKhIoAiooooAKKkt7ea4fZbxSSv/dRSx/SrZ0XVAuTpt4B/1wb/AAoAoUU6SN4nKyIyMOoYYNNoAKKKKACinRxvK2I0Zz1wozUn2S5/595v++DQBDRTpI3jOJEZT/tDFNoAKKACSAASTwAKm+yXP/PvN/3waAIaKla3nQZeGRR6lSKioAKKKkjgllBMUTuBwSqk0AR0VN9kuf8An3m/74NH2S5/595v++DQBDRT0ikeTy0jdpOm0Lk/lTpraeAAzQyxg8DehFAEVFFFABRU0VpcTLuigmkX1VCRUW1t+3ad2cYxzmgBKKmltbiJN8sEqL/eZCBUNABRUq207qGWCVlPIIQkGl+yXP8Az7zf98GgCGipWtbhVLNBKAOSSh4pIYJZ2IhieQjkhFJo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FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH/9k=',
			loadingPreview : 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QBoRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAExAAIAAAARAAAATgAAAAAAAABgAAAAAQAAAGAAAAABcGFpbnQubmV0IDUuMC4xMgAA/9sAQwAGBAUGBQQGBgUGBwcGCAoQCgoJCQoUDg8MEBcUGBgXFBYWGh0lHxobIxwWFiAsICMmJykqKRkfLTAtKDAlKCko/9sAQwEHBwcKCAoTCgoTKBoWGigoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgo/8AAEQgB4AKAAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A6uiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAO88HeF9O1PRlurxZWkZ2HD4AANc94w0yDSdZNtab/K2K4DHJGa734d/8ixF/wBdH/nXI/En/kZP+2K/1oA5WlVSzBVBLE4AAyTSV2Xw10tbnUJb6ZQy22BGD/fPf8B/OgCxoXgNpolm1aVotwyIY/vD6k9PpXSR+DtDRcGzLH1aV8/zp3jDXP7E04NEA1zMSsQPQerH6cfmK8uudZ1K5mMk19clic8SEAfQDgUAei3vgbSZkP2cTWz9irlh+IOa4HxDoV1odwEuMPE/3JVHDf4H2re8G+KrtdQis9RmaeCY7FdzlkY9Oe4rufEOnLqmkXFswBYrujOOjDoaAPEqktYHubmKCIZkkcIo9ycVHXVfDmw+1a79oYZjtU3/APAjwP6n8KAOsi8D6Osaq6TOwGCxkIz+Vcl448Pw6NLbyWW/7PKCCGOdrD39x/I16Hqeqx2OoabayYBu5GTJ7ADj82Kj86qeNbD+0PDtyqjMkI85PqvX9M0AePVr+FNMi1fWorW4Z1iKszbOCcDpWRXT/Dn/AJGaP/rm/wDKgDr/APhBtH/u3H/fz/61NfwJpDdDcr9JB/UVd8cTy23hq6lt5ZIpQUw6MVI+YdxXmUHiDV4WDJqN0T/tyFx+RzQB0+qfD+RI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2+t+H9Gsbe51CDT4EuzwrAcBicZA6A81ylXOV9CIR6hRRRWZoFFFFABRRRQB1fgy/J32Uhzgb48/qP6/nWt4ktBd6VKAMvGPMX8Ov6ZridJnNvqdtKOMOAfoeDXpLAEEHkHg1a1RD0Z5XRUl1H5NzLH/AHHK/kajqCwooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArp/A2POu/Xav9a5it7wbN5eqNGf8AlpGQPqOf8aa3E9jd8X/8gV/99f51wleja5bm50m5jUZbbuH1HP8ASvOachR2CiiipKCiiigAooooAdD/AK1P94V6nXnGiW5udVto8ZG8MfoOa9FdgiMzcBRk1cSZHm+r4/tW729PNb+dVKfPJ5s8kh6uxb8zTKgoKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKnsbg2l5DOvWNgceo71BRQB6lDIs0SSRncjgMD6iuB8RacbC/baP3Eh3IfT1H4VreEdVAH2Gdsc5iJ/9BrodRsor+1aGccHkEdVPqKvdEbM80oq9qmmXGnS7ZlyhPyyAcNVGoLCiiigAoorodA0B7hlnvVKQDkIeC/8A9ahK4Nmh4P04wwteSjDyDCA9l9fxq34qvBa6W6A/vJvkH07/AKfzrWkdIIWdyEjQZJ6ACvPdb1FtRvmk5ES/LGvoKt6Ihau5n0UUVBYUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAAJBBHBHINdfoPiFZFW3v22yDhZT0b6+hrkKKadhNXPUpI0mjKSKrow5BGQawrzwvaTEtbu8B9B8y1zmm61eWGFjffEP4H5H4elb9r4rt2AFzDJGfVfmFVdMmzRSbwncA/LcxEe4Ip8PhKQn99dIB/sLmthPEOmt/y8bfqh/wpkniTTkHyyO/sqH+tFkF2S6foVlZMHVDJIOjyc4+g6VfuriK1hMtxIqIO5rl7zxYxBFnBt/2pDn9BXPXl5cXkm+5laRu2eg+goulsFm9zR17Wn1F/Liylsp4Xu3uf8Kx6KKgsKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD/9k=',
			invalidSettingsPreview : 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QBoRXhpZgAATU0AKgAAAAgABAEaAAUAAAABAAAAPgEbAAUAAAABAAAARgEoAAMAAAABAAIAAAExAAIAAAARAAAATgAAAAAAAABgAAAAAQAAAGAAAAABcGFpbnQubmV0IDUuMC4xMgAA/9sAQwAGBAUGBQQGBgUGBwcGCAoQCgoJCQoUDg8MEBcUGBgXFBYWGh0lHxobIxwWFiAsICMmJykqKRkfLTAtKDAlKCko/9sAQwEHBwcKCAoTCgoTKBoWGigoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgo/8AAEQgB4AKAAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/aAAwDAQACEQMRAD8A6uiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKK1vCUaTeI7BJUV0MnKsMg8GvS/FdnbDw7fkW8IKxEqdg4PtQB49RUtmiy3kEb8q8iqfoTXt6adZIgRLO3CgYAEY/wAKAPC6K734heH4oYF1GwhSNVO2ZEXA56Nj68H6iuCoAKK9g8K2VqfDtiWtoCWiBYmMHJ9688tJLez8aEyxRm2S7dChUbQpYjp7Zz+FAGFRXturaTbX2m3Fv5EQZ0IQ7ANrY4P514mylGKsCGBwQe1ACUUV6/4R0mG00C1EsEZmkXzHZlBJ3cgfgMCgDyCitbxVPFceIL1rZESJX2KEGAdvGfxxW18N9LjvNQnuriNZIoF2qGGRuP8AgAfzoA4+ivd2s7Z1KtbQsp6gxgivHPFGn/2Zrl1bqMR7t0f+6eR+XT8KAMuiivTPhtbQSaFLJJDEz+ew3MgJxtXj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hrQB5f4d/wCQ/pv/AF8x/wDoQr2LWv8AkD3/AP17yf8AoJrxzw8ca9ppPA+0x/8AoQr2u4iW4t5IZMlJFKNj0IwaAPBa2PCemSaprUEaqTFGwklbsFB/r0r0FPBOiq2TDKw9DKf6Vqomm6HZ4XyLOAdSSFyf5k0ATapdrYadcXUhAESFue57D868MZizFm5JOSa6vxp4oGrf6JY7hZqcsxGDIe30FcnQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFADopHikV4nZHU5DKcEfjVy41fUbmIxXF9cyRnqrSkg/WqNFAApKsCpII5BHars2r6jPCYpr+6eIjBVpWII9+apUUAFCkqwKkgg5BHaiigC+2s6myFG1G8KkYIMzf41QoooAKtWmo3tmhS0u7iFCclY5CoJ/CqtFAFu71K+vIwl1eXEyA5CySFhn6GqlFFAF9NZ1NIxGmoXaoBtCiZgAPTrVDrRRQAVLa3M9pL5lrNJDJjG6Nipx+FRUUAW7rU767j8u6vLiaPOdryFhn6Uy1vbq0z9kuZ4N3XypCufyqvRQBof23qv/QTvf+/7f40f23qv/QTvf+/7f41n0UASRzzRTiaOWRJgciRWIbPrmrF1qt/dxeXdXtxLH3R5CQfwqnRQAAkHI4NX11nVFAA1K9AHAAnbj9aoUUAXm1fUnGH1C8Ye87H+tU5JHkYtIzOx6ljk02igAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigB0UbzSLHCjSSNwFUZJ/CtuHwlrcyblsW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8mnx3xtnNpICRIvIHOOcdOneqNek+C/EunJpNvY3cy280QK5k4Vhnrnp3710P2bRZz5vk6dIeu/Yh/WgDI+G5ujoLG5LmLzCId393Azj2z/Wsf4qSIbjToxjequx+hIx/I10+q+J9K0yEjz0mkUYWKAhj9OOBXlWs6lNq2oSXdxgM3AUdFUdAKAKVFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAf//Z'
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
					this.pauseGCode = data.settings.pause_gcode;
					this.resumeGCode = data.settings.resume_gcode;
					this.cancelGCode = data.settings.cancel_gcode;
					this.rotation = Math.floor(data.settings.rotation).toString();
				})
				.catch(error => {
					console.log('There was a problem with the fetch operation:', error);
				});
		},
    fetchData() {
      // API call to backend
			const timeout = 1000;
			const controller = new AbortController();
			const id = setTimeout(() => controller.abort(), timeout);

      fetch('/machine/printwatch/monitor', {signal : controller.signal})
        .then((response) => response.json())
        .then((data) => {
					if (data.status == 8000) {
						this.trackingInfo = data.items.status;
						this.defectLevel = parseInt(parseFloat(data.items.status.buffer.slice(-1)[0][0]) * 100)
					}
        })
        .catch(error => {
          console.log('There was a problem with the fetch operation:', error);
					clearTimeout(id);
        });
    },
		fetchPreview() {
      // API call to backend
			if (!this.previewRefreshController) {
				const timeout = 5000;
				const controller = new AbortController();
				const id = setTimeout(() => controller.abort(), timeout);

				fetch('/machine/printwatch/preview', {signal : controller.signal})
					.then((response) => response.json())
					.then((data) => {
						if (data.status == 8000) {
							if (data.items.status.preview != null) {
								if (data.items.status.preview == 'loading') {
									this.imageDetectionPreview = this.loadingPreview;
								} else if (data.items.status.preview == 'settingsIssue') {
									this.imageDetectionPreview = this.invalidSettingsPreview;
								} else {
									this.imageDetectionPreview = data.items.status.preview;
								}
							} else {
								this.imageDetectionPreview = this.noPreview;
							}
						}
					})
					.catch(error => {
						console.log('There was a problem with the fetch operation:', error);
						clearTimeout(id);
					});
			}
    },
		initMonitor() {
      // API call to backend
      fetch('/machine/printwatch/monitor_init')
        .catch(error => {
          console.log('There was a problem with the fetch operation:', error);
        });
    },
		stopMonitor() {
      // API call to backend
      fetch('/machine/printwatch/monitor_off')
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
      .catch(error => {
        console.log('There was a problem with the fetch operation:', error);
      });
    },
    checkAndStartInterval() {
      if (this.enableMonitoring) {
        this.fetchData(); // Initial API call
				this.fetchPreview();
				//console.log(this.settings);
        this.intervalId = setInterval(() => {
          this.fetchData();
        }, 2000); // Every 2 seconds
				this.streamIntervalId = setInterval(() => {
          this.fetchPreview();
        }, 10000); // Every 10 seconds
      }
    },
    stopInterval() {
      clearInterval(this.intervalId);
			clearInterval(this.streamIntervalId);
    },
		resetController() {
			this.previewRefreshController = false;
			clearTimeout(this.previewRefreshId);
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
				this.imageDetectionPreview = this.loadingPreview;
			} else {
				this.stopMonitor();
				this.stopInterval();
				this.imageDetectionPreview = this.noPreview;
			}
		},
		apiKey : function(){
			if (this.apiKey != '') {
				this.setSettings("api_key", this.apiKey);
			}
		},
		snapshotUrl : function(){
			if (this.snapshotUrl != '' && this.snapshotUrl.length > 5) {
				this.setSettings("camera_ip", this.snapshotUrl);
			}
		},
		emailAddr : function(){
			if (this.emailAddr != '' && this.emailAddr.length > 5) {
				this.setSettings("email_addr", this.emailAddr);
			}
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
			if (this.previewRefreshId != undefined || this.previewRefreshId != null) {
				clearTimeout(this.previewRefreshId);
				this.previewRefreshController = false;
			}
			if (this.testMode) {
				this.imageDetectionPreview = this.loadingPreview;
			} else {
				this.imageDetectionPreview = this.noPreview;
			}
			this.previewRefreshController = true;
			setTimeout(this.resetController, 10000);
		},
		rotation : function(){
			this.setSettings("rotation", this.rotation);
		},
		pauseGCode : function(){
			if (this.pauseGCode != '' && this.pauseGCode.length > 1) {
				this.setSettings("pause_gcode", this.pauseGCode);
			}
		},
		cancelGCode : function(){
			if (this.cancelGCode != '' && this.cancelGCode.length > 1) {
				this.setSettings("cancel_gcode", this.cancelGCode);
			}
		},
		resumeGCode : function(){
			if (this.resumeGCode != '' && this.resumeGCode.length > 1) {
				this.setSettings("resume_gcode", this.resumeGCode);
			}
		},
		defectLevel : function(){
			this.setGaugeColor();
		}
	}
}
</script>
