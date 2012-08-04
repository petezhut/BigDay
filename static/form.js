function unlock() {
    document.rsvp.count.disabled=false;
}
function willattend() {
    var e = document.getElementById("count");
    var strUser = e.options[e.selectedIndex].text;
    var table = document.getElementById('menu');
    if (table.rows.length > parseInt(strUser)) {
        for (i=table.rows.length; i>parseInt(strUser); i--) {
            removeRow();
        }
    } else { 
        for (i=table.rows.length; i<parseInt(strUser); i++) {
            addRow();
        }
    }
}
function kidsmenu(row, ref) {
    if (ref.value == 'Kids') { 
        var table = document.getElementById(row.id);
        var cell = table.insertCell(2);
        var element1 = document.createElement("select");
        element1.setAttribute('name', 'guest_' + ref.id + "_age");
        element1.options[0] = new Option("Child's Age", 0);
        element1.options[1] = new Option('0-5 years old', "0-5");
        element1.options[2] = new Option('6-14 years old', "6-14");
        cell.appendChild(element1);
        table.appendChild(cell);
    } else {
        table = document.getElementById(ref.id);
        if (table.cells.length > 2) {
            table.deleteCell(2);
        }
    }
}
function removeRow() {
    document.getElementById('menu').deleteRow(0);
}
function addRow() {
    var table = document.getElementById('menu');
    try {
        if (table.rows.length != null) {
            var rows = table.rows.length;
        } else {
            var rows = 0;
        }
    } catch(err) {
        var rows = 0;
    }
    var row = table.insertRow(rows);
    row.id = 'guest_' + rows;
    var nameCell = row.insertCell(0); 
    var element1 = document.createElement("input");
    element1.type = "text";
    element1.setAttribute('name', "guest_" + rows + "_name");
    if (rows == 0) {
        element1.value = document.getElementById('RSVP_FirstName').value;
    } else {
        element1.value = "Guest " + rows + " First Name";
    }
    element1.setAttribute('onclick', "this.value=''");
    nameCell.appendChild(element1);

    var menuCell = row.insertCell(1);
    var element2 = document.createElement("select");
    element2.setAttribute('name', "guest_" + rows + "_meal");
    element2.id = rows;
    element2.setAttribute('onchange', 'kidsmenu(this)');
    element2.setAttribute('onchange', 'kidsmenu(guest_' + rows + ', this)');
    element2.options[0] = new Option('Meal Choice', 0);
    element2.options[1] = new Option('Dry Aged Prime Rib', "Dry Aged Prime Rib");
    element2.options[2] = new Option('Kosher Prime Rib', "Kosher Prime Rib");
    element2.options[3] = new Option('Herbed Filet of Red Snapper Roulade', "Herbed Filet of Red Snapper Roulade");
    element2.options[4] = new Option('Roasted Vegetable Tower', "Roasted Vegetable Tower");
    element2.options[5] = new Option('Kids', "Kids");
    menuCell.appendChild(element2);
}
