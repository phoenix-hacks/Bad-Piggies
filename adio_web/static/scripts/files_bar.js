function allowDrop(e) {
    e.preventDefault()

}
function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id)

}

async function updateVideoSource(uri) {
    await fetch("/update_source", 
        {
            method: "POST",
            body: JSON.stringify({
                source: uri
            }),
            headers: {'Content-Type': 'application/json'}
        }
    )

    const DBOpenRequest = window.indexedDB.open('videoFiles', 1)
    var db = null
    DBOpenRequest.onsuccess = (event)=> {
        db = DBOpenRequest.result
        console.log("Successfuly opened db")
    }   

    DBOpenRequest.onupgradeneeded = (event) => {
        db = event.target.result

        db.onerror = (event) => {
            console.error("Failed to load db")
        }

        const objectStore = db.createObjectStore('videoFiles', { keyPath: 'videoTitle'})
        objectStore.createIndex('file')
    }

    htmx.trigger("#video-editor", "get_video", {})
}

function uploadVideoToServer(file) {

    const uri = '/videos'
    let formData = new FormData()

    formData.append('file', file)

    fetch(uri, {
        method: 'POST',
        body: formData
    })
    .then( () => console.log('Uploaded file') )
    .catch( (r) => console.debug(r) )
}

function startPlayingVideo(file) {

    const reader = new FileReader()
    reader.onload = (event) => {
        const videoUrl = event.target.result
        
        const player = document.getElementById("video-player")
        player.src = videoUrl
    }
    reader.readAsDataURL(file)
}

function drop(ev) {
    ev.preventDefault()
    
    const files = ([...ev.dataTransfer.files])
    files.forEach( (file, i) => {
        console.log(file.name)
    })

}

async function open_file_picker(ev) {
    console.log("Opening file explorer")
    const [fileHandle] = await window.showOpenFilePicker()
    const file = await fileHandle.getFile()
    console.log(file.name)

    await uploadVideoAndPrompt(ev, file)
}

async function uploadVideoAndPrompt(e, file) {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('video', file);
    formData.append('prompt', document.getElementById('prompt').value);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            //document.getElementById('progress').style.display = 'none';
            const videoPreview = document.getElementById('video-player');
            videoPreview.src = data.processed_video;
            videoPreview.style.display = 'block';
            console.log('Video path:', data.processed_video);
        } else {
            alert('Error: ' + data.error);
            //document.getElementById('progress').style.display = 'none';
        }
    } catch (error) {
        alert('Error uploading video: ' + error);
        //document.getElementById('progress').style.display = 'none';
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const createButton = document.querySelector('#prompt-buttons-div button:first-child');
    createButton.addEventListener('click', handleProcessing);
});

async function handleProcessing() {
    const promptText = document.querySelector('#prompt').value;
    const videoPlayer = document.querySelector('#video-player');
    
    if (!videoPlayer || !videoPlayer.src) {
        alert('Please select a video first');
        return;
    }
    
    if (!promptText) {
        alert('Please enter AI instructions');
        return;
    }

    // Show loading state
    const createButton = document.querySelector('#prompt-buttons-div button:first-child');
    createButton.textContent = 'Processing...';
    createButton.disabled = true;

    try {
        // Convert the video source to a file
        const videoPreview = document.getElementById('video-player');
        const response = await fetch(videoPreview.src);
        const videoBlob = await response.blob();
        const videoFile = new File([videoBlob], 'video.mp4', { type: 'video/mp4' });

        const formData = new FormData();
        formData.append('video', videoFile);
        formData.append('prompt', promptText);

        const processResponse = await fetch('/process?t=' + new Date().getTime(), {
            method: 'POST',
            body: formData
        });

        const result = await processResponse.json();

        if (processResponse.ok) {
            // Update video player with processed video
            const newSource = document.createElement('source');
            // newSource.src = result.processed_video;
            // newSource.type = 'video/mp4'
            // videoPlayer.appendChild(newSource)
            // videoPlayer.load()
            videoPlayer.src = "static/uploads/video.mp4";
            videoPlayer.src = result.processed_video + '?t=' + new Date().getTime();
            console.log('Processing complete:', result.processed_video);
        } else {
            throw new Error(result.error || 'Failed to process video');
        }
    } catch (error) {
        console.error('Processing error:', error);
        alert('Error processing video: ' + error.message);
    } finally {
        // Reset button state
        createButton.textContent = 'Create';
        createButton.disabled = false;
    }
}

// Optional: Add a helper function to check if a video is loaded
function isVideoLoaded() {
    const videoPlayer = document.querySelector('#video-player');
    return videoPlayer && videoPlayer.src && videoPlayer.src !== window.location.href;
}