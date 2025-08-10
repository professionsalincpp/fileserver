
function viewFile(from_view_file=false) {
console.log("VIEW FILE");
let fileContentPre = document.getElementById("filecontent");
let query_params = new URL(window.location.href).searchParams;
console.log(fileContentPre);
hljs.initHighlightingOnLoad();
hljs.initLineNumbersOnLoad();
if (query_params.has("path")) {
    path = decodeURIComponent(query_params.get("path"));
    fetch("/api/read", 
    {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({"path": path})}).then(response => response.text()).then(
        function(data) {
            data = JSON.parse(data);
            // console.log(data);
            console.log(data);
            setFileContent(data);
        }
    )
}

function base64ToArrayBuffer(str) {
  const binaryString = window.atob(str);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return bytes.buffer;
}


mimetypeLang = {
    "text/x-python": "python",
    "text/x-c": "c",
    "text/x-c++": "cpp",
    "text/x-java": "java",
    "text/x-javascript": "javascript",
    "text/x-ini": "ini",
    "text/x-markdown": "markdown",
    "text/x-shellscript": "bash",
    "text/xml": "xml",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "excel",
    "application/vnd.ms-excel": "excel",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "word",
    "image/png": "png",
    "image/jpeg": "jpeg",
    "image/gif": "gif",
    "image/bmp": "bmp",
    "image/pdf": "pdf",
    "text/x-json": "json",
    "text/plain": "plaintext",
    "text/x-html": "html"
}
function mimetypebylang(lang) {
    const mimetype = Object.keys(mimetypeLang).find(key => mimetypeLang[key] === lang);
    return mimetype;
}
function guessLanguage(mimetype) {
    if (mimetype in mimetypeLang) {
        return mimetypeLang[mimetype];
    }
    return "plaintext";
}

function setFileContent(content) {
    const data = content["data"]["data"];
    const hash = content["data"]["hash"];
    const mimetype = content["data"]["mimetype"];
    const lang = guessLanguage(mimetype);

    let pre = document.createElement("pre");
    let heading = createHeading(lang, hash);
    
    pre.style.whiteSpace = "pre-wrap";
    pre.style.backgroundColor = "#ffffff";
    pre.style.padding = "1px";
    pre.style.borderRadius = "3px";
    pre.style.borderColor = "#d1d9e0";
    pre.style.borderTopLeftRadius = "0px",
    pre.style.borderTopRightRadius = "0px",
    pre.style.height = "100%";
    if (!from_view_file) {
        pre.style.maxHeight = "calc(70vh - 100px)";
    } else {
        pre.style.maxHeight = "calc(100vh - 100px)";
    }
    
    fileContentPre.appendChild(heading);
    fileContentPre.appendChild(pre); 
    let filename = "";
    if (path.includes("/")) {
    
        filename = path.split("/")[path.split("/").length - 1]; 
    } else {
        filename = path;
    }

    if (lang == "excel") {
        setExcelFileContent(pre, content["data"]["data"], mimetype, filename);
    } else if (lang == "word") {
        setWordFileContent(pre, content["data"]["data"], mimetype, filename);
    
    } else if (lang == "jpeg"
        || lang == "png"
        || lang == "gif"
        || lang == "bmp"
        || lang == "pdf"
    ) {
        setImageFileContent(pre, content["data"]["data"], mimetype, filename);
    } else if (lang == "markdown") {
        displayMarkdown(pre, content["data"]["data"], mimetype, filename);
    } else  {
        setCodeFileContent(pre, data, guessLanguage(mimetype), mimetype, filename);
    }
}

function displayMarkdown(pre, text, mimetype, filename) {
    let markdown = markdownit().render(text);
    pre.innerHTML = markdown;
    document.getElementById("download-button").onclick = function() {
        downloadFile(text, "plaintext", "text/plain", filename);
    };
}   


function setExcelFileContent(pre, content, mimetype, filename) {
    if (content) {
        let table_div = document.createElement("div");
        pre.appendChild(table_div);
        let workbook = XLSX.read(base64ToArrayBuffer(content), {type: 'base64'});
        let worksheet = workbook.Sheets[workbook.SheetNames[0]];
        let json_data = XLSX.utils.sheet_to_json(worksheet, {
            header: 1,
        });
        console.log(json_data);
        console.log("worksheet merges");
        console.log(worksheet["!merges"]);
        json_data = processMergedCells(json_data , worksheet["!merges"]);
        console.log(json_data);
        table_div.appendChild(displayJsonXlsx(json_data, worksheet));

        document.getElementById("download-button").onclick = function() {
            downloadFile(base64ToArrayBuffer(content), "base64", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  filename);
        };
    } else {
        fileContentPre.innerText = "No content";
    }
}

function setWordFileContent(pre, content, mimetype, filename) {
    if (content) {
        const doc = mammoth.convertToHtml({ arrayBuffer: base64ToArrayBuffer(content) }).then(function(result) {
            
            pre.innerHTML = result.value;
        });
        document.getElementById("download-button").onclick = function() {
            downloadFile(base64ToArrayBuffer(content), "base64", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  filename);}
    } else {
        pre.innerText = "No content";
    }
}

function setImageFileContent(pre, content, mimetype, filename) {
    if (content) {
        let image_container = document.createElement("div");
        let image = document.createElement("img");

        // center image
        image_container.style.display = "flex";
        image_container.style.justifyContent = "center";
        image.style.display = "block";
        image.src = "data:" + "image/bmp" + ";base64," + content;
        // image.style.width = "80%";
        image.style.height = "calc(60vh - 80px)";
        image_container.appendChild(image);

        binaryContent = base64ToArrayBuffer(content);
        document.getElementById("download-button").onclick = function() {
            downloadFile(binaryContent, mimetype=mimetype, encoding="base64", filename);
        }
        pre.appendChild(image_container);
    } else {
        pre.innerText = "No content";
    }
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function downloadFile(hash, mimetype, encoding, filename) {
    // create blob
    const blob = new Blob([hash], { type: `${mimetype};charset=${encoding}` });
    // create url
    const url = URL.createObjectURL(blob);
    // create link
    const link = document.createElement("a");
    link.href = url;
    link.download = filename || "file.txt";
    // trigger click
    link.click();
}

function createHeading(name, hash) {
    heading = document.createElement("div");
    name_el = document.createElement("p");
    hash_el = document.createElement("p");
    download_el = document.createElement("button");
    // download_el.onclick = function() {
    //     downloadFile(hash);
    // };
    download_el.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18">
    <path d="M4.75 17.25a.75.75 0 0 1 .75.75v2.25c0 .138.112.25.25.25h12.5a.25.25 0 0 0 .25-.25V18a.75.75 0 0 1 1.5 0v2.25A1.75 1.75 0 0 1 18.25 22H5.75A1.75 1.75 0 0 1 4 20.25V18a.75.75 0 0 1 .75-.75Z"></path>
    <path d="M5.22 9.97a.749.749 0 0 1 1.06 0l4.97 4.969V2.75a.75.75 0 0 1 1.5 0v12.189l4.97-4.969a.749.749 0 1 1 1.06 1.06l-6.25 6.25a.749.749 0 0 1-1.06 0l-6.25-6.25a.749.749 0 0 1 0-1.06Z"></path>
    </svg>`;
    download_el.className = "btn btn-primary md-button";
    // set id to download button
    download_el.id = "download-button";
    download_el.style.margin = "0px";
    download_el.style.padding = "0px";
    download_el.style.width = "20px";
    download_el.style.height = "20px";
    name_el.innerText = name;
    hash_el.innerText = hash;
    hash_el.className = "file-hash";
    name_el.style.margin = "0px";
    hash_el.style.margin = "0px";
    name_el.style.padding = "0px";
    hash_el.style.padding = "0px";
    hash_el.style.textDecoration = "none";
    hash_el.style.color = "black";
    heading.style.borderRadius = "3px";
    heading.style.borderBottomLeftRadius = "0px";
    heading.style.borderBottomRightRadius = "0px";
    heading.style.border = "1px solid #d1d9e0";
    heading.style.textAlign = "left";
    heading.style.width = "100%";
    heading.style.boxSizing = "border-box";
    heading.style.margin = "0px";
    heading.style.backgroundColor = "#f6f8fa";
    heading.style.borderBottom = "none";
    heading.style.padding = "10px";
    // flex 
    heading.style.display = "flex";
    heading.style.justifyContent = "space-between";
    heading.style.alignItems = "center";
    name_el.style.fontSize = "14px";
    hash_el.style.fontSize = "14px";
    name_el.style.fontFamily = "'Github Sans', sans-serif";
    hash_el.style.fontFamily = "'Github Sans', sans-serif";
    heading.appendChild(name_el);
    // heading.appendChild(hash_el);
    heading.appendChild(download_el);
    return heading;
}
function setCodeFileContent(pre, content, language, mime, filename) {
    if (content) {
        let code = document.createElement("code");
        
        // console.log(pre)
        
        lines = escapeHtml(content).split("\n");
        for (let i = 0; i < lines.length; i++) {
            // hljs.lineNumbersBlock(lines[i]);
            let line = lines[i];
            code.innerHTML += line + "<br>";
        }
        // code.className += "language-" + language;
        // code.innerText = content
        // const highlightedCode = hljs.highlight(code.innerText, {language: language}).value;

        pre.appendChild(code);
        hljs.highlightAll();
        // get mime type by language
        
        // const mime = mimetypebylang(language);
        // console.log(mime);
        document.getElementById("download-button").onclick = function() {
            downloadFile(content, mimetype=mime, "utf-8", filename);
        };
    } else {
        fileContentPre.innerText = "No content";
    }
}
}