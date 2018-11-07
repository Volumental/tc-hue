function post(url) {
  return fetch(url, {method: "POST"})
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
  post('/api/trigger').finally(function() {
    hide(progress);
    button.disabled = false;
  });
}

function ready() {
  document.getElementById('trigger').onclick = trigger;
}

document.addEventListener('DOMContentLoaded', ready);
