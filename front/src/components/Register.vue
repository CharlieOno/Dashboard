<template>
    <div class="modal" :class="state">
        <div class="modal-background" @click="close()"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title title is-4">Inscrivez-vous en moins de 2 minutes!</p>
            </header>
            <section class="modal-card-body">
                <form>
                    <div class="field">
                        <p class="control has-icons-left">
                            <input v-on:keyup.enter="register()" v-model="email" class="input" type="email" placeholder="Email">
                            <span class="icon is-small is-left">
                            <i class="fas fa-envelope"></i>
                            </span>
                        </p>
                    </div>
                    <div class="field">
                        <p class="control has-icons-left">
                            <input v-on:keyup.enter="register()" autocomplete v-model="password" class="input" type="password" placeholder="Password">
                            <span class="icon is-small is-left">
                            <i class="fas fa-lock"></i>
                            </span>
                        </p>
                    </div>
                    <div class="notification is-danger" v-if="registrationStatus === 1">
                        E-mail et/ou mot de passe incorrect.
                    </div>
                </form>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-primary" v-on:click="register()">Inscription</button>
                <button class="button" v-on:click="close()">Annuler</button>
            </footer>
        </div>
        <button class="modal-close is-large" aria-label="close" @click="close()"></button>
    </div>
</template>

<script>
import axios from 'axios';

const   PENDING = 0;
const   ERROR_ARGS = 1;

export default {
  name: 'Register',
  props: {
      state: {
          type: String,
          default: ''
      }
  },
  data() {
      return {
          email: "",
          password: "",
          registrationStatus: PENDING
      }
  },
  methods: {
      close() {
          this.$emit('update-state', '');
      },
      register() {
            this.axios.post(`http://localhost:8080/register?email=${this.email}&password=${this.password}/`)
            .then((response) => {
                if (response.data === "E-mail or password doesn't exist.") {
                    this.registrationStatus = ERROR_ARGS;
                    return;
                } else {
                    this.close();
                }
            })
      }
  }
}
</script>