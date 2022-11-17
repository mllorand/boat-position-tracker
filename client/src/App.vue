<template>
  <!-- <div id="app"> -->
  <h1>{{ positions }}</h1>
  <!-- </div> -->
</template>

<script>
import SocketioService from './services/socketio.service.js';
// import MapContainer from './components/MapContainer.vue';
export default {
  name: 'App',
  components: {
    // MapContainer
  },

  data() {
    return {
      positions: 'hello'
    }
    // geojson: {
    //   type: 'FeatureCollection',
    //   crs: {
    //     type: 'name',
    //     properties: {
    //       name: 'EPSG:3857',
    //     },
    //   },
    //   features: [
    //     {
    //       type: 'Feature',
    //       properties: {},
    //       geometry: {
    //         type: 'Point',
    //         coordinates: [20.73998593, 48.21339894]
    //       }
    //     },
    //     {
    //       type: 'Feature',
    //       properties: {},
    //       geometry: {
    //         type: 'Point',
    //         coordinates: [20.73990023, 48.21496414]
    //       }
    //     },
    //     {
    //       type: 'Feature',
    //       properties: {},
    //       geometry: {
    //         type: 'Point',
    //         coordinates: [20.73651803, 48.21694363]
    //       }
    //     }
    //   ]
    // }

  },

  created() {
    const socket = SocketioService.setupSocketConnection()
    socket.on('positions', data => {
      this.positions = data
      // console.log('ship1 coordinates', this.geojson.features.at(0).geometry.coordinates)

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

.cell {
  border-radius: 4px;
  background-color: lightgrey;
}

.cell-map {
  grid-column: 1;
  grid-row-start: 1;
  grid-row-end: 3;
}

.cell-edit {
  grid-column: 2;
  grid-row: 1;
}

.cell-inspect {
  grid-column: 2;
  grid-row: 2;
}
</style>
