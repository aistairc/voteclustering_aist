<template>
    <div class="input-ex" :class="{ error: selfHasError }" :type="type">
        <textarea v-if="type=='textarea'" :class="{ error: selfHasError }" v-model="innerValue" @input="input"
                  @focus="$emit('focus')" @blur="$emit('blur')" :placeholder="placeholder"
                  :disabled="disabled"></textarea>
        <input v-else :type="type" :class="{ error: selfHasError }" v-model="innerValue" @input="input"
               @focus="$emit('focus')" @blur="$emit('blur')" @keydown="keydown" :placeholder="placeholder"
               :disabled="disabled">
        <div class="remain" v-if="maxLength">{{ length }} / {{ maxLength }}</div>
    </div>
</template>

<script>
    export default {
        props: {
            'value': {default: ''},
            'type': {default: 'text'},
            'maxLength': {default: null},
            'placeholder': {default: null},
            'disabled': {default: false},
            'hasError': {default: false},
        },
        computed: {
            length() {
                return this.value != null ? this.value.toString().length : 0;
            },
            selfHasError() {
                return (this.maxLength && this.length > this.maxLength) || this.hasError;
            },
        },
        data() {
            return {
                innerValue: ""
            }
        },
        methods: {
            keydown(e) {
                if (this.type == 'number') {
                    if (e.key.length == 1 && isNaN(parseInt(e.key))) {
                        e.preventDefault();
                    }
                }
            },
            input(e) {
                this.$emit('input', this.innerValue)
            }
        },
        watch: {
            value: {
                handler() {
                    if (this.type == 'number') {
                        this.innerValue = this.value.replace(/[^0-9]/g, '');
                    } else {
                        this.innerValue = this.value;
                    }
                },
                immediate: true
            },
            innerValue: {
                handler() {
                    if (this.type == 'number') {
                        var replaced = this.innerValue.replace(/[^0-9]/g, '');
                        if (replaced != this.innerValue) {
                            this.innerValue = replaced;
                        }
                    }
                },
                immediate: true
            }
        }

    }
</script>

<style lang="scss" scoped>
    div.input-ex {
        display: inline-block;
        position: relative;

        input, textarea {
            width: 100%;
            height: 100%;
        }

        .remain {
            font-size: 80%;
            position: absolute;
            right: 0.4em;
            bottom: 0.2em;
            opacity: 0.3;
        }
    }
</style>
