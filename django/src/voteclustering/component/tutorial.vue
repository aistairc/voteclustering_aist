<template>
    <div class="wrapper" v-if="setting" @click="$emit('click')">
        <div class="main" :style="{
            top: center.top - setting.size / 2 - borderSize + 'px',
            left: center.left - setting.size / 2 - borderSize + 'px',
            width: setting.size + borderSize * 2 + 'px',
            height: setting.size + borderSize * 2 + 'px',
            'border': borderSize + 'px rgba(0, 0, 0, 0.6) solid', // sizeに乗じる値は√2-1だが、大きくて困ることはないので少し多めに確保
        }"></div>

        <div class="main" :style="{
            top: center.top - setting.size / 2 + 'px',
            left: center.left - setting.size / 2 + 'px',
            width: setting.size + 'px',
            height: setting.size + 'px',
            'border': '1px #FFF solid', // sizeに乗じる値は√2-1だが、大きくて困ることはないので少し多めに確保
        }"></div>

        <div class="line" :style="{
            left: center.left + 'px',
            top: (messageAbove ? center.top - setting.size / 2 - 46 : center.top + setting.size / 2) + 'px',
        }"></div>
        <div class="point" :style="{
            left: center.left + 'px',
            top: (messageAbove ? center.top - setting.size / 2 - 46 : center.top + setting.size / 2 + 46) + 'px',
        }"></div>
        <div class="message" :style="{
            top: (messageAbove ? center.top - setting.size / 2 - 84 : center.top + setting.size / 2 + 46) + 'px',
        }">{{ setting.message }}
        </div>
    </div>
</template>

<script>
    export default {
        props: ['setting'],
        data() {
            return {
                borderSize: 0,
                center: {left: 0, top: 0},
                messageAbove: false,
            }
        },
        mounted() {
            $(window).on("resize.tutorial", () => {
                this.updateLayout();
            }).resize();
        },
        updated() {
            var $wrapper = $(this.$el);
            var $message = $wrapper.children(".message").reflow();
            var outerWidth = $message.outerWidth();
            $message.css("left", Math.min(Math.max(0, this.center.left - outerWidth / 2), $wrapper.outerWidth() - outerWidth));
        },
        destroyed() {
            $(window).off("resize.tutorial");
        },
        methods: {
            updateLayout() {
                var $wrapper = $(this.$el);
                this.center = this.setting.$target.center(this.setting.$wrapper || $wrapper);
                this.borderSize = Math.sqrt(Math.pow($wrapper.outerWidth(), 2) + Math.pow($wrapper.outerHeight(), 2));
                this.messageAbove = $wrapper.outerHeight() / 2 < this.center.top;

                var $wrapper = $(this.$el);
                var $message = $wrapper.children(".message").reflow();
                var outerWidth = $message.outerWidth();
                $message.css("left", Math.min(Math.max(0, this.center.left - outerWidth / 2), $wrapper.outerWidth() - outerWidth));
            }
        },
        watch: {
            setting() {
                this.updateLayout();
            }
        }
    }
</script>

<style lang="scss" scoped>
    div.wrapper {
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        z-index: 9999;

        div.main {
            position: absolute;
            border-radius: 50%;
        }

        div.line {
            position: absolute;
            width: 1px;
            height: 46px;
            background-color: #FFF;
        }

        div.point {
            position: absolute;
            width: 5px;
            height: 5px;
            margin-left: -2px;
            margin-top: -2px;
            border-radius: 50%;
            background-color: #FFF;
        }

        div.message {
            position: absolute;
            color: #FFF;
            font-size: 18px;
            line-height: 38px;
            padding: 0 0.5em;
            white-space: nowrap;
        }
    }
</style>
