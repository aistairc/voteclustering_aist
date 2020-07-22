const BK_COLORS = [
    "#FF6384", "#36A2EB", "#FFCE56", "#339900", "#ff6633",
    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
    '#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'
];

const HV_COLORS = [
    "#FF6384", "#36A2EB", "#FFCE56", "#339900", "#ff6633",
    '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
    '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
    '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
    '#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
    '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
    '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
    '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
    '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
    '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
    '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF'
];

const NOCHOICE = '<div><h2>回答はありません</h2></div>',
      WINDOW_WIDTH = window.innerWidth,
      WINDOW_HEIGHT = window.innerHeight,
      SIDEBAR_WIDTH = 230,
      MARGIN_WIDTH = 60,
      SVG_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH - MARGIN_WIDTH,
      HEADLINE_HEIGHT = 41,
      FOOTER_HEIGHT = 51,
      HEADER_HEIGHT = 55,
      CONTENT_HEIGHT = WINDOW_HEIGHT - HEADLINE_HEIGHT - FOOTER_HEIGHT - HEADER_HEIGHT;

/**
 * 渡された日時をフォーマットして返却する。
 * @param {String} date
 * @param {String} currentFormat
 * @param {String} format
 * @returns {String} 指定フォーマットの日時
 */
const formatDate = (date, currentFormat, format) => {
    const formatDate = moment(date, currentFormat);
    return formatDate.format(format);
};


/**
 * 渡された文字列をアンエスケープして返却する
 * @param target アンエスケープする対象の文字列
 * @returns {string} アンエスケープ後の文字列
 */
const unescapeHtml = (target) => {
    if (typeof target !== 'string') return target;

    const patterns = {
        '&lt;'   : '<',
        '&gt;'   : '>',
        '&amp;'  : '&',
        '&quot;' : '"',
        '&#x27;' : '\'',
        '&#x60;' : '`'
    };

    return target.replace(/&(lt|gt|amp|quot|#x27|#x60);/g, (match) => {
        return patterns[match];
    });
};
