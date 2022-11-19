<template>
	<div id="map">
		<MapContainer :boats="boats" :headings="headings" :activeRecording="activeRecording"
			v-on:changeline="recordedLine = $event"></MapContainer>
	</div>
</template>


<script>
import SocketioService from './services/socketio.service.js';
import MapContainer from './components/MapContainer.vue';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import Style from 'ol/style/Style';
import RegularShape from 'ol/style/Style'
export default {
	name: 'App',
	components: {
		MapContainer
	},

	data: () => ({

		headings: [3.470315226, 162.6569972, 87.18099145],

		recordedLine: null,

		activeRecording: null,

		boats: {
			type: 'FeatureCollection',
			crs: {
				type: 'name',
				properties: {
					name: 'EPSG:3857',
				},
			},
			features: [
				{
					type: 'Feature',
					properties: {},
					geometry: {
						type: 'Point',
						coordinates: [20.73998593, 48.21339894]
					}
				},
				{
					type: 'Feature',
					properties: {},
					geometry: {
						type: 'Point',
						coordinates: [20.73990023, 48.21496414]
					}
				},
				{
					type: 'Feature',
					properties: {},
					geometry: {
						type: 'Point',
						coordinates: [20.73651803, 48.21694363]
					}
				}
			]
		}

	}),

	mounted() {
		const socket = SocketioService.setupSocketConnection()
		socket.on('positions', data => {

			const positions = JSON.parse(data)



			// console.log(this.recordedLine)

			if (this.activeRecording) {
				const newActiveRecording = {
					type: 'Feature',
					geometry: {
						type: 'LineString',
						coordinates: this.activeRecording.geometry.coordinates
					}
				}
				newActiveRecording.geometry.coordinates.push([positions[this.recordedLine].lon, positions[this.recordedLine].lat])
				this.activeRecording = newActiveRecording
			}

			if (this.recordedLine) {
				const newActiveRecording = {
					type: 'Feature',
					geometry: {
						type: 'LineString',
						coordinates: this.activeRecording.geometry.coordinates
					}
				}

			}


			// const newPoint = {
			// 	type: 'Feature',
			// 		properties: {},
			// 		geometry: {
			// 			type: 'Point',
			// 			coordinates: [positions[this.recordedLine].lon, positions[this.recordedLine].lat]
			// 		}
			// }


			// console.log(newActiveRecording.geometry.coordinates)

			const x = 0.00004
			const y = 0.0001

			const newBoats = {
				type: 'FeatureCollection',
				crs: {
					type: 'name',
					properties: {
						name: 'EPSG:3857',
					},
				},
				features: [
					{
						type: 'Feature',
						properties: { name: 'line1', recorded: this.recordedLine == 'line1'},
						geometry: {
							type: 'Polygon',
							coordinates: [[
								[positions.line1.lon, positions.line1.lat],
								[positions.line1.lon - x, positions.line1.lat - y],
								[positions.line1.lon + x, positions.line1.lat - y],
								[positions.line1.lon, positions.line1.lat]
							]]
						}
					},
					{
						type: 'Feature',
						properties: { name: 'line2', recorded: this.recordedLine == 'line2'},
						geometry: {
							type: 'Polygon',
							coordinates: [[
								[positions.line2.lon, positions.line2.lat],
								[positions.line2.lon - x, positions.line2.lat - y],
								[positions.line2.lon + x, positions.line2.lat - y],
								[positions.line2.lon, positions.line2.lat]
							]]
						}
					},

					{
						type: 'Feature',
						properties: { name: 'line3', recorded: this.recordedLine == 'line3' },
						geometry: {
							type: 'Polygon',
							coordinates:
								[[
									[positions.line3.lon, positions.line3.lat],
									[positions.line3.lon - x, positions.line3.lat - y],
									[positions.line3.lon + x, positions.line3.lat - y],
									[positions.line3.lon, positions.line3.lat]
								]]
						}
					}
				]
			}
			this.headings = [positions.line1.heading, positions.line2.heading, positions.line3.heading]
			// this.activeRecording = newActiveRecording
			this.boats = newBoats

		});
	},

	watch: {
		recordedLine(value) {
			console.log('the changed value of recordedLine', value)
			if (value) {
				this.activeRecording = {
					type: 'Feature',
					geometry: {
						type: 'LineString',
						coordinates: []
					}
				}
			} else {
				this.activeRecording = null
			}
		}
	},

	beforeUnmount() {
		SocketioService.disconnect()
	}
}
</script>

<style>
html,
body {
	height: 100%;
	margin: 0;
}

#app {
	font-family: Avenir, Helvetica, Arial, sans-serif;
	height: 100%;
	display: grid;
	grid-template-columns: 100vh;
	grid-auto-rows: 1fr;
	grid-gap: 1rem;
	padding: 1rem;
	box-sizing: border-box;
}
</style>
