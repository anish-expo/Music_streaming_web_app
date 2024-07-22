//Frontend/src/components/Home.vue

<template>
    <div> 
      <!-- Display Album -->
      <div>
        <h2 style="color:  rgb(69, 7, 128); text-align: right; margin-right: 700px; ">Albums</h2>
        <div class="Album-container">
        <div v-for="album in albums" :key="album.id" class="album-item">
            <p class="album-name">{{ album.name }}</p>
            <img :src="getImageUrlsong(album.image)" :alt="album.name" class="album-image">
            
            <router-link to="/login" class="btn album-button">View Album</router-link>
        </div>
      </div>
    </div>
      
      <!-- Display song -->
      <div>
        <h2 style="color:  rgb(69, 7, 128); text-align: right; margin-right: 700px; ">Songs</h2>
        <div v-for="song in songs" :key="song.id">
          <div class="song-details">
                  <p><strong>Title:</strong> {{ song.title }}</p>
                  <p><strong>Views:</strong> {{ song.play_count }}</p>
                  <p><strong>Rating:</strong> {{ song.average_rating }}</p>
                  <button @click="playSong(song)">
                        {{ isPlaying && currentSong === song ? 'Pause' : 'Play' }}
                      </button>
                </div>
          
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'HomePage',
    data() {
      return {
        songs: [],
        albums: [],
        isPlaying: false,
        currentSong:null,
        
      };
    },
    created() {
      this.fetchSongsAndAlbums();
    },

    methods: {
    
    fetchSongsAndAlbums() {
      axios.get('http://127.0.0.1:5000/home') 
        .then(response => {
          this.songs = response.data.allsong;
          this.albums = response.data.allalbum;
        })
        .catch(error => {
          console.error('Error fetching songs and albums:', error);
        });
    },
    getImageUrlsong(filename) {
      if (!filename) {
        return '';
      }
      
      // const correctedFilename = filename.replace(/\\/g, '/');
      const extractedFilename = filename.split('\\').pop();
      const imageUrl = `http://127.0.0.1:5000/showsong/${extractedFilename}`;
    
      return imageUrl;
    },
    playSong(song) {
            const songId = song.id;
            const filename = song.songfile;
            const extractedFilename = filename.split('\\').pop();
            const audioSource = `http://127.0.0.1:5000/playsong/${songId}/${extractedFilename}`;

            if (this.audio && !this.audio.paused) {
              this.audio.pause();
              this.isPlaying = false; 
            } else {
              this.audio = new Audio(audioSource);
              this.audio.play();
              this.currentSong = song;
              this.isPlaying = true; 
            }
          },
          pauseSong() {
          if (this.audio && !this.audio.paused) {
            this.audio.pause();
            this.isPlaying = false; 
          }
        },
  }
  };
  </script>
  
  <style>
  .Album-container {
    display: grid;
    grid-template-columns: repeat(5, 1fr); /* Adjust the number of columns as needed */
    gap: 5px; /* Adjust the gap between items as needed */
  }
  .album-item {
    text-align: center;
    border: 0px solid #ccc;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .album-name {
    font-weight: bold;
    color: rgb(192, 25, 158);
  }
 .album-image {
    max-width: 150px; /* Adjust the maximum width as needed */
    height: 100px; /* Maintain aspect ratio */
  }
  .album-button {
    margin-top: 10px; /* Add margin to create space between the image and button */
    background-color: rgb(18, 124, 112) !important;
    color: white !important;
  }
  </style>
  