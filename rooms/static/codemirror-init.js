(function() {
  window.onload = function() {
    function load(el) {
      CodeMirror.fromTextArea(el, {
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        // theme: 'ayu-dark',
      });
    }
    load(document.querySelector('textarea.code-editor'));
  };
})();
