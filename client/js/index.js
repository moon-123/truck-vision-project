function uploadVideo(event) {
    event.preventDefault();
    var fileInput = document.getElementById('videoInput');
    var file = fileInput.files[0];
    if (!file) {
        console.error('No file selected');
        return;
    }
    var formData = new FormData();
    formData.append('video', file);
    fetch('http://127.0.0.1:8000/upload_video', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Video uploaded successfully');
            const video = document.getElementById('video');
            videoUrl = 'http://127.0.0.1:8000/video/?query=' + file.name;
            console.log(videoUrl)
            video.src = videoUrl;
        } else {
            console.error('Failed to upload video');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

