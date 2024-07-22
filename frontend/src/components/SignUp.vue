//src/components/SignUp.vue

<template>
    <div class="signup">
      <h2>Signup</h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="name" placeholder="Name" required>
          
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" placeholder="Email" required>

          <span v-if="!validEmail && email !== ''"  class="error-message">Invalid email format</span>
          <span v-else-if="validEmail" class="success-message">Valid email format</span>
          
        </div>
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="username" placeholder="Username" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" placeholder="Password" required>
          <span v-if="!passwordsMatch && confirmPassword !== ''" class="error-message">Passwords must match</span>
          <span v-if="!passwordLengthValid && password !== ''" class="error-message">Password must be at least 6 characters long</span>
        </div>
        <div class="form-group">
          <label for="confirmPassword">Confirm Password:</label>
          <input type="password" id="confirmPassword" v-model="confirmPassword" placeholder="Confirm Password" required>
        </div>
        <div class="form-group">
          <label for="role">Role:</label>
          <select id="role" v-model="role" required>
            <option value="User">User</option>
            <option value="Creator">Creator</option>
          </select>
        </div>
        <div class="form-group">
          <label for="image">Profile Image:</label>
          <input type="file" id="image" @change="handleImageUpload" accept="image/*" >
          <span v-if="!image" class="error-message">No image selected</span>
        </div>
        <!-- <button type="submit" :disabled="!isFormValid">Signup</button> -->
        <button type="submit" :disabled="!isFormValid" :style="{ 'background-color': isFormValid ? 'blue' : 'white' }">Signup</button>

      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        name: '',
        email: '',
        username: '',
        password: '',
        confirmPassword: '',
        image: null,
        role: 'User',
        message: ''
      };
    },
    methods: {
      async submitForm() {
        try {
          const formData = new FormData();
          formData.append('name', this.capitalizeFirstLetter(this.name));
          formData.append('email',this.email);
          formData.append('username',this.username);
          formData.append('password1',this.password);
          formData.append('password2',this.confirmPassword);
          formData.append('role_name',this.role);
          formData.append('image', this.image);
         
       
          
          const response = await axios.post('http://127.0.0.1:5000/signup', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }});
            // console.log(response)
          if (response.status === 200) {
            this.message = response.data.message; 
            const responseData = response.data.message;
            if(responseData === "User created successfully"){
            this.$router.push({ name: 'LogIn' });
            }
        }
        } catch (error) {
          if (error.response && error.response.data) {
            this.message = error.response.data.message; 
        } 
        }
      },
      handleImageUpload(event) {
        const file = event.target.files[0];
        if (file) {
        this.image = file;
      }
      },
      capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
      }
    },
    computed: {
      passwordsMatch() {
        return this.password === this.confirmPassword;
      },
      passwordLengthValid() {
        return this.password.length >= 6;
      },
      validEmail() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValid = emailRegex.test(this.email);
        // console.log('Is email valid:', isValid);
        return isValid;
      },
      isFormValid() {
        return (
          this.name &&
          this.email &&
          this.username &&
          this.password &&
          this.confirmPassword &&
          this.image &&
          this.passwordsMatch &&
          this.passwordLengthValid &&
          this.validEmail
        );
      }
    }
  };
  </script>
  
  <style scoped>
  .signup {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .label {
    display: block;
  }
  
  .error-message {
    color: red;
}
  
  .success-message {
    color: green;
  }
  </style>