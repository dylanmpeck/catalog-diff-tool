function filterTable(boxID, boxName, tableID)
{
  if (document.getElementById(boxID).checked) 
  {
      showElementsWithID(boxName, tableID);
  } else {
      hideElementsWithID(boxName, tableID);
  }
}

function showElementsWithID(boxName, tableID)
{
    var input, filter, table, tr, td, i, txtValue;
    // input = document.getElementById("myInput");
    // filter = input.value.toUpperCase();
    filter = boxName.toUpperCase();
    table = document.getElementById(tableID);
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; // check content type only
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase() === filter) {
                tr[i].style.display = "";
            }
        }
    }
}

function hideElementsWithID(boxName, tableID)
{
    var input, filter, table, tr, td, i, txtValue;
    // input = document.getElementById("myInput");
    // filter = input.value.toUpperCase();
    filter = boxName.toUpperCase();
    table = document.getElementById(tableID);
    tr = table.getElementsByTagName("tr");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1]; // check content type only
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase() === filter) {
                tr[i].style.display = "none";
            }
        }
    }
}