
function selectIcon(selectedEl) {
    // Récupère toutes les icônes
    const icons = document.querySelectorAll('.file-icon');
    icons.forEach(icon => {
        // Retire la classe active de toutes les icônes
        if (icon !== selectedEl) {
            icon.classList.remove('active');
        }
    });
    // Ajoute la classe active sur l'icône cliquée
    selectedEl.classList.toggle('active');
}


function openFile(fileId, fileType, fileName, csrf) {
    if (fileType === "img") {
        openImageViewer(`/desktop/file/?file_id=${encodeURIComponent(fileId)}`);
    } else if (fileType === "txt") {
        openTextEditor(`/desktop/file/?file_id=${encodeURIComponent(fileId)}`, fileId, fileName, csrf);
    }

}


let currentPath = "";  // Chemin actuel dans media/files/<user_id>/

function openExplorer(csrf) {
    document.getElementById("explorer-modal").style.display = "block";
    loadFiles("",csrf); // Charger la racine
}

function closeExplorer() {
    document.getElementById("explorer-modal").style.display = "none";
}

function uploadFile(path) {
    document.getElementById("upload-modal").style.display = "block";
    document.getElementById("path").value = path;
}

function closeUpload() {
    document.getElementById("upload-modal").style.display = "none";
}

function mkdir(path) {
    document.getElementById("mkdirModal").style.display = "block";
    document.getElementById("pathMkdir").value = path;
}

function closeMkdir() {
    document.getElementById("mkdirModal").style.display = "none";
}

function loadFiles(path, csrf="") {
    currentPath = path;
    let fileList = document.getElementById("file-list");
    let uploadButton = document.getElementById("uploadButton");
    let mkdirButton = document.getElementById("mkdir");
    uploadButton.setAttribute("onclick", `uploadFile("${path}")`);
    mkdirButton.setAttribute("onclick", `mkdir("${path}")`);
    fileList.innerHTML = "<p>Chargement...</p>";

    fetch(`/desktop/explorer/?path=${encodeURIComponent(path)}`)
        .then(response => response.json())
        .then(data => {
            fileList.innerHTML = "";  // Nettoie la liste
            if (data.error) {
                fileList.innerHTML = `<p style="color: red;">${data.error}</p>`;
                return;
            }

            // Ajouter les dossiers en premier
            data.folders.forEach(folder => {
                let div = document.createElement("div");
                div.className = "file-item";
                div.innerHTML = "📁 " + folder.name;
                div.onclick = () => loadFiles(folder.path, csrf); // Naviguer dans le dossier
                fileList.appendChild(div);
            });

            // Ajouter les fichiers
            data.files.forEach(file => {
                let div = document.createElement("div");
                div.className = "file-item";
                div.innerHTML = "📄 " + file.name;
                div.onclick = () => openFile(file.id, file.type, file.name,csrf)
                fileList.appendChild(div);
            });

            if (data.folders.length === 0 && data.files.length === 0) {
                fileList.innerHTML = "<p>Aucun fichier ni dossier.</p>";
            }
        })
        .catch(error => {
            console.error("Erreur:", error);
            fileList.innerHTML = "<p style='color: red;'>Erreur de chargement.</p>";
        });
}

function goBack() {
    if (currentPath === "") return; // On est déjà à la racine

    let parts = currentPath.split("/").filter(p => p);
    parts.pop(); // Retirer le dernier dossier
    let newPath = parts.join("/");
    loadFiles(newPath); // Charger le nouveau chemin
}


function openImageViewer(imageUrl, fileName) {
    let viewer = document.getElementById("image-viewer");
    let viewerImg = document.getElementById("viewer-img");
    

    viewer.style.display = "block";  // Afficher la visionneuse
    fetch(imageUrl)
        .then(response => response.json())
        .then(data => {
            viewerImg.src = `data:image/png;base64,${data.file_data}`;
        })

}

function closeImageViewer() {
    document.getElementById("image-viewer").style.display = "none";
}



function openTextEditor(textUrl, fileId, fileName, csrf) {
    let textEditor = document.getElementById("text-editor");
    let editText = document.getElementById("edit-text");
    let buttonSave = document.getElementById("save-button");
    let buttonSavePopup  = document.getElementById("save-button-popup");


    buttonSave.setAttribute("onclick",`saveText(${fileId}, "${csrf}")`);
    buttonSavePopup.setAttribute("onclick",`saveText(${fileId}, "${csrf}")`);

    document.getElementById("file-name").innerText = fileName

    textEditor.style.display = "block";  // Afficher la visionneuse
    fetch(textUrl)
        .then(response => response.json())
        .then(data => {
            editText.innerText = data.file_data;
        })

}

function closeTextEditor() {
    document.getElementById("text-editor").style.display = "none";
}

function saveText(fileId, csrf) {
    let editText = document.getElementById("edit-text").value;

    fetch('/files/update/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrf // Assurez-vous que le token CSRF est inclus
        },
        body: new URLSearchParams({
            file_id: fileId,
            data: editText
        })
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur lors de l\'enregistrement du fichier.');
    });
    closeTextEditor();
    closePopup();
}

function closePopup() {
    document.getElementById("popup").style.display = "none";

}

function openPopup() {
    document.getElementById("popup").style.display = "block";
}


const div = document.getElementById("text-editor");
let offsetX, offsetY, isDragging = false;

div.addEventListener("mousedown", (e) => {
  isDragging = true;
  offsetX = e.clientX - div.offsetLeft;
  offsetY = e.clientY - div.offsetTop;
  div.style.cursor = "grabbing";
});

document.addEventListener("mousemove", (e) => {
  if (isDragging) {
    div.style.left = (e.clientX - offsetX) + "px";
    div.style.top = (e.clientY - offsetY) + "px";
  }
});

document.addEventListener("mouseup", () => {
  isDragging = false;
  div.style.cursor = "move";
});