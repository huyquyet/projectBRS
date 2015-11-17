
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
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function delete_book(id) {
    if (confirm('are you sure you want to remove this book?') == true) {
        var book_id = id;
        $.ajax({
                url: "/admin/book/delete",
                type: "POST",
                data: {
                    book_id: book_id
                },
                success: function (json) {
                    alert(json.result);
                    $('#row_book_' + id).hide();
                },
                error: function (result) {
                    alert(json.result);
                }
            }
        );
    }
    else {
        return false;
    }
}