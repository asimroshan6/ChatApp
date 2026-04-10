function gotoChat(){
    const username = document.getElementById("username").value;
    sessionStorage.setItem("username", username)

    if (!username){
        alert("Username should be valid!");
        return;
    }
    window.location.href = "/chat";
}

