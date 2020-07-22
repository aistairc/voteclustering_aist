const get_question_list_group = (question_id) => {
    return `
    <div class="accordion question-accordion">
        <!-- 質問と選択肢を入力させるリスト -->
        <div class="list-group">
          <div class="list-group-item list-group-item-secondary">
        
            <!-- 質問を削除するボタン -->
            <button type="button" class="close delete-question-button" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
        
            <!-- 質問文 -->
            <div class="form-group row">
              <label for="question_text_${question_id}" class="col-md-2 col-form-label">
                ${translate_catalog['質問文']}　<span class="badge badge-danger">${translate_catalog['必須']}</span>
              </label>
              <input type="text" id="question_text_${question_id}" name="question_text"
                     class="form-control col-md-10 question_text" placeholder="${translate_catalog['(例) 保健室を利用した理由を教えてください']}" required>
            </div>
        
            <!-- 質問の属性を格納するコンテナ -->
            <div class="question-container">
              <!-- 回答形式 -->
              <div class="form-group row">
                <label for="question_type_${question_id}" class="col-md-2 col-form-label">${translate_catalog['回答種別']}</label>
                <select id="question_type_${question_id}" name="question_type" class="form-control question_type col-md-10">
                </select>
              </div>
        
              <!-- 回答形式が自由回答の場合、他者の回答を表示するか -->
              <div class="form-check">
                <input type="hidden" id="question_without_select_hidden_${question_id}"
                       class="question_without_select_hidden"
                       name="question_without_select" disabled="disabled">
                <input class="form-check-input question_without_select_check" type="checkbox"
                       id="question_without_select_check_${question_id}" name="question_without_select">
                <label class="form-check-label"
                       for="question_without_select_check_${question_id}">${translate_catalog['他者の回答を表示しない [＊ 自由記述形式の場合のみ]']}</label>
              </div>
              <!-- 各選択肢に対して、過去の回答者数を表示するか -->
              <div class="form-check">
                <input type="hidden" id="question_with_answered_num_hidden_${question_id}"
                       class="question_with_answered_num_hidden" name="question_with_answered_num" disabled="disabled">
                <input class="form-check-input question_with_answered_num_check" type="checkbox"
                       id="question_with_answered_num_check_${question_id}" name="question_with_answered_num">
                <label class="form-check-label"
                       for="question_with_answered_num_check_${question_id}">${translate_catalog['各選択肢に対して、過去の回答者数を表示する']}</label>
              </div>
              <!-- アラートを出さずに次に進むのに最低必要ないいね数 -->
              <div class="form-group row">
                <input type="hidden" id="question_min_like_required_hidden_${question_id}" name="question_min_like_required"
                       class="question_min_like_required_hidden">
                <label for="question_min_like_required_${question_id}" class="col-md-2 col-form-label">
                  ${translate_catalog['最低いいね数']}　
                  <span class="badge badge-pill badge-warning" data-toggle="tooltip" title="${translate_catalog['自由回答かつ他者の回答を表示する場合必須']}">?</span>
                </label>
                <input type="number" id="question_min_like_required_${question_id}"
                       class="question_min_like_required form-control col-md-10" value="0" required>
              </div>
              <!-- 回答例 -->
              <div class="form-group row">
                <input type="hidden" id="question_example_answer_hidden_${question_id}" name="question_example_answer"
                       class="question_example_answer_hidden">
                <label for="question_example_answer_${question_id}" class="col-md-2 col-form-label">
                  ${translate_catalog['回答例']}　<span class="badge badge-info">${translate_catalog['任意']}</span>
                </label>
                <input type="text" id="question_example_answer_${question_id}"
                       class="form-control col-md-10 question_example_answer" placeholder="${translate_catalog['回答欄のプレースホルダーを入力してください']}">
              </div>
              <!-- スキップ可能か -->
              <div class="form-check">
                <input type="hidden" id="question_is_skip_allowed_hidden_${question_id}"
                       class="question_is_skip_allowed_hidden" name="question_is_skip_allowed" disabled="disabled">
                <input class="form-check-input question_is_skip_allowed_check" type="checkbox"
                       id="question_is_skip_allowed_check_${question_id}" name="question_is_skip_allowed" checked>
                <label class="form-check-label"
                       for="question_is_skip_allowed_check_${question_id}">${translate_catalog['この質問をスキップ可能にする']}</label>
              </div>
              <!-- 回答結果を公開するか -->
              <div class="form-check">
                <input type="hidden" id="question_is_result_public_hidden_${question_id}"
                       class="question_is_result_public_hidden" name="question_is_result_public" disabled="disabled">
                <input class="form-check-input question_is_result_public_check" type="checkbox"
                       id="question_is_result_public_check_${question_id}" name="question_is_result_public" checked>
                <label class="form-check-label"
                       for="question_is_result_public_check_${question_id}">${translate_catalog['この質問への回答データを公開する']}</label>
              </div>
            </div>
          </div>
        
          <!-- 回答の選択肢のリスト -->
          <div class="choices-list"
               data-parent="#question-accordion">
            <!-- 選択肢のリストが入るコンテナ -->
            <div class="list-group choice-container"></div>
            <!-- 選択肢を追加するボタン -->
            <div class="list-group-item">
              <div align="center">
                <button class="add-choice-button btn btn-secondary align-items-center" type="button">
                  ${translate_catalog['選択肢を追加']}
                </button>
              </div>
            </div>
          </div>
        
          <!-- 選択肢のアコーディオンを開閉するボタン -->
          <div class="list-group-item">
            <div align="center">
              <button class="toggle-choices-accordion-button btn btn-secondary align-items-center" type="button">
                <i class="material-icons accordion-arrow">keyboard_arrow_up</i>
              </button>
            </div>
          </div>
        </div>
    </div>
    `;
};

const get_choice_item = (choice_id) => {
    return `
    <div class="list-group-item">
      <div class="form-group row">
        <label for="choice-text_${choice_id}" class="col-md-2 col-form-label">
          ${translate_catalog['選択肢']}　<span class="badge badge-danger">${translate_catalog['必須']}</span>
        </label>
        <div class="col-md-10 delete-choice-group">
          <input type="text" id="choice-text_${choice_id}" class="form-control choice-text"
                 placeholder="${translate_catalog['風邪を引いたため']}" required>
          <button class="delete-choice-button btn btn-sm btn-danger align-items-center" type="button">
            <i class="material-icons">delete</i>
          </button>
        </div>
      
      </div>
    </div>
    `
};
