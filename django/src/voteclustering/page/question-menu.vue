<template>
    <div class="menu" :class="{menu_show: isShow}">
        <ul>
            <li class="menu-home" @click="$emit('home')">HOME</li>
            <li class="menu-title">{{ voteClusteringOptions.enqueteTitle }}</li>
            <li class="menu-item" v-for="item in questionList" v-if="item.type != 'tos'"
                :class="{'menu-item_inactive': !item.linkActive, 'menu-item_checked': item.isAnswered()}"
                @click="$emit('click', item)">Q.{{ item.question }}
            </li>
            <li class="menu-tos" @click="$emit('tos')">{{ languages.tos.menu }}</li>
        </ul>
        <div class="menu-back" @click="hide()">
            <div class="menu-close_button"></div>
        </div>
    </div>
</template>

<script>

    export default {
        props: ['questionList'],
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions,         // 設定
                languages: voteClusteringOptions.languages.question,  // 言語セット
                isShow: false,           // メニュー表示状態
            }
        },
        methods: {
            show() {
                this.isShow = true;
            },
            hide() {
                this.isShow = false;
            },
        }
    }
</script>

<style lang="scss" scoped>

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

</style>
