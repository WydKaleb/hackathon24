const selectedDate = document.getElementById("datePicked")

async function getAssignments(){

    //store url and pass in custom date for api request
    const url = "http://127.0.0.1:8000/api/hw/"+selectedDate.value+"/"; 

    try{
        //api call
        const resp = await fetch(url);
        const data = await resp.json();
        //make sure date is correct
        console.log(data.message);

    }catch(error){
        console.error("error");
    }
}