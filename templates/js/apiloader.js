document.addEventListener(
    "DOMContentLoaded", () => {
        () => {
        let apiContainer = document.getElementById("api");
        fetch("api/structure/").then(response => response.json()).then(data => {
            console.log(data);
            let basename = data["data"]["basepath"];
            data["data"]["endpoints"].forEach(element => {
                path_as_array = element.path.split("/");
                path_as_name = path_as_array.map((element) => {
                    return element[0].toUpperCase() + element.slice(1);
                }).join(" ");
                apiContainer.innerHTML += `
                <div class="request">
                    <h2>${path_as_name}</h2>
                    <div class="request-line ${element.method.toLowerCase()}">
                        <span class="http-method ${element.method.toLowerCase()}">${element.method.toUpperCase()}</span> ${basename}/${element.path} HTTP/1.1
                    </div>
                </div>
                `;
                // iter over the body (dict)
                if (element.body) {
                    apiContainer.innerHTML += `
                        <div class="request-body">
                            <h3>Body</h3>
                            <pre>${JSON.stringify(element.body, null, 2)}
                            </pre>
                        </div>
                    `;
                }
            })
        })}

    }
)

function sendRequestToApi(path, body, method) {
    fetch(path, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    }).then(response => response.json()).then(data => {
        console.log(data);
        
    })
}