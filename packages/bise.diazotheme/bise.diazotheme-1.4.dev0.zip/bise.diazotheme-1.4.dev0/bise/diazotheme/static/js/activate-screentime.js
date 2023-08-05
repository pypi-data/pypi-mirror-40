$(document).ready(function() {
    var content = $("#content");
    if (content.length > 0) {
        if (typeof content.screentimeAnalytics === 'function') {
            content.screentimeAnalytics();
        }
    }
});
