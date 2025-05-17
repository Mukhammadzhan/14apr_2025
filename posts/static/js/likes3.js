function likePost(postId) {
    fetch(`/post/${postId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Лайк поставлен:', data);
        document.querySelector(`#likeButton${postId} .count`).innerText = data.likes;
        document.querySelector(`#dislikeButton${postId} .count`).innerText = data.dislikes;
    })
    .catch(error => {
        console.error('Ошибка при лайке:', error);
    });
}

function dislikePost(postId) {
    fetch(`/post/${postId}/dislike`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        console.log('Дизлайк поставлен:', data);
        document.querySelector(`#likeButton${postId} .count`).innerText = data.likes;
        document.querySelector(`#dislikeButton${postId} .count`).innerText = data.dislikes;
    })
    .catch(error => {
        console.error('Ошибка при дизлайке:', error);
    });
}

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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