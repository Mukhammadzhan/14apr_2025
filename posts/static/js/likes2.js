function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrf_token = getCookie('csrftoken');


function likePost(postId) {
    fetch(`/post/${postId}/like`, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
    })
    .then(response => response.json())
    .then(data => {
        const likeButton = document.getElementById(`likeButton${postId}`);
        likeButton.innerText = `👍${data.likes}`;
        
        likeButton.classList.add('reaction-animate', 'like-active');
        
        setTimeout(() => {
            likeButton.classList.remove('reaction-animate', 'like-active');
        }, 300); // убираем анимацию через 0.3 секунды
    });
}

function dislikePost(postId) {
    fetch(`/post/${postId}/dislike`, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
    })
    .then(response => response.json())
    .then(data => {
        const dislikeButton = document.getElementById(`dislikeButton${postId}`);
        dislikeButton.innerText = `👎${data.dislikes}`;

        dislikeButton.classList.add('reaction-animate', 'dislike-active');

        setTimeout(() => {
            dislikeButton.classList.remove('reaction-animate', 'dislike-active');
        }, 300); // убираем анимацию через 0.3 секунды
    });
}
