function select_dropdown(key, value) {
    document.getElementById('dropdownMenuButton').innerText = value;
    document.getElementById('dropdownMenuButton').value = key;
}

function search() {
    var searchCategory = document.getElementById('dropdownMenuButton').value;
    var searchWord = document.getElementById('search-word').value

    if (searchCategory !== '' || searchWord !== '') {
        location.href = `/qnas_list/?searchCategory=${searchCategory}&searchWord=${searchWord}`
    }
}

function prev(p) {
    var searchCategory = document.getElementById('dropdownMenuButton').value;
    var searchWord = document.getElementById('search-word').value

    if (searchCategory !== '' || searchWord !== '') {
        location.href = `/qnas_list/?searchCategory=${searchCategory}&searchWord=${searchWord}&p=${p}`
    } else {
        location.href = `/qnas_list/?p=${p}`
    }
}

function next(p) {
    var searchCategory = document.getElementById('dropdownMenuButton').value;
    var searchWord = document.getElementById('search-word').value

    if (searchCategory !== '' || searchWord !== '') {
        location.href = `/qnas_list/?searchCategory=${searchCategory}&searchWord=${searchWord}&p=${p}`
    } else {
        location.href = `/qnas_list/?p=${p}`
    }
}