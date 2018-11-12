console.log("Loaded");

FetchStatus().then(DisplayStatus);

function FetchStatus() {
  return fetch("http://localhost:5000/status").then(res => {
    console.log(res);
    return res.text();
  });
}

function DisplayStatus(status) {
  document.getElementById("status-indicator").innerText = status;
}

function SetOn() {
  return fetch("http://localhost:5000/on").then(res => {
    return res.text();
  });
}

function SetOff() {
  return fetch("http://localhost:5000/off").then(res => {
    return res.text();
  });
}
