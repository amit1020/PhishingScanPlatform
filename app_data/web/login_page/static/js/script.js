sections_array = ["loginBx", "registration", "authentication","2FA_Verification_section"];

//For 2FA vertification
let USERNAME = undefined;


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



    async function Send_Data_(data, url) {
        try {
            const response = await fetch(url, {
                method: "POST",
                body: data,
                headers: {
                    "Content-Type": "application/json",
                },
            });
    
            // If the response is not OK (not in 200-299 range), throw an error
            if (!response.ok) {
                throw new Error(`Network response was not ok: ${response.statusText}`);
            }
    
            // Convert response to JSON
            const twoFA_key = await response.json();
            return twoFA_key;
    
        } catch (error) {
            console.error("Fetch error:", error);
            return null; // Return null in case of failure
        }
    };//!Close the function


async function registration_function(){
    url = "http://127.0.0.1:1234/api/add_user/";

    USERNAME = document.getElementById("registration_username").value;
    message_body = JSON.stringify([{
            name: document.getElementById("registration_username").value, 
            password: document.getElementById("registration_password").value,
            email: document.getElementById("registration_email").value,
            phone: document.getElementById("registration_phone_number").value
        }]);

    
        const twoFA_key = await Send_Data_(message_body, url);

        if (twoFA_key) { // Ensure key exists before using it
            Move_between_sections("2FA_Verification_section");
            document.getElementById("p_key").innerHTML = "Your key is: " + twoFA_key;
        } else {
            console.error("Failed to retrieve 2FA key.");
        }
    
        Clear_registration(); // Assuming this function clears input fields  
    };//!Close the function



async function verify_otp(){
        url = "http://127.0.0.1:1234/api/Vertification/2FA"
        message_body = JSON.stringify([{
            username: USERNAME,
            otp: document.getElementById("OTP_code").value
        }]);

        const result = await Send_Data_(message_body, url);
    
        if (result == "Success") { // Ensure key exists before using it
            console.log("2FA verification successful");
        } else {
            console.error("Failed to retrieve 2FA key.");
        }


};//Close the function
    


//clear the registration form
function Clear_registration(){
    document.getElementById("registration_username").value = "";
    document.getElementById("registration_password").value = "";
    document.getElementById("registration_email").value = "";
    document.getElementById("registration_phone_number").value = "";
}

