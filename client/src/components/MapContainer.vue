<template>
		<div ref="map-root" style="width: 100%; height: 100%">
		</div>
</template>

<script>
import View from 'ol/View'
import Map from 'ol/Map'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import OSM from 'ol/source/OSM'
import GeoJSON from 'ol/format/GeoJSON'
import 'ol/ol.css'




export default {
	name: 'MapContainer',
	components: {},
	props: ['positions'],


	mounted() {

		const shipData1 = {
			type: 'Feature',
			properties: {},
			geometry: {
				type: 'Point',
				coordinates: this.positions.line1
			}
		};

		const shipData2 = {
			type: 'Feature',
			properties: {},
			geometry: {
				type: 'Point',
				coordinates: this.positions.line2
			}
		};

		const shipData3 = {
			type: 'Feature',
			properties: {},
			geometry: {
				type: 'Point',
				coordinates: this.positions.line3
			}
		}

		// const data = {
		// 	type: 'Feature',
		// 	properties: {},
		// 	geometry: {
		// 		type: 'Point',
		// 		coordinates: this.positions
		// 	}
		// };

		// a feature (geospatial object) is created from the GeoJSON
		const ship1 = new GeoJSON().readFeature(shipData1, {
			featureProjection: 'EPSG:3857'
		});
		const ship2 = new GeoJSON().readFeature(shipData2, {
			featureProjection: 'EPSG:3857'
		});
		const ship3 = new GeoJSON().readFeature(shipData3, {
			featureProjection: 'EPSG:3857'
		});

		// a new vector layer is created with the feature
		const vectorLayer = new VectorLayer({
			source: new VectorSource({
				features: [ship1, ship2, ship3],
			}),
		})


		// this is where we create the OpenLayers map
		new Map({
			// the map will be created using the 'map-root' ref
			target: this.$refs['map-root'],
			layers: [
				new TileLayer({
					source: new OSM()
				}),
				vectorLayer
			],

			// the map view will initially show the whole world
			view: new View({
				zoom: 5,
				center: [0, 0],
				constrainResolution: true
			}),
		})
	},
}

</script>
