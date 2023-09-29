async function likeComment(commentId) {
    const csrftoken = "{{ csrf_token }}";

    try {
        const response = await fetch(`/like_comment/${commentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            throw new Error(`Network response was not ok (HTTP status: ${response.status})`);
        }

        const data = await response.json();
        document.getElementById(`likeCount_${commentId}`).innerText = 'Likes: ' + data.likes;
    } catch (error) {
        console.error('Error:', error.message);
    }
}
