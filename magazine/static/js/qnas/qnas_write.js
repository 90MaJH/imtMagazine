var checkUnload = true;
$(window).on('beforeunload', function () {
    if (checkUnload) return "이 페이지를 벗어나면 작성된 내용은 저장되지 않습니다.";
});

window.onload = function () {
    if (user.is_active === 'True') {
        var pub_user = document.getElementById('id_pub_user');
        pub_user.value = user.id;
    }
}

function save() {
    checkUnload = false;
    var form = document.postForm;

    if (!form.password) {
        var password = document.createElement("input");
        password.name = 'password';
        password.value = '0000';
        password.style.display = 'none';
        form.appendChild(password);
    }

    if (!form.pub_user_nickname) {
        var pub_user_nickname = document.createElement("input");
        pub_user_nickname.name = 'pub_user_nickname';
        pub_user_nickname.value = user.nickname;
        pub_user_nickname.style.display = 'none';
        form.appendChild(pub_user_nickname);
    }

    form.submit();
}
