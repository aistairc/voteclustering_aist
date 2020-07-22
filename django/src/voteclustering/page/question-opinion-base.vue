<template>
    <div class="opinion-item" @click="$emit('click')" :disabled="disabled">

        <div class="position-relative">
            <slot name="above"/>
        </div>

        <div class="main flex-row-center-center">
            <div class="icon">
                <slot name="icon"/>
            </div>
            <div class="balloon-wrapper">
                <div class="balloon">
                    <slot name="content"/>
                </div>
                <div class="position-relative for-nonsmall">
                    <slot name="contentAfter"/>
                </div>
            </div>
        </div>

        <div class="for-small position-relative">
            <slot name="contentAfter"/>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            disabled: Boolean,
        },
    }
</script>

<style lang="scss" scoped>
    .opinion-item {
        @include display-flex(column, flex-start, stretch);
        margin: 15px 0;
        position: relative;

        @include for-small {
            width: 100%;
        }

        & > div.main {
            @include display-flex(row, center, center);

            & > .icon {
                min-width: 70px;
                position: relative;

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

                @include for-small {
                    margin-right: -7px;
                }
            }

            & > .balloon-wrapper {
                @include display-flex(column, flex-start, stretch);
                width: 435px;
                margin-left: 24px;

                @include for-small {
                    flex: 1 0 1px;
                    width: 1px;
                    margin-left: 18px;
                }

                & > .balloon {
                    user-select: none;

                    width: 100%;
                    border-radius: 5px;
                    background-color: #FFFFFF;
                    position: relative;
                    font-size: 16px;
                    user-select: none;

                    // before要素(吹き出しのしっぽ)まで影をつけるにはdrop-shadowが必要だが、対応していないブラウザもあるため分岐
                    box-shadow: 0 2px 6px 0 rgba(0, 0, 0, 0.16);

                    @supports (filter: drop-shadow(0 0 0 #000)) {
                        filter: drop-shadow(0px 2px 6px rgba(0, 0, 0, 0.16));
                        transform: translateZ(0);
                        box-shadow: none;
                    }

                    &:before {
                        content: '';
                        position: absolute;
                        top: 50%;
                        left: 0;
                        width: 20px;
                        height: 20px;
                        margin: -10px 0 0 -8px;
                        background-color: inherit;

                        transform: scaleY(0.7) rotateZ(45deg);
                    }
                }
            }
        }

        &.highlight {
            &:not(.active):not(.first) {
                & > div.main > .balloon-wrapper > .balloon {
                    background-color: #FEFFED;
                }
            }

            animation: opinionHighlight .5s;
        }

        @include keyframes(opinionHighlight) {
            0% {
                opacity: 0;
                top: 50px;
            }

            100% {
                opacity: 1;
                top: 0px;
            }
        }

        &.active {
            & > div.main > .balloon-wrapper > .balloon {
                background-color: #4CB5D5;
                color: #FFF;
                box-shadow: none;
                filter: none;
            }
        }

        &.shadow-none {
            & > div.main > .balloon-wrapper > .balloon {
                box-shadow: none;
                filter: none;
            }
        }

        &.tail-upper {
            & > div.main > .balloon-wrapper > .balloon {
                &:before {
                    top: 40px;
                }
            }
        }

        &.more {
            & > div.main > .balloon-wrapper > .balloon {
                background-color: rgb(145, 211, 229);
                color: #FFF;

                &:before {
                    background-color: rgb(145, 211, 229);
                }
            }

            &:disabled,
            &.disabled {
                & > div.main > .balloon-wrapper > .balloon {
                    background-color: #DDD;

                    &:before {
                        background-color: #DDD;
                    }
                }
            }
        }

        &.icon-above {
            & > div.main {
                @include display-flex(row, center, flex-start);
            }
        }
    }
</style>
