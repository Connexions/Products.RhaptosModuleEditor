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
