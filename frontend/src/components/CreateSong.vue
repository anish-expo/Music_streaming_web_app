//src/components/CreateSong.vue

<template>
    <div class="createsong">
      <h2>CreateSong</h2>
      <form @submit.prevent="createSong">
        <div class="form-group">
          <label for="title">Title:</label>
          <input type="text" id="title" v-model="title" placeholder="Title" required>
        </div>

        <div class="form-group">
          <label for="artist">Artist:</label>
          <input type="artist" id="artist" v-model="artist" placeholder="Artist" required>
        </div>
        
        <div class="form-group">
          <label for="genre">Genre:</label>
          <input type="text" id="genre" v-model="genre" placeholder="Genre" required>
        </div>

        <div class="form-group">
          <label for="lyrics">Lyrics:</label>
          <textarea id="lyrics" v-model="lyrics" placeholder="Lyrics"  required rows="6"  style= "width: 100%;" ></textarea>
        </div>

       
        <div class="form-group">
          <label for="album">Album:</label>
          <select id="album" v-model="selectedAlbum" @change="onAlbumChange" required>
            <option value="" disabled>Select an album</option>
            <option v-for="album in albums" :key="album.id" :value="album">{{ album.name }}</option>
            <option value="new">New Album</option>
        </select>
          <input v-if="selectedAlbum === 'new'" type="text" v-model="newalbum" placeholder="Enter new album name" required>
        </div>



        <div class="form-group">
          <label for="file">Song File:</label>
          <input type="file" id="file" @change="handleFileUpload" accept=".mp3" >
          <span v-if="!file" class="error-message">No file selected</span>
        </div>
        <!-- <button type="submit" :disabled="!isFormValid">Signup</button> -->
        <button type="submit" :disabled="!isFormValid" :style="{ 'background-color': isFormValid ? 'blue' : 'white' }">AddSong</button>

      </form>
      <p v-if="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { refreshAccessToken } from '@/service/refresh_token';
  
  export default {
    data() {
      return {
        title: '',
        artist: '',
        genre: '',
        album: '',
        lyrics:'',
        newalbum:'',
        selectedAlbum: '', 
        isNewAlbum: false, 
        file:null, 
        albums: [],
        
        message: ''
      };
    },
    async created() {
        // Retrieve the albums from local storage
        const storedAlbums = localStorage.getItem('albums');
        if (storedAlbums) {
          this.albums = JSON.parse(storedAlbums);
        }

      },
    
      computed: {
    isFormValid() {
      if (this.isNewAlbum) {
        // Validate for a new album
        return (
          this.title &&
          this.artist &&
          this.genre &&
          this.lyrics &&
          this.newalbum &&
          this.file
        );
      } else {
        // Validate for an existing album
        return (
          this.title &&
          this.artist &&
          this.genre &&
          this.selectedAlbum &&
          this.lyrics &&
          this.file
        );
      }
    }
  },

    methods: {
      async createSong() {
        try {
          const encodedLyrics = encodeURIComponent(this.lyrics);
          let albumName;
          if (this.selectedAlbum === 'new') {
              albumName = this.newalbum;
            } else {
              albumName = this.selectedAlbum.name;
            }

          const formData = new FormData();
          formData.append('title', this.capitalizeFirstLetter(this.title));
          formData.append('artist',this.artist);
          formData.append('genre',this.genre);
          formData.append('album',albumName);
          formData.append('lyrics',encodedLyrics);
          
          formData.append('file', this.file);
         
       
          const  accessToken = localStorage.getItem('access_token');
          const response = await axios.post('http://127.0.0.1:5000//create-song', formData, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'multipart/form-data'
            }});
            // console.log(response)
            if (response.status === 200) {
            this.message = response.data.message; 
            const responseData = response.data.message;
            if(responseData === "Song created successfully"){
              const username = localStorage.getItem('username');
              this.$router.push({ name: 'CreatorDashboard', params: { username } });
            // this.$router.push({ name: 'CreatorDashboard' });
            }
        }
        }  catch (error) {
            if (error.response && error.response.status === 401) {
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              throw new Error('Refresh token not found in local storage');
            }
            await refreshAccessToken(refreshToken); // Pass the refreshToken to the function
            
            await this.createSong(); 
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
      handleFileUpload(event) {
        
        const file = event.target.files[0];
        if (file) {
        this.file = file;
      }
      },
      capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
      },
    onAlbumChange() {
        
      this.isNewAlbum = this.selectedAlbum === 'new';
      // console.log('Selected Album:', this.selectedAlbum);
      // console.log('isNewAlbum:', this.isNewAlbum);
    }
  }

  };
  </script>
  
  <style scoped>
  .createsong {
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