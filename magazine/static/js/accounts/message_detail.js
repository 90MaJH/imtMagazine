$(document).ready(function () {
   var div = document.getElementById('msg_card_body');
   $('#msg_card_body').animate({
      scrollTop: div.scrollHeight - div.clientHeight
   }, 500);

    $('.footer').remove();
});

function submit(){
    var form = document.message_form;
    form.submit();
}
