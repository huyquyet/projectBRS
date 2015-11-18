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

function create_comment_review(id) {
    var review_id = $('#review_id_' + id).val();
    var content_comment = $('#content_comment_' + id).val();
    $.ajax({
        url: '/comment/create_comment',
        type: 'POST',
        data: {
            review_id: review_id,
            content_comment: content_comment
        },
        success: function (json) {
            var d1 = new Date();
            $('#content_comment_' + id).val('');
            $('#display_comment_review_' + id).append('<div class="row">' +
                '<div class="col-lg-1" style="width: 10%;padding: 5px;">' +
                '<div class="thumbnail">' +
                '<img src="' + json.user_avata + '" id="" alt="id =' + json.user_id + '"width="100%" height="100%">' +
                ' </div>' +
                '</div>' +
                '<div class="col-lg-11" style="width: 90%;padding: 5px;">' +
                '<div style="width: 10%;float: right">' +
                '<form action="/comment/comment_delete/"method="post" id="delete-comment-' + json.comment_id + '">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="ap9rMTqa8ZJggNudUvso0wU3huBQcUzI">' +
                '<input type="hidden" value="' + json.comment_id + '"name="comment_id">' +
                '<input type="hidden" value="' + json.book_id + '"name="book_id">' +
                '<button id="id-btn-' + json.comment_id + '-delete" class="btn btn-xs btn-danger btn-delete-comment"' +
                'onclick="confirm_delete_comment("delete-comment-' + json.comment_id + '")">' +
                'Delete' +
                '</button>' +
                '</form>' +
                '</div>' +
                '<div style="width: 90%;">' +
                '<span style="font-size: 14px;">' +
                '<strong class="text-success"> ' + json.user_first_name + ' ' + json.user_last_name + ': </strong>' + json.content +
                '</span>' +
                '</div>' +
                '<input type="hidden" value="' + json.comment_id + '" name="comment_id">' +
                '<form action="/comment/comment_like_unlike/" method="post">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="ap9rMTqa8ZJggNudUvso0wU3huBQcUzI">' +
                '<input type="hidden" value="like" name="check">' +
                '<button type="submit" class="btn btn-link"style="padding: 2px 0 5px 0;"> Like </button>' +
                ' - ' + d1.getDate() + '-' + d1.getMonth() + '-' + d1.getFullYear() + '<br> 0 like this <br>' +
                '</form>' +
                '</div>' +
                '</div')
        },
        error: function (json) {
        }
    })
}
