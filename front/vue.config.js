const fs = require('fs');

module.exports = {
    devServer: {
        clientLogLevel: 'silent',
        https: {
            key: fs.readFileSync('./localhost.key'),
            cert: fs.readFileSync('./localhost.crt')
        },
        public: 'https://localhost:3000/'
    }
}