var commentList = document.getElementById('');

// new channel message received
swampdragon.onChannelMessage(function (channels, message) {
    // add new comment
    addCommentReview(message.data);
});

//SwampDragon connection open

swampdragon.open(function () {
// Once the connection is open subscribe to notification
    swampdragon.subscribe('commentreview', 'commentreview');
});

// Add new  comment

function addCommentReview(data) {
    if (window.Notification && Notification.permission === 'granted') {
        new Notification(data);
    }

    $('#display_comment_review_' + data.id).append(data);


}
//
//<div class="row" id="comment_review_number_{{ comment.id }}">' +
//        '<div class="col-lg-1" style="width: 10%;padding: 5px;">' +
//        '<div class="thumbnail">' +
//        '<img src="{{ comment.user_profile.avata.url}}"' +
//        'id="" alt="id ={{ comment.user_profile.user.id }}"width="100%" height="100%">' +
//        '</div>' +
//        '</div>' +
//        '<div class="col-lg-11" style="width: 90%;padding: 5px;">' +
//        '<div style="width: 90%;">' +
//        '<span style="font-size: 14px;">' +
//        '<strong class="text-success">{{ comment.user_profile.user.first_name }}' +
//        '{{ comment.user_profile.user.last_name }}: </strong>' +
//        '{{ comment.content }}' +
//        '</span></div>' +
//        '{% return_user_like_of_comment comment.pk as all_like_cmt %}' +
//        '<span id="like_unlike_comment_link_{{ comment.pk }}">' +
//        '{% if user.id in all_like_cmt %}' +
//        '<button type="button" class="btn btn-link"' +
//        ' style="padding: 2px 0 5px 0; "' +
//        'onclick="unlike_comment({{ comment.pk }})"> Unlike' +
//        '</button>' +
//        '{% else %}' +
//        '<button type="button" class="btn btn-link" style="padding: 2px 0 5px 0;"' +
//        'onclick="like_comment({{ comment.pk }})"> Like </button>' +
//        '{% endif %}' +
//        '</span>' +
//        '- {{ comment.date|date:"d-m-Y" }}<br>' +
//        '<span id="number_like_comment_{{ comment.pk }}"> {{ comment.get_total_like }}</span>' +
//        'like this<br></div></div>