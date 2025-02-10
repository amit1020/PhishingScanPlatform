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
        console.log(`🔹 Sending request to: ${url}`);
        console.log(`🔹 Request body:`, data);
        try {
            const response = await fetch(url, {
                method: "POST",
                body: data,
                headers: {
                    "Content-Type": "application/json; charset=UTF-8",  //Ensures JSON encoding
                },
            });
    
            if (!response.ok) {
                throw new Error(`Network error: ${response.status} - ${response.statusText}`);
            }
    
            // Ensure the response is JSON
            const responseData = await response.json().catch(() => null);
            if (!responseData) throw new Error("Invalid JSON response from server");
    
            return responseData;
    
        } catch (error) {
            console.error("Fetch error:", error.message);
            return null;  // Always return null instead of crashing
        }
    }
    


    async function registration_function() {
        let url = `${window.location.origin}/api/add_user/`;
    
        //Makes the USERNAME available globally
        USERNAME = document.getElementById("registration_username").value;


        let message_body = JSON.stringify({
            name: document.getElementById("registration_username").value,
            password: document.getElementById("registration_password").value,
            email: document.getElementById("registration_email").value,
            phone: document.getElementById("registration_phone_number").value
        });

        console.log(message_body);
    
        const response = await Send_Data_(message_body, url);
    
        if (response && response["2FA_key"]) {  
            Move_between_sections("2FA_Verification_section");
            document.getElementById("p_key").innerHTML = "Your key is: " + response["2FA_key"];
        } else {
            console.error("Failed to retrieve 2FA key.");
        }
    
        Clear_registration();  
    }
    
    
    async function verify_otp() {
        let url = `${window.location.origin}/api/Vertification/2FA`;

    
        let message_body = JSON.stringify({
            username: USERNAME,
            otp: document.getElementById("OTP_code").value
        });
    
        const response = await Send_Data_(message_body, url);
    
        if (response && response.status === "Success") {  
            console.log("✅ 2FA verification successful");
        } else {
            console.error("❌ 2FA verification failed.");
        }
    }
    


//clear the registration form
function Clear_registration(){
    document.getElementById("registration_username").value = "";
    document.getElementById("registration_password").value = "";
    document.getElementById("registration_email").value = "";
    document.getElementById("registration_phone_number").value = "";
}

