const app = Vue.createApp({
    delimiters: ['[[', ']]'],
    data() {// Now use [[ msg ]] in templates   
        return {
            trylock : 'Good To Go'
        }
    },
    methods: {
        toTitleCase(str) {
            return str.toLowerCase().replace(/(?:^|\s|-)\S/g, function (match) {
                return match.toUpperCase();
            });
        }
    }

})