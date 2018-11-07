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

function hide_progress() {
  hide(document.getElementById('progress'));
}

function show_progress() {
  show(document.getElementById('progress'));
}

function trigger() {
  show_progress()
  post('/api/trigger').then(hide_progress);
}

function ready() {
  document.getElementById('trigger').onclick = trigger;
}

document.addEventListener('DOMContentLoaded', ready);
