var headers = ['Type', 'Name', 'Direction', 'Description', 'Remove'];

function createTable() {

    var table = document.createElement('table');
    table.setAttribute('id', 'partsTable');

    var tr = table.insertRow(-1);

    for (var i = 0; i < headers.length; i++) {
        var th = document.createElement('th');
        th.innerText = headers[i];
        tr.appendChild(th);
    }

    var div = document.getElementById('parts');
    div.appendChild(table);

}

function addPart() {

    var table = document.getElementById('partsTable');
    var rowCnt = table.rows.length;

    var tr = table.insertRow(rowCnt);

    for (var i = 0; i < headers.length; i++) {

        var td = document.createElement('td');
        td = tr.insertCell(i);

        switch(headers[i]) {

            case 'Type':
                break;
            case 'Name':
                var text = document.createElement('input');
                text.setAttribute('type', 'text');
                text.setAttribute('value', 'rowCnt');
                td.appendChild(text);
                break;
            case 'Direction':
                break;
            case 'Description':
                break;
            case 'Remove':
                var button = document.createElement('input');
                button.setAttribute('type', 'button');
                button.setAttribute('value', 'Remove');
                button.setAttribute('onClick', 'removeRow(this)');
                td.appendChild(button);
                break;
        }
    }

}

function removeRow(oButton) {

    var table = document.getElementById('partsTable');
    table.deleteRow(oButton.parentNode.parentNode.rowIndex);

}
