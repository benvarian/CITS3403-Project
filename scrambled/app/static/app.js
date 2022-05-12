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
    
    hcmModebtn.addEventListener('click', function(){
        document.body.classList.toggle("high-contrast")
        
    })

    

    var rowNum;
    var colNum;
    var words;
    var score;
    var timeTaken;
    var timer;
    
    //Initialisation and helper functions
    //Initialises index page, with global variables and creating guess, letter and submitted table
    //Uses cookies to reload previous game state (words, score, time, etc) if played within the day 
    function init() {
        createSubmitTable();
        getLettersAndScores();
        updateScore(0);
        rowNum = 0;
        colNum = 0;
        words = [];
        score = 0;
        timeTaken = 0;
        if(getCookie("timeTaken") != "") {
            timeTaken = parseInt(getCookie('timeTaken'));
            if(getCookie("rowNum") != "") {
                rowNum = parseInt(getCookie("rowNum"));
                loadPreviousWords();
                updateScore(getCookie("score"));
            }
        }
        timer = startTimer(timeTaken);
        if(rowNum == 6) {
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
    
    // Get letters for the day and creates 
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
        document.getElementById("submit").addEventListener("click", submitWord);
        document.getElementById("reset").addEventListener("click", resetWord);
    }
    
    function getLettersAndScores() {
        xhhtp = new XMLHttpRequest();
        xhhtp.onreadystatechange = function() {
            if(this.readyState == 4 && this.status == 200) {
                let result = JSON.parse(this.responseText);
                createWordAndGuessTable(result.letters);
            }
        }
        xhhtp.open("GET", "http://127.0.0.1:5000/letters");
        xhhtp.send();
    }
    
    function updateScore(scoreUpdated) {
        score = scoreUpdated;
        let scoreDisplay = document.getElementById("score")
        scoreDisplay.innerHTML = "<b>" + score + "</b>";
    }
    
    
    // Game functionality functions
    // Selects the letter 
    function clickedLetter(letter) {
        if(colNum < 7) {
            let guessBoxID = "G" + colNum;
            let guessBox = document.getElementById(guessBoxID);
            if(letter.className != "clickedLetter") {
                guessBox.innerHTML = letter.innerHTML;
                letter.className="clickedLetter";
                colNum++;
            }
        }
    }
    
    function resetWord() {
        for(let i = 0; i < 7; i++) {
            let guessBoxID = "G" + i;
            document.getElementById(guessBoxID).innerHTML = "";
        }
        for(let k = 0; k < 7; k++) {
            let letterID = "L" + k;
            let letter = document.getElementById(letterID)
            letter.className="letter";
        }
        colNum = 0;
    }
    
    function submitWord() {
        if(colNum < 3) {
            //ALERT LESS THAN 3 Letter word
        }
        else {
            var wordGuess = "";
            var wordScore = 0;
            for(let i = 0; i < colNum; i++) {
                let guessBoxID =  "G" + i;
                let guessLetter = document.getElementById(guessBoxID).innerText;
                wordGuess += guessLetter.charAt(0);
                wordScore += parseInt(guessLetter.charAt(1));
            }
            let outcome = checkWord(wordGuess);
            if(outcome) {
                for(let k = 0; k < colNum; k++) {
                    let guessBoxID =  "G" + k;
                    let guessLetter = document.getElementById(guessBoxID);
                    let submittedID = String(rowNum) + String(k);
                    let submittedLetter = document.getElementById(submittedID);
                    submittedLetter.innerHTML = guessLetter.innerHTML;
                }
                words[rowNum] = wordGuess;
                rowNum++;
                if(rowNum == 6) {
                    finishedGame();
                }
            
                createCookie("words", words);
                createCookie("score", score);
                createCookie("rowNum", rowNum);
                resetWord();
            }
            else {
                //modal
                resetWord();
            }
        }
    }
    
    function checkWord(word) {
        xhttp = new XMLHttpRequest()
        xhttp.onreadystatechange = function() {
            if(this.readyState == 4 && this.status == 200) {
                let outcome = JSON.parse(this.responseText).outcome;
            }
        }
        xhttp.open("GET", "http://127.0.0.1:5000/checkword?word=" + word, true)
        xhttp.send();
    }
    
    function loadPreviousWords() {
        words = getCookie("words").split(",");
        for(let i = 0; i < words.length; i++) {
            let word = words[i];
            for(let k = 0; k < word.length; k++) {
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
    
    function finishedGame() {
        document.getElementById("submit").removeEventListener("click", submitWord);
        document.getElementById("reset").removeEventListener("click", resetWord);
        for(let i=0; i < 7; i++) {
            let letter = document.getElementById("L" + i);
            letter.removeEventListener("click", clickedLetter);
            letter.className = "clickedLetter";
        }
        clearInterval(timer);
    
        document.getElementById("finishedScore").innerText= score;
        let time = document.getElementById("minutes").innerText + ":" + document.getElementById("seconds").innerText;
        document.getElementById("finishedTime").innerText = time;
    
        var finishedGameModal = new bootstrap.Modal(
            document.getElementById("finishedGameModal"),
            {}
          );
          finishedGameModal.toggle();
    }
    
    function createCookie(name, value) {
        var date = new Date();
        var midnight = new Date(date.getFullYear(), date.getMonth(), date.getDate(), 23, 59, 59);
        expires = "; expires=" + midnight.toGMTString();
        document.cookie =  name + "=" + value + expires;
    }
    
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
    }
    
    function openRules() {
        var rulesModal = new bootstrap.Modal(
            document.getElementById("rulesModal"),
            {}
          );
          rulesModal.toggle();
    }
    
    function startTimer(timeTaken) {
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
        secondsLabel.innerHTML = pad(timeTaken % 60);
        minutesLabel.innerHTML = parseInt(timeTaken / 60);
        let timer = setInterval(setTime, 1000);
        
        function setTime() {
          ++timeTaken;
          createCookie("timeTaken", timeTaken);
          secondsLabel.innerHTML = pad(timeTaken % 60);
          minutesLabel.innerHTML = parseInt(timeTaken / 60);
        }
        return timer;
    } 
    