

function updateScroll(){
    var objDiv = document.getElementById("textfield");
    objDiv.scrollTop = objDiv.scrollHeight;
}



sendMessage = () => {

    // Get last message sent
    var lastMessage = $(".response:last-of-type")

    // Get user input
    var userMessage = document.getElementById('userInput').value
    console.log("PaPa's new friend: "+userMessage)
    document.getElementById('userInput').value = "" //Empy input


    if(userMessage != ""){
           // Write user message bubble
        lastMessage.after(
            "<div class='response message-right '>  <p class='bg-success'> "+userMessage+" </p>  </div>"
        );
        updateScroll();
        //Fetch request
        fetch('/chat',{
            method: 'POST',
            body: JSON.stringify({ userMessage: userMessage }), // Provide user query message
            headers: {
            'Content-Type': 'application/json',
            }
        }).then((response) => {
            return response.json(); //Parse as JSON
        }).then((data) => {
            console.log("PaPa: "+data.answer)
            // Find last message again 
            lastMessage = $(".response:last-of-type")

            // Write PaPa message bubble
            lastMessage.after(
                "<div class='response message-left '>  <p class='bg-primary'> "+data.answer+" </p>  </div>"
            );
            updateScroll();
        }).catch(() => {
            console.log("Could not recieve response from PaPa :(");
        });

    }

 


    
    
}

// JQUERY --------------------------------------------------

$(document).ready(()=>{

    document.getElementById('userInput').onkeypress = (e) => {
        if (!e) e = window.event;
        var keyCode = e.keyCode || e.which;
        if (keyCode == '13'){
          // Enter pressed
          sendMessage()
        }
      }

    // Sends alternating messages on clicking 'send' /chatbot.html
    $(".send-btn").click(()=>sendMessage())
})

// JQUERY END --------------------------------------------------