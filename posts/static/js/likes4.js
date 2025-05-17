function likePost(postId) {
    fetch(`/post/${postId}/like`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => response.json())
      .then(data => {
          document.querySelector(`#likeButton${postId} .count`).textContent = data.likes;
          document.querySelector(`#dislikeButton${postId} .count`).textContent = data.dislikes;

          toggleButtonState(postId, 'like', data.user_liked);
          toggleButtonState(postId, 'dislike', data.user_disliked);
      });
}

function dislikePost(postId) {
    fetch(`/post/${postId}/dislike`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => response.json())
      .then(data => {
          document.querySelector(`#likeButton${postId} .count`).textContent = data.likes;
          document.querySelector(`#dislikeButton${postId} .count`).textContent = data.dislikes;

          toggleButtonState(postId, 'like', data.user_liked);
          toggleButtonState(postId, 'dislike', data.user_disliked);
      });
}

function toggleButtonState(postId, type, active) {
    const button = document.getElementById(`${type}Button${postId}`);
    if (active) {
        button.classList.add('active');
    } else {
        button.classList.remove('active');
    }
}

// Получение CSRF-токена из куков
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
