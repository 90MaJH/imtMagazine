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


function check_message(msg_header, opponent) {
    window.location.href = `/message_detail/${msg_header}/${opponent}`;
}

function delete_message(e, msg_header) {
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

    var confirm = window.confirm("Do you really want to exit this chatroom?");

    if (confirm) {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                    (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: "POST",
            url: `/message_delete/`,
            data: {
                'msg_header': msg_header,
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success: function (response) {
                if (response === 200) {
                    document.getElementById(`msg-${msg_header}`).remove();
                } else {
                    alert('fail to delete')
                }
            },
            error: function (request, status, error) {
                alert('fail to delete')
            }
        })
    }
}