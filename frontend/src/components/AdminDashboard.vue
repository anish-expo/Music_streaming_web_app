//src/component/AdminDashbord.vue

<template>
    <div class="admin-dashboard">
    <!-- Creator Profile -->
          <div class="admin-profile">
            <div class="profile-info">
              <h1>{{ capitalizeFirstLetter(admin.username) }}</h1>
              <!-- <img :src="require('@/assets/logo.png')" alt="Creator Profile Picture" /> -->
              <img class="image" :src="getImageUrl(admin.image)"/>
              <!-- <button @click="toggleDetails">{{ showDetails ? 'Hide Details' : 'View Details' }}</button> -->
              <button @click="toggleDetails">&#9660;</button>       
              
            </div>         
          </div>

           <!-- Search Section -->
              <div class="search-section">
                <div class="container" style="display: flex; justify-content: space-between; margin: 100px;">
                <div class="input-group mb-3" style="width: 1100px;">
                <div class="input-group">
                  <select class="form-control" v-model="searchType" name="search_type">
                    <option value="song">Search for Song</option>
                    <option value="album">Search for Album</option>
                    <option value="artists">Search for Artists</option>
                    <option value="genre ">Search for Genre</option>
                    <option value="songrating">Search for Song rating</option>
                    <option value="albumrating">Search for Album rating </option>
                </select>
                  <input type="text" class="form-control" v-model="searchQuery" placeholder="Search songs and albums" name="search_query">
                  <div class="input-group-append">
                    <button class="btn btn-primary" type="button" @click="search">Search</button>
                  </div>
                  </div>
                </div>
            </div>
        </div>

        <p v-if="message">{{ message }}</p>
        <!-- details  -->
                    <div v-if="showDetails" class="admin-details">
                        <div>
                          <p> Welcome to Admin Dashboard, {{ admin.username }}</p>
                          <button @click="toggleDetails1">{{ showDetails1 ? 'Hide Details' : 'View Details' }}</button>
                          
                              <div v-if="showDetails1" class="user-details">
                                    <p>Name: {{ admin.name }}</p>
                                    <p>Email: {{ admin.email }}</p>
                                    <p>Total Users(excluding Admin): {{ totalUsers }}</p>
                                    <p>Total Normal Users: {{ totalnormalUsers }}</p>
                                    <p>Total Creators: {{ totalCreators }}</p>
                                    <p> Total Albums: {{ totalAlbums }}</p>
                                    <p> Total Songs: {{ totalSong }}</p>
                              </div>
                      </div>
                        <div><button @click="logout">Logout</button></div>

                      </div>
<!-- search result   -->
                        <div v-if="searchResults.length > 0">
                          <h2>Search Resut</h2>
                          <div v-if="searchType === 'song' || searchType === 'artists' || searchType === 'genre' || searchType === 'songrating'">
                            <h2>Songs</h2>
                            <tbody>
                              <tr v-for="song in searchResults" :key="song.id">
                                <td>{{ song.title }}</td>
                                <td>{{ song.album }}</td>
                                <td>
                                  <button @click="toggleDetailssearch(song)"> Details</button>
                                  <!-- <button @click="playSong(song)">Play</button> -->
                                </td>
                                <!-- <button @click="playSong(song)">Play</button> -->
                                    <button @click="playSong(song)" v-if="song">
                                      {{ isPlaying && currentSong === song ? 'Pause' : 'Play' }}
                                    </button>
                              </tr>
                              <tr v-if="selectedSongsearch "> <!-- Only show details if selectedSong is the same as the current song -->
                                <td colspan="5">
                                  <div>
                                    <p><strong>Title:</strong> {{ selectedSongsearch.title }}</p>
                                    <p><strong>Album:</strong> {{ selectedSongsearch.album }}</p>
                                    <p><strong>Artist:</strong> {{ selectedSongsearch.artist }}</p>
                                    <p><strong>Genre:</strong> {{ selectedSongsearch.genre }}</p>
                                    <p><strong>Lyrics:</strong> {{ decodeURIComponent(selectedSongsearch.lyrics) }}</p>
                                  </div>
                                </td>
                              </tr>
                            </tbody>

                          </div>
                          <div v-if="searchType== 'album' ||  searchType =='albumrating'">
                            <div>
                            <h2 style="color:  rgb(69, 7, 128); text-align: right; margin-right: 700px; ">Albums</h2>
                            <div class="Album-container">
                            <div v-for="album in searchResults" :key="album.id" class="album-item">
                                <p class="album-name">{{ album.name }}</p>
                                <img :src="getImageUrlsong(album.image)" :alt="album.name" class="album-image">
                                <button @click="viewSongssearch(album)">View Songs</button>

                            </div>
                          </div>
                        </div>
                                          
                      
                        <div v-if="(selectedAlbumgen && albumsongssearch) || refreshNeeded2 || removedsongfromalbum">
                              <h2> This is {{ selectedAlbumgen.name }}</h2>
                              <table>
                                <thead>
                                  <tr>
                                    <th>Song Title</th>
                                    
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="song in selectedAlbumgen.songs" :key="song.id">
                                    <td>{{ song.title }}</td>
                                    <td><button @click="playSong(song)">
                                              {{ isPlaying && currentSong === song ? 'Pause' : 'Play' }}
                                            </button></td>
                                                  
                                  </tr>
                                  
                                </tbody>
                                                        
                              </table>
                            </div>

                          </div>
                        
                        </div>
                        
                            <!-- button for admin  -->
                                                    <div class = 'working-button'>
                                                <div class="container1" style="display: flex;  margin: 80px;">
                                                  <button @click="fetchPlaylist">My Playlist</button>
                                                  <button @click="fetchAlbums">All Albums</button>
                                                  <button @click="fetchSongs">All Songs</button>
                                                  
                                                          
                                                </div>

                                              </div>


                                              <!-- playlist -->

                              <div v-if="showPlaylists || refreshNeeded1">
                                <h2>Your Playlists</h2>
                                <div v-if="showCreateForm">
                                <label for="playlistName">Playlist Name:</label>
                                <input type="text" v-model="playlistName" id="playlistName">
                                <label for="playlistDescription">Playlist Description:</label>
                                <input type="text" v-model="playlistDescription" id="playlistDescription">
                                <button @click="submitPlaylist">Submit</button>
                                <button @click="cancelCreate">Cancel</button>
                              </div>
                              <button @click="toggleCreateForm" v-else>Create Playlist</button>

                            <div v-if="playlists.length > 0">
                              <table>
                                <thead>
                                  <tr>
                                    <th>Playlist Name</th>
                                    
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="playlist in playlists" :key="playlist.id">
                                    <td>{{ playlist.name }}</td>
                                    <td><button @click="viewSongsPlaylist(playlist)">View Songs</button></td>
                                    <td><button @click="confirmDelete(playlist,'playlist')">Remove</button></td>
                                  </tr>
                                </tbody>
                              </table>
                            </div>

                            <div v-else>
                              No playlists exist.
                            </div>
                            <div v-if="(selectedPlaylist && playlistsong) ">
                            <h2> This is {{ selectedPlaylist.name }}</h2>
                            <table>
                              <thead>
                                <tr>
                                  <th>Song Title</th>
                                  
                                </tr>
                              </thead>
                              <tbody>
                                <tr v-for="song in selectedPlaylist.songs" :key="song.id">
                                  <td>{{ song.title }}</td>
                                  <td>Rating:{{ song.average_rating }}</td>
                                  <td><button @click="playSong(song)">
                                            {{ isPlaying && currentSong === song ? 'Pause' : 'Play' }}
                                          </button></td>
                                      <td><button @click="removeFromPlaylist(song)">Remove From Playlist</button></td>
                                            
                                </tr>
                              </tbody>
                            </table>
                            </div>
                              </div> 
           <!-- show all albums                     -->

           <div v-if=" showalbum">
        <h2 style="color:  rgb(69, 7, 128); text-align: right; margin-right: 700px; ">Albums</h2>
        <div class="Album-container">
        <div v-for="album in albums" :key="album.id" class="album-item">
            <p class="album-name">{{ album.name }}</p>
            <img :src="getImageUrlsong(album.image)" :alt="album.name" class="album-image">
            <p class="album-name">Rating:{{ album.average_rating }}</p>
            <button @click="viewSongsgen(album)">View Songs</button>
            <td><button @click="confirmDelete(album,'album')">Remove</button></td>
            <button @click="toggleFlag(album)">{{ album.flagged ? 'Flagged' : 'Unflagged' }}</button>
   
        </div>
      </div>
    </div>
            
    <div v-if="(selectedAlbumgen && albumsongs) ">
          <h2> This is {{ selectedAlbumgen.name }}</h2>
          <table>
            <thead>
              <tr>
                <th>Song Title</th>
                
              </tr>
            </thead>
            <tbody>
              <tr v-for="song in selectedAlbumgen.songs" :key="song.id">
                <td>{{ song.title }}</td>
                <td>Rating:{{ song.average_rating }}</td>
                <td><button @click="playSong(song)">
                          {{ isPlaying && currentSong === song ? 'Pause' : 'Play' }}
                        </button></td>
                        <td><button @click="confirmDelete(song, 'song')">Remove song</button></td>
                        <button @click="toggleFlag1(song)">{{ song.flagged ? 'Flagged' : 'Unflagged' }}</button>
                    <td><button @click="togglePlaylistSelection">Add to Playlist</button>
                        <div v-if="showPlaylistSelection">
                          <select id="playlist" v-model="selectedPlaylist" required>
                            <option value="" disabled>Select a playlist</option>
                            <option v-for="playlist in playlists" :key="playlist.id" :value="playlist">{{ playlist.name }}</option>
                            <option value="new">New Playlist</option>
                          </select>
                          <!-- <input v-model="newPlaylistName" type="text" placeholder="New Playlist Name"> -->
                          <input v-if="selectedPlaylist === 'new'" v-model="newPlaylistName" type="text" placeholder="New Playlist Name">
                          <button @click="addToPlaylist(song)">Add</button>
                        </div></td>
                      
              </tr>
              
            </tbody>
                                    
          </table>
        </div>

        <!-- Songs  -->
        <div v-if="showsong" >
          <h2 style="color:  rgb(69, 7, 128); text-align: right; margin-right: 700px; ">Songs</h2>
            <ul class="songs-list">
              <li v-for="song in songs" :key="song.id" class="song-item">
                <!-- Display song details -->
                <div class="song-details">
                  <p><strong>Title:</strong> {{ song.title }}</p>
                  <p><strong>Artist:</strong> {{ song.artist }}</p>
                  <p><strong>Rating:</strong> {{ song.average_rating }}</p>
                  <p><strong>Duration:</strong> {{ song.duration }}</p>
                  <p><strong>Flagged:</strong> {{ song.flagged }}</p>
                  
                </div>
                <!-- Play button -->
                <td><button class="play-button" @click="playSong(song)">Play</button>
                <button @click="toggleDetails3(song)"> Details</button></td>
                <button @click="confirmDelete(song, 'song')">Remove song</button>
                <button @click="toggleFlag1(song)">{{ song.flagged ? 'Flagged' : 'Unflagged' }}</button>
                
                <!-- <button class="play-button" style="background-color: blueviolet;" @click="AddToPlaylist(song)">AddToPlaylist</button> -->
                <button @click="togglePlaylistSelection(song)">Add to Playlist</button>

                

              </li>
              <div v-if="showPlaylistSelection && nowsong">
                        <select id="playlist" v-model="selectedPlaylist" required>
                          <option value="" disabled>Select a playlist</option>
                          <option v-for="playlist in playlists" :key="playlist.id" :value="playlist">{{ playlist.name }}</option>
                          <option value="new">New Playlist</option>
                        </select>
                        <!-- <input v-model="newPlaylistName" type="text" placeholder="New Playlist Name"> -->
                        <input v-if="selectedPlaylist === 'new'" v-model="newPlaylistName" type="text" placeholder="New Playlist Name">
                        <button @click="addToPlaylist(nowsong)">Add</button>
                      </div>
                      
            </ul>
            <tr v-if="selectedSong3 "> <!-- Only show details if selectedSong is the same as the current song -->
          <td colspan="5">
            <div>
              <p><strong>Title:</strong> {{ selectedSong3.title }}</p>
              <p><strong>Rating:</strong> {{ selectedSong3.average_rating }}</p>
              <p><strong>Album:</strong> {{ selectedSong3.album }}</p>
              <p><strong>Artist:</strong> {{ selectedSong3.artist }}</p>
              <p><strong>Genre:</strong> {{ selectedSong3.genre }}</p>
              <p><strong>Lyrics:</strong> {{ decodeURIComponent(selectedSong3.lyrics) }}</p>
            </div>
          </td>
        </tr>
               
        </div>






        </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { refreshAccessToken } from '@/service/refresh_token';
  
  export default {
    name: 'AdminDashboard',
    data() {
      return {
        message:'',
        admin: {},
        totalUsers: 0,
        totalnormalUsers:0,
        totalCreators: 0,
        totalAlbums: 0,
        totalSong:0,
        showDetails:false,
        showDetails1:false,
        searchQuery: '',
        searchType: 'song',
        searchResults:[],
        selectedSongsearch:null,
        isPlaying: false,
        currentSong:null,
        albumsongssearch:false,
        selectedAlbumgen:null,
        playlists: [],
        showPlaylists: false,
        refreshNeeded1:false,
        showCreateForm: false,
        newPlaylistName:'',
        playlistName: '',
        playlistDescription: '',
        selectedPlaylist: null,
        playlistsong: false,
        albums: [] ,
        albumsongs: false,
        showPlaylistSelection: false,
        songs:[],
        selectedSong3:null,
        showsong: false,
        showalbum:false,


        
      };
    },
    mounted() {
      this.fetchDashboardData();
    },
    methods: {
      async fetchDashboardData() { 
      try {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
          throw new Error('Access token not found in local storage');
        }
        const headers = {
          Authorization: `Bearer ${accessToken}`
        };
        const url = `http://127.0.0.1:5000/admin_dashboard/${this.$route.params.username}`;

        const response = await axios.get(url, { headers }); // Wait for the response

        const data = response.data;
        this.message = data.message;
        this.admin = response.data.user;
        this.totalUsers = data.total_users;
        this.totalnormalUsers =data.total_normal_user;
        this.totalCreators = data.total_creators;
        this.totalAlbums = data.total_albums;
        this.totalSong = data.total_song;

        // console.log("Dashboard data:", data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        if (error.response && error.response.status === 401) {
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              throw new Error('Refresh token not found in local storage');
            }
            await refreshAccessToken(refreshToken); // Pass the refreshToken to the function
            
            await this.fetchDashboardData(); // Retry fetching the data
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            // Handle refresh token error
          }
        }
      }
    },
    async toggleFlag(album) {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch(`http://127.0.0.1:5000/flag-album/${album.id}`, {
          method: 'PUT',
          headers: {
            
            Authorization: `Bearer ${accessToken}`  // Add your JWT token or any other authorization mechanism
          }
        });
        if (response.ok) {
          // Update the flag status in the UI
          album.flagged = !album.flagged;
        } else {
          console.error('Failed to toggle flag');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async toggleFlag1(song) {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch(`http://127.0.0.1:5000/flag-song/${song.id}`, {
          method: 'PUT',
          headers: {
            
            Authorization: `Bearer ${accessToken}`  // Add your JWT token or any other authorization mechanism
          }
        });
        if (response.ok) {
          // Update the flag status in the UI
          song.flagged = !song.flagged;
        } else {
          console.error('Failed to toggle flag');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
    toggleDetails3(song) {
          
          this.selectedSong3 = this.selectedSong3 === song ? null : song;
          // console.log('song ddetail',this.selectedSong)
          },
    async removeAlbum(album) {
        try {
            const response = await axios.delete(`http://127.0.0.1:5000/remove_album/${album.id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            if (response.status === 200) {
              const index = this.albums.findIndex(a => a.id === album.id);
              if (index !== -1) {
                this.albums.splice(index, 1);
                this.refreshNeeded1 = true;
              }
            }
        } catch (error) {
            console.error('Error removing album:', error);
            if (error.response && error.response.status === 401) {
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              throw new Error('Refresh token not found in local storage');
            }
            await refreshAccessToken(refreshToken); // Pass the refreshToken to the function
            
            await this.fetchCreatorDashboard(); // Retry fetching the data
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            // Handle refresh token error
          }
        }
        }
    },
    async removeSong(song) {
        try {
            const response = await axios.delete(`http://127.0.0.1:5000/delete-song/${song.id}`, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem('access_token')}`
                }
            });
            if (response.status === 200) {
              this.message = response.data.message;
            }
        } catch (error) {
            console.error('Error removing album:', error);
            if (error.response && error.response.status === 401) {
          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              throw new Error('Refresh token not found in local storage');
            }
            await refreshAccessToken(refreshToken); 
            
            await this.removeSong(song); 
          } catch (refreshError) {
            console.error('Error refreshing access token:', refreshError);
            // Handle refresh token error
          }
        }
        }
    },
    togglePlaylistSelection(song) {
          this.nowsong = song;
          this.showPlaylistSelection = !this.showPlaylistSelection;
        },
    async viewSongsgen(album) {
        this.albumsongs= !this.albumsongs;
          if (this.albumsongs){
        try { 
          const  accessToken = localStorage.getItem('access_token');
          const response = await axios.get(`http://127.0.0.1:5000/get_album_song_admin/${album.id}`, {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }});
            // console.log('fetch album song:',response.data.songs)

          this.selectedAlbumgen = {
            ...album,
            songs: response.data.songs  
          };
        } catch (error) {
          console.error('Error fetching songs:', error);
        }
          }
      },
    async fetchAlbums() {
      try {
        const  accessToken = localStorage.getItem('access_token');
        const response = await axios.get(`http://127.0.0.1:5000/allalbum`,{
            headers: {
                Authorization: `Bearer ${accessToken}`
            }});

        this.albums = response.data.allalbum;
        this.showalbum = !this.showalbum;
        // console.log(this.albums)
      } catch (error) {
        console.error('Error fetching albums:', error);
      }
    },
    async fetchSongs() {
      try {
        const  accessToken = localStorage.getItem('access_token');
        const response = await axios.get(`http://127.0.0.1:5000/allsong`,{
            headers: {
                Authorization: `Bearer ${accessToken}`
            }});

        this.songs = response.data.allsong;
        // console.log(this.songs)
        this.showsong = !this.showsong;
      } catch (error) {
        console.error('Error fetching albums:', error);
      }
    },
    addToPlaylist(song) {
                const newPlaylistName1 = this.newPlaylistName;
                const songId = song.id;
                console.log(song);
                const playlistId = this.selectedPlaylist.id;
              
              const accessToken = localStorage.getItem('access_token');
              axios.post(`http://127.0.0.1:5000/add_to_playlist`, {
                song_id: songId, 
                playlist_id: playlistId,
                new_playlist_name: newPlaylistName1
              },
              {
              headers: {
                Authorization: `Bearer ${accessToken}`
              }
            }).then(response => {
                console.log(response.data.message);
                // Handle success, if needed
              })
              .catch(error => {
                console.error('Failed to add song to playlist:', error);
                // Handle error, if needed
              })
              .finally(() => {
                // Reset the state
                this.selectedPlaylist = null;
                this.newPlaylistName = '';
                this.showPlaylistSelection = false;
              });
            }, 
    confirmDelete(item,type) {
      let itemName;
      if (type === 'album') {
        itemName = item.name;
      } else if (type === 'song') {
        itemName = item.title;
      } else if (type === 'playlist') {
          itemName = item.name;
        }
      const confirmMessage = `Are you sure you want to delete the ${type} "${itemName}"?`;
      if (confirm(confirmMessage)) {
        if (type === 'album') {
          this.removeAlbum(item);
        } else if (type === 'song') {
          this.removeSong(item);
        } else if (type === 'playlist') {
          this.removePlaylist(item);
        }
      }
    },
    async removeFromPlaylist(song) {
        try {
          const response = await axios.delete(`http://127.0.0.1:5000/remove-song-from-playlist/${song.id}/${this.selectedPlaylist.id}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
          });
          if (response.status === 200) {
            this.removedsongfrmplaylist=true;
            this.message = response.data.message;
          }
        } catch (error) {
          console.error('Error removing song from album:', error);
          
        }
      },
    async viewSongsPlaylist(playlist) {
        this.playlistsong= !this.playlistsong;
          if (this.playlistsong){
        try { 
          const  accessToken = localStorage.getItem('access_token');
          const response = await axios.get(`http://127.0.0.1:5000/get_playlist_song/${playlist.id}`, {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }});
            console.log('fetch playlist song:',response.data.songs)

          this.selectedPlaylist = {
            ...playlist,
            songs: response.data.songs  
          };
        } catch (error) {
          console.error('Error fetching songs:', error);
        }
          }
      },
    toggleCreateForm() {
            this.showCreateForm = !this.showCreateForm;
            },
            async submitPlaylist() {
        try {
          const accessToken = localStorage.getItem('access_token');
          const response = await axios.post(
            'http://127.0.0.1:5000/create_playlist',
            {
              name: this.playlistName,
              description: this.playlistDescription
            },
            {
              headers: {
                Authorization: `Bearer ${accessToken}`
              }
            }
          );
          // console.log('Playlist created successfully:', response.data);
          this.message = response.data.message;
          this.showCreateForm = false; 
          this.playlistName = ''; 
          this.playlistDescription = ''; 
          this.fetchPlaylist();
        } catch (error) {
          console.error('Error creating playlist:', error);
          // Optionally, you can show an error message to the user.
        }
      },
      cancelCreate() {
        this.showCreateForm = false;
        this.playlistName = '';
        this.playlistDescription = '';
      },
    async fetchPlaylist(){
      try {
            const accessToken = localStorage.getItem('access_token');
            const response = await axios.get('http://127.0.0.1:5000/getplaylists', {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }
            });

            this.playlists = response.data.playlists;
            // console.log('playlist:',response)
        } catch (error) {
            console.error('Error fetching playlists:', error);
        }

      this.showPlaylists = !this.showPlaylists;
    
    },
    async viewSongssearch(album) {
            this.albumsongssearch= !this.albumsongssearch;
              if (this.albumsongssearch){
            try { 
              const  accessToken = localStorage.getItem('access_token');
              const response = await axios.get(`http://127.0.0.1:5000/get_album_song/${album.id}`, {
                headers: {
                    Authorization: `Bearer ${accessToken}`
                }});
                // console.log('fetch album song:',response.data.songs)

              this.selectedAlbumgen = {
                ...album,
                songs: response.data.songs  
              };
            } catch (error) {
              console.error('Error fetching songs:', error);
            }
              }
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
    toggleDetailssearch(song) {
          
          this.selectedSongsearch = this.selectedSongsearch === song ? null : song;
          // console.log('song ddetail',this.selectedSong)
          },
    toggleDetails1() {
        this.showDetails1 = !this.showDetails1;
      },
    capitalizeFirstLetter(str) {
      if (!str) return ''; // Check if str is falsy, return empty string
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
    getImageUrl(filename) {
      if (!filename) {
        return '';
      }
      
      // const correctedFilename = filename.replace(/\\/g, '/');
      const extractedFilename = filename.split('\\').pop();
      const imageUrl = `http://127.0.0.1:5000/show/${extractedFilename}`;
    
      return imageUrl;
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
    toggleDetails() {
      this.showDetails = !this.showDetails;
    },
    async search() {
          try {
            const response = await axios.post(`http://127.0.0.1:5000/search`, {
                                                        searchType: this.searchType,
                                                        searchQuery: this.searchQuery
                                                      },{
                                                        headers: {
                                                          Authorization: `Bearer ${localStorage.getItem('access_token')}`
                                                        }});
            
            if (response.status === 200) {
              // Assuming the backend returns search results in the response data
              this.searchResults = response.data.results;
              this.message=response.data.message;
              // console.log('Search results:', this.searchResults);
            } else {
              console.error('Failed to fetch search results');
            }
          } catch (error) {
            console.error('Error searching:', error);
          }
        },
    async logout(){
      try{
        await axios.get('http://127.0.0.1:5000/logout', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');

        this.$router.push('/admin-login');
        // router.push('/login');
      }catch (error){
        console.error('Error logging out:', error);
      }
    }
  }
  };
  </script>

  
  <style scoped>
  .admin-dashboard {
    overflow-y: auto; 
    max-height: 100vh; 
    padding: 20px; 
  }
  
    .add-buttons button {
    margin-right: 10px; 
  }
   
    
    .profile-info {
      display: flex;
      flex-direction: column;
      align-items: first baseline;
      margin-left: 10px;
      margin-bottom: 10px;
      
    }
  
  
    
    
    /* Styles for the search section */
    .search-section {
      position: absolute;
      top: 5%;
      margin-left: 200px;
      /* transform: translateY(-50%); */
    }
    
    /* Your existing styles */
     .admin-details {
      margin-top: 20px;
      margin-left: 10px;
      margin-inline: 0px;
    } 
    
    .search-section {
      display: flex;
      align-items: center;
      margin-bottom: 20px;
    }
    .add-buttons {
    display: flex;
    
    margin-left: 400px;
  }
  .image {
    width: 100px;
      height: auto; /* Maintain the aspect ratio */
  }
  
  .songs-container {
    overflow-x: auto; /* Enable horizontal scrolling */
    white-space: nowrap; /* Prevent line breaks */
  }
  
  .songs-list {
    list-style-type: none; /* Remove bullet points */
    padding: 0;
    margin: 0;
  }
  
  .song-item {
    display: inline-block; /* Display songs horizontally */
    margin-right: 20px; /* Add space between songs */
  }
  
  .song-details {
    margin-bottom: 10px; /* Add space between song details */
  }
  
  .play-button {
    background-color: #4caf50; /* Green */
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin-top: 10px;
    cursor: pointer;
  }
  </style>
  