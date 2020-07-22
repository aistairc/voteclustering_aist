<template>
    <div class="question-component">
        <template v-if="question">
            <div class="page page_question" :data-type="question.type">
                <div class="header">
                    <div>
                        <img src="../image/menu.png" class="header-menu" @click="$refs.menu.show()"
                             :style="{visibility: question.type != 'thanks' ? 'visible': 'hidden'}">
                        <div v-if="voteClusteringOptions.language == 'ja'" class="header-logo-ja"></div>
                        <div v-else class="header-logo-en"></div>
                        <img src="../image/help.svg" class="header-help" @click="showGuide">
                    </div>
                </div>

                <div class="body">
                    <div class="body-scroller">
                        <question-item :question="question" :questionList="questionList" :questionIndex="questionIndex"
                                       ref="questionPage" @prev="prev" @next="next" @nextable="nextable = $event"
                                       @finish="$emit('finish')"/>
                        <carousel-pager v-if="questionIndex < questionList.length - 1" :index="questionIndex"
                                        :max="questionList.length - 1" class="for-nonsmall"/>
                    </div>
                </div>
            </div>

            <question-menu ref="menu" :questionList="questionList" @click="question => clickMenuQuestion(question)"
                           @home="$refs.homeConfirmPopup.show()" @tos="$refs.tosConfirmPopup.show()"/>

            <popup ref="homeConfirmPopup" class="custom-design">
                <div class="confirm-popup home-confirm-popup">
                    <div class="confirm-popup-body">
                        <span v-html="languages.toTopConfirm.text"></span>
                        <div class="confirm-popup-buttons">
                            <button class="home-confirm-popup-continue" @click="$refs.homeConfirmPopup.hide()">{{
                                languages.toTopConfirm.cancel }}
                            </button>
                            <button class="home-confirm-popup-finish"
                                    @click="$refs.homeConfirmPopup.hide(); location.reload();">{{
                                languages.toTopConfirm.ok }}
                            </button>
                        </div>
                    </div>
                    <div class="close" @click="$refs.homeConfirmPopup.hide()"><img src="../image/icon-cross.svg"></div>
                </div>
            </popup>

            <popup ref="tosConfirmPopup" class="scroll">
                <div class="popup-tos" v-html="languages.tos.body"></div>
            </popup>

            <div class="pager" v-if="question.type != 'thanks'">
                <div>
                    <div class="left"><img src="../image/left-arrow.svg" @click="$refs.questionPage.prev()"></div>
                    <div class="right"><img src="../image/right-arrow.svg" @click="$refs.questionPage.next()"
                                            v-if="question.skippable !== false || nextable"></div>
                </div>
            </div>
        </template>

        <!-- チュートリアル -->
        <tutorial v-if="tutorial" :setting="tutorial" @click="nextTutorial()"></tutorial>
    </div>
</template>

<script>
    import Question from '../data/question.js';
    import moment from "moment";
    import xssFilters from 'xss-filters';

    export default {
        bodyAttr: 'question',
        props: ['questionList'],
        model: {
            prop: 'questionList',
        },
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions, // 設定
                languages: voteClusteringOptions.languages.question, // 言語セット

                question: null, // 現在の設問
                errorList: [], // エラー一覧
                opinionLoading: false,

                questionIndex: 0, // 設問インデックス
                viewedMaxIndex: 0, // 閲覧した最大インデックス
                oneOpinionCautioned: false, // 1つしか意見を選択していない警告を表示したかどうか
                deferredValidIndex: 0, // deferred系有効値チェック(ページ遷移時に現在実行しているdeferredを無効化するためのインデックス)
                suggestTimeoutHandler: null, // サジェスト一覧取得用タイムアウトハンドラー

                tutorialStep: 0,
                tutorial: null,

                nextable: false,
                startTimestamp: moment().format(),
            }
        },
        inject: ['loading', 'showGuide'],
        created() {
            this.location = location;

            // var user_agent = window.navigator.userAgent.toLowerCase();
            // if (user_agent.indexOf('msie') != -1 || user_agent.indexOf('trident') != -1) {
            //     var ie_interval_i = 0;
            //     this.ie_interval = setInterval(() => {
            //         $(this.$el).find(".question-wrapper").css("position", ie_interval_i ? "relative" : "static");
            //         ie_interval_i = (ie_interval_i + 1) % 2;
            //     }, 10);
            // }
        },
        mounted() {

            this.loading.show();
            this.showQuestion().always(() => {
                this.loading.hide();
            });

            $(this.$el).on("click", ".link-tos", () => {
                this.$refs.tosConfirmPopup.show();
                return false;
            });

            // 全コンポーネントのマウント完了後
            Vue.nextTick(() => {
                this.checkStartTutorial();
            })
        },

        beforeDestroy() {

            // IEの不具合対策に使用していたintervalを終了
            // if (this.ie_interval) {
            //   clearInterval(this.ie_interval);
            // }

            // サジェスト一覧取得用のタイムアウトハンドラーを終了
            if (this.suggestTimeoutHandler) {
                clearTimeout(this.suggestTimeoutHandler);
            }
        },

        methods: {

            // チュートリアル表示チェック(初回アクセス時)
            checkStartTutorial() {
                if (this.tutorialStep == 0 && (CookieManager.get("top_tutorialed") == null)) {
                    this.nextTutorial();
                }
            },

            // チュートリアル表示
            nextTutorial() {
                // 必要なDOMが読み込まれているかチェック
                if ($(this.$el).find(".header-help").length == 0) return;
                if ($(this.$el).find(".header-menu").length == 0) return;

                switch (this.tutorialStep) {
                    case 0: {
                        this.tutorial = {
                            $wrapper: $("body"),
                            $target: $(this.$el).find(".header-help"),
                            size: 40,
                            message: this.voteClusteringOptions.languages.tutorial.helpButton
                        }
                        break;
                    }
                    case 1: {
                        this.tutorial = {
                            $wrapper: $("body"),
                            $target: $(this.$el).find(".header-menu"),
                            size: 50,
                            message: this.voteClusteringOptions.languages.tutorial.menuButton
                        }
                        break;
                    }
                    default: {
                        CookieManager.set("top_tutorialed", 1);
                        this.tutorial = null;
                    }
                }
                this.tutorialStep++;
            },

            clickMenuQuestion(question) {
                if (this.question.key != question.key && question.linkActive) {
                    this.$refs.menu.hide();

                    this.$refs.questionPage.validationCheck(false, false)
                        .always(() => {
                            this.questionList.forEach((x, i) => {
                                if (x.key == question.key) {
                                    this.questionIndex = i;
                                }
                            });
                            this.loading.show();
                            this.showQuestion().always(this.loading.hide);
                        })
                }
            },

            validatePromiseWrap(promise) {
                var valid_index = this.deferredValidIndex;
                return promise.then((result) => {
                    return $.Deferred((deferred) => {
                        if (valid_index !== this.deferredValidIndex) {
                            return deferred.reject("expired reject.");
                        }
                        deferred.resolve(result);
                    }).promise();
                });
            },

            prev() {
                if (this.questionIndex > 0) {
                    this.questionIndex--;
                    return this.showQuestion();
                }
            },

            next() {

                // 最終設問でなければ次の問題へ
                if (this.questionIndex + 1 < this.questionList.length) {
                    this.questionIndex++;
                    return this.showQuestion();

                } else {

                    // 回答をコールバック用に整理
                    const sendData = {
                        answer_list: {},
                        respondent_data: {
                            startTime: this.startTimestamp,
                        },
                    };
                    for (var question of this.questionList) {
                        var answer = question.getAnswer();
                        if (answer !== undefined) {
                            sendData.answer_list[question.key] = {
                                key: question.key,
                                type: question.type,
                                answer: answer,
                            };
                        }
                    }

                    // 最後の設問ならデータ送信を行い、完了したらサンクス画面を表示
                    this.loading.show();
                    this.voteClusteringOptions.endEnquete(sendData)
                        .then(() => {
                            this.question = new Question({
                                type: 'thanks',
                                question: this.languages.thanks.text,
                            });

                        })
                        .fail(() => {
                            alert(this.languages.sendFailed);
                        })
                        .always(() => {
                            this.loading.hide()
                        });
                }
            },

            showQuestion() {
                var question = this.questionList[this.questionIndex];
                this.viewedMaxIndex = Math.max(this.viewedMaxIndex, this.questionIndex);

                // メニューのリストステータス更新
                for (var i = 0; i < this.questionList.length; i++) {
                    this.questionList[i].linkActive = i <= this.viewedMaxIndex && i !== this.questionIndex;
                }

                // サジェスト一覧取得用のタイムアウトハンドラーを終了
                if (this.suggestTimeoutHandler) {
                    clearTimeout(this.suggestTimeoutHandler);
                }

                return this.voteClusteringOptions.nextQuestion(question)
                    .then((question) => {
                        $("body").scrollTop(0);
                        $(window).scrollTop(0);

                        this.deferredValidIndex = (this.deferredValidIndex + 1) % 10000;

                        // this.answer = JSON.parse(JSON.stringify(question.answer));
                        this.errorList = [];
                        this.question = question;
                        // 正規表現でURLを検出
                        this.question.question = xssFilters.inHTMLData(this.question.question);

                        const reg = new RegExp("((https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+))");
                        this.question.question = this.question.question
                                                    .replace(reg,"<a href='$1' target='_blank'>$1</a>")
                                                    .replace(/\r?\n/g, '<br />');

                        this.questionList[this.questionIndex] = question;

                        // 設問タイプによらない共通処理
                        $(this.$el).find(".body-scroller").scrollTop(0);

                        // 警告の表示状況をリセット
                        if (this.voteClusteringOptions.oneOpinionCautionEvery) {
                            this.oneOpinionCautioned = false;
                        }
                    });
            },
        },
        updated() {
            this.checkStartTutorial();
        },
    }
</script>

<style lang="scss" scoped>
    // ヘッダー部共通CSS
    .header {
        flex: 0 0 60px;
        width: 100%;
        height: 60px;
        background-color: #1E364B;
        position: relative;

        @include for-small {
            flex: 0 0 60px;
            height: 60px;
        }

        & > div {
            max-width: 950px;
            height: 100%;
            @include display-flex(row, space-between, center);
            margin: 0 auto;

            .header-menu {
                margin-left: 10px;
                width: 34px;
                cursor: pointer;
            }

            .header-logo-ja {
                flex: 0 1 200px;
                height: 100%;
                background-image: url(../image/logo_centering.png);
                background-position: center;
                background-size: contain;
                background-repeat: no-repeat;
            }

            .header-logo-en {
                flex: 0 1 200px;
                height: 100%;
                background-image: url(../image/logo_en.png);
                background-position: center;
                background-size: contain;
                background-repeat: no-repeat;
            }

            .header-help {
                width: 17px;
                margin: 0 18.5px 0 8.5px;

                cursor: pointer;
            }

            @include for-small {
                .header-menu {
                    margin-left: 14px;
                }

                .header-logo {
                    background-image: url(../image/logo_en.png);
                }

                .header-help {
                    width: 20px;
                    margin: 0 20px 0 10px;
                }
            }
        }
    }

    .question-component {
        width: 100%;
        height: 100%;
    }


    .page_question {
        background-color: #CDD6DC;
        justify-content: flex-start;
        height: auto;
        min-height: 100%;
        position: static;
        // min-height: $pc_height;

        @include for-small {
            background-color: #FFF;
            // min-height: auto;
            // height: 100%;
        }

        .body {
            position: relative;
            padding: 0 50px;

            @include for-small {
                padding: 0;
                @include display-flex(column, flex-start, stretch);
            }
        }

        .footer {
            flex: 0 0 100px;
        }

        .body-scroller {
            flex: 1 0 auto;
            @include display-flex(column, flex-start, center);
        }

        .body-header {
            flex: 0 0 60px;
            width: 100%;
            max-width: 920px;
            position: relative;

            .progress-outer {
                position: absolute;
                right: 10px;
                bottom: 14px;
                width: 200px;
                height: 6px;
                border-radius: 3px;
                background-color: #FFF;
            }

            .progress-inner {
                width: 30%;
                height: 6px;
                border-radius: 3px;
                background-color: #A5D601;
            }

            @include for-small {
                width: 100%;
                flex-basis: 70px;
                height: 70px;
                padding: 30px 40px;

                .progress-outer {
                    position: static;
                    width: 100%;
                    height: 10px;
                    border-radius: 5px;
                    background-color: rgb(221, 221, 221);
                }

                .progress-inner {
                    height: 10px;
                    border-radius: 5px;
                }
            }
        }

        .error-list {
            li {
                @include display-flex(row, flex-start, center);
                color: #F57789;
                min-height: 28px;

                &:before {
                    content: '';
                    display: inline-block;
                    width: 23px;
                    height: 21px;
                    margin-right: 5px;
                    background-image: url(../image/validation_error.svg);
                    background-size: contain;
                    background-repeat: no-repeat;
                    background-position: center;
                }
            }
        }
    }

    .carousel-pager {
        padding-top: 30px;
        margin-bottom: 30px;
    }

    // メニュー部
    .menu {
        display: none;
        position: fixed;
        top: 0;
        right: 0;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 100%;
        user-select: none;
        z-index: 100;

        ul {
            overflow-y: auto;
            -webkit-overflow-scrolling: touch;
            overflow-scrolling: touch;
            background-color: #0F1D29;
            color: #FFF;
            position: relative;

            li {
                width: 100%;
                padding: 20px 17px;
                position: relative;

                &.menu-home {
                    padding-top: 29px;
                    padding-bottom: 29px;
                    cursor: pointer;
                }

                &.menu-title {
                    padding-top: 12px;
                    padding-bottom: 12px;
                    background-color: #1E364B;
                }

                &.menu-item, &.menu-tos {
                    width: 100%;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    padding: 14px 17px;
                    cursor: pointer;

                    &:before {
                        content: '';
                        width: 12px;
                        height: 22px;
                        margin-right: 6px;
                        display: inline-block;
                        vertical-align: top;
                    }

                    &.menu-item_inactive {
                        opacity: 0.3;
                        cursor: default;
                    }

                    &.menu-item_checked:before {
                        background-image: url(../image/icon_check.svg);
                        background-size: contain;
                        background-repeat: no-repeat;
                        background-position: center;
                    }

                    &.disabled {
                        opacity: 0.3;
                    }
                }
            }
        }

        .menu-back {
            position: relative;

            .menu-close_button {
                width: 28px;
                height: 28px;
                margin: 13px 0 0 13px;
                position: relative;
                cursor: pointer;

                &:before, &:after {
                    content: '';
                    position: absolute;
                    top: 13px;
                    left: -5px;
                    width: 38px;
                    height: 2px;
                    border-radius: 1px;
                    background-color: #FFF;
                }

                &:before {
                    transform: rotateZ(45deg);
                }

                &:after {
                    transform: rotateZ(-45deg);
                }
            }
        }

        &.menu_show {
            @include display-flex(row, flex-start, stretch);

            &:before {
                position: absolute;
                top: 0;
                right: 0;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 100%;
                content: '';
                display: block;
                background-color: rgba(0, 0, 0, 0.6);
            }

            ul {
                flex: 0 1 300px;
                animation: leftSlide .2s;
            }

            .menu-back {
                flex: 1 0 50px;
                animation: leftSlide .2s;
            }
        }
    }

    @include keyframes(leftSlide) {
        0% {
            left: -300px;
        }

        100% {
            left: 0;
        }
    }

    /deep/ .popup-tos {
        line-height: 30px;

        h1 {
            width: 100%;
            font-size: 30px;
            line-height: 120px;
            text-align: center;

            @include for-small {
                line-height: 80px;
            }
        }

        h2 {
            padding: 0 19px;
            margin-top: 50px;

            border-radius: 18px;
            line-height: 35px;
            font-size: 16px;

            color: #1E364B;
            background-color: rgba(150, 169, 178, 0.5);
        }

        ul, ol {
            padding-left: 1.6em;
        }

        ul > li {
            list-style-type: disc;
        }

        ol > li {
            list-style-type: decimal;
        }

        i {
            font-style: italic;
        }
    }

    .confirm-popup {
        width: 320px;
        position: relative;

        & > div.confirm-popup-body {
            padding: 30px 30px;
            @include display-flex(column, space-around, center);
            min-height: 130px;
            font-size: 18px;
            line-height: 35px;
            position: relative;

            color: #FFF;
            background-color: #389CBA;
            text-align: center;

            @include for-small {
                padding: 30px 10px;
            }

            &:before {
                position: absolute;
                top: -14px;
                left: 10px;
                width: 37px;
                height: 37px;
                content: '!';
                font-size: 30px;
                line-height: 37px;
                font-weight: 700;
                border-radius: 19px;

                color: #4CB5D5;
                background-color: #FFF;
            }

            .confirm-popup-buttons {
                margin-top: 20px;
                @include display-flex(row, space-around, center);

                button {
                    border: 1px #FFF solid;
                    color: #FFF;
                    border-radius: 0;
                    padding: 0 10px;
                    margin: 0 10px;
                    white-space: nowrap;
                }

                @include for-small {
                    @include display-flex(column-reverse, center, center);

                    button {
                        width: 100%;
                        margin: 10px 0;
                    }
                }
            }
        }

        .close {
            position: absolute;
            @include display-flex(column, center, center);
            top: 0;
            right: 0;
            width: 34px;
            height: 34px;
            background-color: #1E364B;
            cursor: pointer;
        }
    }

    .question-confirm-popup {
        z-index: auto;

        & > div.confirm-popup-body {
            background-color: #F57789;

            &:before {
                color: #F57789;
            }
        }

        .close {
            background-color: rgb(214, 88, 106);
        }
    }

    .confirm-popup_show {
        @include display-flex(row, center, center);
        animation: fadeIn 0.1s;
    }

    /deep/ .link-tos {
        border-bottom: 1px #00A8E1 solid;
    }

    @include for-small {
        .page_question {
            min-width: auto;
        }
    }

    .pager {
        position: fixed;
        left: 0;
        top: 0;
        right: 0;
        width: 100%;
        height: 0;


        & > div {
            width: 100%;
            max-width: 1020px;
            margin: 0 auto;
            position: relative;

            & > div {
                position: absolute;
                @include display-flex(column, center, center);
                top: 60px;
                width: 50px;
                height: calc(100vh - 60px);
                max-height: 620px;

                & > img {
                    cursor: pointer;
                }

                &.left {
                    left: 0;
                }

                &.right {
                    right: 0;
                }
            }
        }

        @include for-small {
            display: none;
        }
    }
</style>
