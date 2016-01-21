(function ($) {

  // Set CSRF token to jQuery's ajax requests.
  (function () {

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
      }
    });

  })();

  // When document is ready.
  $(function () {

    // Remove associations.
    (function () {

      var $attrDeleteBtn = $('.delete-attribute');

      $attrDeleteBtn.on('click', function() {
        var $this = $(this);
        var url = $this.attr('data-url');
        var attr = $this.attr('data-attribute');
        var confirmMsg = $this.attr('data-confirm-msg') + attr + '?';

        if (window.confirm(confirmMsg)) {
          console.log('DO IT', $(this).attr('data-attribute'));
          $.post(url, {action: 'delete', name: attr}, function() {
            document.location.reload(true);
          });
        }
      });

    })();

    // Select invite list items.
    (function () {

      var
      $inviteList = $('.invite-list'),
      $items = $inviteList.find('.invite-item');

      $items.on('click', function (e) {

        var
        $this = $(this),
        sectionId = $this.attr('data-id'),
        $sections = $items.filter('[data-id="' + sectionId + '"]'),
        $checkbox = $sections.find('input[type="checkbox"]');

        // Toggle checkbox
        if (!$(e.target).is($checkbox)) {
          $checkbox.prop('checked', !$checkbox.prop('checked'));
        }

        // Toggle item sections class
        $sections.toggleClass('active');

      });

    })();

    // Content sizer.
    (function () {

      var
      $root = $(document.documentElement),
      $increase = $('.content-sizer-increase'),
      $decrease = $('.content-sizer-decrease'),
      getSize = function () {

        return $root.hasClass('content-size-1') ? 1 :
               $root.hasClass('content-size-2') ? 2 :
               $root.hasClass('content-size-3') ? 3 :
               $root.hasClass('content-size-4') ? 4 : 5;

      },
      updateActions = function () {

        var currentSize = getSize();

        // Disable/enable decrease button.
        if (currentSize === 1) {
          $decrease.addClass('disabled');
        }
        else {
          $decrease.removeClass('disabled');
        }

        // Disable/enable increase button.
        if (currentSize === 5) {
          $increase.addClass('disabled');
        }
        else {
          $increase.removeClass('disabled');
        }

      };

      updateActions();

      $increase.on('click', function () {

        var
        currentSize = getSize(),
        nextSize = currentSize + 1;

        if (currentSize < 5) {
          $root
          .removeClass('content-size-' + currentSize)
          .addClass('content-size-' + nextSize);
        }

        updateActions();

      });

      $decrease.on('click', function () {

        var
        currentSize = getSize(),
        nextSize = currentSize - 1;

        if (currentSize > 1) {
          $root
          .removeClass('content-size-' + currentSize)
          .addClass('content-size-' + nextSize);
        }

        updateActions();

      });

    })();

  });

  //
  // Generic helpers.
  //

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

})(jQuery);