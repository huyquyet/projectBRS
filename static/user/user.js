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
//  loai bo khoang trang dau va cuoi String
function Trim(sString) {
    while (sString.substring(0, 1) == ' ') {
        sString = sString.substring(1, sString.length);
    }
    while (sString.substring(sString.length - 1, sString.length) == ' ') {
        sString = sString.substring(0, sString.length - 1);
    }
    return sString;
}

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
    if (Trim(content_comment) == '') {
        return false;
    } else {
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
                $('#display_comment_review_' + id).append(json.html);
            },
            error: function (json) {
            }
        })
    }
}


function unlike_comment(id_comment) {
    $.ajax({
        url: '/comment/comment_unlike/',
        type: "POST",
        data: {
            id_comment: id_comment
        },
        success: function (json) {
            if (json.result) {
                $('#like_unlike_comment_link_' + id_comment).html('<button type="button" class="btn btn-link" style="padding: 2px 0 5px 0; " onclick="like_comment(' + id_comment + ')" > Like');
                $('#number_like_comment_' + id_comment).html(json.like);
            } else {
                $('#like_unlike_comment_link_' + id_comment).html('<button type="button" class="btn btn-link" style="padding: 2px 0 5px 0; " onclick="unlike_comment(' + id_comment + ')" > Like');
            }
        },
        error: function () {
            alert('error submit data');
        }
    })
}

function like_comment(id_comment) {
    $.ajax({
        url: '/comment/comment_like/',
        type: 'POST',
        data: {
            id_comment: id_comment
        },
        success: function (json) {
            if (json.result) {
                $('#like_unlike_comment_link_' + id_comment).html('<button type="button" class="btn btn-link" style="padding: 2px 0 5px 0; " onclick="unlike_comment(' + id_comment + ')" > Unlike');
                $('#number_like_comment_' + id_comment).html(json.like);
            } else {
                $('#like_unlike_comment_link_' + id_comment).html('<button type="button" class="btn btn-link" style="padding: 2px 0 5px 0; " onclick="like_comment(' + id_comment + ')" > Unlike');
            }
        },
        error: function () {
            alert('error submit data');
        }
    })
}

function delete_comment(id_comment) {
    if (confirm('Are you sure you want delete comment ?') == true) {
        $.ajax({
            url: '/comment/comment_delete/',
            type: 'POST',
            data: {
                comment_id: id_comment
            },
            success: function (json) {
                alert(json.result);
                $('#comment_review_number_' + id_comment).hide();
            },
            error: ''
        })
    }
}

function read_book_start(id_book) {
    console.log('vao day');
    $.ajax({
        url: '/book/user/readbook',
        type: 'POST',
        data: {
            book_id: id_book
        },
        success: function (json) {
            $('#button_read_book').html('<div class="dropdown"><button type="button"' +
                'class="btn btn-info dropdown-toggle" data-toggle="dropdown" style="width:160px">' +
                '<strong>Reading book !</strong>&nbsp;&nbsp;&nbsp;<span class="caret"></span>' +
                '</button>' +
                '<ul class="dropdown-menu"><li>' +
                '<a href="#" onclick="read_book_finish(' + id_book + '); return false;">Finish !</a>' +
                '</li></ul></div>')
        },
        error: ''
    })

}

function read_book_finish(id_book) {
    $.ajax({
        url: '/book/user/readfinish',
        type: 'POST',
        data: {
            book_id: id_book
        },
        success: function (json) {
            $('#button_read_book').html('<div class=" dropdown"><button type="button"' +
                'class="btn btn-info dropdown-toggle" data-toggle="dropdown" style="width:160px">' +
                '<strong>Read book !</strong>&nbsp;&nbsp;&nbsp;<span class="caret"></span></button>' +
                '<ul class="dropdown-menu"><li><a href="#">Want to Read book !</a>' +
                '</li></ul></div>')
        },
        error: function (json) {
            alert(json.result)
        }
    })

}

function set_rating(id_book, rating) {
    $.ajax({
        url: '/book/user/rating/',
        type: 'POST',
        data: {
            book_id: id_book,
            rating: rating
        },
        success: function (json) {
            if (json.result == true) {
                var a = $('#display_star');
                a.html('');
                for (var i = 0; i < 5; i++) {
                    var j = i + 1;
                    if (j <= rating) {
                        a.append('<a href="" class="btn-lg" style="padding: 0;"' +
                            'onclick="set_rating(' + id_book + ',' + j + '); return false;">' +
                            '<span class="glyphicon glyphicon-star" style="color: red"></a>');
                    }
                    else {
                        a.append('<a href="" class="btn-lg" style="padding: 0;"' +
                            'onclick="set_rating(' + id_book + ',' + j + '); return false;">' +
                            '<span class="glyphicon glyphicon-star-empty"></a>');
                    }
                }
                $('#number_point').html(json.number_point);
                $('#number_rating').html(json.number_rating);
            } else {
                alert('Error')
            }
        },
        error: function (json) {
            alert('Error')
        }
    })
}

function favorite_book(id_book) {
    $.ajax({
        url: '/book/user/add_favorite',
        type: 'POST',
        data: {
            book_id: id_book
        },
        success: function (json) {
            if (json.result == true) {
                $('#favorite').html('<button class="btn btn-success "' +
                    'style="width: 190px; height: 30px;margin: 0 0 0 12px; font-size: 14px;">' +
                    'Favorited</button>');
            } else
                alert('Error');
        },
        error: function (json) {
            alert('Error');
        }
    })
}

function load_more_comment(id_review, start, end, number_comment) {
    var end_start = end;
    var end_end = end + (end - start);
    $.ajax({
        url: '/comment/load_more_comment/',
        type: 'POST',
        data: {
            review_id: id_review,
            start: start,
            end: end,
            number_comment: number_comment
        },
        success: function (json) {
            for (var i = 0; i < Object.keys(json).length; i++) {
                var jsons = json[i];
                $('#display_comment_review_' + id_review).prepend('<div class="row" id="comment_review_number_' + jsons.comment_id + '">' +
                    '<div class="col-lg-1" style="width: 10%;padding: 5px;">' +
                    '<div class="thumbnail">' +
                    '<img src="' + jsons.user_avata + '" id="" alt="id =' + jsons.user_id + '"width="100%" height="100%">' +
                    ' </div>' +
                    '</div>' +
                    '<div class="col-lg-11" style="width: 90%;padding: 5px;">' +
                    '<div style="width: 10%;float: right">' +
                    '<button id="id-btn-' + jsons.comment_id + '-delete" type="button"' +
                    'class="btn btn-xs btn-danger btn-delete-comment"onclick="delete_comment(' + jsons.comment_id + ')">' +
                    'Delete' +
                    '</button>' +
                    '</div>' +
                    '<div style="width: 90%;">' +
                    '<span style="font-size: 14px;">' +
                    '<strong class="text-success"> ' + jsons.user_first_name + ' ' + jsons.user_last_name + ': </strong>' + jsons.content +
                    '</span>' +
                    '</div>' +
                    '<span id="like_unlike_comment_link_' + jsons.comment_id + '">' +
                    '<button type="button" class="btn btn-link"style="padding: 2px 0 5px 0;" onclick="like_comment(' + jsons.comment_id + ')"> Like</button>' +
                    '</span>' +
                    ' - ' + jsons.date + '<br> <span id="number_like_comment_' + jsons.comment_id + '">0</span> like this <br>' +
                    '</div>' +
                    '</div>');
            }
            if (end < number_comment) {
                $('#view_more_comment_' + id_review).html('<span class="pull-right">.... ' + end + ' of ' + number_comment + '</span>' +
                    '<button  class="btn btn-link"onclick="load_more_comment(' + id_review + ', ' + end_start +
                    ', ' + end_end + ',' + number_comment + ')"> View more comment.....</button>'
                );
            }
            else {
                $('#view_more_comment_' + id_review).html('');
            }
        },
        error: function (json) {
            alert('Error');
        }
    })
}
