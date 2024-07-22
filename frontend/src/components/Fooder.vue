//Frontend/src/components/Fooder.vue
<template>
    <footer class="footer">
      &copy; {{ currentYear }} MusicV2. All rights reserved.
    </footer>
  </template>
  
  <script>
  export default {
    name: 'FooterComponent',
    data() {
      return {
        currentYear: new Date().getFullYear(),
      };
    },
  };
  </script>
  
  <style scoped>
 
  </style>
  