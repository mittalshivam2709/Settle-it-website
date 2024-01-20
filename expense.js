function displayGroups() {
    document.getElementById('form1').style.display = 'inline-block';
}

function displayFriends() {
    document.getElementById('form2').style.display = 'inline-block';
}

function hideGroups() {
    document.getElementById('form1').style.display = 'none';
}

function hideFriends() {
    document.getElementById('form2').style.display = 'none';
}

function displayFriends2() {
    document.getElementById('form3').style.display = 'inline-block';
}
function hideFriends2() {
    document.getElementById('form3').style.display = 'none';
}

var selectedperson = "";

function selectPerson(event) {
    document.getElementById('sel').style.cursor = "pointer";
    var name = document.getElementById('sel').getAttribute('data-value');
    document.getElementById('name').textContent = name;

    selectedperson = event.target.closest('tr').dataset.value;

}

var selectedGroup = ""; // global variable to store the selected group

function selectGrp(event) {
    // var row = button.parentNode.parentNode;
    document.getElementById('grp').style.cursor = "pointer";
    var name = document.getElementById('grp').getAttribute('data-value');
    document.getElementById('name').textContent = name;

    selectedGroup = event.target.closest('tr').dataset.value;
    // console.log(selectedGroup); // just to check if it's working

}

function cur() {
    document.getElementById('sel').style.cursor = "pointer";
}

var flag=0
function addTextBox() {
    var textBox = document.getElementById("textBox");
    textBox.style.display = "block";
    flag=1
}

function submitForm(event) {

    event.preventDefault(); // prevent the default form submission behavior
    // rest of your code

    // get the form data and selected group

    // create the data to send
    var form = new FormData(event.target);
    var group = selectedGroup;
    var person = selectedperson;
    console.log(person);

    var data = {
        desc: form.get("desc"),
        amount: form.get("amt"),
        group: group,
        person: person,
        flag: flag,
        entries: form.get("entries")
    };

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/signin", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
        }
    };
    xhr.send(JSON.stringify(data));
}

function fn() {

}