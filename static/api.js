async function postData(url = '', origin = 'same-origin',  data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'PUT', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: origin, // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Basic " + btoa("hb301:be92d980-0b99-11ea-a278-0242ac110003")
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    console.log(origin);
    return response.json(); // parses JSON response into native JavaScript objects
}

window.addEventListener("load", () => {

    let xmlButton = document.getElementById("xml");
    let xmlWithCred = document.getElementById("xml-getcred");
    let xmlOmit = document.getElementById("omit");
    let corsElem = document.getElementById("no-cors");

    xmlButton.onclick = (ev) => {

        let xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function ($evt) {
            if (xhr.readyState == 4 && xhr.status == 200) {
                let res = JSON.parse(xhr.responseText);
                console.log("response: ", res);
            }
        }
        xhr.open("PUT", "https://global.xirsys.net/_turn/Finning", true);
        xhr.setRequestHeader("Authorization", "Basic " + btoa("hb301:be92d980-0b99-11ea-a278-0242ac110003"));
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify({ "format": "urls" }));
    }

    xmlWithCred.onclick = (ev) => {
        postData('https://global.xirsys.net/_turn/Finning', 'same-origin', { "format": "urls" })
            .then(data => {
                console.log(data); // JSON data parsed by `data.json()` call
            });
    }

    xmlOmit.onclick = (ev) =>{
        
        postData('https://global.xirsys.net/_turn/Finning', 'omit', { "format": "urls" })
        .then(data => {
            console.log(data); // JSON data parsed by `data.json()` call
        });

    }

    corsElem.onclick = (ev) =>{
        
        postData('https://global.xirsys.net/_turn/Finning', 'omit', { "format": "urls" })
        .then(data => {
            console.log(data); // JSON data parsed by `data.json()` call
        });

    }
    


});