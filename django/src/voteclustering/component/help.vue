<template>
    <div class="help-component">
        <div class="content">
            <div class="item">
                <div class="number">1</div>
                <h2 v-if="hasValue(languages.step1)">{{ languages.step1 }}</h2>
                <p>
                    {{ languages.step1_1 }}
                </p>
            </div>
            <div class="item">
                <div class="number">2</div>
                <h2 v-if="hasValue(languages.step2)">{{ languages.step2 }}</h2>

                <p class="for-sp">{{ languages.step2_sp_1 }}</p>
                <p class="for-sp">{{ languages.step2_sp_2 }}</p>

                <p class="for-pc">{{ languages.step2_pc_1 }}</p>
            </div>
            <div class="item">
                <div class="number">3</div>
                <h2 v-if="hasValue(languages.step3)">{{ languages.step3 }}</h2>
                <p>
                    {{ languages.step3_1 }}
                </p>
            </div>
        </div>
        <button @click="$emit('close')">閉じる</button>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                languages: voteClusteringOptions.languages.help,
            }
        },
    }
</script>

<style lang="scss" scoped>
    .help-component {
        @include display-flex(column, flex-start, stretch);
        position: relative;
        max-width: 960px;

        .content {
            @include display-flex(column, flex-start, stretch);

            @media only screen and (min-width: 1024px) {
                @include display-flex(row, flex-start, flex-start);

                .item {
                    flex: 1 0 0px;
                    margin: 0 20px;
                }
            }

            .item {
                @include display-flex(row, flex-end, stretch);
                flex-wrap: wrap;

                div.number {
                    flex: 0 0 35px;
                    display: inline-block;
                    width: 35px;
                    height: 35px;
                    text-align: center;
                    line-height: 35px;
                    background-color: #1FC4F5;
                    color: #FFF;
                    font-size: 26px;
                    font-weight: bold;
                    margin-right: 15px;
                }

                h2, p {
                    width: calc(100% - 50px);
                }

                h2 {
                    color: #1FC4F5;
                    font-size: 20px;
                    font-weight: bold;
                }

                div.image {
                    width: 100%;

                    img {
                        display: block;
                        margin: 30px auto;
                    }
                }
            }
        }

        button {
            width: 120px;
            height: 50px;
            margin: 0 auto;

            color: #707070;
            border: 1px solid #707070;
            border-radius: 5px;
            cursor: pointer;

            @media only screen and (max-width: 1023px) {
                display: none;
            }
        }
    }
</style>
