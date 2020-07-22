/**
 * 設問クラス
 * @param  Object values 1設問データ
 */
export default function (values) {

    for (var key in values) {
        this[key] = values[key];
    }

    switch (this.type) {

        case "single":
        case "multi":
            this.answer = {}
            for (var choice of this.choices) {
                this.answer[choice.key] = false;
            }
            break;

        case "singletext":
        case "userid":
        case "longtext":
            this.answer = "";
            break;

        case "longtext-multi":
            this.answer = {free: []};
            this.opinionList = [];
            this.suggestList = [];
            break;

        case "question":
            this.answer = {select: {}, free: []};
            this.opinionList = [];
            this.suggestList = [];
            this.more = false;
            break;

        default:
            this.answer = "";
    }

    this.isAnswered = (answer) => {
        if (answer === undefined) {
            answer = this.answer;
        }

        var answered = false;

        switch (this.type) {
            case "userid":
            case "singletext":
            case "longtext": {
                answered = answer != null && (answer.length > 0 && (!voteClusteringOptions.selfOpinion.maxLength || answer.length <= voteClusteringOptions.selfOpinion.maxLength));
                break;
            }

            case "single":
            case "multi": {
                answered = answer != null && Object.values(answer).find(x => x) !== undefined;
                break;
            }

            case "longtext-multi": {
                answered = answer != null && answer.length;
                break;
            }

            case "question": {
                answered = answer != null && (Object.values(answer.select || {}).find(x => x) !== undefined || (answer.free != null && answer.free.length));
                break;
            }

            case "tos": {
                answered = answer === true;
                break;
            }
        }

        return answered;
    }

    this.getAnswer = () => {
        switch (this.type) {
            case "userid":
            case "singletext":
            case "longtext": {
                return this.answer;
            }

            case "single": {
                return Object.keys(this.answer).find(x => this.answer[x]);
            }

            case "multi": {
                return Object.keys(this.answer).filter(x => this.answer[x]);
            }

            case "longtext-multi": {
                return this.answer;
            }

            case "question": {
                const answerList = [];
                Object.keys(this.answer.select).forEach(key => {
                    answerList.push({key: key, isSelected: this.answer.select[key]})
                });
                return {
                    list: answerList,
                    free: this.answer.free,
                    test_select: this.answer.select
                };
            }
        }

        return undefined;
    }
}
