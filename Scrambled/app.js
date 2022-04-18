function init() {
    let attemptTable = document.createElement("table");
    for(let i=0; i < 7; i++) {
        let attempt = document.createElement("tr");
        for(let j=0; j < 7; j++) {
            let box = document.createElement("td");
            box.className = ;
            attempt.appendChild(box);
        }
        attemptTable.appendChild(attempt);
    }
    let gamebox = document.getElementById("gamebox");
    gamebox.appendChild(attemptTable);
}