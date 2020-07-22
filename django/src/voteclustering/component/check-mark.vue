<template>
    <div class="component">
        <div>
            <div :style="{ 'border-color': color }"></div>
        </div>

    </div>
</template>

<script>
    export default {
        props: {
            color: {default: '#000'}
        },
    }
</script>

<style lang="scss" scoped>
    .component {
        @include display-flex(row, center, center);
        position: relative;

        & > div {
            width: 100%;

            &:before {
                display: block;
                content: '';
                padding-top: 100%;
            }

            & > div {
                position: absolute;
                top: 13%;
                left: 5%;
                width: 88.4%;
                height: 53.0%;

                border-left: 2px #000 solid;
                border-bottom: 2px #000 solid;

                transform: rotateZ(-45deg);
            }
        }
    }
</style>
