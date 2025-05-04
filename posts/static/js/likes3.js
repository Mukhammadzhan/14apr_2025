function updateReactionButtons(postId, data) {
    const likeButton = document.getElementById(`likeButton${postId}`);
    const dislikeButton = document.getElementById(`dislikeButton${postId}`);
    
    // Обновляем счетчики
    likeButton.querySelector('.count').textContent = data.likes;
    dislikeButton.querySelector('.count').textContent = data.dislikes;
    
    // Обновляем классы активности
    likeButton.classList.toggle('active', data.user_liked);
    dislikeButton.classList.toggle('active', data.user_disliked);
    
    // Анимация для новой реакции
    if (data.status === 'liked') {
        likeButton.classList.add('reaction-animate');
        setTimeout(() => likeButton.classList.remove('reaction-animate'), 400);
    } 
    else if (data.status === 'disliked') {
        dislikeButton.classList.add('reaction-animate');
        setTimeout(() => dislikeButton.classList.remove('reaction-animate'), 400);
    }
}