<template>
    <lockable-div class="component" ref="loading">
        <div class="page_wrapper">
            <transition :name="transition_mode == 'next' ? 'next' : 'prev'">
                <top v-if="state == 1" @next="next(2)"></top>
                <question v-if="state == 2" v-model="questionList" @prev="prev(1)" @next="next(2)"
                          @finish="finish()"></question>
            </transition>
        </div>

        <popup ref="help">
            <div class="popup-guide">
                <div class="popup-header-band">
                    <span class="popup-header-help"></span>
                    <h2>{{ guideLanguage.title }}</h2>
                    <p>
                        {{ guideLanguage.point1 }}<br>
                        {{ guideLanguage.point2 }}
                    </p>
                </div>
                <div class="popup-body">
                    <div>
                        <div class="popup-guide-image-box"><img src="./image/guide/illust1.svg"></div>
                        <h2>{{ guideLanguage.likeTitle }}</h2>
                        <p class="for-nonsmall" v-html="guideLanguage.likeText"></p>
                        <p class="for-small" v-html="guideLanguage.likeTextForSP"></p>
                    </div>
                    <div class="popup-guide-plus">
                        <img src="./image/guide/plus.svg">
                    </div>
                    <div>
                        <div class="popup-guide-image-box"><img src="./image/guide/illust2.svg"></div>
                        <h2>{{ guideLanguage.writeTitle }}</h2>
                        <p class="for-nonsmall" v-html="guideLanguage.writeText"></p>
                        <p class="for-small" v-html="guideLanguage.writeTextForSP"></p>
                    </div>
                </div>
            </div>
        </popup>

    </lockable-div>
</template>

<script>
    import Question from './data/question.js';

    export default {
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions,
                guideLanguage: voteClusteringOptions.languages.guidePopup,
                questionList: [],
                transition_mode: "next",
                state: 1,
                question: {
                    opinionList: [],
                    selfOpinionList: [],
                    moreOpinion: true,
                    opinionLoading: false,
                    opinionAdded: false,
                },
            }
        },
        provide: function () {
            return {
                loading: {show: this.showLoading, hide: this.hideLoading},
                showGuide: this.showGuide,
            };
        },
        created() {
            this.reset();
        },
        methods: {

            // 回答状態等をリセット
            reset() {
                this.questionList = voteClusteringOptions.questionList.slice().concat([{
                    key: "tos",
                    question: voteClusteringOptions.languages.question.tos.title,
                    type: 'tos',
                    choices: [{key: 1, label: voteClusteringOptions.languages.question.tos.agree}],
                    non_menu: true,
                    skippable: false
                }]).map(x => {
                    return new Question(x);
                });

                Vue.set(this.questionList[this.questionList.length - 1], 'last', true);
            },

            // 前のページへ遷移
            prev(state) {
                this.transition_mode = "prev";
                this.state = state;
            },

            // 次のページへ遷移
            next(state) {
                this.transition_mode = "next";
                this.state = state;
            },
            showLoading() {
                this.$refs.loading && this.$refs.loading.show();
            },
            hideLoading() {
                this.$refs.loading && this.$refs.loading.hide();
            },
            showGuide() {
                this.$refs.help.show();
            },

            finish() {
                // DBの変更を反映するにはリロードの必要があるためHOMEに戻るときにリロード
                location.reload();
                // this.reset();
                // this.state = 1;
            },
        },
    }
</script>

<style lang="scss" scoped>
    .component {
        width: 100%;
        height: 100%;
        position: relative;
    }

    .page_wrapper {
        width: 100%;
        height: 100%;
        position: relative;

        & > * {
            opacity: 1;
            z-index: 0;
            transition: opacity .3s ease;
            will-change: opacity;

            &.next-enter-active, &.prev-enter-active {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
            }

            &.next-enter-active,
            &.next-leave-active {
            }

            &.prev-enter-active,
            &.prev-leave-active {
            }

            &.next-enter,
            &.prev-leave-to {
                opacity: 0;
                z-index: 1;
                // top: 100%;
            }

            &.prev-enter,
            &.next-leave-to {
                opacity: 0;
                z-index: -1;
                // top: -100%;
            }
        }
    }

    .help {
        position: fixed;
        top: 10px;
        right: 10px;
        width: 30px;
        height: 30px;
        border-radius: 15px;
        background-color: #1FC4F5;
        padding-top: 6px;
        cursor: pointer;
        z-index: 3;

        color: white;
        font-size: 20px;
        text-align: center;
        line-height: 20px;
        font-weight: bold;

        @media only screen and (min-width: 940px) {
            right: 50%;
            margin-right: -460px;
        }
    }

    /* 投稿方法ポップアップ */
    .popup-guide {
        height: 100%;
        max-height: 550px;

        .popup-body {
            padding-top: 140px;
            padding-bottom: 40px;
            width: 100%;
            height: 100%;
            @include display-flex(row, center, center);

            & > div {
                @include display-flex(column, center, center);

                & > .popup-guide-image-box {
                    @include display-flex(column, center, center);
                    height: 123px;
                }

                & > h2 {
                    font-size: 20px;
                    margin: 12px 0;
                }

                & > p {
                    height: 88px;
                    font-size: 16px;
                    text-align: center;
                }
            }

            .popup-guide-plus {
                margin: 0 67px 90px;
            }

            @include for-small {
                flex: 1 0 auto;
                margin: 30px 0 30px 0;
                padding: 0;
                @include display-flex(column, center, center);
                display: block;

                .popup-guide-plus {
                    width: 90%;
                    @include display-flex(row, center, center);
                    margin: 40px auto 20px;

                    &:before,
                    &:after {
                        flex: 1 0 auto;
                        width: 1px;
                        height: 1px;
                        content: '';
                        display: block;

                        background-color: #707070;
                    }

                    & > img {
                        margin: 0 13px;
                    }
                }

                & > div {
                    flex: 1 0 auto;
                    // height: 300px;

                    & > p {
                        height: auto;
                    }
                }

                &:after {
                    flex: 1 0 30px;
                    width: 100%;
                    height: 30px;
                    content: '';
                    display: block;
                }
            }
        }
    }
</style>
