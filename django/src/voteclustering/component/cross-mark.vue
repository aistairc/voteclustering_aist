<template>
    <div class="cross-mark" @click="$emit('click')">
        <div :style="{ 'background-color': color }"></div>
        <div :style="{ 'background-color': color }"></div>
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
    .cross-mark {
        position: relative;

        & > div {
            display: block;
            content: '';
            position: absolute;
            top: 50%;
            left: -20.7%;
            width: 141.4%;
            height: 2px;
            margin-top: -1px;
            background-color: #FFF;
            border-radius: 1px;

            &:first-child {
                transform: rotateZ(45deg);
            }

            &:last-child {
                transform: rotateZ(-45deg);
            }
        }
    }
</style>
