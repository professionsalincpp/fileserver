url = "/list/dir/";
this_window_url = window.location.href;
query_params = new URL(this_window_url).searchParams;
path = "";
if (query_params.has("path")) {
    url +=query_params.get("path");
    path = query_params.get("path");
    if (path[path.length - 1] != "/") {
        path += "/";
    }
}

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
        
        
    
        files_list = document.getElementById("filesul");
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
        if (last_path == "") {
            files_list.innerHTML += getItemHtml({"name": "..", "type": "directory"}, "/viewdir");
        } else {
            files_list.innerHTML += getItemHtml({"name": "..", "type": "directory"}, `?path=${last_path}`);
        } 
        if (data["type"] == "file") {
            console.log("PROCESS IF FILE");
            let uploadBtn = document.getElementById("uploadbtn1")
            uploadBtn.parentNode.removeChild(uploadBtn);
            processIfFile(data);
        } else if (data["type"] == "directory") {
            processIfDirectory(data);
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
            for (let i = 0; i < data["data"].length; i++) {
                let href = null;
                let isfile = false;
                if (data["data"][i]["type"] == "file") {
                    href = `viewdir?path=${path+data["data"][i]["name"]}`;
                    isfile = true;
                }
                files_list.innerHTML += getItemHtml(data["data"][i], href, isfile);
            }
            
        }
    });
}, 10)
// остальной код
});

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

function getItemHtml(item, href=null, isfile=false) {
    if (href == null) {
        href = `viewdir?path=${path+item["name"]}`;
    }
    let type = item["type"];
    let name = item["name"];
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
    <div class="list-group-item">
    <div class="row-content" style="display: flex; align-items: center">
    ${icon}
    
    
    <a href="${href}"  class="file">${name}</a>
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
    let uploadModal = document.getElementById("uploadModal");
    if (uploadinput.files.length > 0) {
        let file = uploadinput.files[0];
        console.log("file", file);
        file.arrayBuffer().then(
            (buffer) => {
                // const data = encoder.encode(buffer);
            console.log("buffer", buffer);
            const data = Encoder.encode(buffer, file.type);
            // buffer = new TextDecoder("utf-8").decode(buffer);
            console.log("typeof data", typeof data);
            console.log("data", data);
            const hashHex = CryptoJS.SHA256(data).toString();
            let pathBasename = path + "/" + file.name;
            if (path == "") {
                pathBasename = file.name;
            }
            printArrayBuffer(buffer);
            console.log("first 30 bytes text", buffer.slice(0, 30));
            console.log("first 30 bytes", data.slice(0, 30));
            let body = JSON.stringify({
                path: pathBasename,
                data: data,
                hash: hashHex,
            })
            console.log("path", pathBasename);
            console.log(buffer);
            console.log(hashHex);
            fetch("api/write", {
                method: "PUT",
                body: body,
            }).then(response => response.json()).then(
                function(data) {
                    console.log(data);
                    $("#uploadModal").modal("hide");
                    viewFile();
                    if (data["status"] == "success") {
                    // создать успех
                        createSuccessMessage(data["message"]);
                    } else {
                    // создать ошибку
                        createErrorMessage(data["message"] + "; " + data["error_message"]);
                    }
                })
            }
        )
        
        
    } else {
        alert("No file selected");
    }
}