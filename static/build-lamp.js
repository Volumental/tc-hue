function post(url, body) {
  return fetch(url,
    {
      method: "POST",
      headers: {"Content-Type": "application/json; charset=utf-8"},
      body: JSON.stringify(body)
    })
    .then(function(response) {
      if (!response.ok) {
        throw response.statusText;
      }
      return response;
    })
    .then(function(response) {
      return response.text();
    });
}

function hide(element) {
  element.style.display = 'none';
}

function show(element) {
  element.style.display = 'block';
}

function trigger() {
  var progress = document.getElementById('progress');
  var button = this;
  show(progress);
  button.disabled = true;
  post('/api/trigger').catch(function(error) {
    var label = document.querySelector('label[for="' + button.id + '"]');
    label.innerText = error;
  }).finally(function() {
    hide(progress);
    button.disabled = false;
  });
}

function saveConfig() {
  var config = document.getElementById('config').value;
  var button = this;
  button.disabled = true;
  post('/api/config', config).catch(function(error) {
    var label = document.querySelector('label[for="' + button.id + '"]');
    label.innerText = error;
  }).finally(function() {
    button.disabled = false;
  });
}

function ready() {
  document.getElementById('trigger').onclick = trigger;
  document.getElementById('save_config').onclick = saveConfig;
}

document.addEventListener('DOMContentLoaded', ready);
