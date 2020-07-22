<template>
    <div class="wrapper">
        <slot/>
        <div class="loading" v-if="isShow">
            <div class="loader"></div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                isShow: false,
            }
        },
        methods: {
            show() {
                this.isShow = true;
            },
            hide() {
                this.isShow = false;
            },
        },
        mounted() {
            //this.$loading = $(this.$el).children(".loading");
        },
    }
</script>

<style lang="scss" scoped>
    div.wrapper {
        position: relative;
    }

    div.loading {
        position: fixed;
        top: 0;
        right: 0;
        left: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.1);
        overflow: hidden;

        .loader, .loader:before, .loader:after {
            background: #ffffff;
            -webkit-animation: load1 1s infinite ease-in-out;
            animation: load1 1s infinite ease-in-out;
            width: 1em;
            height: 4em;
        }

        .loader {
            position: absolute;
            top: 50%;
            left: 50%;
            margin-top: -2em;
            margin-left: -2em;
            color: #ffffff;
            text-indent: -9999em;
            position: relative;
            font-size: 11px;
            -webkit-transform: translateZ(0);
            -ms-transform: translateZ(0);
            transform: translateZ(0);
            -webkit-animation-delay: -0.16s;
            animation-delay: -0.16s;
        }

        .loader:before,
        .loader:after {
            position: absolute;
            top: 0;
            content: '';
        }

        .loader:before {
            left: -1.5em;
            -webkit-animation-delay: -0.32s;
            animation-delay: -0.32s;
        }

        .loader:after {
            left: 1.5em;
        }

        @-webkit-keyframes load1 {
            0%, 80%, 100% {
                box-shadow: 0 0;
                height: 4em;
            }
            40% {
                box-shadow: 0 -2em;
                height: 5em;
            }
        }
        @keyframes load1 {
            0%, 80%, 100% {
                box-shadow: 0 0;
                height: 4em;
            }
            40% {
                box-shadow: 0 -2em;
                height: 5em;
            }
        }
    }
</style>
