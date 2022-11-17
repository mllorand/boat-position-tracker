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
import Stroke from 'ol/style/Stroke'
import Fill from 'ol/style/Fill'
import Style from 'ol/style/Style'
import RegularShape from 'ol/style/RegularShape'
import { getCenter } from 'ol/extent'



export default {
	name: 'MapContainer',
	components: {},
	props: {
		geojson: Object,
		headings: Array

	},
	data: () => ({
		olMap: null,
		vectorLayer: null
	}),

	mounted() {

		this.vectorLayer = new VectorLayer({
			source: new VectorSource({
				features: []
			})
		})

		this.olMap = new Map({
			target: this.$refs['map-root'],
			layers: [
				new TileLayer({
					source: new OSM()
				}),
				this.vectorLayer
			],

			view: new View({
				zoom: 5,
				center: [0, 0],
				constrainResolution: true,
			}),

		})

		this.olMap.getView().fit([2308427.160996733, 6142444.414658196, 2308768.012371982, 6143023.4081032])
		this.olMap.getView().setZoom(17)
		this.updateSource(this.geojson)
	},

	watch: {
		geojson(value) {
			this.updateSource(value)
			// this.addTrack()
		}
	},

	methods: {
		updateSource(geojson) {

			const stroke = new Stroke({ color: 'black', width: 1 });
			const fill = new Fill({ color: 'green' });

			const defaultStyle = new Style({
				stroke: stroke,
				fill: fill
			})

			const view = this.olMap.getView()
			const source = this.vectorLayer.getSource()

			const features = new GeoJSON({
				featureProjection: 'EPSG:3857'
			}).readFeatures(geojson)

			source.clear();
			source.addFeatures(features);

			for (let i = 0; i <= 2; i++) {
				const feature = features.at(i)
				feature.setStyle(defaultStyle)
				const anchor = getCenter(feature.getGeometry().getExtent())
				feature.getGeometry().rotate(this.headings.at(i) * (Math.PI / 180), anchor)

			}


			// features.forEach(feature => {
			// 	const anchor = getCenter(feature.getGeometry().getExtent())
			// 	feature.getGeometry().rotate(-90, anchor)
			// 	console.log(this.headings)

			// 	// feature.setStyle(triangle)
			// 	// console.log(feature.getStyle().getImage().getRotation())
			// })
			// view.fit([2308427.160996733, 6142444.414658196, 2308768.012371982, 6143023.4081032])
			// console.log(source.getExtent())
		}
	}
}

</script>
