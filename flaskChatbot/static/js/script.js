

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

    // Display user message
    if(userMessage != ""){
        // Write user message bubble
        lastMessage.after(
            "<div class='response message-right '>  <p class='bg-success'> "+userMessage+" </p>  </div>"
        );
        updateScroll();

        // Display chat bot message
        $.ajax({

            url: "/chat",
            type: 'POST',
            data: JSON.stringify({ userMessage: userMessage }),
            contentType: 'application/json',
            success: function(data){
            console.log(data)
            lastMessage = $(".response:last-of-type")


            if(data.status == "ticketChat"){
                // Write PaPa message bubble
                lastMessage.after(
                    "<div class='response message-left '>  <p class='bg-primary'> "+data.answer+" </p>  </div>"
                );
            }
            else{
                // Display scraped ticket info as a ticket
                lastMessage.after(
                    `<div class='ticket'> 
                        <div class='textArea'>

                            <div class='headings'>
                                <p> Class </p>
                                <p> Ticket type </p>
                                <p> Adult </p>
                                <p> Child </p>
                            </div>
                            <div class='info'>
                                <p> STD </p>
                                <p class="sml-text">`+ data.answer.ticketType + `</p>
                                <p> `+ data.answer.numberOfTickets +` </p>
                                <p> 0 </p>
                            </div>

                            <div class='headings'>
                            </div>
                            <div class='info'>
                            </div>

                            <div class='headings'>
                                <p> From </p>
                                <p> Leaving at </p>
                                <p> Route name </p>
                            </div>
                            <div class='info'>
                                <p>`+ data.answer.fromStation +`</p>
                                <p>`+ data.answer.departureTime +`</p>
                                <p class="sml-text"> `+ data.answer.fareRouteName +` </p>
                            </div>

                            <div class='headings'>
                                <p> To </p>
                                <p> Arriving at </p>
                                <p> Price </p>
                            </div>
                            <div class='info'>
                                <p>`+ data.answer.toStation +`</p>
                                <p>`+ data.answer.arrivalTime +`</p>
                                <p> `+ data.answer.price +` </p>
                            </div>
                        </div> 
                    </div>`
           
                );

                var ticket =  $(".ticket")
                ticket.after(
                    `
                    <div class='button-row'>
                        <a href = '`+ data.answer.pageUrl + `' class = 'btn bg-warning' target='blank'> Book Now </a>
                    </div>
                    <div class="response"></div>
                    `
                )
            }



            updateScroll();

            }



        })





        //Fetch request
        // fetch('/chat',{
        //     method: 'POST',
        //     body: JSON.stringify({ userMessage: userMessage }), // Provide user query message
        //     headers: {
        //     'Content-Type': 'application/json',
        //     }
        // }).then((response) => {
        //     var info = response.json()
        //     console.log(info.answer)
        //     return info //Parse as JSON
        // }).then((data) => {
        //     console.log("PaPa: "+data.answer)
        //     // Find last message again 
        //     lastMessage = $(".response:last-of-type")

        //     // Write PaPa message bubble
        //     lastMessage.after(
        //         "<div class='response message-left '>  <p class='bg-primary'> "+data.answer+" </p>  </div>"
        //     );
        //     updateScroll();
        // }).catch(() => {
        //     console.log("Could not recieve response from PaPa :(");
        // });

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