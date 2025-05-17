function getCSRFToken() {
    const name = 'csrftoken';
    const cookie = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookie ? cookie.split('=')[1] : '';
}

function likeComment(commentId) {
    fetch(`/comments/${commentId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`comment-like-count-${commentId}`).innerText = data.likes;
        document.getElementById(`comment-dislike-count-${commentId}`).innerText = data.dislikes;
    });
}

function dislikeComment(commentId) {
    fetch(`/comments/${commentId}/dislike/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`comment-like-count-${commentId}`).innerText = data.likes;
        document.getElementById(`comment-dislike-count-${commentId}`).innerText = data.dislikes;
    });
}

// Функция получения CSRF токена из cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmed.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
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
