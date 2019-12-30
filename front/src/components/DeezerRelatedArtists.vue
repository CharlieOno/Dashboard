<template>
    <div style="color: white;">
        <div style="margin-bottom: 20px; text-transform: uppercase;">
            <h2><b>{{ this.name }}</b> - Artistes associés</h2>
        </div>
        <div class="columns">
            <div v-for="result in results" :key="result.id" class="column is-3">
                <img :src="result.picture_xl"/>
                <h3><b>{{ result.name }}</b></h3>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DeezerRelatedArtists',
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
        this.axios.get(`https://cors-anywhere.herokuapp.com/https://api.deezer.com/artist/${this.id}/related`)
        .then((response) => {
            this.results = response.data.data.splice(0, 4);
        });
    },
    updated() {
        if (this.id !== this.lastId) {
            this.axios.get(`https://cors-anywhere.herokuapp.com/https://api.deezer.com/artist/${this.id}/related`)
            .then((response) => {
                this.results = response.data.data.splice(0, 4);
            });
            this.lastId = this.id;
        }
    },
}
</script>