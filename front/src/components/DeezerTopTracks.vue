<template>
    <div style="color: white;">
        <div style="margin-bottom: 20px; text-transform: uppercase;">
            <h2><b>{{ this.name }}</b> - Meilleurs morceaux</h2>
        </div>
        <div class="columns">
            <div v-for="result in results" :key="result.id" class="column is-3">
                <img :src="result.album.cover_xl"/>
                <h3><b>{{ result.title }}</b></h3>
                <h3>{{ result.album.title }}</h3>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DeezerTopTracks',
    props: {
        id: {
            type: String,
            default: ''
        },
        name: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            results: [],
            lastId: ''
        }
    },
    mounted() {
        this.axios.get(`https://cors-anywhere.herokuapp.com/https://api.deezer.com/artist/${this.id}/top`)
        .then((response) => {
            this.results = response.data.data.splice(0, 4);
        });
    },
    updated() {
        if (this.id !== this.lastId) {
            this.axios.get(`https://cors-anywhere.herokuapp.com/https://api.deezer.com/artist/${this.id}/top`)
            .then((response) => {
                this.results = response.data.data.splice(0, 4);
            });
            this.lastId = this.id;
        }
    },
}
</script>