//Frontend/src/components/NavigationBar.vue


<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    
      <router-link to="/" class="navbar-brand">
        <img src="../assets/applogo.jpeg"  width="30" height="30">
        MusicV2
      </router-link>

      <div class="navbar-nav ml-auto">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/admin-login" class="nav-link">Admin Login</router-link>
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/signup" class="nav-link">SignUp</router-link>
      </div>

      
    
  </nav>

</template>

<script>
export default {
  name: 'NavigationBar'
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
