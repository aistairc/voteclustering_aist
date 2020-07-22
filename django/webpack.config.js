const path = require('path');
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const autoprefixer = require('autoprefixer');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

module.exports = env => {

    var development = env && env.dev;

	return {
		mode: development ? "development" : "production",
        devtool: development ? 'inline-source-map' : false,
		cache: true,
		entry: {
		    "voteclustering/index": "./src/voteclustering/entry.js",
        },
	
		// ファイルの出力設定
		output: {
			path: path.resolve(__dirname, './static/webpack_bundles/'),
			filename: "[name]-[hash].bundle.js"
		},
		// optimization: {
		// 	splitChunks: {
		// 		name   : 'vendor',
		// 		chunks : 'initial',
		// 	}
		// },
		module: {
			rules: [
				{
					test: /\.vue$/,
					loader: 'vue-loader',
					options: {
						hotReload: true
					}
				},
				{
					test: /\.(sc|c|sa)ss$/,
					use: [
						'style-loader',
						{
							loader: 'css-loader',
							options: {
								sourceMap: development,
							}
						},
						{
							loader: 'postcss-loader',
							options: {
								plugins: [
									autoprefixer()
								],
								sourceMap: development,
							}
						},
						{
							loader: 'sass-loader',
							options: {
								data: '@import "_mixin";',
								includePaths: [
								    // 配列の順番を逆にするとmixinを読み込めずにwebpackでエラーが出る
								    path.resolve(__dirname, './src/voteclustering/scss'),
                                ],
								sourceMap: development,
							}
						},
					]
				},
				{
					test: /\.js$/,
					exclude: /node_modules/,
					loader: 'babel-loader?presets[]=es2015'
				},
				{
					test: /\.(png|jpe?g|gif|svg)$/,
					loader: "url-loader",
					options: {
						limit: 102400,
						name: "./image/[name].[hash].[ext]",
						// name: "../img/[path][name].[ext]",
						outputPath: './',
						publicPath: './'
					}
				}
			],
		},
		resolve: {
			alias: {
				'vue$': 'vue/dist/vue.esm.js',
				'@': path.resolve(__dirname, './static'),
			}
		},
		plugins: [
			new VueLoaderPlugin(),
			new webpack.ProvidePlugin({
				"Vue": ['vue/dist/vue.esm.js', 'default'],
				"CookieManager": [path.resolve(__dirname, "./src/model/cookie-manager.js"), 'default'],
				"$": "jquery",
				"jQuery": "jquery",
				"window.jQuery": "jquery"
			}),
			new webpack.HotModuleReplacementPlugin({}),
            new BundleTracker({path: __dirname, filename: 'webpack-stats.json'}),
		],

		devServer: {
			stats: {
				colors: true
			},
			contentBase: path.join(__dirname, 'public'),
			publicPath: '/',
			hot: true,
			index: '',
			liveReload: false,
			overlay: true,
			disableHostCheck: true,
			host: '0.0.0.0',
		},
        performance: {
		    hints: false
        }
	}
}
