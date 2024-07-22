// src/service/refresh_token.js

import axios from 'axios';

// Function to refresh the access token
export function refreshAccessToken(refreshToken) {
    //const refreshToken = localStorage.getItem('refresh_token');
    // console.log('rs',refreshToken);
    const headers = {
        Authorization: `Bearer ${refreshToken}`
      };
    const url = `http://127.0.0.1:5000/refresh-token`;
  return axios.post(url, {refresh_token: refreshToken}, { headers })
  .then(response => {
    // Handle successful response
    const newAccessToken = response.data.access_token;
    // Store the new access token wherever it's needed in your application
    localStorage.setItem('access_token', newAccessToken);
    return newAccessToken;
  })
  .catch(error => {
    // Handle error
    console.error('Error refreshing access token:', error);
    throw error; // Optionally rethrow the error to handle it elsewhere
  });
}