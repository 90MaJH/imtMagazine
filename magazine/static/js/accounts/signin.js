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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function signout() {
    window.location.href = '/signout';
}

function check_notification(notificationId) {
    window.location.href = `/check_notification/${notificationId}`;
}

function delete_notification(e, notificationId) {
    if (!e)
      e = window.event;

    //IE9 & Other Browsers
    if (e.stopPropagation) {
      e.stopPropagation();
    }
    //IE8 and Lower
    else {
      e.cancelBubble = true;
    }

    $.ajax({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        type: "POST",
        url: `/delete_notification/`,
        data: {
            'notificationId': notificationId,
            'csrfmiddlewaretoken': csrftoken,
        },
        dataType: "json",
        success: function (response) {
            if (response === 200) {
                document.getElementById(`notification-${notificationId}`).remove();
            } else {
                alert('fail to delete')
            }
        },
        error: function (request, status, error) {
            alert('fail to delete')
        }
    })
}