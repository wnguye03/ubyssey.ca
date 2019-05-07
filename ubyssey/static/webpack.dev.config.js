const webpack = require('webpack');
const prodConfig = require('./webpack.config.js');

var devConfig = Object.create(prodConfig);

devConfig.mode = 'development';
devConfig.devtool = 'source-map';
// devConfig.debug = true;
devConfig.plugins = [
  new webpack.DefinePlugin({
    'process.traceDeprecation': true
  })
];

module.exports = devConfig;
