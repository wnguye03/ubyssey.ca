var webpack = require('webpack');

module.exports = {
    entry: {
        article: './js/article.jsx',
        section: './js/section.jsx'
    },
    output: {
        path: __dirname + '/static/js',
        filename: "[name].js"
    },
    module: {
      loaders: [
        {test: /\.jsx$/, include: __dirname + '/js', loader: 'babel-loader'}
      ]
    },
    plugins: [
      new webpack.optimize.UglifyJsPlugin()
    ]
};
