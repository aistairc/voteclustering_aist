<template>
    <div class="page page_top">
        <div class="header_top">
            <img v-if="voteClusteringOptions.language == 'ja'" src="../image/logo.png" class="header-logo_top">
            <img v-else src="../image/logo_en.png" class="header-logo_top">
            <img src="../image/help.svg" class="header-help" @click="showGuide">
        </div>

        <!-- アンケート開始前メッセージ -->
        <div v-if="voteClusteringOptions.openState == 'before'" class="close-message">
            <div class="logo for-small">
                <img src="../image/icon_white.png" class="img-icon">
                <img src="../image/logo_centering.png" class="img-logo">
            </div>
            <div class="message" v-html="languages.beforeMessage"></div>
            <div class="spacer for-small"></div>
        </div>

        <!-- アンケート終了時メッセージ -->
        <div v-else-if="voteClusteringOptions.openState == 'after'" class="close-message">
            <div class="logo for-small">
                <img src="../image/icon_white.png" class="img-icon">
                <img src="../image/logo_centering.png" class="img-logo">
            </div>
            <div class="message" v-html="languages.afterMessage"></div>
            <div class="spacer for-small"></div>
        </div>

        <div v-else class="body">
            <div class="main">
                <div class="top-main">
                    <img src="../image/icon_white.png" class="for-small img-icon">
                    <img src="../image/logo_centering.png" class="for-small img-logo">

                    <p class="top-enquete-title">{{ voteClusteringOptions.enqueteTitle }}</p>
                    <div class="form">
                        <template v-if="voteClusteringOptions.hasPassword">
                            <div class="form-label">Password<span class="validation_error"
                                                                  v-if="error">{{ error }}</span></div>
                            <input type="password" class="nonborder" :class="{'has-error': error != null}"
                                   v-model="password" name="password" placeholder="888888">
                        </template>
                        <button type="button" @click="login" data-enter>Login</button>
                    </div>
                </div>
                <div class="top-sub for-nonsmall">
                    <img src="../image/top/pc.png" class="img-pc">
                    <img src="../image/top/sp.png" class="img-sp">
                </div>
            </div>
        </div>

        <small class="copyright text-align-center">&copy; 2020 National Institute of Advanced Industrial Science and
            Technology (AIST)
        </small>
    </div>
</template>

<script>
    export default {
        bodyAttr: 'top',
        data() {
            return {
                voteClusteringOptions: voteClusteringOptions,
                languages: voteClusteringOptions.languages.top,

                password: null,
                error: null,
            }
        },
        inject: ['loading', 'showGuide'],
        methods: {
            login() {
                if (!voteClusteringOptions.hasPassword) {
                    this.$emit("next");
                    return;
                }

                this.loading.show();

                // ログインチェック
                voteClusteringOptions.loginFunction(this.password)
                    .done((guide) => {

                        // ログインが完了したら次のページへ(必要に応じて操作方法ポップアップを表示)
                        if (guide) {
                            this.showGuide();
                        }
                        this.$emit("next");

                    }).fail((result) => {
                    this.error = result;
                    console.log(result);

                }).always(() => {

                    // いずれの場合もローディング表示を閉じる
                    this.loading.hide();
                })
            },
        },
    }
</script>

<style lang="scss" scoped>
    .page_top {
        @include display-flex(column, center, center);

        background-image: url('../image/top/bg.jpg');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;

        .header_top {
            flex: 0 0 80px;
            @include display-flex(row, space-between, center);
            width: 100%;
            max-width: 950px;
            padding: 0 20px;

            position: relative;

            .header-logo_top {
                height: 40px;
            }

            .header-help {
                height: 24px;
                cursor: pointer;
            }
        }

        .close-message {
            @include display-flex(column, center, center);
            flex: 1 1 auto;

            .logo {
                @include display-flex(column, center, center);
                flex: 1 0 0;

                .img-icon {
                    display: block;
                    width: 72px;
                    margin: 0 auto 10px;
                }

                .img-logo {
                    display: block;
                    width: 254px;
                    margin: 0 auto;
                }
            }

            .message {
                @include display-flex(row, center, center);
                color: #FFF;
                width: 280px;
                height: 110px;
                border-top: 1px #FFF solid;
                border-bottom: 1px #FFF solid;
                margin-bottom: 4em;
                font-size: 20px;
                text-align: center;
            }

            .spacer {
                flex: 0.5 1 0;
            }
        }

        .body {
            @include display-flex(column, center, center);

            & > div.main {
                flex: 0 1 0;
                max-width: 962px;
                width: 100%;
                padding: 0 0 115px 50px;

                @include display-flex(row, flex-start, center);
                position: relative;

                @include for-small {
                    padding: 0;
                    margin: 15px 0;
                }

                .top-main {
                    flex: 1 0 0;
                }

                .top-sub {
                    flex: 1.3 0 0;
                    max-width: 566px;
                    position: relative;

                    .img-pc {
                        margin-top: 15px;
                        width: 100%;
                        position: relative;
                        left: -4%;
                    }

                    .img-sp {
                        position: absolute;
                        bottom: -17%;
                        left: -10%;
                        width: 26.5%;
                    }
                }

                div.form {
                    margin-top: 10px;
                    @include display-flex(column, center, flex-start);
                    width: 240px;
                }

                p {
                    color: #7BDEFC;
                    font-size: 18px;
                    line-height: 37px;
                }

                .form-label {
                    margin-top: 5px;
                    font-size: 16px;
                    color: white;
                }

                input[type=text], input[type=password] {
                    margin-top: 10px;
                    width: 100%;
                    height: 50px;
                    padding-left: 18px;

                    &:placeholder {
                        color: #BCBCBC;
                    }
                }

                button {
                    width: 100%;
                    height: 60px;
                    margin-top: 20px;

                    color: #00A8E1;
                    border-color: #00A8E1;
                    font-size: 20px;
                }
            }
        }

        .validation_error {
            margin-left: 13px;
        }

        .copyright {
            color: ivory;
        }
    }

    @include for-small {
        .page_top {
            background-position: 0 0;
            min-width: auto;

            .header_top {
                display: none;
            }

            .body {
                width: 100%;
                min-height: 100%;

                & > div {
                    display: block;

                    p {
                        font-size: 18px;
                        width: 80%;
                        text-align: center;
                        margin: 10px auto;
                    }

                    .img-icon {
                        display: block;
                        width: 72px;
                        margin: 0 auto 10px;
                    }

                    .img-logo {
                        display: block;
                        width: 254px;
                        margin: 0 auto;
                    }

                    div.form {
                        display: block;
                        width: 300px;
                        margin: 0 auto;
                    }

                    input[type=text], input[type=password] {
                        height: 60px;
                    }
                }
            }
        }
    }
</style>
