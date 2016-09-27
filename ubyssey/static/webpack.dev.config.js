var webpack = require('webpack');
var prodConfig = require('./webpack.config.js');

module.exports = Object.assign({}, prodConfig, {
  devtool: 'source-map',
  debug: true,
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('development')
      }
    })
  ]
});
