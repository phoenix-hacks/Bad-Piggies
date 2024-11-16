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

    startPlayingVideo(file)
}