$(document).ready(function () {
  var $body = $('body');

  $body.on('click', 'a.episode-watch', function () {
    var anchor = this;

    $.ajax({
      url: anchor.href,
      success: function(data) {
        if (data.error) {
          sweetAlert('아니!?', data.message, 'error');
        } else {
          sweetAlert('굿잡!', '기록 되었습니다!', 'success');
          setTimeout(function() {location.reload();}, 1000);
        }
      },
      dataType: 'json'
    });

    return false;
  });
});