'use strict';

let question_id = 0;
let choice_id = 0;

function add_question(close_other_accordion) {
    const question_list_group = get_question_list_group(question_id);
    const question_accordion = $(question_list_group).appendTo('#question-list-container');
    // 毎回selectionに格納するjQueryオブジェクトを生成
    // 使い回すとappendする際に前にappendした場所からoptionが消えてしまうため毎回生成している
    const question_type_selection = $.map(question_type_data, function (key, value) {
        return $('<option>', {value: value, text: key.description});
    });
    question_accordion.find(".question_type").append(question_type_selection);
    question_accordion.hide().fadeIn('slow');
    // フォームをリフレッシュし、新規追加したフォームのバリデーションを有効に
    $('#enquete_setting_form').parsley().refresh();
    // jQuery UIを利用して選択肢を並び替え可能に設定
    question_accordion.find('.choice-container').sortable().disableSelection();

    if (close_other_accordion) {
        $('.choices-list').not(question_accordion.find('.choices-list')).slideUp('slow');
        $('.question-container').not(question_accordion.find('.question-container')).slideUp('slow');
        $('.accordion-arrow').not(question_accordion.find('.accordion-arrow')).text("keyboard_arrow_down");
    }
    // 設問種別の初期値に合わせたフォームの有効無効の初期値を設定
    question_accordion.find('.question_type').change();

    question_id++;

    return question_accordion;
}

function add_choice(choice_list) {
    const choice_item = get_choice_item(choice_id);

    const list_group = choice_list.children('.list-group');
    const choice = $(choice_item).appendTo(list_group).hide().fadeIn('slow');
    // フォームをリフレッシュし、新規追加したフォームのバリデーションを有効に
    $('#enquete_setting_form').parsley().refresh();
    choice_id++;

    return choice;
}

// チェックボックスの状態を基にして送信する値をセットする関数
// (通常チェックボックスがオフだと値自体送信されないのでオフの場合の値を手動でセットする必要がある)
function processCheckbox(checkbox, hidden) {
    if (checkbox.prop('checked')) {
        checkbox.val('true');
        hidden.attr('disabled', 'disabled')
    } else {
        hidden.removeAttr('disabled');
        hidden.val('false');
    }
}

// 無効化される可能性があるフォームについて、無効化時にはhiddenフォームにデフォルト値を格納して送信
function setHiddenInput(input, hidden, defaultValue) {
    if (input.prop('disabled')) {
        hidden.val(defaultValue);
    } else {
        hidden.val(input.val());
    }
}

function strToBoolean(str_input) {
    return str_input.toLowerCase() === 'true';
}

$(function () {
    // DateTimeを入力するフォームにDateTimePickerを適用
    // 各フォームにDateTimePickerの状態変化を検出してバリデーションを走らせるよう設定
    $('#enquete_published_at').datetimepicker({
        onChangeDateTime: function () {
            if (is_debug) console.log("publish changed!!");
            $('#enquete_published_at').parsley().reset();
            $('#enquete_expired_at').parsley().reset();
        }
    });
    $('#enquete_expired_at').datetimepicker({
        onChangeDateTime: function () {
            $('#enquete_expired_at').parsley().reset();
        }
    });
    $('#enquete_finished_at').datetimepicker();
    // 質問の追加ボタンを押すと質問を一つ追加
    $('.add-question-button').on('click', function () {
        add_question(true);
    });
    // 選択肢の追加ボタンを押すと選択肢を一つ追加
    $(document).on('click', '.add-choice-button', function () {
        add_choice($(this).closest('.choices-list'))
    });
    // 質問の削除ボタンを押すと削除
    $(document).on('click', '.delete-question-button', function () {
        $(this).closest('.question-accordion').fadeOut('slow').queue(function () {
            this.remove();
        });
    });
    // 選択肢の削除ボタンを押すと削除
    $(document).on('click', '.delete-choice-button', function () {
        $(this).closest('.list-group-item').fadeOut('slow').queue(function () {
            this.remove();
        });
    });
    // 開閉ボタンを押すことでアコーディオンの開閉を行う処理
    $(document).on('click', '.toggle-choices-accordion-button', function () {
        const choices_card = $(this).closest('.question-accordion').find('.choices-list');
        const question_container = $(this).closest('.question-accordion').find('.question-container');
        const arrow = $(this).children('.accordion-arrow');
        if (choices_card.css('display') === 'none') {
            arrow.text("keyboard_arrow_up")
        } else {
            arrow.text("keyboard_arrow_down")
        }

        choices_card.slideToggle('slow');
        question_container.slideToggle('slow');
    });

    // submitの前に行う処理
    $("#enquete_setting_form").submit(function () {
        // フォームは無効化時に値を送信しないため代わりにhiddenフォームに値を格納して送信
        setHiddenInput($('#enquete_password'), $('#enquete_password_hidden'), '');
        processCheckbox($('#enquete_has_password'), $('#enquete_has_password_hidden'));

        $('.question-accordion').each(function (index, element) {
            // 選択肢のフィールドにnameの値を付加する
            $(element).find('.choice-text').attr('name', 'choice_text_' + index);
            // 無効化される可能性があるフォームの値を対応するhiddenフォームに格納
            setHiddenInput($(element).find('.question_min_like_required'), $(element).find('.question_min_like_required_hidden'), '0');
            setHiddenInput($(element).find('.question_example_answer'), $(element).find('.question_example_answer_hidden'), '');

            // チェックボックスの状態を基に送信する値をセット
            processCheckbox($(element).find('.question_is_skip_allowed_check'), $(element).find('.question_is_skip_allowed_hidden'));
            processCheckbox($(element).find('.question_is_result_public_check'), $(element).find('.question_is_result_public_hidden'));
            processCheckbox($(element).find('.question_with_answered_num_check'), $(element).find('.question_with_answered_num_hidden'));
            processCheckbox($(element).find('.question_without_select_check'), $(element).find('.question_without_select_hidden'));
        });
    });

    // jQuery UIを利用して質問を並び替え可能に設定
    $('#question-list-container').sortable().disableSelection();

    // アンケート用パスワード利用の有無のチェックボックスの変更時にパスワードフォームの有効無効を切り替え
    $(document).on('change', '#enquete_has_password', function () {
        if ($(this).prop('checked')) {
            $('#enquete_password').prop("disabled", false);
            $('#enquete_password_check').prop("disabled", false);
        } else {
            // フォームを無効化した場合に該当フォームのエラーメッセージが消えるようリセット
            $('#enquete_password').prop("disabled", true).parsley().reset();
            $('#enquete_password_check').prop("disabled", true).parsley().reset();
        }
    });

    // 設問形式の選択肢の変更時にフォームの有効無効を切り替え
    $(document).on('change', '.question_type', function () {
        const selected_type_data = question_type_data[$(this).prop('value')];

        if (selected_type_data["has_other_select"]) {
            $(this).closest('.question-accordion').find('.question_without_select_check').prop("disabled", false);
            $(this).closest('.question-accordion').find('.question_min_like_required').prop("disabled", false);
        } else {
            // フォームを無効化した場合に該当フォームのエラーメッセージが消えるようリセット
            $(this).closest('.question-accordion').find('.question_without_select_check').prop("disabled", true).parsley().reset();
            $(this).closest('.question-accordion').find('.question_min_like_required').prop("disabled", true).parsley().reset();
        }
        if (selected_type_data["has_post_respondent"]) {
            $(this).closest('.question-accordion').find('.question_with_answered_num_check').prop("disabled", false);
        } else {
            // フォームを無効化した場合に該当フォームのエラーメッセージが消えるようリセット
            $(this).closest('.question-accordion').find('.question_with_answered_num_check').prop("disabled", true).parsley().reset();
        }
        if (selected_type_data["has_placeholder"]) {
            $(this).closest('.question-accordion').find('.question_example_answer').prop("disabled", false);
        } else {
            // フォームを無効化した場合に該当フォームのエラーメッセージが消えるようリセット
            $(this).closest('.question-accordion').find('.question_example_answer').prop("disabled", true).parsley().reset();
        }
    });

    // 回答者数を表示するかのチェックボックス変更時に最低いいね数の有効無効を切り替え
    $(document).on('change', '.question_without_select_check', function () {
        if ($(this).prop('checked')) {
            // フォームを無効化した場合に該当フォームのエラーメッセージが消えるようリセット
            $(this).closest('.question-accordion').find('.question_min_like_required').prop("disabled", true).parsley().reset();
        } else {
            $(this).closest('.question-accordion').find('.question_min_like_required').prop("disabled", false);
        }
    });

    // ツールチップの読み込み
    $('[data-toggle="tooltip"]').tooltip();

    if (has_setting_data) {
        // 設定ファイルをインポートしている場合そのデータをフォームに代入していく
        $('#enquete_title').val(setting_data['enquete_title']);
        $('#enquete_has_password').prop('checked', strToBoolean(setting_data['enquete_has_password'])).change();
        $('#enquete_published_at').val(setting_data['enquete_published_at']);
        $('#enquete_expired_at').val(setting_data['enquete_expired_at']);
        $('#term_of_service').val(setting_data['enquete_term_of_service']);

        const question_list = setting_data['question_list'];
        for (const question of question_list) {
            // console.log(question);
            const question_accordion = add_question(false);
            question_accordion.find('.question_text').val(question['question_text']);
            question_accordion.find('.question_type').val(question['question_type']).change();
            question_accordion.find('.question_without_select_check')
                .prop('checked', strToBoolean(question['question_without_select'])).change();
            question_accordion.find('.question_with_answered_num_check')
                .prop('checked', strToBoolean(question['question_with_answered_num'])).change();
            question_accordion.find('.question_min_like_required').val(question['question_min_like_required']);
            question_accordion.find('.question_example_answer').val(question['question_example_answer']);
            question_accordion.find('.question_is_skip_allowed_check')
                .prop('checked', strToBoolean(question['question_is_skip_allowed'])).change();
            question_accordion.find('.question_is_result_public_check')
                .prop('checked', strToBoolean(question['question_is_result_public'])).change();
            const choice_list = question['choice_list'];
            for (const choice of choice_list) {
                add_choice(question_accordion.find('.choices-list')).find('.choice-text').val(choice);
            }
        }

        // バリデーションの状態をリセット
        $('#enquete_setting_form').parsley().reset();
    } else {
        // 設定ファイルをインポートしていない場合は最初に質問を一つ追加
        add_question();
    }
});

// 入力が日時のフォーマットに即しているかチェック
window.Parsley.addValidator('isDatetime', {
    requirementType: 'string',
    validateString: function (value) {
        return moment(value, "YYYY/MM/DD HH:SS").isValid()
    },
    messages: {
        ja: '入力された文字列が正しい日時のフォーマットではありません',
        en: 'The entered string is not of the correct datetime format.'
    }
});

// 入力の公開期限が公開日より後になっているかチェック
window.Parsley.addValidator('isExpireAfterPublish', {
    requirementType: 'string',
    validateString: function (value) {
        const expire = moment(value, "YYYY/MM/DD HH:SS");
        const publish = moment($('#enquete_published_at').val(), "YYYY/MM/DD HH:SS");

        // 期限は入力自由のため未入力ならtrueを返す
        // 形式が不正の場合はis_datetimeで検出を行うためこちらではtrueを返す
        if (!expire.isValid() || !expire.isValid()) {
            return true;
        }

        return expire.isAfter(publish)
    },
    messages: {
        ja: '公開期限日が公開開始日より前になっています。',
        en: 'The response expiration date is earlier than the publicly available date.'
    }
});
