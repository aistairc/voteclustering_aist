<template>
    <div class="left-arrow">
        <div :style="{'border-color': color}"></div>
    </div>
</template>

<script>
    export default {
        props: {
            color: {default: '#000'}
        }
    }
</script>

<style lang="scss" scoped>
    div.left-arrow {
        display: inline-block;
        padding: 0 !important;
        margin: 0;

        & > div {
            padding: 0 !important;
            margin: 0 !important;
            display: block;
            box-sizing: border-box;
            width: 70%;
            height: 70%;
            margin-top: 15%;
            margin-left: 30% !important;
            border-bottom: 2px #333 solid;
            border-left: 2px #333 solid;
            transform: rotateZ(45deg);
        }
    }
</style>
