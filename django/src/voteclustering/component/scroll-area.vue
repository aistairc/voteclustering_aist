<template>
    <div class="scroll-area">
        <div class="body">
            <slot/>
        </div>
        <div class="before" v-if="top > 0.01" :style="{ opacity: top }"></div>
        <div class="after" v-if="bottom > 0.01" :style="{ opacity: bottom }"></div>

    </div>
</template>

<script>
    export default {
        data() {
            return {
                top: 0,
                bottom: 1
            }
        },
        mounted() {
            var $body = $(this.$el).children(".body");
            $body.on("scroll", () => {
                this.top = Math.min($body.scrollTop() / 300.0, 1);
                this.bottom = Math.min(($body.get(0).scrollHeight - $body.outerHeight() - 1 - $body.scrollTop()) / 300, 1);
            }).scroll();

            this.observer = new MutationObserver(function (mutations) { // <- this isn't firing
                if (mutations.length) {
                    $body.scroll();
                }
            });

            this.observer.observe($body.get(0), {
                attributes: true,
                childList: true,
                characterData: true,
                subtree: true
            });
        },
        destroyed() {
            this.observer.disconnect();
        },
    }
</script>

<style lang="scss" scoped>
    div.scroll-area {
        position: relative;

        & > div.body {
            position: absolute;
            top: 0;
            right: 0;
            left: 0;
            bottom: 0;
            width: 100%;
            height: 100%;

            overflow: auto;
            -webkit-overflow-scrolling: touch;
            overflow-scrolling: touch;
        }

        & > .before, & > .after {
            @include display-flex(column, center, center);
            position: absolute;
            left: 0;
            right: 0;
            width: 100%;
            height: 7%;
            min-height: 30px;
            pointer-events: none;

            &:before {
                display: block;
                content: '';
                background-image: url(../image/icon-arrow.svg);
                background-size: contain;
                background-position: center;
                background-repeat: no-repeat;
                width: 20px;
                height: 20px;
            }

        }

        & > .before {
            top: 0;
            background: linear-gradient(to bottom, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
            // background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), transparent);

            &:before {
                transform: rotateZ(180deg);
                margin-top: 10px;
            }
        }

        & > .after {
            bottom: 0;
            background: linear-gradient(to top, rgba(255, 255, 255, 1), rgba(255, 255, 255, 0));
            // background: linear-gradient(to top, rgba(0, 0, 0, 0.5), transparent);

            &:before {
                margin-bottom: 10px;
            }
        }
    }
</style>
