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


function unlike_review(id_review, id_user) {
    $.ajax({
            url: '/review/unlike',
            type: 'POST',
            data: {
                review_id: id_review,
                user_id: id_user
            },
            success: function (json) {
                $('#like_unlike_link').html('<button type="button" class="btn btn-link" style="padding: 2px 0 5px 0;" onclick="like_review(' + id_review + ',' + id_user + ')" > Like');
                $('#number_like_review_' + id_review).html(json.like);

            },
            error: function () {
                alert('error submit data');
            }
        }
    )
}

function like_review(id_review, id_user) {
    $.ajax({
        url: '/review/like',
        type: 'POST',
        data: {
            review_id: id_review,
            user_id: id_user
        },
        success: function (json) {
            $('#like_unlike_link').html('<button type="button" class="btn btn-link" style="padding: 2px 0 5px 0;" onclick="unlike_review(' + id_review + ',' + id_user + ')" > Unlike');
            $('#number_like_review_' + id_review).html(json.like);
        },
        error: function () {
            alert('error submit data');
        }
    })
}