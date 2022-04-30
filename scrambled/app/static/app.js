$(window).on('load', () => {
    const darkModebtn = document.getElementById("dark-mode")
    const hcmMode = document.getElementById("HCM-mode")
    const navBarColor = document.getElementById("navBar")
    const gearColor = document.getElementById("gearMode")
    darkModebtn.addEventListener('click', function(){
        document.body.classList.toggle("dark-theme")
        navBarColor.classList.remove("bg-light")
        navBarColor.classList.add("bg-dark")
        gearColor.classList.remove("gear-light")
        gearColor.classList.add("gear-dark")
    })
    })
    hcmMode.addEventListener('click', function(){
        document.body.classList.toggle("high-contrast")
    })
  
function init() {
    // Loads in the guess table 
    for(let i=0; i < 6; i++) {
        let attemptRow = document.createElement("tr");
        for(let j=0; j < 7; j++) {
            let attemptLetter = document.createElement("td");
            attemptLetter.className = "guessBox";
            attemptRow.appendChild(attemptLetter);
        }
        document.getElementById("guessTable").append(attemptRow);
    }

    // Loads in the letters
    let letterRow = document.createElement("tr");
    for(let k = 0; k < 7; k++) {
        let letter = document.createElement("td");
        letter.innerHTML = "A<sub>1</sub>";
        letter.className = "guessLetter";
        // letter.onclick = clickedLetter();
        letterRow.append(letter);
    }
    document.getElementById("letterTable").append(letterRow);

    // Opens rules modal 
    var rulesModal = new bootstrap.Modal(document.getElementById('rulesModal'), {})
    rulesModal.toggle()

}
