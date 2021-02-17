function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

async function editColor(url, className, tagID) {
  var elements = document.getElementsByClassName(tagID);
  console.log(elements);
  // https://developer.mozilla.org/es/docs/Web/JavaScript/Referencia/Objetos_globales/Array/from
  Array.from(elements).forEach(element => {
    var oldClass = element.classList[0];
    var newClass = oldClass.split('-')[0] + '-' +className;
    element.classList.replace(oldClass, newClass);
  });
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      "X-CSRFToken": getCookie('csrftoken')
    }
  });
  const data = await response.text();
  console.log(data);
}