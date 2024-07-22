//Frontend/src/app.vue
<template>
  <NavigationBar/>
  <router-view/>
  <Fooder/>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue';
import Fooder from './components/Fooder.vue';

export default {
  name: 'App',
  components: {
    NavigationBar,
    Fooder
  }
}
</script>

<style>

</style>
