//src/components/EditAlbum.vue

<template>
    <div class="editAlbum">
        <h2>Edit Album</h2>
      <form @submit.prevent="editalbum">
        <div class="form-group">
          <label for="name">Album Name:</label>
          <input type="text" id="name" v-model="name" placeholder="Name" required>
        </div>
        <div class="form-group">
          <label for="artist">Artist:</label>
          <input type="text" id="artist" v-model="artist" placeholder="Artist" required>
        </div>
        <div class="form-group">
          <label for="genre">Genre:</label>
          <input type="text" id="genre" v-model="genre" placeholder="Genre" required>
        </div>
        <div class="form-group">
          <label for="image">Album Image:(optional)</label>
          <input type="file" id="image" @change="handleImageUpload" accept="image/*" >
          
        </div>
        <button type="submit" :disabled="!isFormValid" :style="{ 'background-color': isFormValid ? 'blue' : 'white' }">Edit</button>
      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>

<script>
import axios from 'axios';
import { refreshAccessToken } from '@/service/refresh_token';
export default{
   
    data() {
      return {
        name: '',
        artist: '',
        genre: '',
        image: null,
        message: ''
      };
    },

    created() {
        
        const albumId = this.$route.params.albumId;
        this.fetchAlbumDetails(albumId);
    },
    computed: {
        isFormValid() {
        return (
          this.name &&
          this.artist &&
          this.genre 
          
        );
      }
      },
    methods:{
        fetchAlbumDetails(albumId){
            const  accessToken = localStorage.getItem('access_token');
            axios.get(`http://127.0.0.1:5000/edit_album/${albumId}`, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`
                    }
                })
                .then(response => {
                    const albumData = response.data;
                    this.name = albumData.name;
                    this.artist = albumData.artist;
                    this.genre = albumData.genre;
                    
                    
                })
                .catch(error => {
                    console.error('Error fetching song details:', error);
                });

        },
        async editalbum(){
            try {
          const formData = new FormData();
          formData.append('name', this.capitalizeFirstLetter(this.name));
          formData.append('artist',this.artist);
          formData.append('genre',this.genre);
          formData.append('image', this.image);

          const albumId = this.$route.params.albumId;
          const  accessToken = localStorage.getItem('access_token');
          const response = await axios.post(`http://127.0.0.1:5000/edit_album/${albumId}`, formData, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
                'Content-Type': 'multipart/form-data'
            }});
            // console.log(response)
          if (response.status === 200) {
            this.message = response.data.message; 
            const responseData = response.data.message;
            if(responseData === "album edited successfully"){
              const username = localStorage.getItem('username');
              this.$router.push({ name: 'CreatorDashboard', params: { username } });
            // this.$router.push({ name: 'CreatorDashboard' });
            }
        }
        } catch (error) {
            if (error.response && error.response.status === 401) {
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              throw new Error('Refresh token not found in local storage');
            }
            await refreshAccessToken(refreshToken); // Pass the refreshToken to the function
            
            await this.editalbum(); // Retry fetching the data
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            // Handle refresh token error
          }
        }
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
    }
}
</script>
<style scoped>
.editAlbum {
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
</style>