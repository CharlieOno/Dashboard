import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import '../node_modules/bulma/css/bulma.css'
import './css/main.css'
import axios from 'axios'
import VueAxios from 'vue-axios'
import { LoaderPlugin } from 'vue-google-login';
import FacebookSDK from './plugins/FB';

Vue.use(FacebookSDK);
Vue.use(LoaderPlugin, {
  client_id: "1083183077543-ogjph9laolcpm0uphqk3d0j7u7pf13i5.apps.googleusercontent.com"
})

Vue.GoogleAuth.then(auth2 => {
  if (localStorage.getItem("authToken") !== 0) {
    return;
  }
  if (auth2.isSignedIn.get() === true)
    auth2.signOut();
})

Vue.use(VueAxios, axios);
Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
