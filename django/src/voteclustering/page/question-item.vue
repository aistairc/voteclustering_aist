<template>
    <div class="question-main">

        <!-- 設問文 -->
        <div class="question-sentence">
            <img src="../image/icon.png" class="question-sentence-icon">
            <!--<h1 class="question-sentence-text">{{ question.question }}</h1>-->
            <h1 class="question-sentence-text" v-html="question.question"></h1>
        </div>

        <div class="answer-area"
             :class="{gray: question.type == 'question' || question.type == 'longtext' || question.type == 'longtext-multi'}">

            <!-- 1行入力型設問 -->
            <div v-if="question.type == 'singletext'" class="question-type-area singletext">
                <input-ex type="text" v-model="answer" class="question-answer" :hasError="errorList.length"
                          :placeholder="question.placeholder" :maxLength="voteClusteringOptions.selfOpinion.maxLength"/>
                <ul v-if="errorList.length" class="error-list">
                    <li v-for="error in errorList">{{ error }}</li>
                </ul>
            </div>

            <!-- ユーザーID入力型設問 -->
            <div v-if="question.type == 'userid'" class="question-type-area userid">
                <input-ex type="text" v-model="answer" class="question-answer" :hasError="errorList.length"
                          :placeholder="question.placeholder" :maxLength="voteClusteringOptions.selfOpinion.maxLength"/>
                <ul v-if="errorList.length" class="error-list">
                    <li v-for="error in errorList">{{ error }}</li>
                </ul>
            </div>

            <!-- 複数行入力 -->
            <div v-if="question.type == 'longtext'" class="question-type-area question-type-area_longtext">
                <h2><span v-html="languages.longtext.description"></span></h2>
                <question-opinion-free v-model="answer" :question="question" mode="single"></question-opinion-free>
                <ul v-if="errorList.length" class="error-list">
                    <li v-for="error in errorList">{{ error }}</li>
                </ul>
            </div>

            <!-- 複数行入力(複数) -->
            <div v-if="question.type == 'longtext-multi'" class="question-type-area question-type-area_longtext">
                <h2><span v-html="languages.longtext.description"></span></h2>

                <div class="opinion-list">
                    <template v-for="(opinion, index) in question.opinionList">
                        <question-opinion-item :key="index" v-model="question.opinionList[index]" :question="question"
                                               @delete='deleteSelfOpinion(index)'/>
                    </template>
                </div>

                <question-opinion-free :question="question" @add="x => addFree(x)"></question-opinion-free>
            </div>

            <!-- 単一/複数選択型設問 -->
            <div v-if="question.type == 'single' || question.type == 'multi'" class="question-type-area"
                 :class="['question-type-area_' + question.type, {'question-type-area_single_few': question.choices.length <= 3}]">
                <div v-for="choice in question.choices" class="question-choice-wrapper">
                    <div class="question-choice-num" v-if="question.with_answered_num">{{
                        languages.answeredNum.replace("*N*", choice.answered_num || 0) }}
                    </div>
                    <button class="question-choice" :class="{ active: answer[choice.key] }"
                            @click="clickChoice(choice)">{{ choice.label || choice.key }}
                    </button>
                </div>
            </div>

            <!-- 意見選択＆自由入力設問 -->
            <div v-if="question.type == 'question' && answer.select"
                 class="question-type-area question-type-area_question">

                <h2><span v-html="languages.question.description"></span></h2>

                <!-- みんなの意見一覧 -->
                <div class="opinion-list">
                    <template v-for="(opinion, index) in question.opinionList">
                        <question-opinion-item :key="index" v-model="question.opinionList[index]" :question="question"
                                               @delete='deleteSelfOpinion(index)'/>
                    </template>
                </div>

                <!-- もっと見るボタン＆ローディング表示 -->
                <div v-if="!question.without_select" class="opinion-more-wrapper">
                    <question-opinion-more @click="loadOpinion" :disabled="!question.more"
                                           :style="{visibility: opinionLoading ? 'hidden' : 'visible'}"/>
                    <div v-if="opinionLoading" class="opinion-loading">{{ languages.opinionLoading }}</div>
                </div>

                <!-- 自由記入欄 -->
                <question-opinion-free :question="question" @add="x => addFree(x)"></question-opinion-free>
            </div>

            <!-- 利用規約ページ -->
            <div v-if="question.type == 'tos'" class="question-type-area question-type-area_tos">
                <h2>あなたの回答</h2>
                <hr>
                <template v-for="subQuestion in questionList" v-if="subQuestion.type != 'tos'">
                    <h3 v-html=addQ(subQuestion.question)></h3>
                    <template
                        v-if="subQuestion.type == 'userid' || subQuestion.type == 'singletext' || subQuestion.type == 'longtext'">
                        <p>{{ subQuestion.answer }}</p>
                    </template>
                    <template v-if="subQuestion.type == 'longtext-multi'">
                        <ul>
                            <li v-for="answer in subQuestion.answer">{{ answer }}</li>
                        </ul>
                    </template>
                    <template v-if="subQuestion.type == 'single' || subQuestion.type == 'multi'">
                        <template v-for="choice in subQuestion.choices" v-if="subQuestion.answer[choice.key]">
                            <p>{{ choice.label }}</p>
                        </template>
                    </template>
                    <template v-if="subQuestion.type == 'question'">
                        <template v-if="!subQuestion.without_select">
                            <label class="agree"><img src="../image/question/heart.svg">いいねした回答</label>
                            <ul v-if="subQuestion.opinionList.filter(x => x.select).length">
                                <li v-for="opinion in subQuestion.opinionList" v-if="opinion.select">{{ opinion.text
                                    }}
                                </li>
                            </ul>
                            <p v-else>なし</p>
                        </template>
                        <template v-for="free in subQuestion.answer.free">
                            <label v-if="!subQuestion.without_select" class="free">投稿</label>
                            <p>{{ free }}</p>
                        </template>
                    </template>
                    <hr>
                </template>
                <label class="question-checkbox-label"><input type="checkbox" v-model="answer"><span
                    v-html="languages.tos.agree"></span></label>
            </div>

            <!-- サンクスページ -->
            <div v-if="question.type == 'thanks'" class="question-type-area question-type-area_thanks">
                <button type="button" class="question-button-home" @click="$emit('finish')">{{ languages.thanks.back
                    }}
                </button>
            </div>

            <!-- カルーセル -->
            <carousel-pager v-if="questionIndex < questionList.length - 1" :index="questionIndex"
                            :max="questionList.length - 1" class="for-small"/>

            <!-- 次へボタン -->
            <div v-if="question.type != 'thanks'" class="question-buttons">
                <button type="button" class="skip" @click="next(true)" v-if="question.skippable !== false">skip</button>
                <button type="button" class="next" @click="next(false)" data-enter :disabled="!nextable">{{
                    question.last ? languages.nextLast : languages.next }}
                </button>
            </div>
        </div>

        <!-- 意見選択数警告ポップアップ -->
        <popup ref="minLikeConfirmPopup" class="custom-design">
            <div class="confirm-popup question-confirm-popup">
                <div class="confirm-popup-body">
                    <p v-html="languages.minLikeConfirm.point1.replace('*N*', Object.values((answer || {}).select || {}).filter(x => x).length)"></p>
                    <p v-html="languages.minLikeConfirm.point2.replace('*N*', question.min_like_required || voteClusteringOptions.defaultMinLikeRequired || 1)"></p>
                </div>
                <div class="close" @click="$refs.minLikeConfirmPopup.hide()"><img src="../image/icon-cross.svg"></div>
            </div>
        </popup>

        <!-- 自分の意見削除確認ポップアップ -->
        <nonscroll-popup ref="deletePopup" class="delete-popup short">
            <button @click="removeArrayItem(question.opinionList, deleteSelfOpinionIndex); $refs.deletePopup.close();"
                    class="important"><img src="../image/icon-delete.svg">{{ languages.selfOpinion.delete }}
            </button>
            <button @click="$refs.deletePopup.close()">{{ languages.selfOpinion.deleteCancel }}</button>
        </nonscroll-popup>
    </div>
</template>

<script>
    import Question from '../data/question.js';

    export default {
        props: {
            'question': {required: true},
            'questionIndex': {required: true},
            'questionList': {required: true},
        },
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions, // 設定
                languages: voteClusteringOptions.languages.question, // 言語セット

                errorList: [], // エラー一覧
                opinionLoading: false,

                answer: {}, // 現在の設問の回答(スキップ時はanswersに格納しない)
                oneOpinionCautioned: false, // 1つしか意見を選択していない警告を表示したかどうか
                deferredValidIndex: 0, // deferred系有効値チェック(ページ遷移時に現在実行しているdeferredを無効化するためのインデックス)
                suggestTimeoutHandler: null, // サジェスト一覧取得用タイムアウトハンドラー

                deleteSelfOpinionIndex: 0,
            }
        },
        inject: ['loading', 'showGuide'],
        watch: {
            'question': {
                handler() {
                    this.oneOpinionCautioned = false;
                    this.answer = JSON.parse(JSON.stringify(this.question.answer));
                    this.errorList = [];

                    // 意見選択型の質問の場合
                    if (this.question.type == "question") {

                        // まだ初回問い合わせが終わっていなければ問い合わせ、そうでなければキャッシュから表示
                        if (this.question.opinionList == null || this.question.opinionList.length == 0) {
                            this.loadOpinion();

                        } else {
                            this.question.opinionList.forEach((x, i) => {
                                Vue.set(x, 'highlight', false);
                            });
                        }
                    }
                },
                immediate: true
            },

            'question.opinionList': {
                handler() {
                    switch (this.question.type) {
                        case 'longtext-multi':
                            this.answer = this.question.opinionList.filter(x => x.key == null && x.text).map(x => x.text);
                            break;

                        case 'question':
                            Vue.set(this.answer, 'select', {});
                            // 既に存在する選択肢への回答を集計
                            this.question.opinionList.filter(x => x.key != null).forEach(x => {
                                const isSelected = x.select ? true : false;
                                Vue.set(this.answer.select, x.key, isSelected);
                            });
                            // 新規に選択肢を提案した場合はそれらを集計
                            Vue.set(this.answer, 'free', this.question.opinionList.filter(x => x.key == null && x.text).map(x => x.text));
                            break;
                    }
                },
                deep: true
            },

            nextable: {
                handler() {
                    this.$emit('nextable', this.nextable);
                },
                immediate: true,
            }
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
        computed: {
            nextable() {
                return this.question.isAnswered(this.answer);
            }
        },

        methods: {

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

            prev(skip = false) {
                this.move("prev", skip);
            },

            next(skip = false) {
                this.move("next", skip);
            },

            move(mode, skip) {

                // 入力されていないのにmoveが呼ばれた時もskip扱い
                skip = skip || !this.question.isAnswered(this.answer);

                // ローディング表示、バリデーションチェック
                this.loading.show();
                this.validationCheck(!skip)
                    .done(() => {
                        this.loading.hide()
                        this.question.answer = this.answer;
                        // this.$emit('input', this.answer);
                        this.$emit(mode);
                    })
                    .fail(() => {
                        this.loading.hide()
                        if (skip) {
                            this.$emit(mode);
                        }
                    });
            },

            /**
             * バリデーションチェック
             * @function validationCheck
             * @return {Bool} true:成功 / false:失敗
             * @memberof voteclustering.page.Question
             */
            validationCheck(show_error) {
                show_error = show_error === undefined ? true : show_error;

                // 次へボタンが押せない状態ならリジェクト
                if (!this.question.isAnswered(this.answer)) {
                    return resolver();
                }

                // バリデーションチェック
                return this.voteClusteringOptions.validationCheck(this.question, this.answer)
                    .then(() => {
                        if (this.voteClusteringOptions.selfOpinion.maxLength && typeof this.answer === 'string' && this.answer.length > this.voteClusteringOptions.selfOpinion.maxLength) {
                            var d = $.Deferred();
                            d.reject(["自由入力は" + this.voteClusteringOptions.selfOpinion.maxLength + "文字までです"]);
                            return d.promise();
                        }
                    })
                    .then(() => {

                        // エラーはないが、意見選択の設問で選択数が閾値に達していない場合は一度警告を出す
                        var min_like_required = this.question.min_like_required || this.voteClusteringOptions.defaultMinLikeRequired || 1;

                        if (this.question.type == "question") {
                            const answer_length = Object.values(this.answer.select).filter(x => x).length;
                            if (answer_length < min_like_required && this.answer.free.length === 0 && !this.oneOpinionCautioned) {
                                this.$refs.minLikeConfirmPopup.show();
                                this.oneOpinionCautioned = true;
                                return rejector();
                            }
                        }

                        this.question.answer = this.answer;

                    }, (error_list) => {

                        if (show_error) {
                            // エラーが存在する場合はエラー表示
                            this.errorList = error_list;

                            // ページ末尾までスクロールする(エラー表示箇所が末尾のため)
                            var $body_scroller = $(this.$el).find(".body-scroller");
                            if ($body_scroller.get(0)) {
                                $body_scroller.scrollTop($body_scroller.get(0).scrollHeight - $body_scroller.height());
                            }
                        }

                        return rejector();
                    });
            },

            loadOpinion() {
                this.opinionLoading = true;
                var nowIndex = this.question.id;

                var $promise = this.validatePromiseWrap(this.voteClusteringOptions.loadOpinion(
                    this.question,
                    this.question.opinionList.map(x => x.key),
                    this.question.suggestList.map(x => x.key)
                ))
                    .then((result) => {
                        this.opinionLoading = false;

                        if (nowIndex === this.question.id) {

                            this.question.opinionList.forEach((x, i) => {
                                x.highlight = false;
                            });

                            var first = this.question.opinionList.length == 0;
                            for (var item of result.list) {
                                Vue.set(item, 'highlight', true);
                                Vue.set(item, 'first', first);
                            }

                            Vue.set(this.question, 'opinionList', this.question.opinionList.concat(result.list));
                            Vue.set(this.question, 'more', result.more);
                        }
                    });
            },

            clickChoice(clickChoice) {
                if (this.question.type == 'single') {
                    for (var choice of this.question.choices) {
                        this.answer[choice.key] = clickChoice.key == choice.key;
                    }
                } else {
                    this.answer[clickChoice.key] ^= true;
                }
            },

            addFree(free) {
                switch (this.question.type) {
                    case 'longtext-multi':
                        if (!Array.isArray(this.answer)) {
                            this.answer = [];
                        }
                        if (free.length > 0) {
                            this.question.opinionList.push({
                                text: free
                            })
                        }
                        break;

                    case 'question':
                        if (!Array.isArray(this.answer.free)) {
                            this.answer.free = [];
                        }
                        if (free.length > 0) {
                            this.question.opinionList.forEach((opinion) => {
                                Vue.set(opinion, 'highlight', false);
                            });
                            this.question.opinionList.push({
                                highlight: true,
                                text: free
                            })
                        }
                        break;
                }
            },

            // @vuese
            // 自由記入欄削除(削除インデックスを記憶しておき、確認ポップアップを表示)
            deleteSelfOpinion(index) {
                this.deleteSelfOpinionIndex = index;
                this.$refs.deletePopup.show();
            },

            addQ(questionText){
                var urlText = 'Q. ' + questionText;
                
                return urlText;
            },
        },


    }
</script>

<style lang="scss" scoped>
    .answer-area {
        flex: 1 1 auto;
        @include display-flex(column, flex-start, center);
        width: 100%;
        margin-top: 50px;

        &.gray {
            background-color: rgba(#CDD6DC, 0.4);
        }
    }

    .question-main {
        flex: 1 0 auto;
        @include display-flex(column, flex-start, center);
        width: 100%;
        max-width: 920px;
        margin-top: 40px;
        // margin-bottom: 40px;
        min-height: 600px;

        border-radius: 10px;
        background-color: #FFF;
        padding-top: 50px;

        @include for-small {
            @include display-flex(column, flex-start, stretch);
            width: 100%;
            padding: 0;
            margin-bottom: 0;
            min-height: auto;
            border-radius: 0;
        }
    }

    .question-sentence {
        width: 100%;
        @include display-flex(row, center, center);

        @include for-small {
            padding: 0 20px;
        }

        .question-sentence-icon {
            height: 60px;
            margin-left: 4px;

            @include for-small {
                height: 48px;
            }
        }

        .question-sentence-text {
            width: 600px;
            border-radius: 5px;
            background-color: #F2F2F2;
            padding: 22px 42px;
            position: relative;
            margin-left: 24px;
            font-size: 18px;
            word-break: break-all;

            &:before {
                content: '';
                position: absolute;
                top: 50%;
                left: 0;
                bottom: auto;
                right: auto;
                width: 30px;
                height: 30px;
                margin: -15px 0 0 -8px;
                background-color: #F2F2F2;

                transform: scaleY(0.7) rotateZ(45deg);
            }

            @include for-small {
                flex: 1 0 auto;
                width: 1px;
                padding: 22px 27px;
                margin-left: 18px;
            }
        }
    }

    .question-buttons {
        @include display-flex(row, center, center);
        width: 100%;
        margin-bottom: 40px;

        .skip {
            width: 83px;
            height: 60px;
            margin-right: 10px;

            border-color: #96A9B2;
            color: #96A9B2;
        }

        .next {
            width: 210px;
            height: 60px;

            background-color: #1E364B;
            color: #FFF;
            font-size: 20px;

            &:disabled {
                background-color: #DDDDDD;
            }
        }

        .question-button-next_last {
            background-color: #00A8E1;
        }

        @include for-small {
            padding: 15px;
            margin-bottom: 0;

            background-color: #FFF;

            .skip, .next {
                height: 70px;
            }

            .next {
                flex: 1 0 auto;
            }
        }
    }

    .question-type-area {
        width: 100%;
        min-height: 320px;
        padding-top: 50px;
        padding-bottom: 20px;

        @include for-small {
            min-height: auto;
            padding-bottom: 10px;
            flex: 1 0 auto;
        }

        &.singletext, &.userid {
            width: 400px;
            padding-top: 40px;

            @include for-small {
                width: 100%;
                padding: 0px 38px;
            }

            .input-ex {
                display: block;
                width: 100%;
                height: 50px;
                margin: 0 auto;

                @include for-small {
                    border-width: 2px;
                    height: 70px;
                }
            }
        }
    }

    .question-type-area_single, .question-type-area_multi, .question-type-area_tos {
        @include display-flex(row, flex-start, flex-start);
        align-content: center;
        flex-wrap: wrap;

        width: 670px;
        padding-top: 0;

        .question-choice-wrapper {
            width: 210px;
            margin-right: 20px;
            margin-bottom: 20px;
        }

        @include for-non-small {
            .question-choice-wrapper:nth-child(3n) {
                margin-right: 0;
            }
        }

        .question-choice-num {
            text-align: center;
            font-size: 14px;
            line-height: 38px;

            &:before {
                content: '＼';
                margin-right: 27.5px;
            }

            &:after {
                content: '／';
                margin-left: 27.5px;
            }
        }

        button {
            width: 210px;
            height: 60px;

            border: 2px #DDDDDD solid;
            box-shadow: 0 2px 0 0 #96A9B2;
            position: relative;

            &:active, &.active {
                box-shadow: none;
                top: 2px;
            }

            &.active {
                background-color: #00A8E1;
                border: none;
                color: #FFF;
            }
        }

        @include for-small {
            @include display-flex(row, flex-start, flex-start);
            align-content: flex-start;
            padding: 0px 18px 15px;
            width: 100%;

            .question-choice-wrapper {
                @include display-flex(column-reverse, flex-start, flex-end);
                width: 48%;
                margin-right: 4%;

                button {
                    width: 100%;
                    height: 70px;
                    border-radius: 10px;
                }
            }

            .question-choice-wrapper:nth-child(2n) {
                margin-right: 0;
            }

            .question-choice-num {
                text-align: right;

                &:before, &:after {
                    content: none;
                }
            }
        }
    }

    .question-type-area_single_few {
        @include display-flex(row, center, flex-start);

        @include for-small {
            @include display-flex(column, flex-start, center);
            padding: 30px 37px;
            width: 100%;

            .question-choice-wrapper {
                width: 100%;
                margin-right: 0;

                button {
                    width: 100%;
                    border-radius: 10px;
                }
            }
        }
    }

    .question-type-area_tos {
        margin: 0 auto;
        width: 75%;
        align-self: stretch;
        padding-top: 0;
        @include display-flex(column, center, flex-start);

        @include for-small {
            width: 100%;
            margin: 0;
            padding: 0 20px;
        }

        h2 {
            font-size: 16px;
            font-weight: bold;
        }

        h3 {
            margin-bottom: 16px;
        }

        hr {
            width: 100%;
            align-self: stretch;
            border: none;
            border-top: 1px #DDD solid;
            margin: 16px 0;
        }

        label.agree {
            margin-left: 1.5em;
            vertical-align: bottom;

            img {
                width: 1em;
                margin-right: 0.3em;
            }
        }

        p {
            margin-left: 1.5em;
            white-space: pre-wrap;
            word-break: break-all;
        }

        ul {
            margin-left: 1.5em;
            list-style: disc;

            li {
                margin-left: 1.3em;
                white-space: pre-wrap;
                word-break: break-all;
            }
        }

        label.free {
            margin-top: 15px;
            margin-bottom: 5px;
            margin-left: 1.5em;
            background-color: #00A8E1;
            color: #FFF;
            padding: 3px 11px;
            font-size: 14px;
            line-height: 1;
        }

        .question-checkbox-label {
            margin: 2em 0 1.5em;
            align-self: center;
        }
    }

    .question-type-area_question, .question-type-area_longtext {
        @include display-flex(column, flex-start, center);

        margin-top: 50px;
        padding-top: 30px;

        @include for-small {
            margin: 0;
            border-radius: 0;
        }

        h2 {
            @include display-flex(row, center, flex-start);
            width: 100%;
            margin-bottom: 10px;
            padding: 0 24px;
            text-align: center;
            font-size: 18px;

            span {
                text-align: left;
            }

            /deep/ strong {
                background-color: #F3FA22;
            }

            &:before {
                flex: 0 0 26px;
                content: '';
                display: inline-block;
                width: 26px;
                height: 25px;
                background-image: url(../image/question/balloon_icon.svg);
                background-size: contain;
                background-position: center;
                background-repeat: no-repeat;
                vertical-align: bottom;
                margin-right: 8px;
            }
        }

        // みんなの意見ラッパー
        .opinion-list {
            @include display-flex(column, flex-start, center);

            @include for-small {
                width: 100%;
                padding: 0 10px 0 10px;
            }
        }

        // 読み込み中
        .opinion-more-wrapper {
            width: 100%;
            position: relative;

            @include for-small {
                padding: 0 10px 0 10px;
            }

            .opinion-loading {
                @include display-flex(column, center, center);
                position: absolute;
                top: 0;
                right: 0;
                bottom: 0;
                left: 0;
                pointer-events: none;

                &:before {
                    content: '';
                    display: block;
                    width: 32px;
                    height: 32px;
                    margin-bottom: 8px;
                    background-image: url(../image/loading_light.gif);
                    background-size: contain;
                    background-position: center;
                    background-repeat: no-repeat;
                }

                font-size: 11px;
            }
        }

        // 自由入力
        .opinion-free {
            @include for-small {
                padding: 0 10px 0 10px;
            }
        }
    }

    .question-type-area_longtext {
        margin-top: 0;
    }

    .question-type-area_thanks {
        @include display-flex(column, center, center);

        @include for-small {
            justify-content: flex-end;
            padding-bottom: 38px;
        }

        .question-button-home {
            width: 210px;
            height: 70px;

            border: none;
            background-color: #96A9B2;
            color: #FFF;

            @include for-small {
                width: auto;
                align-self: stretch;
                margin: 0 38px;
            }
        }
    }

    .carousel-pager {
        margin-top: 15px;
        margin-bottom: 15px;
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

    .delete-popup {
        /deep/ .scroller {
            @include display-flex(column, center, stretch);
        }

        button {
            @include display-flex(row, center, center);
            height: 60px;
            border: 1px #9F9F9F solid;
            color: #9F9F9F;
            border-radius: 5px;
            margin: 12px 20px;
            font-size: 18px;

            &.important {
                border: 1px #FF003B solid;
                color: #FF003B;
            }

            img {
                margin-right: 0.5em;
            }
        }
    }
</style>
