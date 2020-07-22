<template>
    <div class="nonscroll-popup" @click="close" v-if="isShow" @touchstart.stop @touchmove.stop>
        <div>
            <div class="body" @click.stop>
                <slot></slot>
                <img class="close" src="../image/guide/close.svg" @click="close">
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                isShow: false
            }
        },
        methods: {
            show() {
                this.isShow = true;
                Vue.nextTick(() => {
                    this.$dummy = $("<span>").hide();
                    $(this.$el).after(this.$dummy).appendTo("body");
                })
            },
            hide() {
                this.close();
            },
            close() {
                this.$dummy.after(this.$el).remove();
                this.isShow = false;
            },
        },
        beforeDestroy() {
            if (this.$dummy != null) {
                this.$dummy.remove();
            }
        }
    }
</script>

<style lang="scss" scoped>
    .nonscroll-popup {
        position: fixed;
        top: 0;
        right: 0;
        left: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 90px 30px 30px;

        z-index: 999;

        &.custom-design {
            & > div > .body {
                width: auto;
                height: auto;
                padding: 0;
                background-color: transparent;
                border-radius: auto;

                .scroller {
                    position: static;
                    border: none;
                    overflow: visible;
                }

                & > .close {
                    display: none;
                }
            }
        }

        & > div {
            @include display-flex(column, center, center);
            width: 100%;
            height: 100%;
            max-width: 100%;
            min-height: 100%;
            white-space: normal;

            .body {
                border-radius: 10px;
                background-color: #FFF;
                width: 100%;
                max-width: 920px;
                padding: 50px 10px;
                position: relative;
                @include display-flex(column, flex-start, stretch);

                @include for-small {
                    border-radius: 5px;
                    padding: 20px;
                }

                .scroller {
                    @include for-small {
                        @include display-flex(column, flex-start, center);

                        position: absolute;
                        top: 15px;
                        left: 15px;
                        right: 15px;
                        bottom: 15px;
                        padding: 15px;
                        border: 1px #BCBCBC solid;

                        overflow: auto;
                        -webkit-overflow-scrolling: touch;
                        overflow-scrolling: touch;
                        -webkit-overscroll-behavior: none;
                        overscroll-behavior: none;
                    }
                }

                & > .close {
                    position: absolute;
                    right: -22px;
                    top: -22px;
                    cursor: pointer;
                }
            }
        }

        &.short {
            & > div {
                .body {
                    max-width: 320px;
                }
            }
        }
    }
</style>
