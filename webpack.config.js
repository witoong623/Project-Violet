var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var CleanObsoleteChunks = require('webpack-clean-obsolete-chunks');

module.exports = {
  context: __dirname,

  entry: {
    index: './website/static/website/js/index'
  },
  output: {
      path: path.resolve('./website/static/website/bundles/'),
      filename: "[name]-[hash].js",
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        exclude: /node_modules/,
        use: ['awesome-typescript-loader']
      },
      {
        test: /\.js$/,
        use: ["source-map-loader"],
        enforce: "pre"
      }
    ]
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new CleanObsoleteChunks({verbose: true, deep: false}),
  ],
  resolve: {
    extensions: ['*', '.js', '.jsx', '.ts', '.tsx']
  }

};