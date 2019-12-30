<template>
    <div style="color: white;">
        <div style="margin-bottom: 20px; text-transform: uppercase;">
            <h2><b>{{ this.name }}</b> - Artistes associés</h2>
        </div>
        <div class="columns">
            <div v-for="result in results" :key="result.id" class="column is-3">
                <img :src="result.images[1].url"/>
                <h3><b>{{ result.name }}</b></h3>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'SpotifyRelatedArtists',
    props: {
        id: {
            type: String,
            default: ''
        },
        token: {
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
        this.axios.get(`https://api.spotify.com/v1/artists/${this.id}/related-artists`,
        { headers: {
            "Authorization": `Bearer ${this.token}`
        }})
        .then((response) => {
            this.results = response.data.artists.splice(0, 4);
        });
    },
    updated() {
        if (this.id !== this.lastId) {
            this.axios.get(`https://api.spotify.com/v1/artists/${this.id}/related-artists`,
            { headers: {
                "Authorization": `Bearer ${this.token}`
            }})
            .then((response) => {
                this.results = response.data.artists.splice(0, 4);
            });
            this.lastId = this.id;
        }
    },
}
</script>