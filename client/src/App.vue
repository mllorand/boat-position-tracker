<template>
  <div id="app">
    <div class="map">
      <MapContainer :positions="positions"></MapContainer>
    </div>
  </div>
  <!-- <h1>{{ positions }}</h1> -->
</template>

<script>
import SocketioService from './services/socketio.service.js';
import MapContainer from './components/MapContainer.vue';
export default {

  name: 'App',
  data() {
    return {
      positions: {
        line1: [20.73998593, 48.21339894],
        line2: [20.73990023, 48.21496414],
        line3: [20.73651803, 48.21694363]
      }
    }
  },

  components: {
    MapContainer
  },

  created() {
    const socket = SocketioService.setupSocketConnection()
    socket.on('positions', data => {
      this.positions =
      {
        line1: [data.line1.lon, data.line1.lat],
        line2: [data.line2.lon, data.line2.lat],
        line3: [data.line3.lon, data.line3.lat]
      }
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
