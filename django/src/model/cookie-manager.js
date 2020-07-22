/**
 * Cookie管理クラス
 */

export default new function () {
    var cookies = {};

    // Cookieを読み込む
    if (document.cookie != '') {
        cookies = document.cookie.split(';').reduce((value, x) => {
            var data = x.trim().split('=');
            value[data[0]] = decodeURIComponent(data[1]);
            return value;
        }, {});
    }

    /**
     * Cookieから値を読み込む
     * @param  String key キー
     * @return String 値
     */
    this.get = function (key) {
        return cookies[key];
    }

    /**
     * Cookieに値を書き込む
     * @param String key     キー
     * @param String value   値
     * @param Object options オプション(未使用)
     */
    this.set = function (key, value, options) {
        cookies[key] = value;
        document.cookie = encodeURIComponent(key) + '=' + encodeURIComponent(value);
    }
}
