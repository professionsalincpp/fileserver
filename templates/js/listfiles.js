const Utils = {
    escapeHtml: function(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

url = "/list/dir/";
this_window_url = window.location.href;
query_params = new URL(this_window_url).searchParams;
path = "";
paste = null;
if (query_params.has("path")) {
    if (query_params.get("path")[0] == "/") {
        path = query_params.get("path").slice(1);
    } else {
        path = query_params.get("path");
    }
    url += path;
    if (path[path.length - 1] != "/") {
        path += "/";
    }
}
if (query_params.has("paste")) {
    paste = query_params.get("paste");
    if (paste[0] == "/") {
        paste = paste.slice(1);
    }
    if (paste[paste.length - 1] == "/") {
        paste = paste.slice(0, -1);
    }
}
let copied_element = null;
let listdir_files = [];

files_list = document.getElementById("filesul");
document.addEventListener("DOMContentLoaded", function() {
    loadIcon("img/file-directory.svg")
    loadIcon("img/file.svg")
    loadIcon("img/file-zip.svg")
    loadIcon("img/file-media.svg")
    loadIcon("img/file-directory-fill.svg")
    loadIcon("img/file-code.svg")
    loadIcon("img/file-badge.svg")
    loadIcon("img/file-binary.svg")
    setTimeout(() => {
        
        
        let pathnav = document.getElementById("pathnav");
        let files_list = document.getElementById("filesul");
        let copy_btn = document.getElementById("copybtn1");
        let paste_btn = document.getElementById("pastebtn1");
        let delete_btn = document.getElementById("deletebtn1");
        let rename_btn = document.getElementById("renamebtn1");
        let fluid_main = document.getElementsByClassName("main")[0];
        let input = null;
        let file_link = null;
        let last_selected = -1;
        paste_btn.style.display = "none";
        rename_btn.style.display = "none";
        delete_btn.style.display = "none";
        if (paste != null) {
            paste_btn.style.display = "block";
        }
        paste_btn.addEventListener("click", function(event) {
            copyFile();
        })
        rename_btn.addEventListener("click", function(event) {
            let selected = files_list.getElementsByClassName("selected")[0];
            console.log("selected", selected);
            file_link = selected.getElementsByClassName("file-link")[0];
            let filename = file_link.getAttribute("path");
            let basename = filename.split("/").pop();
            console.log("filename", filename);
            file_link.style.display = "none";
            input = document.createElement("input");
            input.className = "rename-file-input";
            input.type = "text";
            input.value = basename;
            input.addEventListener("change", function(event) {
                let splitted = filename.split("/").slice(0, -1);
                let newname = "";
                if (splitted.length > 0) {
                    newname = splitted.join("/") + "/" + input.value;
                } else {
                    newname = input.value;
                }
                console.log("newname", newname);
                renameFile(filename, newname);
            })
            file_link.parentNode.appendChild(input, file_link);
        })
        copy_btn.addEventListener("click", function(event) {
            copied_element = files_list.getElementsByClassName("selected")[0]
            .getElementsByClassName("file-row")[0]
            .getElementsByClassName("file-link")[0]
            .getAttribute("path");
            console.log("copied", copied_element);
            paste_btn.style.display = "block";
            let pathnav_elements = files_list.getElementsByClassName("file-body");
            for (let i = 0; i < pathnav_elements.length; i++) {
                let link = pathnav_elements[i].getElementsByTagName("a")[0];
                link.href = link.href + "&paste=" + copied_element;
            }
        })

        delete_btn.addEventListener("click", function(event) {
            let selected = files_list.getElementsByClassName("selected")[0];
            let link = selected.getElementsByClassName("file-link")[0];
            let filename = link.getAttribute("path");
            let is_dir = link.classList.contains("directory");
            deleteFile(filename, is_dir);
        })
        // get parts of path
        let newpath = path;
        if (path[path.length-1] == "/") {
            console.log("removing");
            newpath = path.slice(0, -1);
        } 
        if (newpath.length > 0 && newpath[0] == "/") {
            newpath = newpath.slice(1);
        }
        console.log(newpath);
        splitted_path = newpath.split("/");
        if (path == "") {
            pathnav.innerHTML += `<li class="active">Home<li>`
            
        } else {
            pathnav.innerHTML += `<li class="active"><a path="" href="?">Home</a></li>`
        }
        if (splitted_path.length > 1) {
            pathbefore = "";
            for (let i = 0; i < splitted_path.length - 1; i++) {
                let href = "";
                let ipath = "";
                if (pathbefore == "") {
                    href = `?path=${splitted_path[i]}`;
                    ipath = splitted_path[i];
                    pathbefore = splitted_path[i];
                } else {
                    href = `?path=${pathbefore}/${splitted_path[i]}`;
                    ipath = pathbefore;
                    pathbefore += "/" + splitted_path[i];
                }
                pathnav.innerHTML += `<li><a path="${ipath}" href="${href}">${splitted_path[i]}</a></li>`;
            }
        } 
        console.log(splitted_path);
        if (splitted_path.length > 0 && path != "") {
            pathnav.innerHTML += `<li class="active">${splitted_path[splitted_path.length - 1]}</li>`;
        }
        console.log(url);
        console.log(this_window_url);
        console.log(query_params);
        console.log(files_list);
        // try as a file
        fetch(url).then(response => response.text()).then(
            function(data) {
                console.log(data);
                data = JSON.parse(data);
                console.log(data);
                last_path = ""
                splitted_path = path.split("/");
                console.log(splitted_path);
        if (splitted_path.length > 1) {
            for (let i = 0; i < splitted_path.length - 2; i++) {
                last_path += splitted_path[i] + "/";
            }
            
        }
        console.log(last_path);
        if (path == "") {

        } else if (last_path == "") {
            files_list.innerHTML += getItemHtml({"name": "..", "type": "directory"}, "/viewdir");
        } else {
            files_list.innerHTML += getItemHtml({"name": "..", "type": "directory"}, `?path=${last_path}`);
        } 
        if (data["type"] == "file") {
            console.log("PROCESS IF FILE");
            let uploadBtn = document.getElementById("uploadbtn1")
            uploadBtn.parentNode.removeChild(uploadBtn);
            delete_btn.parentNode.removeChild(delete_btn);
            processIfFile(data);
        } else if (data["type"] == "directory") {
            // if (path == "" || path == "/") {
            //     deletebtn.parentNode.removeChild(deletebtn);
            // } else {
            //     deletebtn.addEventListener("click", function() {
            //         deleteFile(path, true);
            //     })
            // }
            processIfDirectory(data);
        }
        function releaseInput() {
            if (input != null) {
                input.parentNode.removeChild(input);
                input = null;
            }
            if (file_link != null) {
                file_link.style.display = "block";
            }
        }
        function processIfFile(data) {
            let new_path = path;
            if (last_path != "") {
                new_path = last_path + "/" + path;
            } 
            files_list.innerHTML += "<div id='filecontent' style='padding: 15px'></div>"
            // `<iframe src="viewfile?path=${new_path}" style="width: 100%; height: 50vh"></iframe>`
            viewFile()
            console.log("PROCESS IF FILE done");
        }
        function processIfDirectory(data) {
            sortFiles(data["data"]);
            listdir_files = data["data"];
            copy_btn.style.display = "none";
            for (let i = 0; i < data["data"].length; i++) {
                let href = null;
                let isfile = false;
                if (data["data"][i]["type"] == "file") {
                    href = `viewdir?path=${path+data["data"][i]["name"]}`;
                    isfile = true;
                }
                files_list.innerHTML += getItemHtml(data["data"][i], href, isfile);
                
            }
            // get all files divs
            files = document.getElementsByClassName("file-body");
            console.log("files", files);
            for (let i = 0; i < files.length; i++) {
                if (files[i].innerText == "..") {
                    continue
                }
                files[i].addEventListener("click", function(event) {
                    // add select class
                    copy_btn.style.display = "block";
                    rename_btn.style.display = "block";
                    delete_btn.style.display = "block";
                    files[i].classList.add("selected");
                    if (last_selected != i) {
                        releaseInput();
                    }
                    last_selected = i;
                    // remove select class from other files
                    for (let j = 0; j < files.length; j++) {
                        if (j != i) {
                            files[j].classList.remove("selected");
                        }
                    }
                    
                })
            }
            
        }
        console.log("Fluid main",fluid_main);
        fluid_main.addEventListener("click", function(event) {
            console.log("Fluid main",event.target);
            if (event.target.classList.contains("btn") || event.target.classList.contains("rename-file-input") || event.target.parentNode.classList.contains("btn")) {
                console.log("Continue");
                return
            }
            console.log("Not continue");
            if(!event.target.classList.contains("file-body") && !event.target.parentNode.classList.contains("file-body") && !event.target.parentNode.parentNode.classList.contains("file-row")) {
                copy_btn.style.display = "none";
                rename_btn.style.display = "none";
                delete_btn.style.display = "none";
                if (input != null) {
                    try {
                        releaseInput();
                    } catch (e) {
                        console.log(e);
                    }
                }
                for (let i = 0; i < files.length; i++) {  
                    files[i].classList.remove("selected");
                }
            }
        })

    });
    const typeFile = document.getElementById('typeFile');
    const typeDir = document.getElementById('typeDir');
    const fileContentGroup = document.getElementById('fileContentGroup');

    if (typeFile && typeDir && fileContentGroup) {
        function toggleContent() {
            fileContentGroup.style.display = typeFile.checked ? 'block' : 'none';
        }
        typeFile.addEventListener('change', toggleContent);
        typeDir.addEventListener('change', toggleContent);
        toggleContent(); // установить начальное состояние
    }
}, 10)
// остальной код
});

function createItem() {
    const type = document.querySelector('input[name="createType"]:checked').value;
    const name = document.getElementById('createName').value.trim();
    const content = document.getElementById('createContent').value;

    if (!name) {
        createErrorMessage("Name cannot be empty");
        return;
    }

    // Construct full path
    let fullPath = path ? path + '/' + name : name;

    if (type === 'directory') {
        // Create directory via POST /api/create/dir
        fetch('/api/create/dir', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: fullPath })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                $('#createModal').modal('hide');
                createSuccessMessage('Directory created');
                location.reload(); // or refresh dynamically
            } else {
                createErrorMessage(data.error_message || 'Failed to create directory');
            }
        })
        .catch(err => createErrorMessage('Network error: ' + err));
    } else {
        // Create file via POST /api/create/file (empty file)
        fetch('/api/create/file', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: fullPath })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // If content provided, write it using /api/write
                if (content) {
                    const hashHex = CryptoJS.SHA256(content).toString();
                    return fetch('/api/write', {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            path: fullPath,
                            data: content,
                            hash: hashHex
                        })
                    })
                    .then(res => res.json())
                    .then(writeData => {
                        if (writeData.status === 'success') {
                            $('#createModal').modal('hide');
                            createSuccessMessage('File created');
                            location.reload();
                        } else {
                            createErrorMessage(writeData.message + '; ' + writeData.error_message);
                        }
                    });
                } else {
                    // Empty file – done
                    $('#createModal').modal('hide');
                    createSuccessMessage('File created');
                    location.reload();
                }
            } else {
                createErrorMessage(data.error_message || 'Failed to create file');
            }
        })
        .catch(err => createErrorMessage('Network error: ' + err));
    }
}

function renameFile(old_path, new_path) {
    if (old_path[0] == "/") {
        old_path = old_path.slice(1);
    }
    if (new_path[0] == "/") {
        new_path = new_path.slice(1);
    }
    fetch("/api/rename", {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            "path": {
                "old": old_path,
                "new": new_path
            }
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data["status"] == "success") {
                location.reload();
            } else {
                createErrorMessage(
                    data["error_message"]
                );
            }
        });
}

function copyFile() {
    let source = null;
    if (copied_element == null) {
        if (paste == null) {
            return
        }
        source = paste;
    } else {
        source = copied_element;
    }
    if (source == "..") {
        return;
    }
    dest_path = path;
    listdir_files_names = []
    for (let i = 0; i < listdir_files.length; i++) {
        listdir_files_names.push(listdir_files[i]["name"]);
    }
    console.log(listdir_files_names);
    let source_filename = source.split("/").pop();
    let source_path = source.split("/").slice(0, -1).join("/");
    let dest_name = source_filename;
    if (listdir_files_names.includes(source_filename)) {

        console.log("source in listdir_files");
        source_basename = source_filename.split(".")[0];
        source_ext = source_filename.split(".").slice(1).join(".");
        // check if matches name (number)
        maybe_new_name = source_filename;
        const template = /.?\((\d+)\)/
        const base_template = /(.*)\(\d+\)/
        if (source_basename.match(template)) {
            let source_num = parseInt(source_basename.match(template)[1]);
            let bases = source_basename.match(base_template);
            let base = bases[1];
            if (base[base.length - 1] == " ") {
                base = base.slice(0, base.length - 1);
            }
            console.log(`source_num: ${source_num}, base: ${base}`);
            console.log(bases);
            maybe_new_name = `${base} (${source_num + 1}).${source_ext}`;
            // extract number from basename in parens
            while (listdir_files_names.includes(maybe_new_name)) {
                maybe_new_name = `${base} (${source_num + 1}).${source_ext}`;
                source_num = source_num + 1;
            }
            
            dest_name = maybe_new_name;
        } else {
            let count = 1;
            while (listdir_files_names.includes(maybe_new_name)) {
                maybe_new_name = `${source_basename} (${count}).${source_ext}`;
                count = count + 1;
            }
            dest_name = maybe_new_name;
        }
    } else {
        console.log(`${dest_name} not in ${listdir_files_names}`);
    }
    let dest_full_path = ""
    let source_full_path = "";
    console.log("path", path);
    if (path == "") {
        dest_full_path = dest_name;
    } else {
        dest_full_path = dest_path + "/" + dest_name;
    }
    if (source_path == "") {
        source_full_path = source;
    } else {
        source_full_path = source_path + "/" + source_filename;
    }
    

    console.log(`copy ${source} to ${dest_full_path}`);
    fetch(`/api/copy`, {method: "PUT", body: JSON.stringify({"path": {"source": source_full_path, "dest": dest_full_path}})}).then(response => response.json()).then(
        function(data) {
            if (data["status"] == "success") {
                location.reload();
            } else {
                createErrorMessage(data["error_message"]);
            }
        }
    )
}


icons = {}
function loadIcon(url) {
    fetch(url).then(response => response.text()).then(
        function(data) {
            icons[url] = data;
        }
    );
}

function sortFiles(files) {
    files.sort(function(a, b) {
        if (a["type"] == "directory" && b["type"] == "directory") {
            return a["name"].localeCompare(b["name"]);
        } else if (a["type"] == "directory") {
            return -1;
        } else if (b["type"] == "directory") {
            return 1;
        } else {
            return a["name"].localeCompare(b["name"]);
        }
    });
}

let movepath = undefined

function dragStart(event, path) {
    try {
        movepath = path;
        event.dataTransfer.setData("path", path);
        // event.path = path;
        console.log(`Start drag ${event.dataTransfer.getData("path")}`);
    } catch (e) {
        console.log(e);
    }
}

function moveFile(pathsource, pathdest) {
    console.log(`Move ${pathsource} to ${pathdest}`);
    if (pathdest == pathsource) {
        return
    }
    fetch(`api/move`, {method: "PUT", body: JSON.stringify({"path": {"source": pathsource, "dest": pathdest}})}).then(response => response.json()).then(
        function(data) {
            if (data["status"] == "success") {
                // if pathsource is file go to parent directory
                
                location.reload();
            } else {
                createErrorMessage(data["error_message"]);
            }
        }
    )
}
function dragEnd(event) {
    try {
        const x = event.clientX;
        const y = event.clientY;
        console.log(`End drag ${movepath}`);
        const elementUnder = document.elementFromPoint(x, y);
        console.log(elementUnder); // выведет элемент, над которым находится перетаскиваемый элеме
        if (elementUnder.getAttribute("path") != null) {
            let pathsource = movepath;
            let pathdest = elementUnder.getAttribute("path");
            moveFile(pathsource, pathdest);
        }
        movepath = undefined;
        event.preventDefault();;
    } catch (e) {
        console.log(e);
    }
}

function getItemHtml(item, href=null, isfile=false) {
    if (href == null) {
        href = `viewdir?path=${path+item["name"]}`;
    }
    let type = item["type"];
    let name = item["name"];
    // full path
    let path1 = path;
    if (path1 != "") {
        if (path1[path1.length - 1] != "/") {
            path1 += "/";
        }

    }
    let fullpath = path1 + name;
    extension = ""
    if (name.split(".").length > 1) {
        extension = name.split(".")[name.split(".").length - 1];
    }
    icon = "";
    icons_dict = {
        "directory": "img/file-directory.svg",
        "file": "img/file.svg",
        "zip": "img/file-zip.svg",
        "media": "img/file-media.svg",
        "binary": "img/file-binary.svg",
        "code": "img/file-code.svg",
        "badge": "img/file-badge.svg",
    }
    extensions_dict = {
        "jpg": "media",
        "jpeg": "media",
        "png": "media",
        "bmp": "media",
        "xls": "media",
        "xlsx": "media",
        "java": "code",
        "py": "code",
        "cpp": "code",
        "ini": "code",
        "txt": "file",
        "trash": "directory",
        "": "directory",
    }
    icon = icons[icons_dict[extensions_dict[extension]]];
    if (isfile && extensions_dict[extension] == "directory") {
        icon = icons["img/file.svg"];
        console.log("DIRECTORY");
    }
    if (icon == null) {
        if (type == "file") {
            icon = icons["img/file.svg"];
        } else {
            icon = icons["img/file-directory.svg"];
        }
    }
    if (type == "directory") {
        is_empty = item["is_empty"];
        if (!is_empty) {
            icon = icons["img/file-directory-fill.svg"];
        } else {
            icon = icons["img/file-directory.svg"]
        }
    }
    console.log(icons);
    return `
    <div class="list-group-item file-body" draggable="true">
    <div class="file-row" style="display: flex; align-items: center">
    ${icon}
    
    
    <a href="${href}" path="${fullpath}" droppable="${!isfile}" draggable="true" ondragstart="dragStart(event, '${fullpath}')" ondragend="dragEnd(event)" oncontextmenu="return false"  class="${'file' + (isfile ? '' : ' directory')} file-link">${name}</a>
    </div>
    </div>
    `
}

function getLastPath(path) {
    if (path == "") {
        return "";
    } else {
        return path.split("/")[path.split("/").length - 1];
    }
}

const mimetypeMap = {
    '.cpp': 'text/x-c++',
    '.c': 'text/x-c',
    '.java': 'text/x-java',
    '.py': 'text/x-python',
    '.html': 'text/html',
    '.htm': 'text/html',
    '.js': 'text/x-javascript',
    '.css': 'text/css',
    '.json': 'text/x-json',
    '.xml': 'text/xml',
    '.ini': 'text/x-ini',
    '.md': 'text/x-markdown'
};

function printArrayBuffer(buffer) {
    try {
        const uint8Array = new Uint8Array(buffer);
        
        // заполнить массив байтами
        // for (let i = 0; i < uint8Array.length; i++) {
            //     uint8Array[i] = buffer[i];
            // }
            
            // вывести номера байтов в формате
            let output = "b'";
            for (let i = 0; i < Math.min(30, uint8Array.length); i++) {
                const byte = uint8Array[i];
                if (byte < 16) {
                    output += "\\x0" + byte.toString(16);
            } else {
                // если байт больше 16, то выводим его как есть (символ)
            if (byte >= 32 && byte <= 126) {
                output += String.fromCharCode(byte);
            } else {
                output += "\\x" + byte.toString(16);
            }
            
            
            // output += "\\x" + byte.toString(16);
        }
    }
    output += "'";
    console.log(output.slice(0, 30));
} catch (e) {
    console.error("Error decoding buffer:", e);
}
}

function decodeFromBase64(input) {
    input = input.replace(/\s/g, '');
    return atob(input);
}

function encodeToBase64(input) {
    // convert to Uint8Array if needed
    if (!(input instanceof Uint8Array)) {
        if (input instanceof ArrayBuffer) {
            input = new Uint8Array(input);
        }
    }
    const Base64 = window.Base64;
    console.log(Base64);
    return Base64.fromUint8Array(input);
}

class Encoder {
    static encodingsMap = {
        "text/plain": "utf-8",
        "*/*": "utf-8",
        
    // Images
    "image/bmp": "base64",
    "image/png": "base64",
    "image/jpeg": "base64",
    "image/gif": "base64",
    "image/pdf": "base64",
    "image/tiff": "base64",
    "image/x-icon": "base64",
    "image/x-ms-bmp": "base64",
    "image/x-xbitmap": "base64",
    "image/x-xbm": "base64",
    "image/x-xpixmap": "base64",
    "image/x-xwindowdump": "base64",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "base64",
    "application/vnd.ms-excel": "base64",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "base64",
};

static encode(data, mimetype) {
    const encoding = Encoder.getEncoding(mimetype);
    if (encoding === "base64") {
        console.log("To base64");
        try {
            // decode from utf-8, because used .text() method
            return encodeToBase64(data);
        } catch (e) {
            console.log("Error", e);
            return `Error encoding base64 data: ${e}`;
        }
    }
    return new TextDecoder(encoding).decode(data);
}

static decode(data, mimetype) {
    const encoding = Encoder.getEncoding(mimetype);
    if (encoding === "base64") {
        try {
        return atob(data);
    } catch (e) {
        return `Error decoding base64 data: ${e}`;
    }
}
return new TextDecoder(encoding).decode(data);
}

static getEncoding(mimetype) {
    return Encoder.encodingsMap[mimetype] || "utf-8";
}
}

setTimeout(() => {
    
    console.log(`Hello World "${Encoder.encode(new TextEncoder().encode("Hello World"), "image/png")}"`);
}, 1000);
// console.log(btoa("AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/wABAgMEBQYHCAkKCwwNDg8QERITFBUWFxgZGhscHR4fICEiIyQlJicoKSorLC0uLzAxMjM0NTY3ODk6Ozw9Pj9AQUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVpbXF1eX2BhYmNkZWZnaGlqa2xtbm9wcXJzdHV2d3h5ent8fX5/gIGCg4SFhoeIiYqLjI2Oj5CRkpOUlZaXmJmam5ydnp+goaKjpKWmp6ipqqusra6vsLGys7S1tre4ubq7vL2+v8DBwsPExcbHyMnKy8zNzs/Q0dLT1NXW19jZ2tvc3d7f4OHi4+Tl5ufo6err7O3u7/Dx8vP09fb3+Pn6+/z9/v8AAQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhIiMkJSYnKCkqKywtLi8wMTIzNDU2Nzg5Ojs8PT4/QEFCQ0RFRkdISUpLTE1OT1BRUlNUVVZXWFlaW1xdXl9gYWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXp7fH1+f4CBgoOEhYaHiImKi4yNjo+QkZKTlJWWl5iZmpucnZ6foKGio6SlpqeoqaqrrK2ur7CxsrO0tba3uLm6u7y9vr/AwcLDxMXGx8jJysvMzc7P0NHS09TV1tfY2drb3N3e3+Dh4uPk5ebn6Onq6+zt7u/w8fLz9PX29/j5+vv8/f7/AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8gISIjJCUmJygpKissLS4vMDEyMzQ1Njc4OTo7PD0+P0BBQkNERUZHSElKS0xNTk9QUVJTVFVWV1hZWltcXV5fYGFiY2RlZmdoaWprbG1ub3BxcnN0dXZ3eHl6e3x9fn+AgYKDhIWGh4iJiouMjY6PkJGSk5SVlpeYmZqbnJ2en6ChoqOkpaanqKmqq6ytrq+wsbKztLW2t7i5uru8vb6/wMHCw8TFxsfIycrLzM3Oz9DR0tPU1dbX2Nna29zd3t/g4eLj5OXm5+jp6uvs7e7v8PHy8/T19vf4+fr7/P3+/w=="))

function guessMimetype(filename, maybe_mimetype) {
    const extension = filename.split('.').pop();
    return mimetypeMap[extension] || maybe_mimetype;
}

function createContextMenu() {
    const contextMenu = document.createElement("div");
    contextMenu.id = "context-menu";
    contextMenu.className = "context-menu";
    contextMenu.style.display = "none";
    contextMenu.innerHTML = `
        <ul>
            <li>Пункт 1</li>
            <li>Пункт 2</li>
        </ul>
    `;
    document.body.appendChild(contextMenu);
}

function createSuccessMessage(message) {
    let messageContainer = document.getElementById("message-container")
    let message1 = document.createElement("div");
    message1.className = "alert alert-success";
    message1.role = "alert";
    let closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.className = "close";
    closeButton.dataset.dismiss = "alert";
    closeButton.innerHTML = "×";
    message1.appendChild(closeButton);
    message1.innerHTML += `
        <strong>Success!</strong> <span id="message-text" style="margin-right: 10px;">${message}</span>
    `;
    messageContainer.appendChild(message1);

    setTimeout(() => {
        message1.style.transition = 'transform 0.5s ease-out';
        message1.style.transform = 'translateX(100%)';
        setTimeout(() => {
            message1.remove();
        }, 500);
    }, 5000);
}

function createErrorMessage(message) {
    let messageContainer = document.getElementById("message-container")
    let message1 = document.createElement("div");
    message1.className = "alert alert-danger";
    message1.role = "alert";
    let closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.className = "close";
    closeButton.dataset.dismiss = "alert";
    closeButton.innerHTML = "×";
    message1.appendChild(closeButton);
    message1.innerHTML += `
        <strong>Error!</strong> <span id="message-text" style="margin-right: 10px;">${message}</span>
    `;
    messageContainer.appendChild(message1);
    setTimeout(() => {
        message1.style.transition = 'transform 0.5s ease-out';
        message1.style.transform = 'translateX(100%)';
        setTimeout(() => {
            message1.remove();
        }, 500);
    }, 5000);
}
function uploadFile() {
    let uploadinput = document.getElementById("uploadfileinput");
    if (!uploadinput.files.length) {
        alert("No file selected");
        return;
    }

    const file = uploadinput.files[0];
    const uploadId = UploadManager.addUpload(file.name); // добавляем в панель

    uploadId.updateProgress(5, 'Reading file...');

    file.arrayBuffer().then(buffer => {
        uploadId.updateProgress(30, 'Encoding to base64...');
        const data = Encoder.encode(buffer, file.type); // ваша функция Encoder.encode
        uploadId.updateProgress(60, 'Computing hash...');
        const hashHex = CryptoJS.SHA256(data).toString();

        let pathBasename = path ? path + '/' + file.name : file.name;
        uploadId.updateProgress(80, 'Sending to server...');

        return fetch('/api/write', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                path: pathBasename,
                data: data,
                hash: hashHex
            })
        });
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            uploadId.setStatus('Completed', false, true);
            createSuccessMessage(data.message || 'Upload successful');
            $('#uploadModal').modal('hide');
            // Перезагружаем страницу, чтобы увидеть новый файл
            window.location.reload();
        } else {
            uploadId.setStatus(data.message || 'Upload failed', true);
            createErrorMessage(data.message + '; ' + data.error_message);
        }
    })
    .catch(err => {
        uploadId.setStatus('Error: ' + err.message, true);
        createErrorMessage('Upload error: ' + err);
    });

    // Очищаем поле ввода, чтобы можно было загрузить тот же файл повторно
    uploadinput.value = '';
}

// ---------- Upload Manager (управление панелью загрузок) ----------
const UploadManager = (function() {
    const uploadsList = document.getElementById('uploads-list');
    const container = document.getElementById('uploads-queue');
    const clearBtn = document.getElementById('clear-completed');

    const items = new Map(); // id -> { element, filename, status }

    function generateId() {
        return 'upload_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    function createItemElement(filename) {
        const div = document.createElement('div');
        div.className = 'upload-item';
        div.innerHTML = `
            <div class="filename">${Utils.escapeHtml(filename)}</div>
            <div class="progress"><div class="progress-bar" style="width:0%"></div></div>
            <div class="status">Starting...</div>
        `;
        return div;
    }

    function updateProgress(id, percent, statusText) {
        const item = items.get(id);
        if (!item) return;
        const bar = item.element.querySelector('.progress-bar');
        const status = item.element.querySelector('.status');
        bar.style.width = percent + '%';
        status.textContent = statusText || (percent + '%');
    }

    function setStatus(id, statusText, isError = false, isCompleted = false) {
        const item = items.get(id);
        if (!item) return;
        const status = item.element.querySelector('.status');
        status.textContent = statusText;
        if (isError) {
            item.element.classList.add('error');
        } else if (isCompleted) {
            item.element.classList.add('completed');
        }
    }

    function addUpload(filename) {
        const id = generateId();
        const element = createItemElement(filename);
        uploadsList.prepend(element);
        items.set(id, { element, filename, status: 'uploading' });
        if (container) container.style.display = 'block';
        return {
            id,
            updateProgress: (percent, statusText) => updateProgress(id, percent, statusText),
            setStatus: (statusText, isError, isCompleted) => setStatus(id, statusText, isError, isCompleted)
        };
    }

    function removeCompleted() {
        items.forEach((item, id) => {
            if (item.element.classList.contains('completed') || item.element.classList.contains('error')) {
                item.element.remove();
                items.delete(id);
            }
        });
        if (items.size === 0 && container) {
            container.style.display = 'none';
        }
    }

    // Инициализация
    if (container) container.style.display = 'none';
    if (clearBtn) {
        clearBtn.addEventListener('click', removeCompleted);
    }

    return { addUpload };
})();