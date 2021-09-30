// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
  // hljs.highlightAll();
// });

console.log("go get it");
let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')

if (alertWrapper) {
  alertClose.addEventListener('click', () =>
    alertWrapper.style.display = 'none'
  )
}

