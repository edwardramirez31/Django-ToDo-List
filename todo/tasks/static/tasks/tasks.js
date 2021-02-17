function markTask (url, id) {
  // MARK AND UNMARK IN THE FRONTEND 
  var divID = 'Check-Item-' + id;
  checkItem = document.getElementById(divID);
  console.log(checkItem);
  label = checkItem.getElementsByTagName('label')[0];
  console.log(label.style.textDecoration);
  if (label.style.textDecoration == false) {
    label.style.textDecoration = 'line-through';
  } else {
    label.style.textDecoration = '';
  };

  $.post(url);
}

function deleteTask(url, id) {
  $('#Check-Item-' + id).parent().remove();
  $.post(url);
}

var postURL;
var labelID;

function updateTask(url, id) {
  postURL = url;
  labelID = id;
}

var modal_btn = document.querySelector('#modal-update');
modal_btn.addEventListener('click', async (e) => {
  let modalLabel = document.querySelector("#update-label");
  var text = modalLabel.value;
  var label = document.querySelector(`#task-${labelID}`);
  label.innerHTML = text;
  modalLabel.value = '';
  $('#taskModal').modal('hide');
  var response = await fetch(postURL, {
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      "X-CSRFToken": getCookie('csrftoken')
    },
    body: JSON.stringify({"new_title": text})
  });
  var data = await response.text();
  console.log(data);
});
