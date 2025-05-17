function getCSRFToken() {
    const name = 'csrftoken';
    const cookie = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : '';
}

function likeComment(commentId) {
    fetch(`/comment/${commentId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => updateCommentReactions(commentId, data));
}

function dislikeComment(commentId) {
    fetch(`/comment/${commentId}/dislike/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Accept': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => updateCommentReactions(commentId, data));
}

function updateCommentReactions(commentId, data) {
    document.getElementById(`comment-like-count-${commentId}`).textContent = data.likes;
    document.getElementById(`comment-dislike-count-${commentId}`).textContent = data.dislikes;

    const likeBtn = document.querySelector(`#comment-${commentId} .comment-like-btn`);
    const dislikeBtn = document.querySelector(`#comment-${commentId} .comment-dislike-btn`);

    if (data.likes > parseInt(likeBtn.textContent)) {
        likeBtn.classList.add('active');
        dislikeBtn.classList.remove('active');
    } else if (data.dislikes > parseInt(dislikeBtn.textContent)) {
        dislikeBtn.classList.add('active');
        likeBtn.classList.remove('active');
    } else {
        likeBtn.classList.remove('active');
        dislikeBtn.classList.remove('active');
    }
}
