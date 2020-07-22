<template>
    <question-opinion-base class="opinion-more more" :class="{disabled: disabled}" @click="!disabled && $emit('click')"
                           :disabled="disabled">
        <template v-slot:icon>
            <img src="../image/question/more.svg">
        </template>
        <template v-slot:content>
            <div class="content">
                <div class="opinion-more-circle"></div>
                <div></div>
                {{ languages.moreOpinion }}
            </div>
        </template>
    </question-opinion-base>
</template>

<script>
    export default {
        props: {
            disabled: Boolean,
        },
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions,         // 設定
                languages: voteClusteringOptions.languages.question,  // 言語セット
            }
        }
    }
</script>

<style lang="scss" scoped>

    // みんなの意見、自由記入欄、もっと見るボタン共通デザイン
    .opinion-more {
        cursor: pointer;

        &.disabled, &:disabled {
            cursor: default;

            .content {
                &:after {
                    background-color: #CCC;
                }
            }
        }

        .content {
            @include display-flex(row, space-between, center);

            width: 100%;
            height: 60px;
            position: relative;
            font-size: 18px;
            user-select: none;

            @include for-small {
                padding-left: 12px;
            }

            &:after {
                content: '';
                display: block;
                width: 50px;
                height: 100%;
                margin-left: 10px;

                border-radius: 0 5px 5px 0;
                background-color: rgb(76, 181, 213);
                background-image: url(../image/question/more_light.svg);
                background-size: 24px auto;
                background-position: center;
                background-repeat: no-repeat;
            }

            .opinion-more-circle {
                width: 6px;
                height: 6px;
                flex: 0 0 6px;
                border-radius: 3px;
                background-color: #FFF;
                margin-left: 50px;
                margin-right: 46px;
                position: relative;

                @include for-small {
                    display: none;
                    margin: 20px 20px;
                }

                &:before, &:after {
                    content: '';
                    display: block;
                    width: 6px;
                    height: 6px;
                    border-radius: 3px;
                    background-color: #FFF;
                }

                &:before {
                    position: absolute;
                    top: 0;
                    right: -20px;
                    width: 6px;
                    height: 6px;
                }

                &:after {
                    position: absolute;
                    top: 0;
                    right: -40px;
                    width: 6px;
                    height: 6px;
                }
            }
        }
    }
</style>
