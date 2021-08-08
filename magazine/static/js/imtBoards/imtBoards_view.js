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

function postDelete(postId) {
    if (post.pub_user === '0') {
        var password = prompt('type your password', 'under 4 charatcters');

        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                    (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: "POST",
            url: `/checkPassword/`,
            data: {
                'passwordFromUser': password,
                'target': 'imtBoards_post',
                'postId': postId,
                'replySeq': 0,
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success: function (response) {
                if (response === 200) {
                    $.ajax({
                        beforeSend: function (xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                                (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                            }
                        },
                        type: "POST",
                        url: `/deletePost/`,
                        data: {
                            'target': 'imtBoards',
                            'postId': postId,
                            'csrfmiddlewaretoken': csrftoken,
                        },
                        dataType: "json",
                        success: function (response) {
                            if (response === 200) {
                                alert('delete success')
                                location.href = '/imtBoards_list/';
                            } else {
                                alert('fail to delete')
                            }
                        },
                        error: function (request, status, error) {
                            alert('fail to delete')
                        }
                    })
                } else {
                    alert('wrong password')
                }
            },
            error: function (request, status, error) {
                // window.location.replace("/accounts/login/")
            }
        })
    } else if (post.pub_user === user.id) {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                    (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: "POST",
            url: `/deletePost/`,
            data: {
                'target': 'imtBoards',
                'postId': postId,
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success: function (response) {
                if (response === 200) {
                    alert('delete success')
                    location.href = '/imtBoards_list/';
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

function postModify(postId) {
    if (post.pub_user === '0') {
        var password = prompt('type your password', 'under 4 charatcters');

        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                    (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: "POST",
            url: `/checkPassword/`,
            data: {
                'passwordFromUser': password,
                'target': 'imtBoards_post',
                'postId': postId,
                'replySeq': 0,
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success: function (response) {
                if (response === 200) {
                    location.href = `/imtBoards_modify/${postId}`;
                } else {
                    alert('wrong password')
                }
            },
            error: function (request, status, error) {
                // window.location.replace("/accounts/login/")
            }
        })
    } else if (post.pub_user === user.id) {
        location.href = `/imtBoards_modify/${post.id}`;
    }

}

function sendMessage(opponent){
    location.href = `/message_detail/0/${opponent}`
}

function replyDelete(e, postId, seq, replyUser) {
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

    if (Number(replyUser) === 0) {
        var password = prompt('type your password', 'under 4 charatcters');

        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                    (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: "POST",
            url: `/checkPassword/`,
            data: {
                'passwordFromUser': password,
                'target': 'imtBoards_reply',
                'postId': postId,
                'replySeq': seq,
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success: function (response) {
                if (response === 200) {
                    $.ajax({
                        beforeSend: function (xhr, settings) {
                            if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                                (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                            }
                        },
                        type: "POST",
                        url: `/deleteReply/`,
                        data: {
                            'target': 'imtBoards',
                            'postId': postId,
                            'replySeq': seq,
                            'csrfmiddlewaretoken': csrftoken,
                        },
                        dataType: "json",
                        success: function (response) {
                            if (response === 200) {
                                location.reload();
                            } else {
                                alert('fail to delete')
                            }
                        },
                        error: function (request, status, error) {
                            alert('fail to delete')
                        }
                    })
                } else {
                    alert('wrong password')
                }
            },
            error: function (request, status, error) {
                // window.location.replace("/accounts/login/")
            }
        })
    } else if (Number(replyUser) === Number(user.id)) {
        $.ajax({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain &&
                    (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            },
            type: "POST",
            url: `/deleteReply/`,
            data: {
                'target': 'imtBoards',
                'postId': postId,
                'replySeq': seq,
                'csrfmiddlewaretoken': csrftoken,
            },
            dataType: "json",
            success: function (response) {
                if (response === 200) {
                    location.reload();
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

function replySubmit() {
    var form = document.replyForm;

    if (!form.reply_user_nickname) {
        var reply_user_nickname = document.createElement("input");
        reply_user_nickname.name = 'reply_user_nickname';
        reply_user_nickname.value = user.nickname;
        reply_user_nickname.style.display = 'none';
        form.appendChild(reply_user_nickname);
    }

    if (!form.password) {
        var password = document.createElement("input");
        password.name = 'password';
        password.value = '0000';
        password.style.display = 'none';
        form.appendChild(password);
    }

    if (user.is_active === 'True') {
        document.getElementById('id_reply_user').value = user.id;
    } else {
        document.getElementById('id_reply_user').value = 0;
    }

    form.submit();
}

function reReply(orgId, orgContext) {
    document.getElementById('rereply-comment').classList.remove("visible-false-custom");
    document.getElementById('parent-reply-id').value = orgId;
    document.getElementById('re-reply').innerText = `re-reply for ${orgContext}...`;
    document.getElementById('re-reply-cancel').innerHTML =
        '<span onClick="reReplyCancel()">X</span>';
}

function reReplyCancel() {
    document.getElementById('rereply-comment').classList.add("visible-false-custom");
    document.getElementById('parent-reply-id').value = 0;
    document.getElementById('re-reply').innerText = ``
    document.getElementById('re-reply-cancel').innerHTML = ''
}
