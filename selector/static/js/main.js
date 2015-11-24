
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$(document).ready(function() {
  var $attrDeleteBtn = $('.delete-attribute');

  $attrDeleteBtn.on('click', function() {
    var $this = $(this);
    var url = $this.attr('data-url');
    var attr = $this.attr('data-attribute');
    var confirmMsg = $this.attr('data-confirm-msg') + attr + '?';
    var csrftoken = getCookie('csrftoken');
    // set CSRFToken
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

    if (window.confirm(confirmMsg)) {
      console.log('DO IT', $(this).attr('data-attribute'));
      $.post(url, {action: 'delete', name: attr}, function() {
        document.location.reload(true);
      });
    }
  });
});
