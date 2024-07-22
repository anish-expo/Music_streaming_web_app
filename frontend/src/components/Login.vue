//src/components/Login.vue

<template>
    <div class="login-container">
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username or email">Username or Email:</label>
          <input type="text" id="username" v-model="form.username" />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <div class="password-input">
            <input :type="showPassword ? 'text' : 'password'" id="password" v-model="form.password" />
            <button type="button" @click="togglePasswordVisibility">
              {{ showPassword ? 'Hide' : 'Show' }} Password
            </button>
          </div>
        </div>
        <button type="submit">Login</button>
      </form>
      <span>{{ errorMessage }}</span>
      
    </div>
    
  </template>
  

  <script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
    name: 'LogIn',
    data() {
      return {
        form: {
          username: '',
          password: ''
        },
        showPassword: false,
        errorMessage: '' 
      };
    },
    methods: {
      login() {
    axios.post('http://127.0.0.1:5000/other_login', this.form)
      .then(response => {
        if (response && response.data) {
          const { access_token, refresh_token, username } = response.data;
          localStorage.setItem('access_token', access_token);
          localStorage.setItem('refresh_token', refresh_token);
          localStorage.setItem('username', username);
          this.redirectBasedOnRole(access_token);
          
        } else {
          console.error('Login error: Response data is undefined');
        }
      })
      .catch(error => {
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.message;
          
          
        } else {
          this.errorMessage = 'An error occurred during login. Please try again later.';
          
        }
      });
  },
      togglePasswordVisibility() {
        this.showPassword = !this.showPassword;
      },
      redirectBasedOnRole(access_token) {
        // Decode the access token to extract user role
        const decodedToken = jwtDecode(access_token);
        //console.log(decodedToken)
        const userRole = decodedToken.role;
        
        // console.log('decodeToken:',decodedToken)
        // Redirect based on user role
        if (userRole === 'User') {
          // console.log('response:',username)
          const username = localStorage.getItem('username');
          this.$router.push({ name: 'UserDashboard', params: { username } });
        } 
        else if(userRole== 'Creator'){
          const username = localStorage.getItem('username');
          this.$router.push({ name: 'CreatorDashboard', params: { username } });

        }
        else {
          // Redirect to user dashboard or any other appropriate page
          this.$router.push('/admin-login');
        }
      }
    
    } 



}


</script>

<style scoped>
.login-container {
display: flex;
justify-content: center;
align-items: center;
height: 50vh;
}

.login-form {
width: 300px;
padding: 20px;
border: 1px solid #ccc;
border-radius: 8px;
}

.form-group {
margin-bottom: 15px;
}

.password-input {
display: flex;
align-items: center;
}

.password-input input {
flex: 1;
margin-right: 8px;
}
</style>