// option 하나 선택하면 나머지에서 선택 못하게 막으려는 모듈.
// 공수 대비 필요성이 낮아보여서 개발 중단
window.onload = function() {
    targets = $('option')
    for(var i=0; i<targets.length; i++){
        targets[i].classList.add(targets[i].label);
    }
}