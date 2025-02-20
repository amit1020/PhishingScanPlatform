

    //https://www.freecodecamp.org/news/how-to-send-http-requests-using-javascript/
    async function Send_Data_(data, url) {
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
    


    async function GetURL(saved_url){

        let endpoint = `${window.location.origin}/api//`; //Api endpoint
        
        let message_body = JSON.stringify({
            url: saved_url
        });
        console.log(message_body);

    
    
    }
    
    
    
    
    