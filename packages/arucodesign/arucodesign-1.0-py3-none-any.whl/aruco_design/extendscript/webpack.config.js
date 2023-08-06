const path = require('path');
const glob = require('glob');

const BomPlugin = require('webpack-utf8-bom');


// tsファイルの取得
const basePath = path.resolve(__dirname, 'src/');
const targets = glob.sync(`${basePath}/*.ts`);
const entries = {};
targets.forEach(value => {
  const re = new RegExp(`${basePath}/`);
  const key = value.replace(re, '').replace('.ts', '');
  entries[key] = value;
});


module.exports = {
  // モード値を production に設定すると最適化された状態で、
  // development に設定するとソースマップ有効でJSファイルが出力される
  mode: 'production',

  // メインとなるJavaScriptファイル（エントリーポイント）
  entry: entries,

  output: {
    path: path.join(__dirname, 'dist')
  },

  module: {
    rules: [
      {
        // 拡張子 .ts の場合
        test: /\.ts$/,
        // TypeScript をコンパイルする
        use: ['ts-loader']
      }
    ]
  },
  // import 文で .ts ファイルを解決するため
  resolve: {
    extensions: [
      '.ts'
    ]
  },
  plugins: [
    new BomPlugin(true)
  ]
};

