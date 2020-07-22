import "@babel/polyfill";

require('./scss/style.scss');
global.$ = $;

// 共通処理
Vue.mixin({
    mounted() {
        let {bodyAttr} = this.$options
        if (bodyAttr) {
            bodyAttr = typeof bodyAttr === 'function' ? bodyAttr.call(this) : bodyAttr
            $("html, body").attr("data-page", bodyAttr);
        }
    }
});


// componentディレクトリ以下のvueファイルを全て読み込み、グローバルコンポーネントに追加
import ComponentLoader from './model/component-loader'

ComponentLoader.registerGlobal(require.context('./component', true, /[\w\-]+\.(vue|js)$/));
ComponentLoader.registerGlobal(require.context('./page', true, /[\w\-]+\.(vue|js)$/));

// 各種ユーティリティ読み込み
import Util from "./model/util.js";

Vue.prototype.$showedLengthCaution = false;

// HTMLの#App要素にアプリをマウント
import App from "./app.vue";

$(function () {
    new Vue({
        render: h => h(App),
    }).$mount("#app");
});
