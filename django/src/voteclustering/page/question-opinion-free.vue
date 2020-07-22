<template>
    <question-opinion-base class="opinion-free shadow-none tail-upper icon-above"
                           :class="{caution: free.length >= voteClusteringOptions.selfOpinion.lengthCautionThreshold}">

        <template v-slot:above>
            <transition name="fade">
                <div class="sp-point for-small"
                     v-if="free.length >= voteClusteringOptions.selfOpinion.lengthCautionThreshold && focusing">
                    ※回答は複数投稿可能です。ポイントごとに分けて投稿してください。
                </div>
            </transition>
        </template>

        <template v-slot:icon>
            <div class="icon">
                <img src="../image/question/free.svg">
            </div>
        </template>
        <template v-slot:content>
            <div class="content">
                <div class="opinion-free-area" :class="['mode-' + mode]">
                    <input-ex type="textarea" v-model="free"
                              :placeholder="question.type == 'question' ? languages.question.placeholder : languages.longtext.placeholder"
                              :maxLength="voteClusteringOptions.selfOpinion.maxLength" @focus="focusing = true"
                              @blur="focusing = false"/>
                    <div class="buttons" v-if="mode == 'multi'">
                        <button class="cancel" @click="free = ''">{{ languages.selfOpinion.cancelButton }}</button>
                        <button class="add" @click="add"
                                :disabled="free.length == 0 || (voteClusteringOptions.selfOpinion.maxLength && free.length > voteClusteringOptions.selfOpinion.maxLength)">
                            {{ languages.selfOpinion.addButton }}
                        </button>
                    </div>
                </div>
            </div>
        </template>
        <template v-slot:contentAfter v-if="mode == 'multi'">
            <div class="point">{{ languages.selfOpinion.multiPoint }}</div>
            <div class="suggest" v-if="question.suggestList.length">
                <header>{{ languages.selfOpinion.suggest }}</header>
                <ul>
                    <li v-for="opinion in question.suggestList" @click="clickSuggest(opinion)">{{ opinion.text }}</li>
                </ul>
            </div>
        </template>

    </question-opinion-base>
</template>

<script>
    export default {
        props: {
            value: {type: String, default: ''},
            question: {type: Object, default: {}},
            mode: {type: String, default: 'multi'}
        },
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions,         // 設定
                languages: voteClusteringOptions.languages.question,  // 言語セット

                free: "",
                focusing: false,
            }
        },
        created() {
            this.suggestTimeoutHandler = null;
        },
        methods: {
            add() {
                this.$emit('add', this.free);
                this.free = '';
            },
            clickSuggest(clickSuggest) {
                var targetOpinion = null;

                this.question.opinionList.forEach((opinion) => {
                    opinion.highlight = false;
                    if (opinion.key == clickSuggest.key) {
                        targetOpinion = opinion;
                    }
                });

                if (!targetOpinion) {
                    targetOpinion = clickSuggest;
                    Vue.set(targetOpinion, 'highlight', true);
                    this.question.opinionList.push(targetOpinion);
                }

                // 選択状態にする
                Vue.set(targetOpinion, 'select', true);
                this.free = "";
            }
        },
        watch: {
            value: {
                handler() {
                    this.free = this.value;
                },
                immediate: true,
            },
            free: {
                handler() {

                    // タイムアウトハンドラを削除
                    if (this.suggestTimeoutHandler) {
                        clearTimeout(this.suggestTimeoutHandler);
                    }
                    this.question.suggestList = [];

                    if (!this.question.without_select && this.question.type == 'question' && this.free.length) {

                        // 指定ミリ秒後に発火するタイムアウトハンドラを作成
                        this.suggestTimeoutHandler = setTimeout(() => {

                            this.voteClusteringOptions.suggestList(this.question, this.question.opinionList.map(x => x.key), this.question.suggestList.map(x => x.key), this.free)
                                .then((result) => {
                                    this.question.suggestList = result;
                                })
                        }, this.voteClusteringOptions.suggestInterval)
                    }

                    this.$emit('input', this.free);
                },
                immediate: true
            }
        }
    }
</script>

<style lang="scss" scoped>

    .height-calculator {
        position: fixed;
        top: 10px;
        bottom: 10px;
        left: 10px;
        width: 100px;
        background-color: #F00;
    }

    .sp-point {
        display: block;
        position: absolute;
        right: 0;
        left: 0;
        bottom: calc(100% + 5px);
        max-width: 100%;
        padding: 5px 8px;

        background-color: #FDC93C;
        border-radius: 5px;
        color: #1E364B;
        font-size: 10px;

        &.fade-leave-active {
            transition: opacity .3s ease;
        }

        &.fade-leave-to {
            opacity: 0;
        }
    }

    .opinion-free {

        &.caution {
            .point {
                color: #1E364B;
                background-color: #FDC93C;
            }

            button.add {
                &:not(:disabled) {
                    animation: selfOpinionLengthCaution 2s infinite;
                }
            }

            @keyframes selfOpinionLengthCaution {
                50% {
                    background-color: #1FC4F5;
                }
            }
        }

        .icon {
            margin-top: 25px;
        }
    }

    .content {
        padding: 5px;
        position: relative;

        .opinion-free-area {
            border: 1px #96A9B2 solid;
            border-radius: 5px;
            position: relative;
            z-index: 1;

            .input-ex {
                width: 100%;
                height: 100px;

                vertical-align: top;
                position: relative;
                border: none;
                resize: none;

                /deep/ textarea {
                    padding: 9px 14px;
                    border: none;
                    resize: none;
                }
            }

            &.mode-single {
                textarea {
                    height: 180px;
                }
            }

            .buttons {
                @include display-flex(row, space-between, center);
            }

            button {
                width: 90px;
                height: 40px;
                background-color: #00A8E1;
                color: #FFF;
                white-space: nowrap;
                margin: 10px;

                &.cancel {
                    background-color: transparent;
                    color: #7898A7;
                }

                &:disabled {
                    background-color: #DDD;
                }
            }
        }
    }


    .point {
        margin-top: 20px;
        padding: 9px 12px;
        border-radius: 5px;
        text-align: left;
    }

    .suggest {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;

        background-color: #FFF;
        border-radius: 5px;
        border: 1px #DDDDDD solid;

        box-shadow: 0px 2px 6px #00000029;

        header {
            padding: 13px 16px;
            font-size: 14px;
            border-bottom: 1px #EAEBEB solid;
        }

        li {
            padding: 12px 17px;
            font-size: 16px;

            &:hover {
                background-color: #F4F4F4;
            }
        }
    }

</style>
