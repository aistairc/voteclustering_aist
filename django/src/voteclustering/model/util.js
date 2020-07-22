var methods = {

    /**
     * 指定されたパラメーターが空かどうか判定する
     * @param  {[type]}  value [description]
     * @return {Boolean}       [description]
     */
    isEmpty(value) {
        return value == null || value == "";
    },

    /**
     * 指定されたパラメーターに空でない要素があるかどうか取得する
     * @param  Any value チェックしたいパラメーター
     * @return Bool
     */
    hasValue(...value) {
        return value.filter(x => {
            if (x == null || x === "") {
                return false;
            } else if (Array.isArray(x)) {
                return hasValue(...x);
            } else if (typeof x === 'object' && x !== null) {
                return hasValue(...Object.values(x));
            } else {
                return true;
            }
        }).length > 0;
    },

    /**
     * 指定されたパラメーターのうち、空でない最初の値を返却する
     * @param  Any values 値
     * @return Any
     */
    getFirstValue(...values) {
        for (var value of values) {
            if (hasValue(value)) {
                return value;
            }
        }
        return null;
    },

    /**
     * 指定されたパラメーターのうち、数値とみなせる最初の値を返却する
     * @param  Any values 値
     * @return Number
     */
    getFirstNumber(...values) {
        var result = values.find(x => {
            var number = Number(x);
            return !isNaN(number);
        });
        return result !== undefined ? Number(result) : null;
    },

    /**
     * 数値をカンマ区切りに変換する
     * @param  Number num
     * @return String
     */
    splitComma(num) {
        if (num == null) return 0;
        return String(num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,')
    },

    /**
     * 「Y/m/d」形式の文字列を「Y年m月d日」に変換する
     * @param  String value
     * @return String
     */
    toJPDateFormat(value) {
        if (value == null) return "";
        return value.replace(/\//g, "-").replace(/^([0-9]+)-([0-9]+)-([0-9]+)/g, "$1年$2月$3日");
    },

    /**
     * 配列から指定インデックスの要素を削除する
     * @param  [Any] array
     * @param  Number index
     */
    removeArrayItem(array, index) {
        array.splice(index, 1);
    },

    /**
     * DBレコードの配列を論理削除する
     * @param  [Any] array
     * @param  Number index
     */
    removeDBItem(array, index) {
        if (array[index].id) {
            Vue.set(array[index], "delete", true)
        } else {
            array.splice(index, 1);
        }
    },

    /**
     * 配列の指定要素を移動する
     * @param  [Any] array
     * @param  Number index
     * @param  Number volume
     */
    moveArrayItem(array, index, volume) {
        var after = Math.min(Math.max(0, index + volume), array.length - 1);
        var value = array[index];
        array.splice(index, 1);
        array.splice(after, 0, value);
    },

    /**
     * confirmを表示し、同意されたら関数を実行する
     * @param  String message
     * @param  Function f
     */
    execWithConfirm(message, f) {
        var result = window.confirm(message);
        if (f && result) {
            f();
        }
        return result;
    },

    /**
     * console.logに出力する
     * @param  Any parameter
     */
    log(...parameter) {
        window.console.log(...parameter);
    },

    resolver() {
        var d = $.Deferred();
        d.resolve();
        return d.promise();
    },

    rejector() {
        var d = $.Deferred();
        d.reject();
        return d.promise();
    },
};

// Vueのメソッドに登録する
Vue.mixin({methods: methods});

// Vueのフィルターと、グローバルなメソッドに登録する
for (var key in methods) {
    Vue.filter(key, methods[key]);
    global[key] = methods[key];
}

// jQueryのメソッドを追加する
(function ($) {

    $.fn.center = function ($basis) {
        var basis_offset = {top: 0, left: 0}
        if ($basis !== undefined) {
            basis_offset = $basis.offset();
        }

        var $this = $(this);
        var offset = $this.offset();
        offset.left += $this.outerWidth() / 2 - basis_offset.left;
        offset.top += $this.outerHeight() / 2 - basis_offset.top;

        return offset;
    }

    $.fn.reflow = function () {
        return $(this).each(function () {
            var dummy = this.offsetHeight;
            var dummy = this.offsetWidth;
        });
    }

    $.fn.caretPosition = function () {
        var pos = 0;
        var input = $(this).get(0);
        if (document.selection) {
            input.focus();
            var range = document.selection.createRange();
            range.moveStart('character', -input.value.length);
            pos = oSel.text.length;

        } else if (input.selectionStart || input.selectionStart == '0') {
            pos = input.selectionDirection == 'backward' ? input.selectionStart : input.selectionEnd;
        }

        return pos;
    }

    /**
     * Excelのようにフォームのフォーカスをカーソル移動できるようにする
     * @param  Object options
     */
    $.fn.excelize = function (options) {
        var $wrapper = $(this);

        options = Object.assign({
            enter: true,
        }, options);

        const target = "input[type=text], input[type=password], input[type=checkbox], input[type=date], input[type=number], textarea";

        // カーソルキーでセルを移動する処理
        $wrapper.on("keydown", target, function (event) {
            var $this = $(this);
            var x_score = 0;
            var y_score = 0;

            if (!$this.is("textarea")) {
                if (event.keyCode == 38 || event.keyCode == 40) {
                    y_score = event.keyCode == 38 ? -1 : 1;
                }

                if (options.enter && event.keyCode == 13) {
                    y_score = event.shiftKey ? -1 : 1;
                }
            } else {
                var pos = $this.caretPosition();
                var length = $this.val().length;
                if ((event.keyCode == 38 && pos == 0) || (event.keyCode == 40 && pos == length)) {
                    y_score = event.keyCode == 38 ? -1 : 1;
                }
            }

            if (event.keyCode == 37 || event.keyCode == 39) {
                var pos = $this.caretPosition();
                var length = $this.val().length;
                if ((event.keyCode == 37 && pos == 0) || (event.keyCode == 39 && pos == length)) {
                    x_score = event.keyCode == 37 ? -1 : 1;
                }
            }

            if (x_score != null || y_score != null) {
                var $this = $(this);
                var this_position = $this.offset();
                var this_width = $this.width();
                var this_height = $this.height();
                this_position.right = this_position.left + $this.width();
                this_position.bottom = this_position.top + $this.height();
                var candidate = [];

                $wrapper.find(target).each(function () {
                    var $target = $(this);
                    var target = $target.offset();
                    target.right = target.left + $target.width();
                    target.bottom = target.top + $target.height();

                    if (((y_score != 0 && (
                            (this_position.left <= target.left && target.left < this_position.right) ||
                            (this_position.left <= target.right && target.right < this_position.right) ||
                            (target.left <= this_position.left && this_position.left < target.right) ||
                            (target.left <= this_position.right && this_position.right < target.right)
                        )) ||
                        (x_score != 0 && (
                            (target.top <= this_position.top && this_position.top < target.bottom) ||
                            (target.top <= this_position.bottom && this_position.bottom < target.bottom) ||
                            (this_position.top <= target.top && target.top < this_position.bottom) ||
                            (this_position.top <= target.bottom && target.bottom < this_position.bottom)
                        ))) &&
                        (target.top - this_position.top) * y_score + (target.left - this_position.left) * x_score > 0.1) {
                        candidate.push({
                            score: Math.abs(target.top - this_position.top) + Math.abs(target.left - this_position.left),
                            $element: $target,
                        })
                    }
                })

                if (candidate.length > 0) {
                    candidate.sort(function (a, b) {
                        return a.score - b.score;
                    });

                    $this.blur();
                    candidate[0].$element.focus();
                }
            }
        });
    }

    $(function () {
        $(document).on("keydown", "input[type=text], input[type=password], input[type=date], input[type=number]", function (event) {
            if (event.keyCode == 13) {
                var $target = $(this).parent();
                while (!$target.is("body")) {
                    var $submit_button = $target.find("[data-enter]");
                    if ($submit_button.length > 0) {
                        $submit_button.eq(0).click();
                        break;
                    }
                    $target = $target.parent();
                }
            }
        });
    });

})($);

export default new function () {

}
