<template>
  <div class="columns bg-2" style="min-height: 94vh; margin-top: inherit;">
    <div class="column is-3" style="border-right: 1px solid #404040;">
      <aside class="menu has-text-white" style="padding: 15px;">
        <p class="menu-label has-text-white">
          Services disponibles
        </p>
        <div v-if="authToken !== 0">
          <ul class="menu-list">
            <li>
              <span>Spotify</span>
              <button v-if="spotifyToken === 0" class="is-pulled-right button-light" style="margin-top: -0.5rem;" @click="loginSpotify()">Se connecter</button>
              <button v-if="spotifyToken !== 0" class="is-pulled-right button-dark" style="margin-top: -0.5rem;" @click="logoutSpotify()">Déconnecter</button>
              <ul>
                <li><a class="widget-link" @click="toggleSpotifyLastSongs()">Dernières sorties d'un artiste</a></li>
                <li><a class="widget-link" @click="toggleSpotifyTopTracks()">Meilleurs morceaux d'un artiste</a></li>
                <li><a class="widget-link" @click="toggleSpotifyRelatedArtists()">Artistes associés à un artiste</a></li>
              </ul>
            </li>
            <li>
              <span>Deezer</span>
              <button v-if="deezerToken === 0" class="is-pulled-right button-light" style="margin-top: -0.5rem;" @click="loginDeezer()">Se connecter</button>
              <button v-if="deezerToken !== 0" class="is-pulled-right button-dark" style="margin-top: -0.5rem;" @click="logoutDeezer()">Déconnecter</button>
              <ul>
                <li><a class="widget-link" @click="toggleDeezerLastSongs()">Dernières sorties d'un artiste</a></li>
                <li><a class="widget-link" @click="toggleDeezerTopTracks()">Meilleurs morceaux d'un artiste</a></li>
                <li><a class="widget-link" @click="toggleDeezerRelatedArtists()">Artistes associés à un artiste</a></li>
              </ul>
            </li>
          </ul>
        </div>
        <div class="notification bg-1 border" v-if="authToken === 0">
          <p class="title is-6 color-3">Veuillez-vous connecter pour ajouter des widgets.</p>
        </div>
        <p class="menu-label has-text-white">
          Mes widgets
        </p>
        <ul class="menu-list">
          <li>
            <div v-for="widget in widgets" :key="widget.id" class="notification bg-1 border">
                <span class="color-3"><b>{{ widget.name }}</b> - {{ widget.type }}</span>
                <div class="dropdown is-hoverable is-pulled-right">
                  <div class="dropdown-trigger">
                    <button class="button is-small" aria-haspopup="true" aria-controls="dropdown-menu3" style="background: inherit; color: white; margin-top: -0.2rem;">
                      <span class="icon is-small">
                        <i class="fas fa-angle-down" aria-hidden="true"></i>
                      </span>
                    </button>
                  </div>
                  <div class="dropdown-menu" id="dropdown-menu3" role="menu">
                    <div class="dropdown-content">
                      <a href="#" class="dropdown-item" @click="modifyWidget(widget)">Modifier</a>
                      <a href="#" class="dropdown-item" @click="moveUpWidget(widget)">Monter</a>
                      <a href="#" class="dropdown-item" @click="moveDownWidget(widget)">Descendre</a>
                      <a href="#" class="dropdown-item" @click="deleteWidget(widget)">Supprimer</a>
                    </div>
                  </div>
                </div>
            </div>
          </li>
        </ul>
      </aside>
    </div>
    <div class="column is-9">
      <div v-for="widget in widgets" :key="widget.id" class="container bg-1 border widget">
        <SpotifyLastSongs :id="widget.data" :name="widget.name" :token="spotifyToken.toString()" v-if="widget.type === 'spotifyLastSongs'" />
        <SpotifyTopTracks :id="widget.data" :name="widget.name" :token="spotifyToken.toString()" v-if="widget.type === 'spotifyTopTracks'" />
        <SpotifyRelatedArtists :id="widget.data" :name="widget.name" :token="spotifyToken.toString()" v-if="widget.type === 'spotifyRelatedArtists'" />
        <DeezerLastSongs :id="widget.data.toString()" :name="widget.name" v-if="widget.type === 'deezerLastSongs'" />
        <DeezerTopTracks :id="widget.data.toString()" :name="widget.name" v-if="widget.type === 'deezerTopTracks'" />
        <DeezerRelatedArtists :id="widget.data.toString()" :name="widget.name" v-if="widget.type === 'deezerRelatedArtists'" />
      </div>
    </div>
    <SpotifyLastSongsConfig :config="configWidgetId" :token="spotifyToken.toString()" :state="spotifyLastSongsState" @update-state="updateSpotifyLastSongs" />
    <SpotifyTopTracksConfig :config="configWidgetId" :token="spotifyToken.toString()" :state="spotifyTopTracksState" @update-state="updateSpotifyTopTracks" />
    <SpotifyRelatedArtistsConfig :config="configWidgetId" :token="spotifyToken.toString()" :state="spotifyRelatedArtistsState" @update-state="updateSpotifyRelatedArtists" />
    <DeezerLastSongsConfig :config="configWidgetId" :state="deezerLastSongsState" @update-state="updateDeezerLastSongs" />
    <DeezerTopTracksConfig :config="configWidgetId" :state="deezerTopTracksState" @update-state="updateDeezerTopTracks" />
    <DeezerRelatedArtistsConfig :config="configWidgetId" :state="deezerRelatedArtistsState" @update-state="updateDeezerRelatedArtists" />
  </div>
</template>

<script>
import SpotifyLastSongsConfig from './SpotifyLastSongsConfig';
import SpotifyLastSongs from './SpotifyLastSongs';
import SpotifyTopTracksConfig from './SpotifyTopTracksConfig';
import SpotifyTopTracks from './SpotifyTopTracks';
import SpotifyRelatedArtistsConfig from './SpotifyRelatedArtistsConfig';
import SpotifyRelatedArtists from './SpotifyRelatedArtists';
import DeezerLastSongsConfig from './DeezerLastSongsConfig';
import DeezerLastSongs from './DeezerLastSongs';
import DeezerTopTracksConfig from './DeezerTopTracksConfig';
import DeezerTopTracks from './DeezerTopTracks';
import DeezerRelatedArtistsConfig from './DeezerRelatedArtistsConfig';
import DeezerRelatedArtists from './DeezerRelatedArtists';

class Widget {

  constructor(type, data, name, id) {
    if (id === 0) {
      this.id = this.uuidv4();
    } else {
      this.id = id;
    }
    this.type = type;
    this.name = name;
    this.data = data;
  }

  uuidv4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
}

export default {
  name: 'home',
  components: {
    SpotifyLastSongsConfig,
    SpotifyLastSongs,
    SpotifyTopTracksConfig,
    SpotifyTopTracks,
    SpotifyRelatedArtistsConfig,
    SpotifyRelatedArtists,
    DeezerLastSongsConfig,
    DeezerLastSongs,
    DeezerTopTracksConfig,
    DeezerTopTracks,
    DeezerRelatedArtistsConfig,
    DeezerRelatedArtists
  },
  created() {
    var urlObject = (new URL(window.location.href)).searchParams;
    var urlParams = this.getUrlVars();

    if (this.authToken !== 0 && urlObject.get('spotify') === "true" && urlParams.access_token && this.spotifyToken === 0) {
      this.axios.post(`http://localhost:8080/login/spotify?auth_token=${this.authToken}&spotify_token=${urlParams.access_token}/`)
      .then((response) => {
          localStorage.setItem('spotifyToken-' + this.authToken, urlParams.access_token);
          this.$forceUpdate();
      })
    }
    if (this.authToken !== 0 && urlObject.get('deezer') === "true" && urlParams.access_token && this.deezerToken === 0) {
      this.axios.post(`http://localhost:8080/login/deezer?auth_token=${this.authToken}&deezer_token=${urlParams.access_token}/`)
      .then((response) => {
          localStorage.setItem('deezerToken-' + this.authToken, urlParams.access_token);
          this.$forceUpdate();
      })
    }
    if (this.authToken !== 0) {
      this.axios.post(`http://localhost:8080/list/widget?auth_token=${this.authToken}`)
      .then((response) => {
        response.data.forEach(widget => {
          this.widgets.unshift(new Widget(widget.type, widget.data, widget.name, widget.id));
        });
      });
    }
  },
  data() {
    return {
      spotifyLastSongsState: '',
      spotifyTopTracksState: '',
      spotifyRelatedArtistsState: '',
      deezerLastSongsState: '',
      deezerTopTracksState: '',
      deezerRelatedArtistsState: '',
      configWidgetId: '',
      widgets: [],
      get authToken() {
        return localStorage.getItem('authToken') || 0;
      },
      set authToken(value) {
        localStorage.setItem('authToken', value);
      },
      get spotifyToken() {
        return localStorage.getItem('spotifyToken-' + this.authToken) || 0;
      },
      set spotifyToken(value) {
        localStorage.setItem('spotifyToken-' + this.authToken, value);
      },
      get deezerToken() {
        return localStorage.getItem('deezerToken-' + this.authToken) || 0;
      },
      set deezerToken(value) {
        localStorage.setItem('deezerToken-' + this.authToken, value);
      }
    }
  },
  methods: {
    //
    //  Login / Logout from Spotify+Deezer
    //
    loginSpotify() {
      window.location.href = `https://accounts.spotify.com/authorize?client_id=1db60673fcf648a189dfac04beb7d735&redirect_uri=`
      + encodeURI("https://localhost:3000?spotify=true") + `&response_type=token`;
    },
    logoutSpotify() {
      localStorage.removeItem('spotifyToken-' + this.authToken);
      this.$forceUpdate();
    },
    loginDeezer() {
      window.location.href = `https://connect.deezer.com/oauth/auth.php?app_id=386784&redirect_uri=`
      + encodeURI("https://localhost:3000?deezer=true") + `&perms=basic_access,email&response_type=token`;
    },
    logoutDeezer() {
      localStorage.removeItem('deezerToken-' + this.authToken);
      this.$forceUpdate();
    },
    //
    //  Utilities
    //
    getUrlVars() {
      var vars = {};
      var parts = this.$route.path.replace(/[/?&]+([^=&]+)=([^&]*)/gi, function(m,key,value, value2) {
          vars[key] = value;
      });
      return vars;
    },
    //
    //  Widget's communication with configuration modal
    //
    toggleSpotifyLastSongs() {
      if (this.spotifyToken === 0) {
        return;
      }
      this.spotifyLastSongsState = 'is-active';
    },
    updateSpotifyLastSongs(res) {
      this.configWidgetId = '';
      this.spotifyLastSongsState = res.state;
      if (res.id !== "none" && res.config === '') {
        var widget = new Widget('spotifyLastSongs', res.id, res.name, 0);

        this.widgets.unshift(widget);
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${widget.id}&widget_type=${widget.type}&widget_name=${widget.name}&widget_data=${widget.data}`);
      }
      if (res.id !== 'none' && res.config !== '') {
        var x = this.widgets.map(function(e) { return e.id; }).indexOf(res.config);

        this.widgets[x].data = res.id;
        this.widgets[x].name = res.name;
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${this.widgets[x].id}&widget_type=${this.widgets[x].type}&widget_name=${this.widgets[x].name}&widget_data=${this.widgets[x].data}`);
      }
    },
    toggleSpotifyTopTracks() {
      if (this.spotifyToken === 0) {
        return;
      }
      this.spotifyTopTracksState = 'is-active';
    },
    updateSpotifyTopTracks(res) {
      this.configWidgetId = '';
      this.spotifyTopTracksState = res.state;
      if (res.id !== "none" && res.config === '') {
        var widget = new Widget('spotifyTopTracks', res.id, res.name, 0);

        this.widgets.unshift(widget);
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${widget.id}&widget_type=${widget.type}&widget_name=${widget.name}&widget_data=${widget.data}`);
      }
      if (res.id !== 'none' && res.config !== '') {
        var x = this.widgets.map(function(e) { return e.id; }).indexOf(res.config);

        this.widgets[x].data = res.id;
        this.widgets[x].name = res.name;
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${this.widgets[x].id}&widget_type=${this.widgets[x].type}&widget_name=${this.widgets[x].name}&widget_data=${this.widgets[x].data}`);
      }
    },
    toggleSpotifyRelatedArtists() {
      if (this.spotifyToken === 0) {
        return;
      }
      this.spotifyRelatedArtistsState = 'is-active';
    },
    updateSpotifyRelatedArtists(res) {
      this.configWidgetId = '';
      this.spotifyRelatedArtistsState = res.state;
      if (res.id !== "none" && res.config === '') {
        var widget = new Widget('spotifyRelatedArtists', res.id, res.name, 0);

        this.widgets.unshift(widget);
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${widget.id}&widget_type=${widget.type}&widget_name=${widget.name}&widget_data=${widget.data}`);
      }
      if (res.id !== 'none' && res.config !== '') {
        var x = this.widgets.map(function(e) { return e.id; }).indexOf(res.config);

        this.widgets[x].data = res.id;
        this.widgets[x].name = res.name;
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${this.widgets[x].id}&widget_type=${this.widgets[x].type}&widget_name=${this.widgets[x].name}&widget_data=${this.widgets[x].data}`);
      }
    },
    toggleDeezerLastSongs() {
      if (this.deezerToken === 0) {
        return;
      }
      this.deezerLastSongsState = 'is-active';
    },
    updateDeezerLastSongs(res) {
      this.configWidgetId = '';
      this.deezerLastSongsState = res.state;
      if (res.id !== "none" && res.config === '') {
        var widget = new Widget('deezerLastSongs', res.id, res.name, 0);

        this.widgets.unshift(widget);
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${widget.id}&widget_type=${widget.type}&widget_name=${widget.name}&widget_data=${widget.data}`);
      }
      if (res.id !== 'none' && res.config !== '') {
        var x = this.widgets.map(function(e) { return e.id; }).indexOf(res.config);

        this.widgets[x].data = res.id;
        this.widgets[x].name = res.name;
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${this.widgets[x].id}&widget_type=${this.widgets[x].type}&widget_name=${this.widgets[x].name}&widget_data=${this.widgets[x].data}`);
      }
    },
    toggleDeezerTopTracks() {
      if (this.deezerToken === 0) {
        return;
      }
      this.deezerTopTracksState = 'is-active';
    },
    updateDeezerTopTracks(res) {
      this.configWidgetId = '';
      this.deezerTopTracksState = res.state;
      if (res.id !== "none" && res.config === '') {
        var widget = new Widget('deezerTopTracks', res.id, res.name, 0);

        this.widgets.unshift(widget);
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${widget.id}&widget_type=${widget.type}&widget_name=${widget.name}&widget_data=${widget.data}`);
      }
      if (res.id !== 'none' && res.config !== '') {
        var x = this.widgets.map(function(e) { return e.id; }).indexOf(res.config);

        this.widgets[x].data = res.id;
        this.widgets[x].name = res.name;
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${this.widgets[x].id}&widget_type=${this.widgets[x].type}&widget_name=${this.widgets[x].name}&widget_data=${this.widgets[x].data}`);
      }
    },
    toggleDeezerRelatedArtists() {
      if (this.deezerToken === 0) {
        return;
      }
      this.deezerRelatedArtistsState = 'is-active';
    },
    updateDeezerRelatedArtists(res) {
      this.configWidgetId = '';
      this.deezerRelatedArtistsState = res.state;
      if (res.id !== "none" && res.config === '') {
        var widget = new Widget('deezerRelatedArtists', res.id, res.name, 0);

        this.widgets.unshift(widget);
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${widget.id}&widget_type=${widget.type}&widget_name=${widget.name}&widget_data=${widget.data}`);
      }
      if (res.id !== 'none' && res.config !== '') {
        var x = this.widgets.map(function(e) { return e.id; }).indexOf(res.config);

        this.widgets[x].data = res.id;
        this.widgets[x].name = res.name;
        this.axios.post(`http://localhost:8080/register/widget?auth_token=${this.authToken}&widget_id=${this.widgets[x].id}&widget_type=${this.widgets[x].type}&widget_name=${this.widgets[x].name}&widget_data=${this.widgets[x].data}`);
      }
    },
    //
    //  Widget's tweaks
    //
    modifyWidget(widget) {
      this.configWidgetId = widget.id;
      if (widget.type === 'spotifyLastSongs') {
        this.toggleSpotifyLastSongs();
      }
      if (widget.type === 'spotifyTopTracks') {
        this.toggleSpotifyTopTracks();
      }
      if (widget.type === 'spotifyRelatedArtists') {
        this.toggleSpotifyRelatedArtists();
      }
      if (widget.type === 'deezerLastSongs') {
        this.toggleDeezerLastSongs();
      }
      if (widget.type === 'deezerTopTracks') {
        this.toggleDeezerTopTracks();
      }
      if (widget.type === 'deezerRelatedArtists') {
        this.toggleDeezerRelatedArtists();
      }
    },
    moveDownWidget(widget) {
      var x = this.widgets.map(function(e) { return e.id; }).indexOf(widget.id);

      if (x === this.widgets.length - 1) {
        return;
      }
      this.widgets[x] = this.widgets.splice(x + 1, 1, this.widgets[x])[0];
    },
    moveUpWidget(widget) {
      var x = this.widgets.map(function(e) { return e.id; }).indexOf(widget.id) - 1;

      if (x === -1) {
        return;
      }
      this.widgets[x] = this.widgets.splice(x + 1, 1, this.widgets[x])[0];
    },
    deleteWidget(widget) {
      var x = this.widgets.map(function(e) { return e.id; }).indexOf(widget.id);

      this.axios.post(`http://localhost:8080/remove/widget?widget_id=${this.widgets[x].id}`);
      this.widgets.splice(x, 1);
    }
  },
}
</script>

<style>
.widget-link {
  font-weight: bold;
  color:#00d1b2 !important;
}

.widget-link:hover {
 background-color: #323233 !important;
}

.widget-link:after {
  content: "+";
  float: right;
}

.widget {
  padding: 20px;
  margin-top: 20px !important;
}

.border {
  border: 1px solid #404040;
}

</style>