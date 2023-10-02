async function likeComment(commentId) {
    const csrftoken = getCookie('csrftoken');

    try {
        const response = await fetch(`/like_comment/${commentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok (HTTP status: ${response.status})`);
        }

        const data = await response.json();
        const likeCountElement = document.getElementById(`likeCount_${commentId}`);
        likeCountElement.innerText = `| Likes: ${data.likes}`;
        const likeButton = document.getElementById(`likeButton_${commentId}`);
        likeButton.innerText = data.liked ? 'Unlike' : 'Like';
    } catch (error) {
        console.error('Error:', error.message);
    }
}

// Function to get CSRF cookie value
function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}
