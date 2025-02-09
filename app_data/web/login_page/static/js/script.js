sections_array = ["loginBx", "registration", "authentication","2FA_Verification_section"];

function Move_between_sections(sec){
    sections_array.forEach(function(item){
        if(item != sec){
            document.getElementById(item).style.display = "none";
        }else{
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



async function Send_Data_(){}



async function registration_function(){
    //const formData = new URLSearchParams();


    //formData.set("username", document.getElementById("registration_username").value);
    //formData.set("password", document.getElementById("registration_password").value);
    //formData.set("email", document.getElementById("registration_email").value);
    //username = document.getElementById("registration_username").value;
    //password = document.getElementById("registration_password").value;
    //email = document.getElementById("registration_email").value;
    //phone_number = document.getElementById("registration_phone_number").value;
    message_body = JSON.stringify([{
            name: document.getElementById("registration_username").value, 
            password: document.getElementById("registration_password").value,
            email: document.getElementById("registration_email").value,
            phone: document.getElementById("registration_phone_number").value
        }]);
    
    //"http://127.0.0.1:1234/api/add_user/",
   await fetch("http://127.0.0.1:1234/api/add_user/", {
        method: "POST",
        body: message_body,
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
    .then((twoFA_key) => {
        Move_between_sections("2FA_Verification_section");
        document.getElementById("p_key").innerHTML = "Your key is: " + twoFA_key;
    })// Close the then function

    .catch((error) => console.error("Fetch error:", error)); // In case of an error, it will be captured and logged.
    Clear_registration();
    };









function verify_otp(){

};//Close the function
    


//clear the registration form
function Clear_registration(){
    document.getElementById("registration_username").value = "";
    document.getElementById("registration_password").value = "";
    document.getElementById("registration_email").value = "";
    document.getElementById("registration_phone_number").value = "";
}

