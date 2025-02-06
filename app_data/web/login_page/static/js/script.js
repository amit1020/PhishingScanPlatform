sections_array = ["loginBx", "registration", "authentication_login","authentication_register"];

function Move_between_sections(sec) {
    sections_array.forEach(function (item) {
        if (item != sec) {
            document.getElementById(item).style.display = "none";
        } else {
            document.getElementById(item).style.display = "block";
        }

    });

};//! Close the function 




//let data = [];
//data.push(document.getElementById("registration_username").value);
//data.push(document.getElementById("registration_password").value);
//data.push(document.getElementById("registration_email").value);
//console.log(data);

//formData.set("username", document.getElementById("registration_username").value);
//formData.set("password", document.getElementById("registration_password").value);
//formData.set("email", document.getElementById("registration_email").value);
//console.log(formData);



//https://www.freecodecamp.org/news/how-to-send-http-requests-using-javascript/



async function Send_data(params) {
    /*
     JSON.stringify({
            name: username,
            password: password,
            email: email,
            phone: phone_number
        })
     
     */
    await fetch("http://127.0.0.1:1234/api/add_user/", {
        method: "POST",
        body: params,   
        headers: {
            "Content-Type": "application/json",
            //"Authorization": "your-token-here",
        },

    }).then(response => {
        // If the response is not 2xx, throw an error
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        // If the response is 200 OK, return the response in JSON format.
        return response.json();

    })//! Close the fetch function
        .then((data) => console.log(data)) // You can continue to do something to the response.
        .catch((error) => console.error("Fetch error:", error)); // In case of an error, it will be captured and logged.

};




function registration_function() {
    //const formData = new URLSearchParams();
    params = JSON.stringify({
        name: document.getElementById("registration_username").value,
        password: document.getElementById("registration_password").value,
        email: document.getElementById("registration_email").value,
        phone: document.getElementById("registration_phone_number").value
    });

    response = Send_data(params);
    
    let img = document.createElement('img');
    img.src = response;


    document.getElementById('QR_code').appendChild(img);
    


    Move_between_sections("2FA_section");


};




function submitcode() {
    console.log("submit code");
};

