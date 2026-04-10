async function createRoom(){
    const room_name = document.getElementById("roomNameCreate").value;
    const password = document.getElementById("roomPasswordCreate").value;
    const username = document.getElementById("usernameCreate").value;

    if (!room_name || !password || !username){
        alert("All should be filled");
        return;
    }

    try{
        const response = await fetch("/create-room", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({room_name: room_name, password: password, username: username})
        });
        const data = await response.json();
        if (!response.ok){
            alert(data.detail || "Some error occurred");
            return;
        }

        localStorage.setItem("token", data.token);
        localStorage.setItem("room_name", data.room_name);
        window.location.href = "/chat";

    } catch (e) {
        console.log("Error: " + e);
    }
}

async function gotoChat(){
    const room_name = document.getElementById("roomName").value;
    const password = document.getElementById("roomPassword").value;
    const username = document.getElementById("username").value;


    if (!room_name || !password || !username){
        alert("All should be filled");
        return;
    }
    try{
        const response = await fetch("/join-room", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({room_name: room_name, password: password, username: username})
        });

        const data = await response.json();

        if (!response.ok){
            alert(data.detail || "Some error occurred");
            return;
        }
        localStorage.setItem("token", data.token);
        localStorage.setItem("room_name", data.room_name);

        window.location.href = "/chat";

    } catch (e) {
        console.log("Error: " + e);
    }
}
