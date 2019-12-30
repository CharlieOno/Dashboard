<template>
    <div class="modal" :class="state">
        <div class="modal-background" @click="close()"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title title is-4">Spotify - Dernières sorties d'un artiste</p>
            </header>
            <section class="modal-card-body " style="margin-bottom: inherit;">
                <div class="columns" style="margin-bottom: inherit;">
                    <div class="column is-9">
                        <input v-model="searchQuery" class="input" type="text" placeholder="Rechercher un artiste">
                    </div>
                    <div class="column is-3">
                        <button @click="search()" class="button">Rechercher</button>
                    </div>
                </div>
                <div class="control">
                    <label class="radio" v-for="result in results" :key="result.id">
                        <input type="radio" name="selection" :value="result.id" v-model="picked">
                        {{ result.name }}
                    </label>
                </div>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-primary" v-on:click="add()">Ajouter</button>
                <button class="button" v-on:click="close()">Annuler</button>
            </footer>
        </div>
        <button class="modal-close is-large" aria-label="close" @click="close()"></button>
    </div>
</template>

<script>
export default {
    name: 'SpotifyLastSongsConfig',
    props: {
        state: {
            type: String,
            default: ''
        },
        token: {
            type: String,
            default: ''
        },
        config: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            searchQuery: "",
            picked: "",
            results: []
        }
    },
    methods: {
        close() {
          this.$emit('update-state', {
              state: "",
              id: "none"
          });
        },
        search() {
            this.axios.get(`https://api.spotify.com/v1/search?q=${this.searchQuery}&type=artist`,
            { headers: {
                "Authorization": `Bearer ${this.token}`
            }})
            .then((response) => {
                this.results = response.data.artists.items;
            });
        },
        add() {
            var x = this.results.map(function(e) { return e.id; }).indexOf(this.picked);

            this.$emit('update-state', {
                state: "",
                id: this.results[x].id,
                name: this.results[x].name,
                config: this.config
            });
        }
    }
}
</script>

<style>

.radio {
    width: 100%;
}

.radio + .radio {
    margin-left: inherit;
}

</style>