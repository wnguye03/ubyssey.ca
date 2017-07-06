var webpack = require('webpack');
var prodConfig = require('./webpack.config.js');

var devConfig = Object.create(prodConfig);

devConfig.devtool = 'cheap-module-eval-source-map';
devConfig.debug = true;
devConfig.plugins = [
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('development')
    }
  })
];

devConfig.watchOptions = {
  poll: 1000,
  // ignored: /node_modules/
}

module.exports = devConfig;
