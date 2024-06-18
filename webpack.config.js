const path = require('path');

module.exports = {
  mode: 'production',
  entry: `./develop-static/js/base.js`,
  output: {
    filename: "main.js",
    path: path.join(__dirname, './static/js/'),
    library: "Main"
  }
};