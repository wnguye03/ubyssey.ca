var webpack = require('webpack');
var version = require('./package.json').version;

module.exports = {
    entry: {
        main:    './src/js/main.js',
        dfp:     './src/js/dfp.js',
        article: './src/js/article.jsx',
        section: './src/js/section.jsx'
    },
    output: {
        path: __dirname + '/dist/js',
        filename: '[name]-' + version + '.js'
    },
    module: {
      loaders: [
        {
          test: /\.jsx?$/,
          loader: 'babel',
          exclude: /node_modules/,
          query: {
            presets: ['react']
          }
        }
      ]
    },
    plugins: [
      new webpack.DefinePlugin({
        'process.env': {
          'NODE_ENV': JSON.stringify('production')
        }
      }),
      new webpack.optimize.DedupePlugin(),
      new webpack.optimize.UglifyJsPlugin()
    ]
};
