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
    .then(data => {
        console.log('Лайк поставлен:', data);
    
        const likeButton = document.querySelector(`#likeButton${postId}`);
        const dislikeButton = document.querySelector(`#dislikeButton${postId}`);
    
        // Обновляем счётчики
        likeButton.querySelector('.count').innerText = data.likes;
        dislikeButton.querySelector('.count').innerText = data.dislikes;
    
        // Добавляем/убираем класс active
        likeButton.classList.toggle('active', data.user_reaction === 'like');
        dislikeButton.classList.toggle('active', data.user_reaction === 'dislike');
    
        // Добавляем анимацию
        likeButton.classList.add('reaction-animate', 'like');
        setTimeout(() => likeButton.classList.remove('reaction-animate', 'like'), 400);
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
    .then(data => {
        console.log('Дизлайк поставлен:', data);
    
        const likeButton = document.querySelector(`#likeButton${postId}`);
        const dislikeButton = document.querySelector(`#dislikeButton${postId}`);
    
        // Обновляем счётчики
        likeButton.querySelector('.count').innerText = data.likes;
        dislikeButton.querySelector('.count').innerText = data.dislikes;
    
        // Добавляем/убираем класс active
        likeButton.classList.toggle('active', data.user_reaction === 'like');
        dislikeButton.classList.toggle('active', data.user_reaction === 'dislike');
    
        // Добавляем анимацию
        dislikeButton.classList.add('reaction-animate', 'dislike');
        setTimeout(() => dislikeButton.classList.remove('reaction-animate', 'dislike'), 400);
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
