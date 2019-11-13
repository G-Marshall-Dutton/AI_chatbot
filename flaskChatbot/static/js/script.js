

function testFunction(){

}

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

        // Get users question and clear input
        var input = $(".messageInput")
        var userQuery = input.val() 
        input.val('') 

        if(userQuery != ""){

            lastMessage.after(
                "<div class='response message-right '>  <p class='bg-success'> "+ userQuery +"</p>  </div>"
            )
        
            

            // Call python function
            jQuery.get(
                '/send_request_to_AI', 
                {text: userQuery},
                function(data) {
                    lastMessage.after(
                        "<div class='response message-left '>  <p class='bg-primary'>" + data + "</p>  </div>"
                    );
                }
            )
        }

        // Check if it was right or left side and respond
        // If message came form AI

        // if(lastMessage.hasClass("message-right")){
        //     lastMessage.after(
        //         "<div class='response message-left '>  <p class='bg-primary'> Helping... </p>  </div>"
        //     );
        // }
        // If message came from user


        updateScroll();
    });
  
  });

// JQUERY END --------------------------------------------------