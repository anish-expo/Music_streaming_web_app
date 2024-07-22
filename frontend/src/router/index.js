//src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Navbar from '../components/NavigationBar.vue';
import Footer from '../components/Fooder.vue';
import AdminLogin from '../components/AdminLogin.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import SignUp from '../components/SignUp.vue';
import LogIn from '@/components/Login.vue';
import UserDashboard from '../components/UserDashboard.vue';
import CreatorDashboard from '../components/CreatorDashboard.vue';
import AlbumCreation from '../components/AlbumCreation.vue';
import CreateSong from '../components/CreateSong.vue';
import EditSong from '../components/EditSong.vue';
import EditAlbum from '@/components/EditAlbum.vue';


const routes = [
  {
    path: '/',
    name: 'Home',
    components: { default: Home, header: Navbar, footer: Footer }
  },
  {
    path: '/admin-login',
    name: 'AdminLogin',
    component: AdminLogin
  },
  {
    path: '/admin-dashboard/:username',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/signup',
    name: 'SignUp' ,
    component: SignUp
  },
  {
    path: '/login',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/user-dashboard/:username',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/creator-dashboard/:username',
    name: 'CreatorDashboard',
    component: CreatorDashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/create-album',
    name: 'AlbumCreation',
    component: AlbumCreation,
    meta: {requiresAuth: true}
  },
  {
    path: '/create-song',
    name: 'CreateSong',
    component: CreateSong,
    meta: {requiresAuth: true}
  },
  {
    path: '/edit-song/:songId',
    name: 'EditSong',
    component: EditSong,
    meta: { requiresAuth: true}
  },
  {
    path: '/edit-album/:albumId',
    name: 'EditAlbum',
    component: EditAlbum,
    meta: { requiresAuth: true}
  }


];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token') !== null;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Check if route requires authentication
    if (!isAuthenticated) {
      // Redirect to login page if not authenticated
      next('/admin-login');
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // Proceed to the route
  }
});

export default router;
