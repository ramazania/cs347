let currentPassword = [];
const maxPasswordLen = 4;
let emptyIcon = "rgba(0, 0, 0, 0.49)";

// creates the gameboard given the max number of attempts for the game
function setUpBoard(maxAttempts) {
    const gameTable = document.getElementById("gameInfo");
        for (let i = 0; i < maxAttempts; i++) { 
            const curRow = gameTable.insertRow(i+1);

            const cell1 = curRow.insertCell(0);
            cell1.innerHTML = (i+1).toString();

            const cell2 = curRow.insertCell(1);
            cell2.innerHTML = "?";

            const cell3 = curRow.insertCell(2);
            cell3.innerHTML = "?";
        }
}

// creates the given colors as buttons and icons to be used for the game
function setUpColors(colorList) {
    const playerPassword = document.getElementById("currentpassword");
    const colorOptions = document.getElementById("passwordattempt");
        for (let i = 0; i < 6; i++) {
            // creating a label to not get broswer warnings
            const colorLabel = document.createElement("label");
            colorLabel.for = colorList[i];
            colorLabel.classList.add("colorlabel");
            colorLabel.title = colorList[i];

            // creating a checkbox for the player to input their guesses
            const colorButton = document.createElement("input");
            colorButton.type = "checkbox";
            colorButton.classList.add("coloricon");
            colorButton.classList.add("colorbutton");
            colorButton.id = colorList[i];
            colorButton.name = "";
            colorButton.value = colorList[i];
            colorButton.onclick = function () {toggleUnmarked(colorButton.id)};
            colorButton.style.backgroundColor = colorList[i];

            // creating the icons to show the user's current password
            if (i < maxPasswordLen) {
                const colorPassIcon = document.createElement("span");
                colorPassIcon.classList.add("coloricon");
                colorPassIcon.id = "icon" + (i+1).toString();
                colorPassIcon.style.backgroundColor = emptyIcon;
                playerPassword.appendChild(colorPassIcon);
            }

            colorLabel.appendChild(colorButton);
            colorOptions.appendChild(colorLabel);
        }
}

// toggles the "marked" class of a button, indicating a specific 
// code color is has been added to the guess
function toggleUnmarked(color){
    const element = document.getElementById(color);
    element.classList.toggle("marked");
    updateCurrentPassword();
    checkOptions(maxPasswordLen);
}

// checks if the player's password is ready for submission
function checkOptions(maxPassLen) {
    let coloricons = document.getElementsByClassName("colorbutton");
    let cur_unmarked = document.getElementsByClassName("marked");
    // if the player's guess has reached the max password length, 
    // update all buttons for submisson
    if (cur_unmarked.length == maxPassLen) {
        for (let i=0; i < coloricons.length; i++) {
            if (!coloricons[i].classList.contains("marked")) {
                coloricons[i].disabled = true;
                document.getElementById("submit").value = "Send";
                document.getElementById("submit").disabled = false;
            }
        } 
    // else if the player's guess is smaller than the max password length,
    // update the page to prevent submission
    } else if (cur_unmarked.length == maxPassLen-1) {
        for (let i=0; i < coloricons.length; i++) {
            coloricons[i].disabled = false;
            document.getElementById("submit").value = "Waiting";
            document.getElementById("submit").disabled = true;
        }
    }
}

// updates the stored information of the current password
function updateCurrentPassword() {
    const activeEle = document.activeElement;
    let activeEleID = activeEle.id;
    // making sure the active elemen is a color the player can choose
    if (activeEle.type == "checkbox") { 
        // if the color is already in the password, remove it
        if (currentPassword.includes(activeEleID)) { 
            let colorIndex = currentPassword.indexOf(activeEleID);
            currentPassword.splice(colorIndex,1);
            activeEle.name = "";
        } else { // else, add it
            currentPassword.push(activeEleID);
        }
        let counter = 1;
        // update the name attribute of each selected color, to identify color order
        currentPassword.forEach(color => { 
            let similarEle = document.getElementById(color);
            similarEle.name = "color" + counter.toString();

            document.getElementById("icon" + counter.toString()).style.backgroundColor = color;
            counter++;
        });
        if (counter < maxPasswordLen+1) {
            document.getElementById("icon" + counter.toString()).style.backgroundColor = emptyIcon;
            counter++;
        }

    }
}

$(document).ready(function(){ // updates the game page without refreshing
    $("#passwordattempt").submit(function(event){
        event.preventDefault();
        $.ajax({
            url: '/update',
            type: 'GET',
            data: $('form').serialize(),
            success: function(response){
                if (response.isComplete > 0) { // check if the game is over
                    window.location.href = '/gamecomplete'; 
                } else { // else, update the game page
                    let cur_row = $('#gameInfo tr').eq(response.attempts); // Target the current non-updated row of the board
                    let cur_cells = cur_row.children('td');
                    let lastGuess = document.createElement("div");
                    lastGuess.classList.add("lastGuess");
                    for (i = 0; i < maxPasswordLen; i++) {
                        const colorPassIcon = document.createElement("span");
                        colorPassIcon.classList.add("coloricon");
                        colorPassIcon.style.backgroundColor = response.guess[i];
                        lastGuess.appendChild(colorPassIcon);
                        } 
                    $(cur_cells[1]).html(lastGuess); // Update the guess cell with the player's last password
                    $(cur_cells[2]).html("Red: " + response.red + "\nWhite: " + response.white); // Update the hint cell for the last password
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});