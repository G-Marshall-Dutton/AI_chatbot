

function updateScroll(){

    var objDiv = document.getElementById("textfield");
    objDiv.scrollTop = objDiv.scrollHeight;
}

// JQUERY --------------------------------------------------

$(document).ready(function(){

    

    // Sends alternating messages on clicking 'send' /chatbot.html
    $(".send-btn").click(function(){

        // Get last message sent
        var lastMessage = $(".response:last-of-type")

        // Check if it was right or left side and respond
        if(lastMessage.hasClass("message-right")){
            lastMessage.after(
                "<div class='response message-left '>  <p class='bg-primary'> Helping... </p>  </div>"
            );
        }
        else {
            lastMessage.after(
                "<div class='response message-right '>  <p class='bg-success'> Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip... </p>  </div>"
            );
        }

        updateScroll();
    });
  
  });



// JQUERY END --------------------------------------------------