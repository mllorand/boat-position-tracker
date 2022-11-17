<template>
  <!-- <div id="app"> -->
    <div id="map">
      <MapContainer :geojson="geojson"></MapContainer>
    </div>
  <!-- <h1>{{ positions }}</h1> -->
  <!-- </div> -->
</template>

<script>
import SocketioService from './services/socketio.service.js';
import MapContainer from './components/MapContainer.vue';
export default {
  name: 'App',
  components: {
    MapContainer
  },

  data: () => ({
     
    // positions: 'hello',
    
    geojson: {
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

      const newGeojson = {
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
            coordinates: [positions.line1.lon, positions.line1.lat]
          }
        },
        {
          type: 'Feature',
          properties: {},
          geometry: {
            type: 'Point',
            coordinates: [positions.line2.lon, positions.line2.lat]
          }
        },
        {
          type: 'Feature',
          properties: {},
          geometry: {
            type: 'Point',
            coordinates: [positions.line3.lon, positions.line3.lat]
          }
        }
      ]
    }

    this.geojson = newGeojson
      // console.log('ship1 coordinates', this.geojson.features.at(0).geometry.coordinates)
      // console.log(positions)
      // console.log(positions.line1.lon)

      // this.geojson.features.at(0).geometry.coordinates = [positions.line1.lon, positions.line1.lat]
      // this.geojson.features.at(1).geometry.coordinates = [positions.line2.lon, positions.line2.lat]
      // this.geojson.features.at(2).geometry.coordinates = [positions.line3.lon, positions.line3.lat]
      
    });
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
