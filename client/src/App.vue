<template>
  <h1>{{ positions }}</h1>
</template>

<script>
import SocketioService from './services/socketio.service.js';

export default {
  name: 'App',
  data() {
    return {
      positions: null
    }    
  },
  created() {
    const socket = SocketioService.setupSocketConnection()
    socket.on('positions', data => {
            this.positions = data
        });
  },
  beforeUnmount() {
    SocketioService.disconnect()
  }
}
</script>
