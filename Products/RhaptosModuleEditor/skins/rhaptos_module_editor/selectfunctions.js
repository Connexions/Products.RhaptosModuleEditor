function selectAllValue(val) {
    checkboxes = document.getElementById("add_roles_table").getElementsByTagName("input")
    for (i = 0; i < checkboxes.length; i++)
       if (checkboxes[i].value==val && checkboxes[i].title=="required_role") {
          checkboxes[i].checked = true ;
       }
}

function deselectAllValue(val) {
    checkboxes = document.getElementById("add_roles_table").getElementsByTagName("input")
    for (i = 0; i < checkboxes.length; i++)
       if (checkboxes[i].value==val) {
          checkboxes[i].checked = false ;
       }
}

/*
 * When a module is imported (for example through SWORD), there may be additional roles that should
 * be added to the module. This Javascript will do that.
 */

function searchUser(name) {
  var form = document.getElementsByName('collaborators_search')[0];
  var textbox = null;
  for (i = 0; i < form.elements.length; i++) {
    if ('search' == form.elements[i].name) {
      textbox = form.elements[i];
    }
  }
  textbox.value = name;
  form.submit();
}

