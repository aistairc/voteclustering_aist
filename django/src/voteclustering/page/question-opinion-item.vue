<template>
    <!-- 「過去の回答を表示する設定」または「過去の表示しない設定、かつ自分の回答」を満たしている回答を表示させる -->
    <question-opinion-base v-if="!question.without_select || (question.without_select && opinion.key == null)" class="opinion-item"
                           :class="{'highlight': opinion.highlight, 'first': opinion.first, 'active': opinion.select, 'self-opinion': opinion.key == null}"
                           @click="clickOpinion()">
        <template v-slot:icon>
            <div class="icon">
                <div v-if="opinion.key" class="opinion-item-icon"></div>
                <img v-else src="../image/question/free.svg">
                <p v-if="opinion.num != null && question.with_answered_num">{{ languages.likeNum.replace('*N*', opinion.num) }}</p>
            </div>
        </template>
        <template v-slot:content>
            <div class="content">
                <div>
                    <label v-if="opinion.key == null">{{ languages.selfOpinion.label }}</label>
                    <span>{{ opinion.text }}</span>
                </div>
                <button v-if="opinion.key == null" class="delete" @click="$emit('delete')">
                    <cross-mark color="#96A9B2"/>
                </button>
            </div>
        </template>
    </question-opinion-base>
</template>

<script>
    export default {
        props: {
            value: {require: true},
            'question': {required: true},
        },
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions,         // 設定
                languages: voteClusteringOptions.languages.question,  // 言語セット
                opinion: {},
            }
        },
        watch: {
            value: {
                handler() {
                    this.opinion = this.value;
                },
                immediate: true
            }
        },
        methods: {
            clickOpinion() {
                if (this.opinion.key) {
                    Vue.set(this.opinion, 'select', !this.opinion.select);
                    this.$emit('input', this.opinion);
                }
            },
        }
    }
</script>

<style lang="scss" scoped>

    .opinion-item {
        margin: 15px 0;
        cursor: pointer;
        position: relative;

        &:nth-child(4n+2) .opinion-item-icon {
            background-image: url(../image/question/opinion1_inactive.svg);
        }

        &.active:nth-child(4n+2) .opinion-item-icon {
            background-image: url(../image/question/opinion1_active.svg);
        }

        &:nth-child(4n+3) .opinion-item-icon {
            background-image: url(../image/question/opinion2_inactive.svg);
        }

        &.active:nth-child(4n+3) .opinion-item-icon {
            background-image: url(../image/question/opinion2_active.svg);
        }

        &:nth-child(4n+0) .opinion-item-icon {
            background-image: url(../image/question/opinion3_inactive.svg);
        }

        &.active:nth-child(4n+0) .opinion-item-icon {
            background-image: url(../image/question/opinion3_active.svg);
        }

        &:nth-child(4n+1) .opinion-item-icon {
            background-image: url(../image/question/opinion4_inactive.svg);
        }

        &.active:nth-child(4n+1) .opinion-item-icon {
            background-image: url(../image/question/opinion4_active.svg);
        }

        .icon {
            .opinion-item-icon {
                width: 100%;
                height: 45px;
                background-size: contain;
                background-position: center;
                background-repeat: no-repeat;
            }

            img {
                display: block;
                height: 45px;
                margin: 0 auto;
            }

            p {
                position: absolute;
                top: 100%;
                left: 0;
                width: 100%;
                margin-top: 5px;
                text-align: center;
                white-space: nowrap;
                font-size: 12px;
                line-height: 14px;
            }
        }

        &.self-opinion {
            cursor: default;

            .opinion-item-balloon {
                box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.16);
                @supports (filter: drop-shadow(0 0 0 #000)) {
                    filter: drop-shadow(0px 1px 0px #96A9B2) drop-shadow(0px -1px 0px #96A9B2) drop-shadow(-1px 0px 0px #96A9B2) drop-shadow(1px 0px 0px #96A9B2);
                    transform: translateZ(0);
                    box-shadow: none;
                }
            }
        }

        .content {
            @include display-flex(row, flex-start, center);
            padding: 20px 20px;

            @include for-small {
                // @include display-flex(row, flex-start, flex-start);
                align-items: flex-start;
            }

            div {
                flex: 1 1 auto;
                @include display-flex(row, flex-start, center);

                @include for-small {
                    @include display-flex(column, flex-start, flex-start);
                }
            }

            label {
                display: inline-block;
                min-width: 55px;
                background-color: #00A8E1;
                color: #FFF;
                line-height: 25px;
                text-align: center;
                font-size: 14px;
                margin-right: 10px;
            }

            span {
                position: relative;
                word-break: break-all;
                white-space: pre-wrap;
            }

            button.delete {
                margin-left: 10px;
                flex: 0 0 24px;

                @include display-flex(row, center, center);
                width: 24px;
                height: 24px;
                border: 1px #9D9D9D solid;
                border-radius: 3px;

                & > .cross-mark {
                    width: 10px;
                    height: 10px;
                    flex: 0 0 auto;
                }
            }
        }
    }
</style>
