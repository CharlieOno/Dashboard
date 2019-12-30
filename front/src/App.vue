<template>
  <div id="app">
    <nav class="navbar bg-1" role="navigation" aria-label="main navigation" style="height: 6vh; border-bottom: 1px solid #404040">
      <div class="navbar-brand">
        <a class="navbar-item" href="/">
          <img src="./assets/audionet.png">
        </a>

        <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu" v-if="authToken === 0">
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons" style="margin-bottom: 0rem;">
              <a class="button-dark" @click="toggleRegisterModal()">
                <strong>S'inscrire</strong>
              </a>
              <a class="button-light" @click="toggleLoginModal()" style="margin-left: 10px;">
                Se connecter
              </a>
            </div>
          </div>
        </div>
      </div>

      <div id="navbarBasicExample" class="navbar-menu" v-if="authToken !== 0">
        <div class="navbar-end">
          <div class="navbar-item">
              <a class="button-dark" v-on:click="logout()">
                Déconnexion
              </a>
          </div>
        </div>
      </div>
    </nav>
    <Home :key="homeKey"/>
    <Login :state="LoginState" @update-state="updateLoginModal"/>
    <Register :state="RegisterState" @update-state="updateRegisterModal"/>
  </div>
</template>

<script>
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import Vue from 'vue';

export default {
  components: {
    Login,
    Register,
    Home
  },
  data() {
    return {
      LoginState: '',
      RegisterState: '',
      homeKey: 0,
      get authToken() {
        return localStorage.getItem('authToken') || 0;
      },
      set authToken(value) {
        localStorage.setItem('authToken', value);
      }
    }
  },
  methods: {
    toggleLoginModal() {
      this.LoginState = 'is-active';
    },
    updateLoginModal(state) {
      this.LoginState = state;
      this.renderHome();
    },
    toggleRegisterModal() {
      this.RegisterState = 'is-active';
    },
    updateRegisterModal(state) {
      this.RegisterState = state;
    },
    handleFacebookSession(response) {
      if (!response.session) {
        return;
      }
      Vue.FB.logout(this.handleFacebookSession);
    },
    logout() {
      localStorage.removeItem("authToken");
      Vue.GoogleAuth.then((auth2) => {
        auth2.signOut();
      });
      Vue.FB.getLoginStatus(this.handleFacebookSession);
      this.$forceUpdate();
      this.renderHome();
    },
    renderHome() {
      this.homeKey += 1;
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  height: 8vh;
}

.color-1 {
  color: rgb(32, 24, 30) !important;
}

.color-2 {
  color: #303030 !important;
}

.color-3 {
  color: #FFF9FB !important;
}

.color-4 {
  color: #00d1b2 !important;
}

.color-5 {
  color: rgb(187, 10, 119) !important;
}

.bg-1 {
  background-color: rgb(32, 24, 30) !important;
}

.bg-2 {
  background-color: #1b131a !important;
}

.bg-3 {
  background-color: #FFF9FB !important;
}

.bg-4 {
  background-color: #4B88A2 !important;
}

.bg-5 {
  background-color: rgb(187, 10, 119) !important;
}

.button-dark {
  background-color: #1b131a;
  padding: calc(0.5rem - 1px) 1rem calc(0.5rem - 1px) 1rem;
  color: white;
  text-align: center;
  white-space: nowrap;
  justify-content: center;
  border: 1px solid #3d313c;
  height: 2.5em;
  line-height: 1.5;
  position: relative;
  vertical-align: top;
  display: inline-flex;
  font-size: 0.9rem;
  text-transform: uppercase;
  cursor: pointer;
}

.button-dark:hover {
  color: #cfcfcf;
}

.button-light {
  background-color: #3d313c;
  padding: calc(0.5rem - 1px) 1rem calc(0.5rem - 1px) 1rem;
  color: white;
  text-align: center;
  white-space: nowrap;
  justify-content: center;
  border: 1px solid #1b131a;
  height: 2.5em;
  line-height: 1.5;
  position: relative;
  vertical-align: top;
  display: inline-flex;
  font-size: 0.9rem;
  text-transform: uppercase;
  cursor: pointer;
}

.button-light:hover {
  color: #cfcfcf;
}

</style>
