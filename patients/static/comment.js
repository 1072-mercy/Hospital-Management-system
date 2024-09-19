document.addEventListener('DOMContentLoaded', function () {
    const commentInput = document.getElementById('comment-input');
    const submitButton = document.getElementById('submit-comment');
    const commentsList = document.getElementById('comments-list');
    const patientEmailInput = document.getElementById('patientEmail');

    submitButton.addEventListener('click', function () {
        const commentText = commentInput.value.trim();
        const patientEmail = patientEmailInput.value;

        if (commentText !== '') {
            const commentElement = document.createElement('div');
            commentElement.classList.add('comment');
            commentElement.textContent = commentText;
            commentsList.appendChild(commentElement);
            commentInput.value = '';

            // Include logic to send the comment to the server with patientEmail
            console.log('Sending data:', { comment_text: commentText, patient_email: patientEmail });
            fetch('/comments', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    comment_text: commentText,
                    patient_email: patientEmail,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Server response:', data);
                    // You can handle the response if needed
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            alert('Please enter a comment.');
        }
    });
});