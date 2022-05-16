$(window).on('load', () => {

    const darkModebtn = document.getElementById("dark-mode")
    const hcmModebtn = document.getElementById("HCM-mode")
    const navBarColor = document.getElementById("navBar")
    const gearColor = document.getElementById("gearMode")
    const questionColor = document.getElementById("questionMode")
    const graphColor = document.getElementById("graphMode")
    const idcolorMode = document.getElementById("idMode")
    const xColor1 = document.getElementById("squareColor1")
    const xColor2 = document.getElementById("squareColor2")
    const xColor3 = document.getElementById("squareColor3")
    const xColor4 = document.getElementById("squareColor4")

    darkModebtn.addEventListener('click', function(){
        document.body.classList.toggle("dark-theme")
       
       
        if (navBarColor.classList.contains("bg-dark")) 
        {
            navBarColor.classList.remove("bg-dark")
            navBarColor.classList.add("bg-light")
            gearColor.classList.remove("gear-dark")
            gearColor.classList.add("gear-light")
            questionColor.classList.remove("question-dark")
            questionColor.classList.add("question-light")
            graphColor.classList.remove("graph-dark")
            graphColor.classList.add("graph-light")
            idcolorMode.classList.remove("id-dark")
            idcolorMode.classList.add("id-light")
            xColor1.classList.remove("squareColor-dark")
            xColor1.classList.add("squareColor-light") 
            xColor2.classList.remove("squareColor-dark")
            xColor2.classList.add("squareColor-light") 
            xColor3.classList.remove("squareColor-dark")
            xColor3.classList.add("squareColor-light") 
            xColor4.classList.remove("squareColor-dark")
            xColor4.classList.add("squareColor-light")

        } else if (navBarColor.classList.contains("bg-light")) 
        {
            navBarColor.classList.remove("bg-light")
            navBarColor.classList.add("bg-dark")
            gearColor.classList.remove("gear-light")
            gearColor.classList.add("gear-dark")
            questionColor.classList.remove("question-light")
            questionColor.classList.add("question-dark")
            graphColor.classList.remove("graph-light")
            graphColor.classList.add("graph-dark")
            idcolorMode.classList.remove("id-light")
            idcolorMode.classList.add("id-dark")
            xColor1.classList.remove("squareColor-light")
            xColor1.classList.add("squareColor-dark")
            xColor2.classList.remove("squareColor-light")
            xColor2.classList.add("squareColor-dark")
            xColor3.classList.remove("squareColor-light")
            xColor3.classList.add("squareColor-dark")
            xColor4.classList.remove("squareColor-light")
            xColor4.classList.add("squareColor-dark")
        }
        
       
    })
    })

// Normal Scrambled Functionality 
var rowNum;
var colNum;
var words;
var score;
var timeTaken;
var timer;

// To tell which mode it is currently on
var mode;

// Speed Scrambled functionality
var speedRowNum;
var speedColNum;
var speedWords;
var speedScore;
var speedTimeLeft;
var speedTimer;

//Initialisation 
//Initialises normal Scrambled, with global variables and creating guess, letter and submitted table
//Uses cookies to reload previous game state (words, score, time, etc) if played within the day 
function initNormal() {
    mode = "normal";
    document.getElementById("gameMode").setAttribute("href", "/speed");
    createSubmitTable();
    getLettersAndScores();
    score = 0
    updateScore(0);
    rowNum = 0;
    colNum = 0;
    words = [];
    timeTaken = 0;
    if(getCookie("timeTaken") != "") {
        timeTaken = parseInt(getCookie('timeTaken'));
        if(getCookie("rowNum") != "") {
            rowNum = parseInt(getCookie("rowNum"));
            loadPreviousWords();
            if(getCookie("score") != "") {
                updateScore(getCookie("score"));
            }
        }
    }
    timer = startTimer(timeTaken);
    if(rowNum == 6) {
        finishedGame();
    }
} 

// Initialises speed mode
function initSpeed() {
    mode = "speed";
    document.getElementById("gameMode").setAttribute("href", "/index");
    createSubmitTable();
    getLettersAndScores();
    speedScore = 0;
    updateScore(0);
    speedRowNum = 0;
    speedColNum = 0;
    speedWords = [];
    speedTimeLeft = 120;
    if(getCookie("speedTimeLeft") != "") {
        speedTimeLeft = getCookie("speedTimeLeft");
        if(getCookie("speedRowNum") != "") {
            speedRowNum = getCookie("speedRowNum");
            loadPreviousWords();
            if(getCookie("speedScore") != "") {
                updateScore(getCookie("speedScore"));
            }
        }
    }
    speedTimer = startTimer(speedTimeLeft); 
    if(rowNum == 6 || speedTimeLeft <= 0) {
        finishedGame();
    }
}


// Creates the table to for the submitted words
function createSubmitTable() {
    for(let i=0; i < 6; i++) {
        let submittedRow = document.createElement("tr");
        for(let j=0; j < 7; j++) {
            let submittedBox = document.createElement("td");
            submittedBox.setAttribute("id", String(i) + String(j));
            submittedBox.className = "submittedBox";
            submittedRow.appendChild(submittedBox);
        }
        $("#submittedTable").append(submittedRow);
    }
}

// Get letters for the day and creates letter array and guess array
function createWordAndGuessTable(letters) {
    for(let k = 0; k < 7; k++) {
        let letter = document.createElement("td");
        letter.innerHTML = letters[k][0] + "<sub>" + letters[k][1] + "</sub>";
        letter.className = "letter";
        letter.setAttribute("id",  "L" + k);
        letter.addEventListener("click", function() {
            clickedLetter(letter);
        })
        $("#letterRow").append(letter);

        let guessBox = document.createElement("td");
        guessBox.className = "guessBox";
        guessBox.setAttribute("id", "G" + k);
        $("#guess").append(guessBox);
    } 
    document.getElementById("submit").addEventListener("click", checkWord);
    document.getElementById("reset").addEventListener("click", resetWord);
}

// Ajax request for letters of the day for each mode 
function getLettersAndScores() {
    xhhtp = new XMLHttpRequest();
    xhhtp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            let result = JSON.parse(this.responseText);
            createWordAndGuessTable(result.letters);
        }
    }
    if(mode == "speed") {
        xhhtp.open("GET", "http://127.0.0.1:5000/letters/speed");
    }
    else {
        xhhtp.open("GET", "http://127.0.0.1:5000/letters/normal");
    }
    xhhtp.send();
}

// Game functionality functions
// Selects the letter 
function clickedLetter(letter) {
    let column;
    if(mode == "speed") {
        column = speedColNum;
    }
    else {
        column = colNum;
    }
    if(column < 7) {
        let guessBoxID = "G" + column;
        let guessBox = document.getElementById(guessBoxID);
        if(letter.className != "clickedLetter") {
            guessBox.innerHTML = letter.innerHTML;
            letter.className="clickedLetter";
            if(mode == "speed") {
                speedColNum++;
            }
            else {
                colNum++;
            }
        }
    }
}

// Reset word attempt
function resetWord(mode) {
    for(let i = 0; i < 7; i++) {
        let guessBoxID = "G" + i;
        document.getElementById(guessBoxID).innerHTML = "";
    }
    for(let k = 0; k < 7; k++) {
        let letterID = "L" + k;
        let letter = document.getElementById(letterID)
        letter.className="letter";
    }
    if(mode == "speed") {
        speedColNum = 0;
    }
    else {
        colNum = 0;
    }
}

// Gets the word from attempt + warning if words less than 3 letters
function getWord(columns) {
    let word = "";
    for(let i = 0; i < columns; i++) {
        let guessBoxID =  "G" + i;
        let guessLetter = document.getElementById(guessBoxID).innerText;
        word += guessLetter.charAt(0);
    }
    return word;
}

function checkWord() {
    let columns;
    let rows; 
    if(mode == "speed") {
        columns = speedColNum;
        rows = speedRowNum;
    }
    else {
        columns = colNum;
        rows = rowNum;
    }
    if(columns < 3) {

    }
    let word = getWord(columns);
    xhttp = new XMLHttpRequest()
    xhttp.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            outcome = (JSON.parse(this.responseText)).outcome;
            checkedWordResponse(outcome, columns, rows, word)
        }
    }
    xhttp.open("GET", "http://127.0.0.1:5000/checkword?word=" + word, true)
    xhttp.send();
}

function checkedWordResponse(outcome, columns, rows, word) {
    if(outcome) {
        for(let k = 0; k < columns; k++) {
            let guessBoxID =  "G" + k;
            let guessLetter = document.getElementById(guessBoxID);
            let submittedID = String(rows) + String(k);
            let submittedLetter = document.getElementById(submittedID);
                submittedLetter.innerHTML = guessLetter.innerHTML;
        }

        if(mode == "speed") {
            speedWords[speedRowNum] = word;
            speedRowNum++;
            createCookie("speedWords", speedWords);
            createCookie("speedRowNum", speedRowNum);
            createCookie("speedScore", speedScore);
        }
        else {
            words[rowNum] = word;
            rowNum++;
            createCookie("words", words);
            createCookie("rowNum", rowNum);
            createCookie("score", score);
        }
        resetWord()
        if(rowNum == 6) {
            finishedGame();
        }
    }
    else {
        //modal
        resetWord();
    }
}

// Loads previous words
function loadPreviousWords() {
    let prevWords;
    if(mode == "speed") {
        speedWords = getCookie("speedWords").split(",");
        prevWords = speedWords;
    }
    else {
        words = getCookie("words").split(",");
        prevWords = words;
    }
    for(let i = 0; i < prevWords.length; i++) {
        let prevWord = prevWords[i];
        for(let k = 0; k < prevWord.length; k++) {
            let submittedBox = document.getElementById(String(i) + String(k));
            let letterFound = false;
            let j = 0; 
            while(!letterFound) {
                let letter = document.getElementById("L" + String(j));
                j++;
                if(letter.innerText.charAt(0) == word.charAt(k)) {
                    submittedBox.innerHTML = letter.innerHTML;
                    letterFound = true;
                }
            }
        }
    }
}

// Finished game functionality for Normal Scrambled 
function finishedGame() {
    document.getElementById("submit").removeEventListener("click", submitWord);
    document.getElementById("reset").removeEventListener("click", resetWord);
    for(let i=0; i < 7; i++) {
        let letter = document.getElementById("L" + i);
        letter.removeEventListener("click", clickedLetter);
        letter.className = "clickedLetter";
    }

    if(mode == "speed") {
        clearInterval(speedTimer);
    }
    else {
        clearInterval(timer);
        let time = document.getElementById("minutes").innerText + ":" + document.getElementById("seconds").innerText;
        document.getElementById("finishedTime").innerText = time;
    }

    document.getElementById("finishedScore").innerText= score;

    var finishedGameModal = new bootstrap.Modal(
        document.getElementById("finishedGameModal"),
        {}
      );
      finishedGameModal.toggle();
}

// Starts timer for Normal and Speed Scrambled 
function startTimer(time) {
    function pad(val) {
        var valString = val + "";
        if (valString.length < 2) {
            return "0" + valString;
        } else {
            return valString;
        }
    }
    let minutesLabel = document.getElementById("minutes");
    let secondsLabel = document.getElementById("seconds");
    secondsLabel.innerHTML = pad(time % 60);
    minutesLabel.innerHTML = parseInt(time / 60);

    let timer;
    if(mode == "normal") {
        timer = setInterval(normalTime, 1000);
    }
    else {
        timer = setInterval(speedTime, 1000);
    }
    
    function normalTime() {
      ++timeTaken;
      createCookie("timeTaken", timeTaken);
      secondsLabel.innerHTML = pad(timeTaken % 60);
      minutesLabel.innerHTML = parseInt(timeTaken / 60);
    }

    function speedTime() {
        speedTimeLeft--;
        createCookie("speedTimeLeft", speedTimeLeft);
        secondsLabel.innerHTML = pad(speedTimeLeft % 60);
        minutesLabel.innerHTML = parseInt(speedTimeLeft / 60);
        if(speedTimeLeft == 0) {
            finishedGame();
        }
    }
    return timer;
} 

// Updates score during game
function updateScore(update) {
    if(mode == "speed") {
        speedScore += update;
        let scoreDisplay = document.getElementById("score")
        scoreDisplay.innerHTML = "<b>" + speedScore + "</b>";
    }
    else {
        score += update;
        let scoreDisplay = document.getElementById("score")
        scoreDisplay.innerHTML = "<b>" + score + "</b>";
    }
}

// Cookie functions to create and get cookies 
// Creates cookies for page to store daily game progress
function createCookie(name, value) {
    var date = new Date();
    var midnight = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59);
    expires = "; expires=" + midnight.toGMTString();
    document.cookie =  name + "=" + value + expires;
}

// Gets the value of cookie with the specified name 
function getCookie(name) {
    let cname = name + "=";
    let cookieArray = document.cookie.split(';');
    for(let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) == " ") {
            cookie = cookie.substring(1);
        }
        if(cookie.indexOf(cname) == 0) {
            return cookie.substring(name.length + 1, cookie.length);
        }
    }
    return "";
<<<<<<< HEAD
}
=======
}
>>>>>>> moving-files-around
