<template>
    <div class="carousel-pager">
        <div v-for="i in max" :class="{active: i == index + 1}"></div>
    </div>
</template>

<script>
    export default {
        props: {
            index: {require: true},
            max: {require: true},
        }
    }
</script>

<style lang="scss" scoped>
    div.carousel-pager {
        @include display-flex(row, center, center);

        & > div {
            width: 8px;
            height: 8px;
            margin: 0 6px;

            background-color: #96A9B2;
            border-radius: 50%;

            &.active {
                background-color: #1E364B;
            }
        }
    }
</style>
