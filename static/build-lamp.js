function post(url) {
  return fetch(url, {method: "POST"})
    .then(function(response) {
      return response.text();
    });
}

function trigger() {
  post('/api/trigger').then(console.log);
}

function ready() {
  document.getElementById('trigger').onclick = trigger;
}

document.addEventListener('DOMContentLoaded', ready);
