var path = require("path");
var config = require('./webpack.config.js');
var BundleTracker = require('webpack-bundle-tracker');

config.output.path = path.resolve('./website/static/website/js/');
config.output.filename = "[name].js";

config.plugins = [
    new BundleTracker({filename: './webpack-stats-prod.json'}),
]

module.exports = config
