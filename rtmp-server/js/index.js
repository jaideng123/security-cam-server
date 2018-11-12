console.log("Loaded");
const baseUrl = "http://76.183.120.203/";

FetchStatus().then(DisplayStatus);

function FetchStatus() {
  return fetch(baseUrl + "status").then(res => {
    console.log(res);
    return res.text();
  });
}

function DisplayStatus(status) {
  document.getElementById("status-indicator").innerText = status;
}

function SetOn() {
  return fetch(baseUrl + "on").then(res => {
    return res.text();
  });
}

function SetOff() {
  return fetch(baseUrl + "off").then(res => {
    return res.text();
  });
}
